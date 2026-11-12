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
- [ ] Day 3　Lines／Ways、賠率表；Excel 建捲軸、算各獎項組合數
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

- 2026-11-12：Day 3 第 1 步完成。Q1（均勻＋獨立 → 1/∏Lᵢ）、Q2（剛好 3/4/5 連 = 640/128/32，加總 800 驗算）、Q3（雙重計數 3cᵢ、E[Xᵢ]=3cᵢ/Lᵢ、Ways 路數總和 3c₁·3c₂·3c₃·N₄·L₅、P(X=0)≠1−3c/L、間隔通式 N=Σmax(0,gⱼ−2)、捷徑成立 ⇔ 間距 ≥ 列數）全部通過。第 2 步也完成：Lines/Ways 派彩差異（只算最長、互斥才能加總）練習通過；**決定採用 5×3、243 Ways**。對照 ezslotdesign slotmath4 尚缺：Wild 替代公式、EV 除以押注（Day 4）。複習筆記：`notes/study-notes.html`，已發布為 artifact（網址記在 Claude 記憶）。數學式一律用純文字，不用 LaTeX。第 3 步也完成：`config/game.json`「轉起來!」— bet 50 點、賠率以點數／每路（整數）、8 符號（H1–H3 high、A K Q J T low）、5 軸各 30 格（H1 2、H2 3、H3 3、A K Q 各 4、J T 各 5，同符號間距 ≥ 3），驗收含 symbols／paytable／捲軸一致性檢查，全部通過。勝在 Claude Code 對話框用 `! 指令` 執行（bash，路徑用 `/`，python 加 `-X utf8`）。**下次從 Day 3 第 4 步開始**：Excel 建捲軸表、COUNTIF 算 cᵢ 與每停止位置視窗個數、各獎項 3/4/5 連路數，並用 L − 3c 捷徑交叉驗算 N。

- 2026-11-11：Day 1、Day 2 由勝自行複習完成（排列組合、條件機率、期望值、變異數、離散分布、一步轉移矩陣、穩態分布、RTP），統計部分邊做邊補。環境：Windows + PowerShell，虛擬環境 `.venv`，repo DavidChung0305/slot-math-portfolio。Day 3 開始：第 1 步「捲軸帶與樣本空間、Lines 組合數、Ways 視窗計數」理論題已出（Q1 總組合數與等機率、Q2 單線剛好 3 連 A 的組合數，數值例 Lᵢ=10、cᵢ=2、Q3 Ways 視窗 A 個數總和），尚未作答。**下次從回答 Q1–Q3 開始**，接著決定 Lines 或 Ways、設計 config/game.json，再開 Excel。
