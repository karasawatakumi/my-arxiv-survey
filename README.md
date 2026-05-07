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
uv run scripts/fetch_arxiv.py "co:cvpr" 100
# → outputs/arxiv_co_cvpr_100.csv
```

- 第1引数は **arXiv の search_query 式**（例: `"co:cvpr"`, `"diffusion"`, `"ti:transformer AND abs:attention"`）
- 第2引数は取得件数（1〜30000）
- デフォルトでカテゴリ `cs.CV / cs.RO / cs.AI / cs.LG` の論文のみ返す（`primary_category` がいずれかに一致するものに絞る）
- `--categories cs.CL,cs.LG` で上書き、`--categories ""` で無効化

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
uv run scripts/enrich_comments.py outputs/arxiv_co_cvpr_100.csv
# → outputs/arxiv_co_cvpr_100_enriched.csv
```

`comment` 列を OpenAI に送って Structured Outputs で4列を返す:

- `is_cvpr2026`: `yes` / `no` / `unsure`
- `track`: `main` / `findings` / `workshop` / `other` / `unknown`
- `accepted`: `yes` / `no` / `unsure`
- `notes`: 補足（"Highlight" など）

`--limit N` で先頭N件のみ処理（テスト用）。`--model` で OpenAI モデル指定（デフォルト `gpt-4o-mini`）。

> CVPR 2026 では Findings トラックが新設されている（arXivコメントから複数の独立した著者が "Findings Track" と明記しているのが確認できる）。

### 3. title + abstract からタスクカテゴリを付与（GPT）

```bash
uv run scripts/enrich_tasks.py outputs/arxiv_co_cvpr_100_enriched.csv
# → outputs/arxiv_co_cvpr_100_enriched_tasks.csv
```

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

## フィルタ運用例

最終CSV `outputs/arxiv_co_cvpr_100_enriched_tasks.csv` に対して:

```bash
# Findings トラックの medical-imaging
awk -F, '$14=="\"yes\"" && $15=="\"findings\"" && $18=="\"medical-imaging\""' \
  outputs/arxiv_co_cvpr_100_enriched_tasks.csv

# コード公開済み + 著者4人以下
uv run python -c "
import csv
with open('outputs/arxiv_co_cvpr_100_enriched_tasks.csv') as f:
    for r in csv.DictReader(f):
        if r['repo_url'] and int(r['author_count']) <= 4:
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

デフォルトで `outputs/cvpr_100_tasks.csv` を読み込む。別CSVに切り替えたい場合は右上の file picker から選択。

機能:
- 検索（title / abstract / task_summary / task_keywords / comment / authors を横断）
- フィルタ: `is_cvpr2026=yes` only / `track` / `task_primary` / `modality` / has_repo / 著者数レンジ
- ソート: published, author_count, title（列ヘッダクリックでも切替）
- 行クリック → abstract / authors / categories / comment / keywords を展開
- 各行から `abs / pdf / repo` リンク

依存: PapaParse のみ（CDN）。ビルド不要。
