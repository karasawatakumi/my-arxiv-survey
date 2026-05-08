# arxiv-survey

arXiv論文をクエリで取得し、GPTで「学会情報」「タスク分類」を抽出して、ブラウザで閲覧/フィルタするパイプライン。

<img width="3450" height="1930" alt="image" src="https://github.com/user-attachments/assets/3935e8d0-870b-4c33-979c-ffbbdd21a435" />

**🌐 公開ビューア: https://karasawatakumi.github.io/my-arxiv-survey/**

`outputs/cvpr2026_tasks.csv` をそのまま読み込みます。お気に入り(★)はブラウザのlocalStorageに保存されるので、別端末で開く時は「export → import」で同期可能。

## クイックスタート

```bash
uv sync                               # 依存解決
echo 'OPENAI_API_KEY=sk-...' > .env    # GPT用キー

# 1. fetch → 2. comment分類 → 3. task分類
uv run scripts/fetch_arxiv.py "co:cvpr AND co:2026" 1700 -o outputs/cvpr2026.csv
uv run scripts/enrich_comments.py outputs/cvpr2026.csv         -o outputs/cvpr2026_enriched.csv
uv run scripts/enrich_tasks.py    outputs/cvpr2026_enriched.csv -o outputs/cvpr2026_tasks.csv

# 4. フロントで閲覧
uv run python -m http.server 8765   # → http://localhost:8765/
```

## ディレクトリ構成

| パス | 役割 |
|---|---|
| `.env` | `OPENAI_API_KEY` を記載（gitignore済） |
| `pyproject.toml` / `uv.lock` | uv プロジェクト定義 |
| `index.html` | 静的フロント（CSVブラウザ） |
| `scripts/fetch_arxiv.py` | arXiv API → CSV |
| `scripts/enrich_comments.py` | comment列 → 学会情報 (GPT) |
| `scripts/enrich_tasks.py` | title+abstract → タスク分類 (GPT) |
| `outputs/` | 生成CSV置き場（gitignore済） |

## パイプラインの全体像

| 段階 | 入力 | 出力（追加列） |
|---|---|---|
| **fetch** | クエリ + N | `id, title, authors, author_count, primary_category, categories, comment, repo_url, published, updated, summary, pdf_url` |
| **enrich_comments** | fetch CSV | `is_cvpr2026, track, accepted, notes` |
| **enrich_tasks** | enriched CSV | `task_primary, task_secondary, task_keywords, modality, task_summary` |

## 1. fetch_arxiv.py

### CLI

| 引数 | 説明 | デフォルト |
|---|---|---|
| `query` (位置1) | arXiv `search_query` 式 | (必須) |
| `n` (位置2) | 取得件数（1〜30000） | (必須) |
| `-o, --output` | 出力CSVパス | `outputs/arxiv_<query>_<n>.csv` |
| `--categories` | カンマ区切りカテゴリ（primary_category絞り込み） | `cs.CV,cs.RO,cs.AI,cs.LG` |

### `search_query` フィールドプレフィクス

| prefix | 意味 | prefix | 意味 |
|---|---|---|---|
| `ti:` | title | `co:` | comment |
| `au:` | author | `jr:` | journal-ref |
| `abs:` | abstract | `cat:` | subject category |
| `all:` | 全フィールド（プレフィクス無しと同等） | | |

例: `"co:cvpr AND co:2026"`, `"ti:transformer AND abs:attention"`, `"diffusion"`

### 事前に総件数を確認

```bash
curl -sS "https://export.arxiv.org/api/query?search_query=co:cvpr+AND+co:2026&max_results=1" | grep totalResults
```

### API レート制限対策（スクリプト内蔵）

| 設定 | 値 | 備考 |
|---|---|---|
| PAGE_SIZE | 25 | 大きい `max_results` だと即429 |
| REQUEST_DELAY | 10秒 | API最小推奨3秒、安全側 |
| MAX_RETRIES | 5 | 429/5xx/タイムアウト時 |
| BACKOFF | 10/20/30/40/50秒 | リトライ間隔 |
| `urlopen` timeout | 90秒 | |

429が連続する場合は IP変更（Wi-Fi切替・テザリング）で即解消することが多い。

### incremental write

ページ単位で逐次CSVに書き込むため、途中で死んでも書き込み済み分は残る。**同じ `-o` で再実行すると上書きされる**点に注意。

## 2. enrich_comments.py

### CLI

| オプション | 説明 | デフォルト |
|---|---|---|
| `input_csv` (位置1) | 入力CSV | (必須) |
| `-o, --output` | 出力CSV | `outputs/<input>_enriched.csv` |
| `--model` | OpenAIモデル | `gpt-4o-mini` |
| `--limit` | 先頭N件のみ処理（テスト用） | (なし) |
| `--workers` | 並列リクエスト数 | 5 |

### 出力スキーマ（Structured Outputs）

| 列 | 値 |
|---|---|
| `is_cvpr2026` | `yes` / `no` / `unsure` |
| `track` | `main` / `findings` / `workshop` / `other` / `unknown` |
| `accepted` | `yes` / `no` / `unsure` |
| `notes` | "Highlight" 等の補足 |

