# AP Microeconomics Lecture Quality Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修复 AP 微观经济学讲义中可验证的知识和题目答案问题，补充开源 README，并保持现有构建框架和图表脚本不变。

**Architecture:** 继续以 `AP微观经济学讲义.md` 和 `补充练习题.md` 作为唯一教学源文件；只对文本、题干和答案做局部修订。`build.py`、Pandoc、现有图表资产和样式继续按原路径工作，README 只描述现有能力，不引入新构建系统。

**Tech Stack:** UTF-8 Markdown, Python 3, Pandoc, Chrome/Edge headless PDF export, existing PNG/SVG charts, Git.

## Global Constraints

- 不重构 `Markdown → Pandoc HTML → 浏览器 PDF` 构建流程。
- 不修改 `build.py`、`generate_charts.py`、`generate_svg_charts.py` 或 `generate_ppt.py` 的源代码。
- 保持主讲义六个 Unit、现有题目编号和图表文件名不变。
- 不删除现有文件；`.gitignore` 只改变 Git 纳入范围。
- 2026 年考试信息以 College Board 官方考试页和成绩分布页为准。
- 完成所有验证后，按用户指定的 7897 网络端口推送到 `origin/main`。

---

### Task 1: 修订考试信息与 Unit 1–3 的条件性表述

**Files:**
- Modify: `AP微观经济学讲义.md:15-53, 216-405, 445-475, 1530-1740`

**Interfaces:**
- Consumes: College Board 2026 exam and score-distribution pages；现有 Unit 1–3 文字与数值表。
- Produces: 事实准确、条件清楚且不改变章节结构的 Unit 1–3 文本。

- [ ] **Step 1: 更新考试概览**

  将考试日期 `待定` 改为 `2026年5月4日（当地时间中午12:00）`；保留 19/26/23/20/12 分布；删除“2026 年考试人数约 12.7 万人”，并把来源说明改为“College Board 官方成绩分布页面”。

- [ ] **Step 2: 修正 Unit 1 消费束叙述**

  将“满足 `10X + 20Y = 60` 的整数组合”前的说明改为：严格可行集为 `10X + 20Y ≤ 60`；当前表列出恰好用完预算的组合，因为给定边际效用为正且这些组合涵盖本例最优束。保留现有 `2 杯奶茶 + 2 块蛋糕` 答案，并明确全局判断应比较可行束的 TU，而不是只看最后一单位 `MU/P`。

- [ ] **Step 3: 修正 Unit 3 的长期和利润最大化措辞**

  将“长期中所有要素都可以调整，所以长期不存在边际报酬递减的说法”改为：“本讲义把边际报酬递减作为短期中固定要素不变、增加可变要素的分析；长期通常改用规模报酬分析，但这不是说生产关系不可能出现边际产量下降。”

  将“适用于所有市场结构：生产满足 `MR = MC`”改为带条件的表述：在可行内点且 MC 曲线从下向上穿过 MR 的标准利润最大化解中，选择 `MR = MC`；离散题应比较相邻单位，边界解不要求等式。完全竞争下再说明 `MR=P`。

- [ ] **Step 4: Run targeted checks**

  Run: `python -c "from pathlib import Path; p=next(Path('.').glob('AP*.md')); t=p.read_text(encoding='utf-8'); assert '2026年5月4日' in t and '12.7 万人' not in t; assert '长期中所有要素都可以调整，所以长期不存在' not in t"`

- [ ] **Step 5: Commit**

  ```powershell
  git add -- AP微观经济学讲义.md
  git commit -m "fix: clarify exam facts and unit one to three economics"
  ```

### Task 2: 修订 Unit 2、4、5、6 的模型边界和绝对化结论

**Files:**
- Modify: `AP微观经济学讲义.md:1190-1360, 2240-2395, 2545-2735, 2885-3165`

**Interfaces:**
- Consumes: 现有供需、贸易、市场结构、要素市场和市场失灵段落。
- Produces: 竞争市场/小国/有效配给/线性图示等假设清楚的正文与总结表。

