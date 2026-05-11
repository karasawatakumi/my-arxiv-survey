# arxiv-survey

arXiv論文をクエリで取得し、GPTで「学会情報」「タスク分類」を抽出して、ブラウザで閲覧/フィルタするパイプライン。

<img width="3450" height="1930" alt="image" src="https://github.com/user-attachments/assets/3935e8d0-870b-4c33-979c-ffbbdd21a435" />

**🌐 公開ビューア: https://karasawatakumi.github.io/my-arxiv-survey/**

ビューワーの主な機能:

- **お気に入り(★) / メモ(📝)**: ブラウザの localStorage に永続化、JSON で export/import 可能 (別端末との同期)
- **検索 + フィルタ**: title / abstract / keywords / メモ 横断検索、track / task / modality / has_repo / 著者数などで絞り込み
- **行展開**: クリックで abstract / authors / categories / メモエディタを展開
- **カバレッジ表示**: ヘッダに `📅 through YYYY-MM-DD · N papers · fetched ...` (`outputs/cvpr2026_tasks.meta.json` サイドカーから読み込み)
- 既定では `outputs/cvpr2026_tasks.csv` を読み込み、`scripts/update.sh` の差分更新にも自動追従

## クイックスタート

```bash
uv sync                               # 依存解決
echo 'OPENAI_API_KEY=sk-...' > .env    # GPT用キー

# 初回フル: fetch → comment分類 → task分類
uv run scripts/fetch_arxiv.py "co:cvpr AND co:2026" 1700 -o outputs/cvpr2026.csv
uv run scripts/enrich_comments.py outputs/cvpr2026.csv         -o outputs/cvpr2026_enriched.csv
uv run scripts/enrich_tasks.py    outputs/cvpr2026_enriched.csv -o outputs/cvpr2026_tasks.csv

# 以降は差分更新 (新規 + 改訂版だけ取り込んで _tasks.csv にマージ + meta 更新)
scripts/update.sh

# フロントで閲覧
uv run python -m http.server 8765   # → http://localhost:8765/
```

## ディレクトリ構成

| パス | 役割 |
|---|---|
| `.env` | `OPENAI_API_KEY` を記載（gitignore済） |
| `pyproject.toml` / `uv.lock` | uv プロジェクト定義 |
| `index.html` | 静的フロント（CSVブラウザ） |
| `scripts/fetch_arxiv.py` | arXiv API → CSV (`--update` で差分モードも) |
| `scripts/enrich_comments.py` | comment列 → 学会情報 (GPT) |
| `scripts/enrich_tasks.py` | title+abstract → タスク分類 (GPT) |
| `scripts/merge_update.py` | 差分_tasks.csv を既存_tasks.csv にマージ (改訂版置換 + 新規append) |
| `scripts/write_meta.py` | `<csv>.meta.json` サイドカー生成 (カバレッジ情報) |
| `scripts/update.sh` | 差分fetch → 2回のenrich → merge → meta 更新 を一発で |
| `outputs/` | 生成CSV置き場（gitignore済）/ `*.meta.json` はビューワーが読む |

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
| `n` (位置2) | 取得件数（1〜30000）、`--update`時は上限キャップ | (必須) |
| `-o, --output` | 出力CSVパス | `outputs/arxiv_<query>_<n>.csv` |
| `--categories` | カンマ区切りカテゴリ（primary_category絞り込み） | `cs.CV,cs.RO,cs.AI,cs.LG` |
| `--update <CSV>` | 差分モード: 既存CSVを読み、`updated > max(existing.updated)` のみ `sortBy=lastUpdatedDate desc` で取得 | なし |

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
| BACKOFF (5xx等) | 10/20/30/40秒 | `BACKOFF_BASE * attempt` |
| BACKOFF (429) | 60/120/240/480秒 | 指数式。arXiv の IP単位クールダウンは2〜3分続くことがあるため計~15分の回復ウィンドウ |
| `urlopen` timeout | 90秒 | |

429が15分待っても解消しない場合は IP変更（Wi-Fi切替・テザリング）で即解消することが多い。

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

## 差分更新 (`scripts/update.sh`)

初回フル取得を済ませた後は、`scripts/update.sh` で **新着 + 改訂版** だけを取り込んで `_tasks.csv` にマージします。`enrich_*` を全件で再実行する必要が無いのでコストは1〜2桁安く、定常運用はこれで十分。

