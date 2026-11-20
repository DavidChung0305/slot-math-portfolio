# 機率工程師作品集專案（slot-math-portfolio）

## 我是誰、目標是什麼

- 我是勝，政大應用數學系畢業，修過統計、機率論、隨機過程（沒學過測度論）。
- 會 C#、ASP.NET Core、SQL Server、Git；Python 還不熟。
- 目標：轉職**機率工程師**（博弈老虎機與抽卡遊戲的數學模型）。
- 這個專案是求職作品集，要能證明：數學模型算得對、模擬驗證得了、程式寫得乾淨。

## 教學模式（最重要，每次都要遵守）

你是帶我做專案的導師，不是代寫的工程師。

1. **一次只做一小步。** 每一步先說明「要做什麼、為什麼」，再讓我動手。
2. **數學先讓我推。** 遇到公式（RTP、變異數、馬可夫鏈），先問我怎麼推，我卡住再給提示，最後才給完整推導。
3. **程式碼我來寫，你來審。** 預設只給函式簽名、虛擬碼或關鍵片段；我寫完你檢查並指出問題。只有我說「直接寫」時，才給完整程式碼。
4. **每一步都有驗收標準。** 例如「RTP 要等於 0.9600」「pytest 全部通過」「模擬值落在 95% 信賴區間內」。沒通過就不往下走。
5. **主動檢查我的理解。** 每完成一個段落，問我一兩個面試可能會問的問題。
6. **用繁體中文回答。** 程式碼的變數和註解可以用英文。
7. **每次結束前更新下方的「進度紀錄」。** 寫下完成了什麼、卡在哪裡、下次從哪裡開始。

## 技術選擇

| 工具 | 用途 |
|---|---|
| Excel | PAR Sheet、理論值計算、矩陣運算（MMULT、MINVERSE） |
| Python（NumPy、Pandas、pytest） | 主力：模擬器、抽卡模型、RNG 檢定 |
| C# | 結算引擎，和 Python 交叉驗證 |
| GitHub Actions、Docker | 自動化迴歸測試 |

## 目錄結構

```
slot-math-portfolio/
├── CLAUDE.md
├── config/       遊戲設定（JSON）：捲軸、賠率表、免費遊戲規則
├── excel/        PAR Sheet
├── python/
│   ├── slotmath/     結算邏輯、理論計算
│   ├── sim/          蒙地卡羅模擬
│   ├── gacha/        抽卡保底模型
│   └── tests/        pytest
├── csharp/       結算引擎（交叉驗證）
├── docs/         收斂圖、派彩分佈圖、分析報告
├── .github/workflows/
├── Dockerfile
└── README.md
```

## 程式規範

- 遊戲設定一律放在 `config/*.json`，Excel、Python、C# 讀同一份設定。
- **金額用整數計算**（以「分」或最小押注單位），不要用 float 累加。
- 模擬一律用 `numpy.random.Generator`，固定種子可重現；平行時每個工作者用獨立的子種子。
- 模擬要向量化（一次產生一整批停止位置），不要逐轉 for 迴圈。
- 每個結算函式都要有 pytest，包含邊界情況（全 Wild、Scatter 剛好 3 個、最大贏分盤面）。
- 輸出的理論值和模擬值要並排，附 95% 信賴區間：RTP ± 1.96·σ/√N。

## 參考資料

- ezslotdesign.com/slotmath2/：Ways、Scatter、免費遊戲、重觸發的範例與答案
- 清大開放式課程「隨機過程」第 3 章：多步轉移、狀態分類、賭徒破產
- Grinstead & Snell《Introduction to Probability》11.2：吸收鏈 N = (I − Q)⁻¹、t = N·1、B = N·R

## 20 天計畫

### 階段 A：做出能投履歷的作品（Day 1–10）

- [x] Day 1　期望值、條件機率、全期望值、排列組合
- [x] Day 2　伯努利／二項／幾何分布、離散分布的 μ 與 σ、中央極限定理、信賴區間；Python 與 NumPy 基礎
- [x] Day 3　Lines／Ways、賠率表；Excel 建捲軸、算各獎項組合數
- [x] Day 4　Excel：Wild、Scatter、主遊戲 RTP、命中頻率
- [x] Day 5　Excel：免費遊戲、重觸發 1/(1−r)、總 RTP
- [x] Day 6　Excel：變異數、波動度指數、派彩區間分佈（樞紐分析表）、信賴區間 → PAR Sheet v1
- [ ] Day 7　Python 結算邏輯：讀 JSON、單盤面結算、整數計算
- [ ] Day 8　NumPy 模擬 1,000 萬轉；Pandas 理論值與模擬值對照表
- [ ] Day 9　pytest、GitHub、README
- [ ] Day 10　改寫履歷、練習面試題 → **開始投履歷**

**投履歷門檻：** RTP／命中率／波動度正確；模擬 RTP 落在 95% 信賴區間內；README 有對照表；能口頭推導重觸發公式和信賴區間。

### 階段 B：邊投邊補（Day 11–20）