- [ ] **Step 1: 限定 Unit 2 福利结论**

  在补贴段落说明“在竞争市场且不存在未计入的外部收益/成本时，补贴若使数量偏离有效率水平会产生 DWL；纠正正外部性时则可能提高总剩余”。

  在关税/配额表中把“若租金归国内，DWL 较小；若归外国，DWL 较大”改为：“相同进口量下，全球配置性 DWL 由生产和消费扭曲决定；若配额租金归外国，进口国国民福利还会额外损失租金外流。”

- [ ] **Step 2: 修订 Unit 4 市场结构表和识别流程**

  把“常见例示为 2–10 家”和决策树中的“少数几个（2–10）”改为“少数相互依赖的主要厂商，数量没有固定阈值”。

  将市场结构表中的寡头 `P > MC`、`DWL > 0` 改为“依博弈/竞争方式而定”；将垄断的对应结论改为“标准单一价格垄断模型通常有 `P > MC` 和 DWL，完全价格歧视是例外”。把“垄断既没有生产效率”改为“标准单一价格垄断通常不在 min ATC 处生产”。

- [ ] **Step 3: 修订 Unit 5 条件性表述**

  保留一般条件 `MRP = MFC`，并在“MRP 曲线就是劳动需求曲线”处补充“在其他投入、技术和产品市场条件给定时；完全竞争产品市场下 `MRP=VMP=MP×P`”。

- [ ] **Step 4: 修订 Unit 6 自然垄断和外部性表述**

  将负/正外部性中的“价格偏低”改为“相对于社会边际成本/收益的有效率基准，市场数量偏离社会最优”；将 DWL 结论限定为标准竞争模型和图示条件。

  在自然垄断的政府干预表中，把未管制厂商“经济利润 > 0”改为“可能为正、零或负，取决于需求与成本；标准图示下若 `P>ATC` 才为正利润”，并保留 `P=MC` 可能需要补贴的结论。

- [ ] **Step 5: Run targeted checks**

  Run: `Select-String -Encoding utf8 -Path 'AP微观经济学讲义.md' -Pattern '2–10|2-10|经济利润 > 0.*DWL 最大|长期不存在边际报酬'`

  Expected: only no longer applicable historical text is absent; remaining matches must be reviewed before commit.

- [ ] **Step 6: Commit**

  ```powershell
  git add -- AP微观经济学讲义.md
  git commit -m "fix: qualify market model conclusions"
  ```

### Task 3: 修复练习题—答案数据闭合和对应关系

**Files:**
- Modify: `AP微观经济学讲义.md:2560-2885, 3840-3970`
- Modify: `补充练习题.md:338-470`

**Interfaces:**
- Consumes: 主讲义 Unit 5 FRQ、主讲义答案区、补充题库 Unit 5。
- Produces: 题干数据足以推出答案，且主讲义 60 MCQ/7 FRQ 与补充题 30 MCQ/2 FRQ 均有对应答案。

- [ ] **Step 1: 补全主讲义 Unit 5 FRQ 数据**

  在 `Marginal Product of Labor` 表的第 5 名工人之后加入：

  ```markdown
  | 6                 | 10                        |
  ```

  这样第 6 名工人的 `MRP=10×$10=$100<$120`，答案“雇佣 5 名”由题干直接支持。

- [ ] **Step 2: 限定主讲义 Unit 5 MCQ 6**

  将 `A profit-maximizing firm will hire labor up to the point where` 改为 `A profit-maximizing firm in a perfectly competitive labor market will hire labor up to the point where`，使答案 `w=MRP` 与此前的一般条件 `MRP=MFC` 不矛盾。

- [ ] **Step 3: 同步限定补充题库 Unit 5 MCQ 1**

  将同一题干改为 `A profit-maximizing firm in a perfectly competitive labor market will hire labor up to the point where`，保留答案 `w=MRP`。

