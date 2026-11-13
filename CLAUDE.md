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
- [ ] Day 4　Excel：Wild、Scatter、主遊戲 RTP、命中頻率
- [ ] Day 5　Excel：免費遊戲、重觸發 1/(1−r)、總 RTP
- [ ] Day 6　Excel：變異數、波動度指數、派彩區間分佈（樞紐分析表）、信賴區間 → PAR Sheet v1
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

- 2026-11-13（下午）：Day 4 第 1 步進行中。重講 RTP：先用玩具遊戲（1 軸 4 格、押 10、派 0/20/0/5）逐題確認名詞（軸、停輪組合 T、總押注 T×bet、總派彩＝金額加總而非盤面數），勝推出 RTP = 25/40 = 0.625 並用 E[W]/bet 驗證、算出假設例 0.96。Ways：乘法原理（2×2×1 = 4 路）、全部盤面總路數 Sum₁Sum₂Sum₃N₄L₅（勝自己寫出 3/4/5 連公式），H1 = 155,520／31,104／7,776 路、總派彩 16,329,600、RTP 貢獻 1.344%。Excel `Ways` 工作表：符號為欄（B–I = H1…T），列 2–6 Sum1–5 `=Window1!M33`…、7 N4 `=Window4!M34`、8 N5 `=Window5!M34`、9 L5 `=Window5!$G$2`、11–13 Ways3/4/5（如 `=B2*B3*B4*B7*B9`），openpyxl 驗收通過。卡過：公式寫 `L5` 被當儲存格位址（同 H1 陷阱）、表頭前置空格又出現一次。**注意：目前 8 符號總 RTP 只有約 28.7%（Claude 已私下算出，尚未告訴勝），讓勝在 Excel 算出後自己發現，再討論調整賠率／捲軸／加 Wild。** 筆記新增第 13 節 RTP、第 14 節 Ways 總路數。賠率表：勝選 Power Query（理由：單一設定檔），但誤在 Reels 查詢的進階編輯器裡貼上 Paytable 程式碼，Reels 表被取代 → Counts、Window1–4 公式變 `#REF!`、Window5 與 Counts F 欄被改指 `Paytable[Symbol]`。已修復：原工作表改名 `Paytable`（表格 Paytable：Symbol、Pay3–5），從空白查詢重建 `Reels` 查詢（Pos 0–29、Reel1–5），Ctrl+H 修 Window1–5（各 91 筆），Counts 重打 B2 往右／下拖；openpyxl 全活頁簿驗收通過、無 #REF!。excel/ 尚未 commit，已建議勝 commit。已 commit 8891d8c（excel 首次進 git，未 push）。之後完成 Ways 表：Pay3–5 列 `=INDEX(Paytable[[Pay3]:[Pay3]], MATCH(B$1, Paytable[[Symbol]:[Symbol]], 0))`（勝自己寫出、理解 #N/A 與表格欄位鎖定）；Win3–5（第 19–21 列）、WinTotal（22）、RTP 貢獻（23）`=B22/($L$19*$L$20)`；新增 `Config` 查詢（`#table({"Bet"}, {{Source[bet]}})`），L19 T `=Window1!G2*…*Window5!G2`、L20 Bet `=INDEX(Config[Bet], 1)`；L22 TotalWin 349,166,700、L23 RTP = **0.28738**，與 Python 獨立計算一致。卡過：存檔沒存到（Power Query 視窗／編輯狀態）。勝要「給答案」時直接給公式即可。**目前主遊戲 RTP 只有 28.7%，是設計太小氣不是算錯。** 勝想降 Bet：算出目標 90% 需 Bet ≈ 15.97 → 取 16 得 89.8%（往上取整 RTP 變低）；討論後**決定 (b)：Bet 維持 50，等 Wild、Scatter、免費遊戲都加完再一次調到目標總 RTP**（業界約主遊戲 65–70%、Scatter＋免費遊戲 25–30%、總 ~96%）。勝答對命中頻率不變。Wild 概念完成：單盤面 K 2 路、A 1 路；Sum 改為「K 或 W」個數加總、N 改為「沒有 K 也沒有 W」（勝答對）。Day 3 打勾。**下次從 Wild 三個設計決定開始**（Claude 建議：W 只放軸 2–5、W 不派彩、每軸 1 個且取代原符號維持 30 格；勝尚未決定），之後改 game.json、Excel 加 W、重算 RTP；再做命中頻率、Scatter。excel 在 8891d8c 之後的修改尚未 commit。

