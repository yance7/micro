# AP Microeconomics 中文讲义

一套面向 AP Microeconomics 学习者的中文开源讲义。内容按课程路径拆成独立章节，保留关键英文术语、模型推导、39 张经济学图表、60 道单元选择题、配套 FRQ 与逐题解析。

> 本项目是非官方学习材料，与 College Board 无隶属或背书关系。考试日期、形式和政策请以官方页面为准。

## 开始阅读

| 章节 | 主题 | 主要内容 |
| --- | --- | --- |
| 00 | [课程与考试概览](lecture/00-课程介绍.md) | 考试结构、计分与学习导航 |
| 01 | [基本经济概念](lecture/01-基本经济概念.md) | 稀缺性、机会成本、PPC、比较优势、消费者选择 |
| 02 | [供给与需求](lecture/02-供给与需求.md) | 市场均衡、弹性、政府干预、福利与国际贸易 |
| 03 | [生产、成本与完全竞争](lecture/03-生产成本与完全竞争.md) | 生产函数、成本曲线、短期决策与长期均衡 |
| 04 | [不完全竞争](lecture/04-不完全竞争.md) | 垄断、价格歧视、垄断竞争、寡头与博弈论 |
| 05 | [要素市场](lecture/05-要素市场.md) | MRP、竞争性劳动市场、买方垄断与最低工资 |
| 06 | [市场失灵与政府作用](lecture/06-市场失灵与政府作用.md) | 外部性、公共品、公共资源与收入分配 |
| 07 | [练习题答案与解析](lecture/07-练习题答案.md) | 六个单元全部 MCQ 与 FRQ 的对应答案 |

推荐从 00 章顺序学习；复习时可直接进入对应单元，并在完成单元末练习后打开答案章核对。题目与答案使用相同的单元和题号组织。

## 讲义特色

- 中文解释配合标准英文术语，适合入门和考前复习。
- 从定义、数值例子到图形结论逐步推导，明确模型成立的前提。
- 每个知识单元后直接附练习，不需要在多个题库文件之间跳转。
- 图表脚本与 Markdown 源文件均可维护；HTML/PDF 仅作为本地构建产物，不纳入仓库。

## 本地构建

需要 Python 3、Pandoc、`numpy`、`matplotlib`，以及可选的 Chrome/Edge（用于自动导出 PDF）。

```powershell
python build.py
```

构建脚本按上表顺序拼接八个模块，重新生成图表并输出本地 `AP微观经济学讲义.html`；检测到 Chromium 浏览器时还会生成本地 PDF。发布前可运行结构与题目映射检查：

```powershell
python verify_repository.py
```

## 项目结构

```text
micro/
├── lecture/                    # 八个可独立阅读的讲义模块
├── charts/                     # 讲义引用的 PNG 图表
├── github-style/               # GitHub 风格的 HTML/打印样式
├── build.py                    # 分章 Markdown → HTML → 本地 PDF
├── verify_repository.py        # 章节、题目、答案和资源完整性检查
├── generate_charts.py          # PNG 图表生成脚本
├── generate_svg_charts.py      # SVG 图表生成脚本
└── style.css                   # 补充样式
```

## 内容可靠性与贡献

本版已对六个单元的概念、公式、数值例题、60 道 MCQ、FRQ 小问及答案映射进行交叉检查。经济模型高度依赖假设；如发现问题，欢迎提交具体章节、题号、推导或权威来源。涉及内容修改时，请同时检查题干与答案；涉及图表时，请重新运行构建并确认标签与模型一致。

官方参考：[AP Microeconomics Course](https://apcentral.collegeboard.org/courses/ap-microeconomics)、[Exam Assessment](https://apstudents.collegeboard.org/courses/ap-microeconomics/assessment)、[Score Distributions](https://apstudents.collegeboard.org/about-ap-scores/score-distributions/ap-microeconomics)。