- [ ] **Step 4: Run correspondence validator**

  读取两个 Markdown 文件，验证：主讲义每个 Unit 的 MCQ 编号为 1–10、答案键同样为 1–10；主讲义 7 道 FRQ 的小问数量依次为 5、4、5、5、5、4、5；补充题每 Unit 的 MCQ 编号为 1–5、答案表为 1–5，且两个补充 FRQ 的小问分别为 (a)–(d) 和 (a)–(e)。

- [ ] **Step 5: Commit**

  ```powershell
  git add -- AP微观经济学讲义.md 补充练习题.md
  git commit -m "fix: close exercise data and answer mappings"
  ```

### Task 4: 添加开源 README 和仓库忽略规则

**Files:**
- Create: `README.md`
- Create: `.gitignore`

**Interfaces:**
- Consumes: `AGENTS.md`、`build.py`、现有目录结构、官方 AP 链接。
- Produces: 不夸大覆盖范围、可供 GitHub 读者快速理解和构建的中文 README，以及不纳入本地依赖/内部材料的忽略规则。

- [ ] **Step 1: Write README**

  README 必须包含项目定位、适用读者、六单元目录、图表资产、构建命令、输出说明、文件结构、审查边界、官方考试资料链接和贡献建议；明确讲义是学习辅助材料，不声称为 College Board 官方出版物。

- [ ] **Step 2: Write `.gitignore`**

  至少包含：`node_modules/`、`__pycache__/`、`*.py[cod]`、`_temp_*`、`overflow_results*.json`、`test_output.html`、`micro_review*.md`、`对话上下文总结.md`、`ap*-frq-set*.pdf`，并保留源 Markdown、脚本、图表和样式文件可被 Git 跟踪。

- [ ] **Step 3: Run README/config checks**

  Run: `Test-Path README.md; Test-Path .gitignore; Select-String -Encoding utf8 -Path README.md -Pattern 'AP Microeconomics|python build.py|charts|College Board'`

- [ ] **Step 4: Commit**

  ```powershell
  git add -- README.md .gitignore
  git commit -m "docs: add open source project README"
  ```

### Task 5: 完成语法、结构、构建和 Git 范围验证

**Files:**
- Verify: `*.py`, `AP微观经济学讲义.md`, `补充练习题.md`, `charts/`, generated HTML/PDF, Git status

**Interfaces:**
- Consumes: Tasks 1–4 的已提交结果。
- Produces: 可复核的构建输出、题目答案对应证据，以及“图片脚本无源代码 diff”的 Git 证据。

- [ ] **Step 1: Run Python syntax validation**

  使用 `ast.parse` 读取当前目录所有 `.py` 文件，预期 4 个脚本全部 PASS。

- [ ] **Step 2: Run exercise mapping validation**

  重新运行结构化检查，输出主讲义 6×10 MCQ、7 FRQ 和补充题 30 MCQ、2 FRQ 的计数、答案键计数及连续编号。

- [ ] **Step 3: Run build**

  Run: `python build.py`

  Expected: charts step exits 0, Pandoc exits 0, HTML is regenerated, and Chrome/Edge either writes a non-empty PDF or gives the documented manual-export message; no `_temp_lecture.md`, `_temp_lecture.html`, or `_temp_output.pdf` remains.

- [ ] **Step 4: Inspect output metadata**

  Confirm the generated HTML and PDF exist and are non-empty; confirm all 40 Markdown chart/image references resolve to files under `charts/`.

- [ ] **Step 5: Check Git scope**

  Run: `git status --short --branch; git diff --name-only HEAD~3..HEAD`

  Confirm no `generate_*.py`, `build.py`, or chart source file appears in the final source diff, and ignored local files are not staged.

- [ ] **Step 6: Commit verification record if needed**

  If the build only changes generated deliverables, review the diff and commit them with `build: regenerate lecture outputs`; otherwise leave generated output changes unstaged and report the exact state.
