# AP Microeconomics Lecture Notes

一份面向国际课程高中生的 AP 微观经济学中文讲义：用清晰的模型、逐步推导和配套图表，把六个单元串成一条可复习、可打印、可继续维护的学习路径。

> 本项目是学习辅助材料，不是 College Board 官方出版物，也不代表 College Board 的立场。

## 这份讲义适合谁？

- 正在学习 AP Microeconomics、需要中文解释和英文术语对照的学生
- 希望从零建立“稀缺性 → 供需 → 成本 → 市场结构 → 要素市场 → 市场失灵”知识链的学习者
- 需要通过图形、公式和练习题反复训练 AP FRQ/MCQ 基础技能的课堂或自学者

## 内容结构

| 单元 | 主题 | 核心内容 |
| --- | --- | --- |
| Unit 1 | Basic Economic Concepts | 稀缺性、机会成本、PPC、比较优势、边际分析、消费者选择 |
| Unit 2 | Supply and Demand | 供需、均衡、弹性、政府干预、福利、国际贸易 |
| Unit 3 | Production, Cost & Perfect Competition | 生产函数、成本曲线、完全竞争、短期与长期决策 |
| Unit 4 | Imperfect Competition | 垄断、价格歧视、自然垄断、垄断竞争、寡头与博弈论 |
| Unit 5 | Factor Markets | 派生需求、MRP、劳动市场、买方垄断、最低工资 |
| Unit 6 | Market Failure & Role of Government | 外部性、公共品、公共资源、收入分配与政府政策 |

每个单元都配有图形化讲解和练习；主讲义末尾集中提供答案与解析。另有一份[补充练习题](./补充练习题.md)，包含 30 道 MCQ 和 2 道 FRQ。

## 图表与输出

`charts/` 中包含 39 张现有 PNG 图表，覆盖 PPC、供需、税收、关税、成本曲线、市场结构、要素市场和外部性等 AP 常见模型；`generate_svg_charts.py` 可另行生成 SVG 版本。讲义源文件通过 Markdown、Pandoc 和 GitHub 风格样式生成：

```text
AP微观经济学讲义.md
        │
        ├── generate_charts.py ──> charts/*.png
        ├── github-style/ + style.css
        └── build.py ──> AP微观经济学讲义.html ──> AP微观经济学讲义.pdf
```

## 快速开始

### 环境要求

- Python 3
- Pandoc
- Chrome 或 Edge（可选，用于自动导出 PDF）
- Python 依赖：`numpy`、`matplotlib`；运行 `generate_ppt.py` 时还需要 `python-pptx`

### 构建讲义

在仓库根目录运行：

```powershell
python build.py
```

也可以单独运行：

```powershell
python generate_charts.py       # 生成 PNG 图表
python generate_svg_charts.py   # 生成 SVG 图表
```

构建完成后，HTML 和 PDF 输出会出现在仓库根目录；这两个派生文件默认不纳入 Git，避免提交与源文件不同步的构建产物。若本机没有 Chrome/Edge，脚本仍会生成 HTML，并提示手动打印 PDF。

## 文件导航

```text
micro/
├── AP微观经济学讲义.md       # 讲义唯一主源文件
├── 补充练习题.md              # 补充题库及答案
├── charts/                    # 图表资产
├── build.py                   # Markdown → HTML → PDF
├── generate_charts.py         # PNG 图表生成脚本
├── generate_svg_charts.py     # SVG 图表生成脚本
├── github-style/              # GitHub 风格 HTML 样式
├── style.css                  # 项目样式补充
└── AGENTS.md                  # 项目维护与构建约定
```

## 内容审查范围

本项目维护时应同时检查：

1. 概念、公式、图形和模型假设是否一致；
2. 每道练习题的题干数据是否足以推出答案；
3. MCQ 答案键、FRQ 小问和答案解析是否一一对应；
4. 生成的 HTML/PDF 是否保留中文、数学公式、图表和分页布局；
5. 时效性考试信息是否仍与 College Board 官方页面一致。

## 官方资料

- [AP Microeconomics Exam — AP Central](https://apcentral.collegeboard.org/courses/ap-microeconomics/exam)
- [AP Microeconomics Assessment — AP Students](https://apstudents.collegeboard.org/courses/ap-microeconomics/assessment)
- [AP Microeconomics Score Distributions](https://apstudents.collegeboard.org/about-ap-scores/score-distributions/ap-microeconomics)

## 贡献建议

欢迎提交针对具体行号、公式、图形或题目答案的改进建议。涉及知识内容的修改，请同时说明适用条件和可核验来源；涉及图表的修改，请附上重新生成后的图表或构建结果。提交前请运行 `python build.py`，并确认没有把本地依赖、临时文件或官方原题 PDF 纳入提交。