- [ ] Day 11　多步轉移 Pⁿ、第一步分析、賭徒破產
- [ ] Day 12　吸收鏈 N、t、B；Excel MMULT／MINVERSE；狀態分類觀念
- [ ] Day 13　狀態設計：累進倍數、Hold & Spin
- [ ] Day 14　抽卡硬保底、軟保底：期望抽數、綜合機率 = 1／平均抽數
- [ ] Day 15　Python 模擬 10 萬名玩家抽卡，抽數分佈與理論對照
- [ ] Day 16　10 億轉大規模模擬（分批 + multiprocessing）；收斂圖；尾端風險；精度檢查
- [ ] Day 17　GitHub Actions 迴歸測試；Dockerfile
- [ ] Day 18　RNG 卡方均勻性檢定；PAR Sheet v2；GLI-19 概要
- [ ] Day 19　C# 結算引擎，與 Python 逐盤交叉驗證
- [ ] Day 20　更新 README 與履歷、模擬面試、檢討

## 面試題清單（做到相關段落時要能回答）

1. 兩款 RTP 都是 96% 的遊戲差在哪？
2. 模擬 RTP 95.8%、理論 96%，這樣算對嗎？
3. 每轉觸發機率 1/200，平均幾轉觸發？100 轉內至少觸發一次的機率？
4. 用兩種方法推導含重觸發的免費遊戲平均轉數
5. 硬保底 90 抽，平均幾抽出 SSR？綜合機率多少？
6. Hold & Spin 的狀態怎麼定義？
7. 賭徒破產問題
8. 怎麼確保模擬結果正確？
9. 跑 10 億轉怎麼避免浮點數誤差？
10. 怎麼把數值驗證放進 CI/CD？

## 進度紀錄

（每次工作結束時由 Claude 更新，最新的放最上面）

- 2026-11-21（續）：commit 5f97b66（Day 6 收尾）。**Day 7 改做 pytest（勝同意先 pytest、再調 RTP 到 ~96%）。** `python/tests/test_exact.py` 共 **10 passed**（`cd python && ../.venv/Scripts/python.exe -m pytest -v`，約 1 秒）：symbol_win 3 連 20（Claude 示範）、4 連 180／5 連 400（勝請 Claude 寫；勝問 five_of_a_kind 是什麼）、軸 1 沒有 [0,1,2,3,2]、軸 3 斷掉 [1,2,0,3,2] → 0（勝自己寫 ✓，預測兩個都 0 ✓）；board_win（Claude 寫 fixture `game`、勝請 Claude 寫測試）：Scatter 剛好 3 個 [0,0,4,3,2] = 100、剛好 2 個 [0,0,4,0,2] = 0（勝一度把 A／B 的 S 個數對調、以為 B 要看免費遊戲，已釐清 board_win 只算 X）、5 個 S [0,4,7,4,3] = 2500（勝手算 ✓）；fixture `all_wins`：max = 2500 且 (==2500).sum() == 3⁵、總點數 624,113,505 迴歸（Excel 已交叉驗證）。教過：規則交界（勝問）、突變測試（勝請 Claude 做：c[3]==0 改 ==1 → 3 連、5 連 FAILED，已還原）、漏乘軸 3 預測勝答「都消失」→ Claude 解說只有 5 連、軸 3 斷掉會失敗（測試數字別挑 1）、assert 語法（勝問）、為什麼 243 = 3⁵（勝說「教我」）。轉職筆記新增「Day 7：pytest」並重新發布。**tests/、notes、CLAUDE.md 尚未 commit。下次繼續 Day 7**：可再加 window_counts 頭尾相接測試（停止位置 29 → 格 29、0、1）、all_board_wins 與 board_win 隨機抽盤一致、all_board_awards 平均 = r、total_moments 與模擬 CI 一致（模擬測試要固定 seed、N 不要太大）；之後調總 RTP 到 ~96%（先讓勝想要調哪裡：賠率／捲軸／免費遊戲倍數，各會怎麼影響 σ）。

- 2026-11-21：**Day 6 完成 → PAR Sheet v1。** commit 1925419（exact.py、simulate.py、兩份筆記、Excel；commit 前 Claude 清掉 exact.py 行尾空白／空白行、補檔尾換行）。勝選 (a) Python → CSV → Power Query，並請 Claude 寫 Python：`exact.py` 新增 `total_moments(config)`（第一步分析公式，係數用 config 的 multiplier）、`python/sim/export_par.py`（`python -m sim.export_par`，輸出 `excel/data/par_stats.csv` 14 個指標、`par_dist.csv` 6 區間；區間標籤用 `(1,5]`，因 "1-5" 會被 Excel 當日期）。勝做 Excel：Power Query 讀兩個 CSV → `Volatility` 工作表（表格 ParStats A1:B15、ParDist D1:G7；「匯入資料」視窗不會選，Claude 圖解：表格／目前工作表／=Volatility!$D$1）；勝說「教我」→ Claude 給 J `=INDEX(ParStats[Value], MATCH("VI", ParStats[Metric], 0)) / SQRT(I2)`、K/L = RTP_Total ∓ J，N = 1,000／10,000／1,000,000 → [48.70%, 73.85%]、[57.30%, 65.25%]、[60.88%, 61.67%]，openpyxl 驗收 ✓（K、L 尚未設百分比格式）。理解題：N ×1000 → 半寬 1/31.6，勝答對（半寬 ∝ 1/√N）✓。轉職筆記新增「Day 6 收尾」小節並重新發布。更新流程：改 game.json → `python -m sim.export_par` → Excel 全部重新整理。**下次從 Day 7 開始**：Day 7 原計畫（讀 JSON、單盤面結算、整數計算）大多已在 exact.py 完成 → 先跟勝確認 Day 7 改做什麼（建議：補 `retrigger` 開關、把 board_win 整理成正式結算函式並開始寫 pytest 邊界案例：全 Wild、Scatter 剛好 3 個、最大贏分盤面），以及何時把總 RTP 調到 ~96%（建議 Day 7–8 之間，調完重跑 export 即可更新 PAR Sheet）。