> CVPR 2026 では Findings トラックが新設されている（複数の独立した著者が arXiv コメントに "Findings Track" と明記しているのが確認できる）。

## 3. enrich_tasks.py

### CLI

`enrich_comments.py` と同じ（`--model`, `--limit`, `--workers`, `-o`）。

### 出力スキーマ

| 列 | 内容 |
|---|---|
| `task_primary` | 固定タクソノミから1個（最も中心的なタスク） |
| `task_secondary` | 固定タクソノミから0〜2個 |
| `task_keywords` | 自由記述3〜5個（`3d gaussian splatting`, `visual localization` 等） |
| `modality` | `image` / `video` / `3d` / `point-cloud` / `multimodal` / `sensor` / `other` |
| `task_summary` | 1行(≤100字)サマリ |

### 固定タクソノミ（31カテゴリ）

| グループ | カテゴリ |
|---|---|
| Perception | `classification` `detection` `segmentation` `pose-estimation` `human-mesh` `depth-estimation` `tracking` `action-video` |
| Generation | `image-generation` `video-generation` `3d-generation` `editing` |
| Reconstruction | `3d-reconstruction` `novel-view-synthesis` |
| Foundation/Pretrain | `vlm` `foundation-model` `self-supervised` |
| Adapt/Robustness | `domain-adaptation` `continual-learning` `test-time-adaptation` `federated-learning` `ood-robustness` `adversarial-robustness` |
| System | `efficiency-compression` |
| Domain | `medical-imaging` `autonomous-driving` `robotics-vla` `face-avatar` |
| Low-level | `low-level` |
| Misc | `benchmark-dataset` `other` |

ドメイン特化カテゴリ（medical / autonomous-driving / robotics-vla / face-avatar）を技術系（vlm / foundation-model）より優先する設定。当てはまりが弱い場合は `other` に倒し、内容は `task_keywords` 側に出す。

## 規模感とコスト

CVPR 2026 全件 ≒ 約1500件取得時の実績:

| 段階 | 並列度 | 所要時間 | コスト |
|---|---|---|---|
| fetch | なし | ~30分 | 無料 |
| enrich_comments | 5並列 | ~10分 | < $0.20 |
| enrich_tasks | 5並列 | ~10分 | < $0.20 |
| **合計** | | **~50分** | **< $0.50** |

fetchはarXiv API側のIP単位レート制限のため並列化不可。enrich側は `--workers 10` 等にしてさらに短縮可能（OpenAI tier1なら余裕）。

## フロント（index.html）

普段は **公開URL https://karasawatakumi.github.io/my-arxiv-survey/** にブックマークを置けば十分。ローカルで動かす場合:

```bash
uv run python -m http.server 8765   # → http://localhost:8765/
```

デフォルト読み込みファイルは `index.html` 内の `DEFAULT_CSV` 定数（現在 `outputs/cvpr2026_tasks.csv`）。別CSVは右上の file picker から。

| 機能 | 内容 |
|---|---|
| 検索 | title / abstract / task_summary / task_keywords / comment / authors 横断 |
| フィルタ | is_cvpr2026=yes only / track / task_primary / modality / has_repo / 著者数レンジ |
| ソート | published, author_count, title（列ヘッダクリックでも切替） |
| 詳細展開 | 行クリック → abstract / authors / categories / comment / keywords |
| リンク | 各行から `abs / pdf / repo` |
| お気に入り(★) | localStorage永続化、JSONエクスポート/インポート。キーは正規化arXiv IDなのでCSV更新後も維持 |

依存: **PapaParse** のみ（CDN）。ビルド不要。

## 他学会・他クエリへの流用

`fetch_arxiv.py` のクエリを変えるだけで他学会も取れる:

```bash
uv run scripts/fetch_arxiv.py "co:neurips AND co:2026" 3000 -o outputs/neurips2026.csv
uv run scripts/fetch_arxiv.py "co:iccv AND co:2025" 2000   -o outputs/iccv2025.csv
```

ただし以下は **CVPR 2026特化のまま** なので別学会で本格運用するには手当が必要:

| ファイル | 直すべき箇所 | 例 |
|---|---|---|
| `enrich_comments.py` | SCHEMA / SYSTEM_PROMPT | `is_cvpr2026` → `is_neurips2026`、track値 |
| `enrich_tasks.py` | TASK_CATEGORIES | NLP系なら `language-model` `qa` `summarization` 等 |
| `index.html` | DEFAULT_CSV / フィルタラベル | "cvpr 2026 only" の文言 |

逆に **fetch / 並列enrich / 静的フロント** などインフラ部分はそのまま流用可能。

## フィルタ運用例

```bash
# コード公開済み + 著者4人以下の CVPR 2026 main/findings
uv run python -c "
import csv
with open('outputs/cvpr2026_tasks.csv') as f:
    for r in csv.DictReader(f):
        if (r['is_cvpr2026']=='yes' and r['track'] in ('main','findings')
            and r['repo_url'] and int(r['author_count']) <= 4):
            print(r['title'], '|', r['repo_url'])
"
```

`task_keywords` を grep すれば、固定タクソノミに無いトピック（visual localization, 3d gaussian splatting 等）でも絞れる。