- 2026-11-13：Day 3 第 4 步 4-3 進行中。勝原本不懂 MOD，從「取餘數、時鐘繞回」講起，自己發現 MOD(30,30)=0 而捲軸沒有第 0 格，推出環狀位置公式「往下第 k 格 = MOD(p − 1 + k, L) + 1」（中間寫錯過除數改成 29、忘了 +k，用代入驗算修正）。`Window` 工作表完成位置欄：A Pos 1–30、B Row1 `=A2`、C Row2 `=MOD(A2, $G$2) + 1`、D Row3 `=MOD(A2+1, $G$2) + 1`；G2 `=COUNTA(Reels[Reel1])` 取代寫死的 30。openpyxl 驗收通過。教學注意：勝對 Excel 函式名稱與術語不熟，新函式要從「它是什麼、舉例」講起，一次一個；指示要附「做完長什麼樣子」的示意圖，否則會不懂要產出什麼。接著學 INDEX（置物櫃比喻）：一開始看 Excel 列號找位置，差一格（off-by-one，表頭佔第 1 列）；I–K 欄 Sym1–Sym3 `=INDEX(Reels[Reel1], B2/C2/D2)`，第一次往右拖導致 Reel1 變 Reel2/Reel3（Excel 不報錯、只有逐格比對抓得到），且漏拖 K31；修正後 openpyxl 逐格比對 game.json 通過（目前只做 Reel 1）。之後勝預測 H1 看得到的停止位置（一開始方向反了寫成 20–22、27–29，又一次看 Excel 列號差一格；修正後答對 19–21、26–28，加總 6、0 有 24 個）。M–T 欄 8 符號計數 `=COUNTIF($I2:$K2, M$1)`（$ 自己放對；曾因表頭 " Q" 前置空格數不到、舊公式 J3:L3 殘留，已修）；第 33 列 Sum `=SUM(M2:M31)`、第 34 列 N `=COUNTIF(M2:M31, 0)`，8 符號全部符合 Σ = 3c、N = L − 3c，openpyxl 驗收通過。面試題：間距 2 時 N 比 L − 3c 多（重疊幾個多幾個），但 Σ 永遠 = 3c，勝答對方向，原因由 Claude 補完整。之後擴充到 5 軸：`Window` 改名 `Window1`，「移動或複製 → 建立複本」做出 Window2–5，Ctrl+H（搜尋範圍＝工作表、查詢＝公式）把 Reel1 換成 Reel2…，每張取代 91 筆（90 INDEX + 1 COUNTA）。5 張表 openpyxl 全部驗收通過（注意 5 軸組成相同，Sum/N 驗不出換軸，要看 Pos 5、Pos 30 的符號）。筆記第 12 節已更新並重新發布 artifact。**4-3 完成，Day 3 第 4 步結束。下次從 Day 4 開始**：用 5 張 Window 表的 Sum（Σ = 3c）與 N 算 Ways「剛好 3/4/5 連」路數（先讓勝推公式），再加 Wild、Scatter、RTP（記得 EV 要除以押注 50）。

- 2026-11-12：Day 3 第 1 步完成。Q1（均勻＋獨立 → 1/∏Lᵢ）、Q2（剛好 3/4/5 連 = 640/128/32，加總 800 驗算）、Q3（雙重計數 3cᵢ、E[Xᵢ]=3cᵢ/Lᵢ、Ways 路數總和 3c₁·3c₂·3c₃·N₄·L₅、P(X=0)≠1−3c/L、間隔通式 N=Σmax(0,gⱼ−2)、捷徑成立 ⇔ 間距 ≥ 列數）全部通過。第 2 步也完成：Lines/Ways 派彩差異（只算最長、互斥才能加總）練習通過；**決定採用 5×3、243 Ways**。對照 ezslotdesign slotmath4 尚缺：Wild 替代公式、EV 除以押注（Day 4）。複習筆記：`notes/study-notes.html`，已發布為 artifact（網址記在 Claude 記憶）。數學式一律用純文字，不用 LaTeX。第 3 步也完成：`config/game.json`「轉起來!」— bet 50 點、賠率以點數／每路（整數）、8 符號（H1–H3 high、A K Q J T low）、5 軸各 30 格（H1 2、H2 3、H3 3、A K Q 各 4、J T 各 5，同符號間距 ≥ 3），驗收含 symbols／paytable／捲軸一致性檢查，全部通過。勝在 Claude Code 對話框用 `! 指令` 執行（bash，路徑用 `/`，python 加 `-X utf8`）。第 4 步完成 4-1、4-2：`excel/par_sheet_v1.xlsx` — `Reels` 工作表由 Power Query 直接讀 game.json（表格名 Reels，欄 Pos、Reel1–5）；`Counts` 工作表 `=COUNTIF(Reels[Reel1], $A2)`、合計列 SUM = 30，已用 openpyxl 逐格比對 JSON 通過。卡過的點：符號名 H1 被當成儲存格位址、$ 混合參照、公式錯一列、編輯中 Ctrl+S 沒存到。驗收方式：Claude 用 openpyxl 讀 xlsx 比對 JSON。**下次從 4-3 開始**：`Window` 工作表，每個停止位置、每軸視窗內各符號個數（頭尾相接取 3 格）→ 算 N（看不到該符號的停止位置數），與 L − 3c 捷徑交叉驗算；之後 Day 4 再做 Ways 路數、Wild、Scatter、RTP。

- 2026-11-11：Day 1、Day 2 由勝自行複習完成（排列組合、條件機率、期望值、變異數、離散分布、一步轉移矩陣、穩態分布、RTP），統計部分邊做邊補。環境：Windows + PowerShell，虛擬環境 `.venv`，repo DavidChung0305/slot-math-portfolio。Day 3 開始：第 1 步「捲軸帶與樣本空間、Lines 組合數、Ways 視窗計數」理論題已出（Q1 總組合數與等機率、Q2 單線剛好 3 連 A 的組合數，數值例 Lᵢ=10、cᵢ=2、Q3 Ways 視窗 A 個數總和），尚未作答。**下次從回答 Q1–Q3 開始**，接著決定 Lines 或 Ways、設計 config/game.json，再開 Excel。