- 2026-11-20（晚）～21：**Day 6 派彩區間分佈完成。** 概念（勝說「教我」）：同 RTP、同 σ 的遊戲 A（50% 0／50% 2）與 B（90% 0.667／10% 4）手感不同；勝答 B 命中 100%、LDW 90% ✓，調整方向答「LDW 增加」（Claude 補：中間獎 ↓、大獎更稀有更大以維持 RTP、σ）。`exact.py` 新增 `payout_distribution(wins, bet, edges)`（Claude 逐段講＋勝要求「用圖解釋」→ 10 盤玩具例圖解布林陣列、zip、(lo, hi]；勝貼上）：主遊戲 0 51.83%（≤ 1 − 47.63%，差 = 只有 Scatter 派彩的盤面）、0-1 33.78%、1-5 13.03%、5-20 1.35%、20-100 0.0085%、>100 0，加總 1 ✓。勝說「教我」→ P(LDW | 中獎) ≈ 70%；加免費遊戲後「0」「0-1」不變（觸發盤面必有 Scatter 派彩）、其餘往右搬、>100 出現；不能窮舉 → 模擬。**`python/sim/simulate.py` 的 `simulate_spins(config, n, seed)` 由 Claude 寫**（勝說「你幫我寫，現在在幹嘛」— 勝對整體方向迷失，Claude 用 PAR Sheet 清單說明目前位置）：攤平 wins／awards 抽 index、pending 一輪一輪向量化重觸發、整數點數；100 萬轉 seed 2026：RTP 0.61239 CI [0.60841, 0.61638] ∋ 0.61274 ✓、sd 2.0333 ✓、0 51.88%、0-1 33.81%（與窮舉在誤差內）、1-5 12.27%、5-20 1.84%、20-100 0.19%、>100 2 次、最大 109.6 倍。未接 `retrigger` 開關。exact.py 小整理待勝做：第 57、96 行行尾空白、第 76 行整行空白、檔尾缺換行。數學複習筆記已更新。教學注意：勝累了或迷失時，先給「整體地圖」再進細節。**exact.py、sim/、notes、CLAUDE.md、excel 尚未 commit。下次從 Day 6 最後一步開始：把 σ、VI、95% 區間、派彩區間分佈（主遊戲窮舉＋含免費遊戲模擬）寫進 Excel → PAR Sheet v1**（Python 輸出 CSV 再由 Power Query 讀，或 Claude 用 COM 寫入；先讓勝決定），之後 pytest。總 RTP 調到 ~96% 的時機也要決定。

- 2026-11-20（下午）：**Day 6 步驟 5 免費遊戲變異數完成：σ_total = 2.0283。** E[Z]：勝依序答 `m*X`（漏 ×2、X 應為 E[X]）→ `2X + r·E[X]` → `2E[X] + r·2E[X]`（只到子代）→ 級數得 2E[X]·1/(1−r)（寫成 `1/1-r`，已提醒括號）→ 方程式 E[Z] = 2E[X] + r·E[Z] ✓；E[Z] = 1.1264。理解題「每主遊戲轉從免費遊戲拿多少」勝先答 E[Z]×P(觸發)×2E[X]（重複算 2E[X]、應乘 r），改正為 r·E[Z] ≈ 0.0991 = RTP_FG ✓。二階：勝展開 Z² = 4X² + 4XS + S² ✓；E[S²] 的項數（a 個平方、a(a−1) 個交叉，勝一度說「6 個，合成」已釐清）✓；同分布／獨立勝說「教我」→ 骰子例；E[S²] = E[A]E[Z²] + E[A(A−1)]E[Z]² 勝寫出 ✓；X、A 不獨立勝答出 ✓；E[XS] = E[XA]E[Z] 勝說「教我」；組合 E[Z²] 勝說「你組」→ Claude 組；E[T²] 勝展開 X² + 2XS + S² ✓、答出不用移項的原因（T 的子孫是免費轉）✓。Python：`expand` 搬到模組層級、新增 `all_board_awards(config)`（勝要求整段程式碼，Claude 給完整檔案並講解，勝貼上），驗收 A.mean() = 0.08795 ✓。勝寫 E[XA] 先後錯 `wins**a`、`/bet**2`、小寫 a，E[A(A−1)] 錯 `A * A(A-1)`，最後 `(A * (A-1)).sum() / n` ✓。結果：E[XA] 0.29330（E[X]E[A] 0.04518，正相關）、E[A(A−1)] 0.8273（手算一致）、E[Z²] 10.6718、E[T²] 4.4895、**Var(T) 4.1141、σ_total 2.0283**；Claude 跑 200 萬次含重觸發模擬：RTP 0.61279（95% CI 含理論）、σ 2.0247 ✓。**新增數學複習筆記** `notes/math-review.html`（勝要求：只收數學、持續更新；artifact https://claude.ai/artifact/SU99vi7DQ9xWYAZoTkw4r4，記憶 math-review-artifact）；study-notes.html 本次未更新。exact.py 尚有 `# ★` 標記註解待勝刪除。面試檢查：Q1（σ 怎麼算、為何不能變異數相加）勝答出不獨立／正相關，Claude 補 Var(X+S) = Var X + Var S + 2Cov、Cov(X,S) = E[Z]·Cov(X,A) 與範例答法；Q2（×3 倍數）勝答 RTP、σ 都變大、σ 較多 ✓，Claude 補數字 RTP 66.23%、σ 2.6204。**VI 完成：** 勝說「教我」並要求「所有名詞解釋清楚、重要定理教學」→ Claude 講名詞表、Var(cX)/Var(X+Y) → σ/√N、大數法則、CLT、標準化與 1.96、VI = 1.96σ = 3.976、三種用法（預測、驗證、反推轉數 N ≥ (VI/e)²），寫進數學複習筆記第 13 節。練習：10,000 轉區間 [57.29%, 65.25%] ✓（勝先繞道 VI/1.96）；VI 10 vs 2 → 25 倍 ✓（用詞把 VI 說成變異數，已更正：VI ∝ σ、轉數 ∝ σ²）。**exact.py、notes、CLAUDE.md、excel 尚未 commit。下次從 Day 6 派彩區間分佈開始**（先讓勝想：為什麼只有 σ 不夠、要看贏分落在 0、0–1、1–5、5–20… 倍各區間的機率；主遊戲可用 30⁵ 窮舉 np.histogram，含免費遊戲要用模擬），之後 95% CI 整理、寫進 Excel → PAR Sheet v1、pytest。總 RTP 調到 ~96% 的時機也要決定。