```bash
scripts/update.sh                              # cvpr2026 既定
scripts/update.sh outputs/foo_tasks.csv        # 別CSV対象
QUERY="co:cvpr AND co:2026" scripts/update.sh  # クエリ変更
CAP=8000 scripts/update.sh                     # 上限引き上げ (デフォルト5000)
```

### 内部動作

1. `fetch_arxiv.py --update <既存CSV>` で `sortBy=lastUpdatedDate desc` で取得し、`updated > max(existing.updated)` の境界で停止。出力CSVには **新規 + 改訂版 (v2/v3 等)** の両方が混在。
2. `enrich_comments.py` → `enrich_tasks.py` を差分CSVに対して実行 (差分が0件なら meta だけ書き換えて exit)。
3. `merge_update.py` で既存 `_tasks.csv` にマージ:
   - 改訂版 (既存ID) → その行を置換 (enrich列含めて全列更新)
   - 新規 → 末尾に append
4. `write_meta.py` が `<csv>.meta.json` を更新 (`total_rows`, `latest_published`, `latest_updated`, `last_fetched_at`, `query`)。
5. 元CSVは `*.bak.<timestamp>.csv` にバックアップを残す。

### 改訂版の扱い

arXiv は v1→v2→v3 と改訂されるたび `updated` が更新されるので、本パイプラインは **改訂版検出時に enrich_comments と enrich_tasks の両方を再実行** します。タイトル変更や comment への "Accepted to CVPR 2026" 追記、abstract 改訂などにも追従できる代わりに、改訂版の数だけ GPT コストが追加でかかります (通常は無視できる数)。

### 制限・既知の挙動

- `--update` モードは `published` ではなく `updated` を境界に使うので、既存IDが arXiv で改訂されると差分に乗ります。改訂を取りこぼしたくない要件ならこの挙動が望ましいですが、「純粋な新着だけ欲しい」場合は merge 後に `published > X` でフィルタしてください。
- カテゴリ外への primary_category 移動は当パイプラインのフィルタ (`cs.CV,cs.RO,cs.AI,cs.LG`) でクライアント側除外されるため、稀に「既存行が更新されないまま残る」ケースがあります。完全な整合が必要なら定期的にフル再取得を回すのが堅い。

## 規模感とコスト

CVPR 2026 全件 ≒ 約1500件取得時の実績:

| モード | 段階 | 並列度 | 所要時間 | コスト |
|---|---|---|---|---|
| 初回フル | fetch | なし | ~30分 | 無料 |
| 初回フル | enrich_comments | 5並列 | ~10分 | < $0.20 |
| 初回フル | enrich_tasks | 5並列 | ~10分 | < $0.20 |
| 初回フル | **合計** | | **~50分** | **< $0.50** |
| **差分 (`update.sh`)** | 全段階 | 5並列(enrich) | **~2〜5分** | **数¢以下** |

fetchはarXiv API側のIP単位レート制限のため並列化不可。enrich側は `--workers 10` 等にしてさらに短縮可能（OpenAI tier1なら余裕）。

差分モードの実例(2026-05-11): 既存1564件 → 25件取得 (22新規 + 3改訂版) → 1586件、所要 3分弱、コスト 1¢未満。日次運用なら数十件で収まる想定。

## フロント（index.html）

普段は **公開URL https://karasawatakumi.github.io/my-arxiv-survey/** にブックマークを置けば十分。ローカルで動かす場合:

```bash
uv run python -m http.server 8765   # → http://localhost:8765/
```

デフォルト読み込みファイルは `index.html` 内の `DEFAULT_CSV` 定数（現在 `outputs/cvpr2026_tasks.csv`）。別CSVは右上の file picker から。

| 機能 | 内容 |
|---|---|
| 検索 | title / abstract / task_summary / task_keywords / comment / authors / メモ 横断 |
| フィルタ | is_cvpr2026=yes only / track / task_primary / modality / has_repo / favorites only / with notes only / 著者数レンジ |
| ソート | published, author_count, title（列ヘッダクリックでも切替） |
| 詳細展開 | 行クリック → abstract / authors / categories / comment / keywords / **メモ編集** |
| リンク | 各行から `abs / pdf / repo` |
| カバレッジ表示 | ヘッダに `📅 through YYYY-MM-DD · N papers · fetched ...`。`outputs/cvpr2026_tasks.meta.json` をサイドカーで読み込み |
| お気に入り(★)・メモ(📝) | localStorage永続化、JSONエクスポート/インポート (★+📝 一括)。キーは正規化arXiv IDなのでCSV更新後も維持 |

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
