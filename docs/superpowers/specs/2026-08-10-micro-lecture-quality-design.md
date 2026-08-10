# AP 微观经济学讲义质量修订设计

## 目标

在不改变现有 `Markdown → Pandoc HTML → 浏览器 PDF` 构建框架、图表组织方式或图片 Python 脚本的前提下，修复讲义中可验证的知识性错误和题目—答案不一致，补充适合开源仓库的 README，并完成本地 Git 初始化。

## 当前项目边界

- 核心源文件：`AP微观经济学讲义.md`。
- 补充题库：`补充练习题.md`。
- 图表资产：`charts/` 中现有 39 个 PNG/SVG 文件。
- 构建链：`build.py` 调用 `generate_charts.py`，再通过 Pandoc 生成 HTML，并尝试用 Chrome/Edge 导出 PDF。
- 样式：`style.css` 和 `github-style/`。
- 图片脚本只做 Python 语法检查，不修改其源代码。

## 方案比较

### 方案 A：定点修订（采用）

只修改会影响知识准确性、题目可解性、答案一致性和开源使用说明的内容。优点是风险小、与现有讲义结构兼容、容易逐项验证；缺点是不会重做学习路径或大规模增加练习。

### 方案 B：教学结构重构

增加每个 Topic 的学习目标、诊断题、CED 映射、分层练习和完整 FRQ rubric。教学收益更大，但会显著改变文档规模和排版，超出本次“保持基本雏形和框架”的范围。

### 方案 C：只发布审查报告

保留原讲义，仅新增问题清单。这不会修复学生实际会遇到的错误，因此不能满足本次任务。

## 采用方案的内容修订

### 考试概览

- 按 College Board 当前官方页面更新 2026 年考试日期为 5 月 4 日（当地时间中午 12:00）。
- 保留官方公布的 2026 年 5/4/3/2/1 分数比例 19%/26%/23%/20%/12%，并保留来源链接。
- 删除官方成绩表没有提供依据的“约 12.7 万人”说法。

### 主讲义知识表述

- Unit 1：保留已正确的比较优势公式；补强离散消费束说明，明确严格可行集是支出不超过预算；将长期边际报酬表述限定为短期分析，避免说成长期完全不存在该概念。
- Unit 2：为补贴产生无谓损失、CS/PS 三角形和关税/配额福利比较补充竞争市场、小国、线性或有效配给等必要条件；明确全球 DWL 与进口国配额租金外流的区别。
- Unit 3：将利润最大化规则表述为在适当的 MC 上升穿越条件下使用 `MR = MC`；避免把短期边际报酬递减和长期规模报酬混为绝对互斥概念。
- Unit 4：删除“寡头 2–10 家”作为识别阈值；将寡头的 `P>MC`、DWL 和长期利润改成依模型而定的条件性表述；为垄断生产效率结论保留标准模型限定。
- Unit 5：在 FRQ 表中补充第 6 名工人的 MP=10，使答案“雇佣 5 名”可由题干推出；将没有明确竞争性劳动市场条件的 MRP 题干补充为完全竞争劳动市场。
- Unit 6：将自然垄断未管制利润从绝对结论改为取决于需求和成本；为外部性中的“价格偏低”和 DWL 结论补充模型限定。

### 练习题与答案

- 主讲义的 6 个单元保持现有 60 道 MCQ 和 7 道 FRQ，不改题目编号体系。
- 逐单元检查 MCQ 数量、答案键数量和题目编号连续性。
- 检查 FRQ 每个小问是否都有对应答案；修复题干缺数据导致的唯一答案无法推出问题。
- 在补充题库中修正同样缺少“完全竞争劳动市场”限定的 MRP 题干，并验证 30 道 MCQ 与 2 道 FRQ 的对应关系。

## 新增仓库文件

### `README.md`

中文为主、保留 AP 英文术语，包含：项目定位、适用读者、六单元内容、图表特色、构建命令、输出文件、文件结构、审查范围、官方考试资料链接和贡献说明。README 不擅自指定许可证。

### `.gitignore`

忽略 `node_modules/`、Python 缓存、构建临时文件、溢出检查结果、内部审查/对话记录和本地下载的 College Board 原题 PDF；不删除这些现有文件。讲义源文件、图表、脚本、样式和 README 属于可发布内容。

## Git 操作

- 在当前目录初始化 `main` 分支。
- 将 `origin` 设为 `https://github.com/yance7/micro.git`；本次不执行 push。
- 提交设计文档和最终源文件变更，提交内容只纳入源文件、脚本、图表、样式、README、AGENTS.md 和补充题库，不纳入本地依赖、内部审查记录或官方原题 PDF。

## 验证策略

1. 用 `ast.parse` 对全部 Python 脚本做语法检查。
2. 用结构化脚本核对主讲义 6×10 MCQ、答案键、7 道 FRQ 及其小问；同样核对补充题库 30 道 MCQ、2 道 FRQ。
3. 用公式和穷举复核比较优势、弹性、成本、MRP、外部性等数值答案。
4. 运行 `python build.py`，确认图表生成、Pandoc HTML 生成和 PDF 导出路径均可执行，并确认没有残留临时文件。
5. 检查 Git 状态和提交内容，确认图片 Python 脚本没有源代码 diff。

## 权威资料

- [College Board AP Microeconomics Exam](https://apcentral.collegeboard.org/courses/ap-microeconomics/exam)
- [College Board AP Microeconomics assessment](https://apstudents.collegeboard.org/courses/ap-microeconomics/assessment)
- [College Board AP Microeconomics score distributions](https://apstudents.collegeboard.org/about-ap-scores/score-distributions/ap-microeconomics)