- 2026-11-19～20：**Day 6 進行中：主遊戲變異數完成（σ = 1.2556）。** 暖身與 Day 5 收尾後進 Day 6。變異數：勝說「教我算」，Claude 從遊戲 A/B（平均都 1）講定義與捷徑公式；勝問「只是練習嗎」，Claude 說明玩具與真實遊戲同公式，勝選「繼續熟練」，完成練習 2（X 0/0/1/0/4，E[X²] 3.4，Var 2.4）。交叉項：勝問「為什麼不是只中最大獎」→ Claude 釐清同符號只算最長、不同符號相加（Ways!L23 就是相加）；勝算出 (0.2+0.6)² vs 0.2²+0.6²、差 2ab。結論：E[X²] 要逐盤面加總後平方，30⁵ 盤 Excel 放不下 → Python。勝選 **(1) 你寫、我審**，但完全不會 Python，實際上多為 Claude 逐段教（勝要求**每段 Python 都附詳細 C# 對照**，已存記憶 python-with-csharp）。`python/slotmath/exact.py`（勝打字）：`load_config`、`window_counts(reel, symbols, rows=3, wild=None)`（list comprehension 用 rows；5 軸與 Excel Window1–5 M–T 逐格一致）、`symbol_win(c, pays)`、`board_win(stops, counts, s_counts, config)`（[2,3,0,4,7] = 450、[0,4,7,4,3] = 2500）、`all_board_wins(config)`（NumPy 廣播、expand/reshape、np.where、scatter 查表；0.6 秒；RTP **0.5136737** = Excel Scatter!F7；隨機 2,000 盤與 board_win 0 不一致；最大贏分 2500 點 = 5 個 S）、`moments(wins, bet)`（整數先加總最後除 bet²）→ **E[X] 0.51367、Var 1.5766、σ 1.2556**（Fraction 精確驗算一致）。卡過：IndentationError（docstring 多 1 空格）、counts 是什麼（Claude 印出軸 2 表對照 Excel）、廣播 `:` 放不同維的理由、reshape「一欄怎麼塞進 30」。Claude 犯錯兩次已更正：c2[4] 預期值漏了 W 對 H1–H3 的 +1；迷你廣播例「每軸 3 格」與 a=[1,0,2] 矛盾（改稱「從 30 列 counts 取 3 列」）。教學注意：勝對 Python/NumPy 需要圖解（資料流程、立方體、判斷樹）。exact.py 小風格問題：`p%L`、`(p+k)`、`stops[i],j` 少空格、`symbol_win`/`board_win` 前只空一行、`board_win` 回傳 `total` 未轉 int。筆記第 14 節新增變異數、交叉項、Python 各函式，面試問答 +2，artifact 已重新發布。**exact.py、notes、CLAUDE.md 尚未 commit。下次從步驟 5「免費遊戲變異數」開始**：已出題但未答 — Z = 1 次免費轉連同子孫總共贏幾倍押注，Z = 2X + (Z₁+…+Z_A)，請勝仿 m = 1 + r·m 寫 E[Z] = 2E[X] + r·E[Z] → E[Z] = 2·0.51367/(1−0.08795) ≈ **1.1264**（= m × 1.0274）。接著推二階動差（Claude 已私下算好，勿先說）：E[Z²](1−r) = 4E[X²] + 4E[XA]E[Z] + E[A(A−1)]E[Z]²；每主遊戲轉 T = X + Σ_{j≤A} Z_j，E[T²] = E[X²] + 2E[XA]E[Z] + r·E[Z²] + E[A(A−1)]E[Z]²。所需：E[X²] = 1.84050、E[XA] = 0.293302（X 與 A 相關：同一盤面的 S 同時決定 Scatter 派彩與觸發）、E[A] = 0.08795、E[A²] = 0.91525 → E[Z²] = 10.6718、**E[T] = 0.61274、Var(T) = 4.1141、σ_total = 2.0283**（200 萬次重觸發模擬 σ 2.0293 一致）。Python 需另算每盤面 A（awards 查表 n_scatter）。之後：VI = 1.96σ、派彩區間分佈、95% CI、寫進 Excel → PAR Sheet v1、pytest。

