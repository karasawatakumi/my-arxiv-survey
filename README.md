# arxiv-survey

arXiv論文のメタデータを取得し、GPTで `comment` から学会情報を、`title` + `abstract` からタスクカテゴリを抽出するパイプライン。

## ディレクトリ構成

```
arxiv-survey/
├── .env              # OPENAI_API_KEY を記載（リポジトリには含めない）
├── pyproject.toml    # uv プロジェクト定義
├── uv.lock
├── index.html        # 静的フロント（CSVブラウザ）
├── scripts/
│   ├── fetch_arxiv.py       # arXiv API から取得 → CSV
│   ├── enrich_comments.py   # comment から学会情報を抽出
│   └── enrich_tasks.py      # title + abstract からタスクカテゴリを付与
└── outputs/                 # 生成CSV（デフォルト出力先）
```

## セットアップ

[uv](https://docs.astral.sh/uv/) を使う:

```bash
uv sync
```

`.env` を作成:

```
OPENAI_API_KEY=sk-...
```

スクリプトはすべて `uv run` 経由で実行する。

## パイプライン

3スクリプトを順に通すと、最終CSVに以下の列が揃います:

| 段階 | 追加される列 |
|---|---|
| fetch | id, title, authors, **author_count**, primary_category, categories, comment, **repo_url**, published, updated, summary, pdf_url |
| enrich_comments | is_cvpr2026, track, accepted, notes |
| enrich_tasks | task_primary, task_secondary, task_keywords, modality, task_summary |

### 1. arXiv から取得

```bash
uv run scripts/fetch_arxiv.py "co:cvpr AND co:2026" 1700 -o outputs/cvpr2026.csv
```

- 第1引数は **arXiv の search_query 式**（例: `"co:cvpr"`, `"diffusion"`, `"ti:transformer AND abs:attention"`）
- 第2引数は取得件数（1〜30000）。実際のヒット件数より多めにしておくと自然に枯渇終了する
- デフォルトでカテゴリ `cs.CV / cs.RO / cs.AI / cs.LG` の論文のみ返す（`primary_category` がいずれかに一致するものに絞る）
- `--categories cs.CL,cs.LG` で上書き、`--categories ""` で無効化
- ページ単位で逐次CSV書き込み。途中で死んでも書き込み済み分は保持される（同じ `-o` で再実行すると上書きされるので注意）

総件数を事前に確認したい場合（API1コール）:
```bash
curl -sS "https://export.arxiv.org/api/query?search_query=co:cvpr+AND+co:2026&max_results=1" | grep totalResults
```

#### arXiv search_query フィールドプレフィクス

| prefix | 意味 |
|---|---|
| `ti:` | title |
| `au:` | author |
| `abs:` | abstract |
| `co:` | comment |
| `jr:` | journal-ref |
| `cat:` | subject category |
| `all:` | 全フィールド |

プレフィクスなしは `all:` 相当。

#### N と API 制約

- arXiv API は IP単位でレート制限が厳しい。本スクリプトは:
  - PAGE_SIZE=25（大きい `max_results` だと即429になりやすいため）
  - リクエスト間隔 10秒（API最小推奨は3秒、安全側に振っている）
  - 429 / 5xx / タイムアウト時は最大5回リトライ（バックオフ 10/20/30/40/50秒）
  - `urlopen` のタイムアウトは90秒
- それでも429が連続する場合は、IPを変える（Wi-Fi切替・テザリング）と即解消することが多い。

### 2. comment から学会情報を抽出（GPT）

```bash
uv run scripts/enrich_comments.py outputs/cvpr2026.csv -o outputs/cvpr2026_enriched.csv
```

`comment` 列を OpenAI に送って Structured Outputs で4列を返す:

- `is_cvpr2026`: `yes` / `no` / `unsure`
- `track`: `main` / `findings` / `workshop` / `other` / `unknown`
- `accepted`: `yes` / `no` / `unsure`
- `notes`: 補足（"Highlight" など）

オプション:
- `--limit N` 先頭N件のみ処理（テスト用）
- `--model` OpenAIモデル指定（デフォルト `gpt-4o-mini`）
- `--workers N` 並列リクエスト数（デフォルト 5。1500件で5並列なら ~7-10分）

> CVPR 2026 では Findings トラックが新設されている（arXivコメントから複数の独立した著者が "Findings Track" と明記しているのが確認できる）。

### 3. title + abstract からタスクカテゴリを付与（GPT）

```bash
uv run scripts/enrich_tasks.py outputs/cvpr2026_enriched.csv -o outputs/cvpr2026_tasks.csv
```

同じく `--limit / --model / --workers` あり。

固定タクソノミ（31カテゴリ） + 自由記述キーワードのハイブリッド:

- `task_primary`: 1個 — 固定リストから最も中心的なタスク
- `task_secondary`: 0〜2個 — 固定リストから（明示的に該当するもののみ）
- `task_keywords`: 3〜5個 — 自由記述（"3d gaussian splatting", "visual localization" 等）
- `modality`: image / video / 3d / point-cloud / multimodal / sensor / other
- `task_summary`: 1行(≤100字)サマリ

固定カテゴリ:
classification, detection, segmentation, pose-estimation, human-mesh, depth-estimation, tracking, action-video, image-generation, video-generation, 3d-generation, editing, 3d-reconstruction, novel-view-synthesis, vlm, self-supervised, foundation-model, domain-adaptation, continual-learning, test-time-adaptation, federated-learning, ood-robustness, adversarial-robustness, efficiency-compression, medical-imaging, autonomous-driving, robotics-vla, face-avatar, low-level, benchmark-dataset, other

> ドメイン特化カテゴリ（medical-imaging / autonomous-driving / robotics-vla / face-avatar）は技術系（vlm / foundation-model 等）より優先する設定。
> 当てはまりが弱い場合は `other` に倒し、内容は `task_keywords` で見られるようにしている。

## 規模感とコスト（CVPR 2026 全件 = 約1500件の例）

| 段階 | 並列度 | 所要時間 | コスト |
|---|---|---|---|
| fetch | (なし) | ~30分 | 無料（API） |
| enrich_comments | 5並列 | ~10分 | < $0.20（gpt-4o-mini）|
| enrich_tasks | 5並列 | ~10分 | < $0.20（gpt-4o-mini）|
| **計** | | **~50分** | **< $0.50** |

fetchはarXiv APIのレート制限（IPごと）で並列化不可。enrichはOpenAI tier1で5並列なら余裕、増やすこともできる（`--workers 10` 等）。

## 他学会・他クエリへの流用

スクリプトはCVPR専用ではなく、`fetch_arxiv.py` のクエリを変えるだけで他学会も取れます。NeurIPS/ICCV/ECCV/ICLR/ICML 等。

```bash
uv run scripts/fetch_arxiv.py "co:neurips AND co:2026" 3000 -o outputs/neurips2026.csv
uv run scripts/fetch_arxiv.py "co:iccv AND co:2025" 2000 -o outputs/iccv2025.csv
```

ただし以下は **CVPR 2026に特化したまま** なので、別学会でちゃんと使うには手を入れる必要があります:

1. **`enrich_comments.py` の SCHEMA / SYSTEM_PROMPT**: `is_cvpr2026` キー名や、Findings Track の判定ルールが CVPR 2026 前提。NeurIPS なら `is_neurips2026` + Track が `main / dataset-and-benchmark / workshop` 等
2. **`index.html` の `DEFAULT_CSV` と「cvpr 2026 only」フィルタラベル**: 別学会用にフロントを使う場合は名前を直すか、フロント側を学会非依存にリファクタする手も
3. **タクソノミ**: `enrich_tasks.py` の `TASK_CATEGORIES` は CV寄り。NLP系学会だと `language-model / text-generation / qa / summarization / ...` 等を入れた方が良い

逆に **fetch / 並列enrich / 静的フロント** といった**インフラ部分はそのまま使える**。

## フィルタ運用例

最終CSV `outputs/cvpr2026_tasks.csv` に対して:

```bash
# コード公開済み + 著者4人以下のCVPR 2026 main/findings
uv run python -c "
import csv
with open('outputs/cvpr2026_tasks.csv') as f:
    for r in csv.DictReader(f):
        if (r['is_cvpr2026']=='yes' and r['track'] in ('main','findings')
            and r['repo_url'] and int(r['author_count']) <= 4):
            print(r['title'], '|', r['repo_url'])
"
```

`task_keywords` を grep すれば、固定タクソノミに無いトピック（visual localization、3d gaussian splatting 等）でも絞れる。

## フロント（ブラウザ閲覧）

`index.html` が静的フロント。CSVをロードしてフィルタ/ソート/詳細展開ができる。

```bash
uv run python -m http.server 8765
# → http://localhost:8765/ をブラウザで開く
```

デフォルトで `outputs/cvpr2026_tasks.csv` を読み込む（`index.html` の `DEFAULT_CSV` で変更可）。別CSVに切り替えたい場合は右上の file picker から選択。

機能:
- 検索（title / abstract / task_summary / task_keywords / comment / authors を横断）
- フィルタ: `is_cvpr2026=yes` only / `track` / `task_primary` / `modality` / has_repo / 著者数レンジ
- ソート: published, author_count, title（列ヘッダクリックでも切替）
- 行クリック → abstract / authors / categories / comment / keywords を展開
- 各行から `abs / pdf / repo` リンク
- ★お気に入り（localStorage 永続化、JSONエクスポート/インポート対応）。キーは正規化された arXiv ID なので、CSV更新（再fetch / 別学会CSVに差し替え等）後も維持される

依存: PapaParse のみ（CDN）。ビルド不要。