- 2026-11-19：**Day 5 免費遊戲 RTP 完成。** 暖身題：勝在 Claude 示範指示變數 X = I₅ + I₇ 後答出 P(X=2) = 1/30，一度把 P(X=1) 用成 5/30（實為 4/30，5/30 是 P(X≥1)）。設計決定（勝）：3/4/5 個 S 給 **10/15/20 次**、**贏分 ×2**（含 Scatter 派彩，Claude 建議、勝未反對）、**可重觸發**；Claude 定免費遊戲用同一套捲軸。勝寫出 r = Σ P(k)·次數 = **0.08795**、等比級數 10/(1−r)、第一步分析 m = 1 + r·m（勝問為什麼，Claude 用全期望值分情況＋自我相似解釋）→ m = 1/(1−r) ≈ 1.0964；Q1 每次送 5 次（r = 5·P(≥3)）、Q2 r ≥ 1 不收斂答對（Claude 補分支過程與上限規則）。條件期望（勝說「教我」：骰子例、1,000,000 轉次數直觀、E[Y|A] = E[Y]/P(A)）→ E[初始|觸發] = 10.27，勝答出比 10 大的原因。RTP_FG = r/(1−r) × 2 × RTP_spin（勝問 RTP_spin／RTP_FG 是什麼、為什麼乘 G7，Claude 解釋單位：次數 × 每次贏幾倍押注、Wald 等式；勝一度答「乘 bet」，提示後答出 ×2）。game.json 新增 `"free_game": {"trigger_symbol":"S","awards":{"3":10,"4":15,"5":20},"multiplier":2,"retrigger":true}`（Claude 教寫、勝貼入）。Excel：Power Query `Config` 加欄 FGMult；新查詢 `FGAwards`（K、Spins）載入 `FreeGame` 工作表 — 勝的「重複」查詢後修改沒保留（仍是 ScatterPay (2) 舊公式），Claude 用 COM 改公式、查詢／表格／連線改名 FGAwards 並存檔；C `=BINOM.DIST(A2,5,Scatter!$H$2,FALSE)`、D `=C2*B2`；摘要勝放在 **F 標籤／G 公式**：G2 P(trigger) 0.00856、G3 r、G4 10.27、G5 m、G6 `=INDEX(Config[FGMult],1)`、G7 `=Scatter!F7`、G8 RTP_FG **9.91%**、G9 **總 RTP 61.27%**（與 Python 一致）。注意：Excel 尚未讀 `retrigger` 開關（m 固定用 1/(1−r)）。筆記第 14 節新增免費遊戲各小節、面試問答 +3、artifact 已重新發布。已 commit e6a98ed 並 push（含上次的修改）。**下次從 Day 6 開始**：變異數與波動度指數（先讓勝推：單轉派彩 X 的 Var = E[X²] − E[X]²，主遊戲每個盤面的 X² 怎麼算；免費遊戲含重觸發的變異數較難，可先用模擬或複合分布思路）、派彩區間分佈、信賴區間 → PAR Sheet v1。總 RTP 調到 ~96% 的時機也要在 Day 6 前後決定。

- 2026-11-18：開頭把前次未 commit 的 excel／notes／CLAUDE.md commit 成 dc2dcc5 並 push（origin/main 同步）。**加速方式：勝選 (a)+(b)** — (a) Excel 公式 Claude 直接給、勝解釋為什麼；(b) 機械性 Excel 操作 Claude 用 PowerShell COM 代勞（Excel 沒開時用背景 `New-Object -ComObject Excel.Application` 開檔、改完存檔關閉）；數學推導與設計決定仍由勝先做。暖身題：勝答出「軸 1 視窗少一個候選符號」，Claude 補「S 取代 J、J 變少」。**Scatter 派彩完成：** 勝寫出 RTP_scatter = Σ P(k)·mₖ、選 2×/10×/50× 算出 **2.12%**（漏答點數換算，Claude 補 100/500/2500）。game.json 新增 `"scatter": {"symbol":"S","pays":{"3":100,"4":500,"5":2500}}`；Excel 新增 Power Query `ScatterPay`（K、Pay）與 `Scatter` 工作表：H2:L2 q_i `=COUNTIF(Reels[Reel i],"S")*3/COUNTA(Reels[Reel i])`、M2 AllEqual、D `=BINOM.DIST(A2,5,$H$2,FALSE)`、E `=B2/INDEX(Config[Bet],1)`、F = D×E，F5 Scatter RTP 2.12%、F6 `=Ways!L23` 主遊戲 49.25%、**F7 總 RTP 51.37%**；Python 逐軸 convolve 獨立驗收一致。勝要求解釋三條公式（×3 停止位置圖、BINOM.DIST 參數、INDEX(Config[Bet],1)）。勝第一次寫 P(≥3) 為 `BINOM.DIST(3,5,0.1,TRUE)`（實為 P(≤3)），提示後改對 `1 − BINOM.DIST(2,5,0.1,TRUE)`。Q1（3c/L 前提：間距 ≥ 3，第 5、7 格例 q = 5/30）、Q2（各軸 q 不同 → Poisson 二項、全機率法則拆軸 5，例 0.0126）勝說「教我」，由 Claude 講解。**未答確認題：** 第 5、7 格有 S 時，視窗內 S 的平均個數 E[X]（答案 6/30 = 0.2，即 3c/L 仍是期望值）— 下次當暖身。筆記第 14 節與面試問答已更新、artifact 已重新發布。**game.json、excel、notes、CLAUDE.md 尚未 commit。下次從 Day 5 免費遊戲開始**（先讓勝決定 3/4/5 個 S 給幾次免費轉、免費遊戲中是否有倍數、能否重觸發，再推平均免費轉數 1/(1−r)）。

- 2026-11-17（晚）：Day 4 Scatter 進行中。講解 Scatter 定義（不連線、數個數、付押注倍數、觸發免費遊戲）；勝認出二項分布，Claude 帶算 q = 0.1 時 P(3/4/5) = 0.0081／0.00045／0.00001、P(≥3) = 0.00856、≈117 轉觸發；只放軸 1、3、5 時 P = q³ = 0.001。決定：S 放軸 1–5（勝：3/4/5 個給不同免費轉次數）、W 不代替 S、每軸 1 個 S 取代 J（Claude 建議，理由見筆記）。game.json 已改（S 位置：軸 1 第 2 格、軸 2 第 7、軸 3 第 10、軸 4 第 6、軸 5 第 5；symbols 加 `{"id":"S","tier":"scatter"}`；勝曾在檔尾多打一個 S 導致 JSON 錯誤，已修），commit b829e9a；之前的 Wild／命中頻率 commit cd9fc14。Excel 重新整理後 **主遊戲 RTP 49.25%**（J 12.29% → 5.25%），Hit 表因 MATCH 找不到 "S" 出現 2,700 列 #N/A、命中頻率被算成 43.72%；勝要求 Claude 直接改，Claude 用 PowerShell COM 操作開著的 Excel 把 H2:J27001 改成 `=IF(E2="S", FALSE, AND(…))`（不用 IFERROR 的理由已解釋）並存檔，驗收 **命中頻率 47.63%（1 in 2.10）** 與 Python 一致。**excel 與 notes、CLAUDE.md 尚未 commit。** 未答的題：命中頻率為何從 51.68% 降到 47.63%（J 變少；軸 1 視窗出現 S 時候選少一個）— 下次當暖身題。**下次從 Scatter 派彩開始**：決定 3/4/5 個 S 付幾倍押注（建議如 2×/10×/50×，存成點數整數），config 加 scatter 區塊，Excel 用二項分布算 Scatter RTP 貢獻；之後 Day 5 免費遊戲。勝說「想加快腳步但又覺得困難」，Claude 提了加速建議（見下一次對話開頭確認勝的選擇）。

- 2026-11-17：Day 4 命中頻率完成。勝答出：各符號中獎不互斥不能相加、只看前 3 軸、規則「∃ s ∈ 視窗₁，軸 2、3 都有 s 或 W」。Excel 新增 `Hit` 工作表窮舉 27,000 種：A n `=ROW()-2`、B–D P1–P3（30 進位：`INT(n/900)+1`、`MOD(INT(n/30),30)+1`、`MOD(n,30)+1`，Claude 教）、E–G S1–S3 `=INDEX(Window1!$I$2:$K$31, $B2, 1/2/3)`（勝自己寫出）、H–J Hit1–3 `=AND(INDEX(Window2!$M$2:$T$31, $C2, MATCH(E2, Window2!$M$1:$T$1, 0))>0, …Window3…$D2…)`、K `=OR(H2:J2)`；N1–N4（M 欄中文標籤）中獎 13,953／27,000、**命中頻率 51.68%、1 in 1.94**，openpyxl 逐列驗收與 Python 一致。全期望值推 E[W|H] = RTP ÷ 命中頻率 ≈ 1.09 倍、LDW；勝答對降押注時 RTP↑、命中頻率不變、平均倍數↑。教學注意：勝對「列」很容易混淆（視窗列／Excel 列／INDEX 第幾列），已在筆記加名詞表，之後固定用 軸／格／停止位置／視窗上中下／Excel 列，並附 ASCII 圖解；勝這段常說「教我寫」，INDEX 二維、MATCH 的用途、混合參照都需要圖解才懂。Claude 曾出錯一題換算提示，已更正。筆記第 14 節新增名詞表、命中頻率、Hit 表、LDW，面試問答 +2，artifact 已發布。**excel、notes、CLAUDE.md 尚未 commit。下次從 Day 4 Scatter 開始**（先讓勝推：Scatter 不必連線、任意位置計數，P(剛好 k 個) 用各軸「視窗有 Scatter」的機率做多項組合；決定 Scatter 放哪幾軸、每軸幾個、付押注倍數還是只觸發免費遊戲）。

- 2026-11-16：Day 4 Wild 段落完成。三個設計決定（勝都自己推出理由）：(1) W 只放軸 2–5（軸 1 決定路屬於哪個符號；軸 1 有 W 會一路多算、要取最高，各符號不能分開算）；(2) 純替代 Wild、不派彩、不進 paytable（軸 1 沒 W，不可能全 W 連線）；(3) 軸 2–5 各把 1 個 T 換成 W（位置：軸 2 第 6 格、軸 3 第 4 格、軸 4 第 7 格、軸 5 第 9 格），維持 30 格，symbols 加 `{"id":"W","tier":"wild"}`。已 commit 5504eb1。倍數分析：每軸 Sum 都 +3，H1 ×1.5、K ×1.25，5 連 H1 ×5.06、K ×2.44（勝自己算）；H1 整體只 ×2.99 因為 3 連乘較少倍數且 N4 24→21，整體是加權平均（勝答出前半）。Excel：Window2–5 M–T 欄改 `=COUNTIF($I2:$K2, M$1)+COUNTIF($I2:$K2, "W")`，Window1 不改；openpyxl 逐格驗收通過，**主遊戲 RTP 28.74% → 56.29%**（與 Python 一致；J 12.29% 最大、T 不變 4.69%）。面試題：有 W 後 N ≠ L − Sum（Window2 A：第 5 格 A 緊鄰第 6 格 W，N = 17 而非 15），結論 N 要直接數，勝答對。教學注意：venv 的 Python 才有 openpyxl（`.venv/Scripts/python.exe`）。筆記第 14 節新增 Wild 設計、倍數分析、Excel 結果、N 陷阱，面試問答 +3，artifact 已重新發布。**excel 的修改尚未 commit。下次從 Day 4「命中頻率」開始**（先讓勝推：命中 = 至少一個符號至少 3 連，各符號事件不互斥，不能把各符號命中機率相加，要算「沒有任何中獎」的盤面數，Ways 下需逐軸組合思考），之後 Scatter。

- 2026-11-13（下午）：Day 4 第 1 步進行中。重講 RTP：先用玩具遊戲（1 軸 4 格、押 10、派 0/20/0/5）逐題確認名詞（軸、停輪組合 T、總押注 T×bet、總派彩＝金額加總而非盤面數），勝推出 RTP = 25/40 = 0.625 並用 E[W]/bet 驗證、算出假設例 0.96。Ways：乘法原理（2×2×1 = 4 路）、全部盤面總路數 Sum₁Sum₂Sum₃N₄L₅（勝自己寫出 3/4/5 連公式），H1 = 155,520／31,104／7,776 路、總派彩 16,329,600、RTP 貢獻 1.344%。Excel `Ways` 工作表：符號為欄（B–I = H1…T），列 2–6 Sum1–5 `=Window1!M33`…、7 N4 `=Window4!M34`、8 N5 `=Window5!M34`、9 L5 `=Window5!$G$2`、11–13 Ways3/4/5（如 `=B2*B3*B4*B7*B9`），openpyxl 驗收通過。卡過：公式寫 `L5` 被當儲存格位址（同 H1 陷阱）、表頭前置空格又出現一次。**注意：目前 8 符號總 RTP 只有約 28.7%（Claude 已私下算出，尚未告訴勝），讓勝在 Excel 算出後自己發現，再討論調整賠率／捲軸／加 Wild。** 筆記新增第 13 節 RTP、第 14 節 Ways 總路數。賠率表：勝選 Power Query（理由：單一設定檔），但誤在 Reels 查詢的進階編輯器裡貼上 Paytable 程式碼，Reels 表被取代 → Counts、Window1–4 公式變 `#REF!`、Window5 與 Counts F 欄被改指 `Paytable[Symbol]`。已修復：原工作表改名 `Paytable`（表格 Paytable：Symbol、Pay3–5），從空白查詢重建 `Reels` 查詢（Pos 0–29、Reel1–5），Ctrl+H 修 Window1–5（各 91 筆），Counts 重打 B2 往右／下拖；openpyxl 全活頁簿驗收通過、無 #REF!。excel/ 尚未 commit，已建議勝 commit。已 commit 8891d8c（excel 首次進 git，未 push）。之後完成 Ways 表：Pay3–5 列 `=INDEX(Paytable[[Pay3]:[Pay3]], MATCH(B$1, Paytable[[Symbol]:[Symbol]], 0))`（勝自己寫出、理解 #N/A 與表格欄位鎖定）；Win3–5（第 19–21 列）、WinTotal（22）、RTP 貢獻（23）`=B22/($L$19*$L$20)`；新增 `Config` 查詢（`#table({"Bet"}, {{Source[bet]}})`），L19 T `=Window1!G2*…*Window5!G2`、L20 Bet `=INDEX(Config[Bet], 1)`；L22 TotalWin 349,166,700、L23 RTP = **0.28738**，與 Python 獨立計算一致。卡過：存檔沒存到（Power Query 視窗／編輯狀態）。勝要「給答案」時直接給公式即可。**目前主遊戲 RTP 只有 28.7%，是設計太小氣不是算錯。** 勝想降 Bet：算出目標 90% 需 Bet ≈ 15.97 → 取 16 得 89.8%（往上取整 RTP 變低）；討論後**決定 (b)：Bet 維持 50，等 Wild、Scatter、免費遊戲都加完再一次調到目標總 RTP**（業界約主遊戲 65–70%、Scatter＋免費遊戲 25–30%、總 ~96%）。勝答對命中頻率不變。Wild 概念完成：單盤面 K 2 路、A 1 路；Sum 改為「K 或 W」個數加總、N 改為「沒有 K 也沒有 W」（勝答對）。Day 3 打勾。**下次從 Wild 三個設計決定開始**（Claude 建議：W 只放軸 2–5、W 不派彩、每軸 1 個且取代原符號維持 30 格；勝尚未決定），之後改 game.json、Excel 加 W、重算 RTP；再做命中頻率、Scatter。excel 在 8891d8c 之後的修改尚未 commit。

- 2026-11-13：Day 3 第 4 步 4-3 進行中。勝原本不懂 MOD，從「取餘數、時鐘繞回」講起，自己發現 MOD(30,30)=0 而捲軸沒有第 0 格，推出環狀位置公式「往下第 k 格 = MOD(p − 1 + k, L) + 1」（中間寫錯過除數改成 29、忘了 +k，用代入驗算修正）。`Window` 工作表完成位置欄：A Pos 1–30、B Row1 `=A2`、C Row2 `=MOD(A2, $G$2) + 1`、D Row3 `=MOD(A2+1, $G$2) + 1`；G2 `=COUNTA(Reels[Reel1])` 取代寫死的 30。openpyxl 驗收通過。教學注意：勝對 Excel 函式名稱與術語不熟，新函式要從「它是什麼、舉例」講起，一次一個；指示要附「做完長什麼樣子」的示意圖，否則會不懂要產出什麼。接著學 INDEX（置物櫃比喻）：一開始看 Excel 列號找位置，差一格（off-by-one，表頭佔第 1 列）；I–K 欄 Sym1–Sym3 `=INDEX(Reels[Reel1], B2/C2/D2)`，第一次往右拖導致 Reel1 變 Reel2/Reel3（Excel 不報錯、只有逐格比對抓得到），且漏拖 K31；修正後 openpyxl 逐格比對 game.json 通過（目前只做 Reel 1）。之後勝預測 H1 看得到的停止位置（一開始方向反了寫成 20–22、27–29，又一次看 Excel 列號差一格；修正後答對 19–21、26–28，加總 6、0 有 24 個）。M–T 欄 8 符號計數 `=COUNTIF($I2:$K2, M$1)`（$ 自己放對；曾因表頭 " Q" 前置空格數不到、舊公式 J3:L3 殘留，已修）；第 33 列 Sum `=SUM(M2:M31)`、第 34 列 N `=COUNTIF(M2:M31, 0)`，8 符號全部符合 Σ = 3c、N = L − 3c，openpyxl 驗收通過。面試題：間距 2 時 N 比 L − 3c 多（重疊幾個多幾個），但 Σ 永遠 = 3c，勝答對方向，原因由 Claude 補完整。之後擴充到 5 軸：`Window` 改名 `Window1`，「移動或複製 → 建立複本」做出 Window2–5，Ctrl+H（搜尋範圍＝工作表、查詢＝公式）把 Reel1 換成 Reel2…，每張取代 91 筆（90 INDEX + 1 COUNTA）。5 張表 openpyxl 全部驗收通過（注意 5 軸組成相同，Sum/N 驗不出換軸，要看 Pos 5、Pos 30 的符號）。筆記第 12 節已更新並重新發布 artifact。**4-3 完成，Day 3 第 4 步結束。下次從 Day 4 開始**：用 5 張 Window 表的 Sum（Σ = 3c）與 N 算 Ways「剛好 3/4/5 連」路數（先讓勝推公式），再加 Wild、Scatter、RTP（記得 EV 要除以押注 50）。

- 2026-11-12：Day 3 第 1 步完成。Q1（均勻＋獨立 → 1/∏Lᵢ）、Q2（剛好 3/4/5 連 = 640/128/32，加總 800 驗算）、Q3（雙重計數 3cᵢ、E[Xᵢ]=3cᵢ/Lᵢ、Ways 路數總和 3c₁·3c₂·3c₃·N₄·L₅、P(X=0)≠1−3c/L、間隔通式 N=Σmax(0,gⱼ−2)、捷徑成立 ⇔ 間距 ≥ 列數）全部通過。第 2 步也完成：Lines/Ways 派彩差異（只算最長、互斥才能加總）練習通過；**決定採用 5×3、243 Ways**。對照 ezslotdesign slotmath4 尚缺：Wild 替代公式、EV 除以押注（Day 4）。複習筆記：`notes/study-notes.html`，已發布為 artifact（網址記在 Claude 記憶）。數學式一律用純文字，不用 LaTeX。第 3 步也完成：`config/game.json`「轉起來!」— bet 50 點、賠率以點數／每路（整數）、8 符號（H1–H3 high、A K Q J T low）、5 軸各 30 格（H1 2、H2 3、H3 3、A K Q 各 4、J T 各 5，同符號間距 ≥ 3），驗收含 symbols／paytable／捲軸一致性檢查，全部通過。勝在 Claude Code 對話框用 `! 指令` 執行（bash，路徑用 `/`，python 加 `-X utf8`）。第 4 步完成 4-1、4-2：`excel/par_sheet_v1.xlsx` — `Reels` 工作表由 Power Query 直接讀 game.json（表格名 Reels，欄 Pos、Reel1–5）；`Counts` 工作表 `=COUNTIF(Reels[Reel1], $A2)`、合計列 SUM = 30，已用 openpyxl 逐格比對 JSON 通過。卡過的點：符號名 H1 被當成儲存格位址、$ 混合參照、公式錯一列、編輯中 Ctrl+S 沒存到。驗收方式：Claude 用 openpyxl 讀 xlsx 比對 JSON。**下次從 4-3 開始**：`Window` 工作表，每個停止位置、每軸視窗內各符號個數（頭尾相接取 3 格）→ 算 N（看不到該符號的停止位置數），與 L − 3c 捷徑交叉驗算；之後 Day 4 再做 Ways 路數、Wild、Scatter、RTP。

- 2026-11-11：Day 1、Day 2 由勝自行複習完成（排列組合、條件機率、期望值、變異數、離散分布、一步轉移矩陣、穩態分布、RTP），統計部分邊做邊補。環境：Windows + PowerShell，虛擬環境 `.venv`，repo DavidChung0305/slot-math-portfolio。Day 3 開始：第 1 步「捲軸帶與樣本空間、Lines 組合數、Ways 視窗計數」理論題已出（Q1 總組合數與等機率、Q2 單線剛好 3 連 A 的組合數，數值例 Lᵢ=10、cᵢ=2、Q3 Ways 視窗 A 個數總和），尚未作答。**下次從回答 Q1–Q3 開始**，接著決定 Lines 或 Ways、設計 config/game.json，再開 Excel。
