# axlabs-mckinsey-pptx（中文版）

> 简体中文 | [한국어 원문](./README.ko.md)
>
> **这是 [AX Labs](https://theaxlabs.com/) 制作的 Claude Code 插件（本仓库为 fork，增加了中文支持）。**
> 在聊天框里说一句话，就能**自动生成麦肯锡风格的高质量 PPT**。
> 比如输入"做一份 Q4 业务回顾"，它会从 40 个专业模板中挑出合适的，
> 生成包含封面、图表、矩阵、路线图的完整 `.pptx` 文件，保存到文件夹里。
> 不需要打开 PowerPoint 拖拽排版，也不需要设计功底。

![Author](https://img.shields.io/badge/author-AX%20Labs-0b1f3a)
![License](https://img.shields.io/badge/license-MIT-blue)
![Templates](https://img.shields.io/badge/templates-40-brightgreen)
![Platform](https://img.shields.io/badge/platform-Claude%20Code-6b4bff)

---

## 这是什么？（1 分钟了解）

- **用途：** 只用文字描述，就能自动生成咨询公司风格的 PPT。
- **适合谁：** 策划、市场、管理层、咨询顾问、学生——**任何厌倦了一页页手工做 PPT 的人。**
- **怎么用：** 在 Claude Code（一个聊天式 AI 工具）里**像说话一样**用中文提需求即可。
  不需要开发知识，也不用背命令。
- **产出：** 真正的 `.pptx` 文件。可以用 PowerPoint / WPS / Keynote 打开编辑、发邮件、直接演示。

**一句话示例：**
> "做一份 Q4 业务回顾 PPT。营收 1200 亿，同比增长 14%，有 2 个 KPI 延误。"

↓ 30 秒到 1 分钟后 ↓

→ 生成 `output/q4-review.pptx`。包含封面、摘要、增长图表、问题矩阵、
  路线图、结论等 6–8 页麦肯锡风格幻灯片。

---

## 首次安装准备（5 分钟）

这个工具运行在 **Claude Code** 里。可以把 Claude Code 理解为"在命令行里使用的 AI 助手"。

### 第 1 步：安装 Claude Code

如果还没有，请到 [Claude Code 官方下载页](https://claude.com/claude-code) 安装。
支持 Mac / Windows / Linux。

### 第 2 步：安装本插件

启动 Claude Code 后，在**聊天框里**输入下面两行，**一行一行地**输入：

```
/plugin marketplace add pizijian38-pixel/mckinsey-pptx
```

```
/plugin install axlabs-mckinsey-pptx@axlabs
```

> 看到 "Installed axlabs-mckinsey-pptx" 就说明安装成功。
>
> 第一行用的是本 fork（含中文字体主题）。如果想用韩国原作者的版本，
> 把它换成 `seulee26/mckinsey-pptx`。

### 第 2.5 步：⚠️ 完全退出 Claude Code 再重新打开（重要！）

**插件安装后必须重启 Claude Code 才会真正加载。**
刚装完时在 `/agents` 列表里看不到它是正常的。

1. 在聊天框输入 `/exit`（或直接关闭终端窗口）
2. 重新启动 Claude Code
3. 代理会自动加载

不重启的话，无论怎么说"帮我做 PPT"，麦肯锡代理都不会响应。**一定要重启。**

### 第 3 步：安装依赖（只需一次）

对 Claude 说下面这句话，它会自动安装需要的东西：

```
安装这个插件需要的 Python 库。
```

如果想把 PPT 渲染成图片预览（可选）：

- Mac：对 Claude 说"执行 `brew install --cask libreoffice && brew install poppler`"
- 其他系统：正常安装 LibreOffice 即可

> 💡 没有预览工具也能正常生成 `.pptx`，直接用 PowerPoint、WPS 或 Keynote 打开就行。
> 装了预览工具后，AI 会把幻灯片渲染成图片，自己检查有没有文字溢出。

### 确认安装

在 Claude Code 聊天框输入：

```
/agents
```

列表里出现 `mckinsey-slide-agent` 就说明准备好了。

---

## 使用方法：在聊天框里说话就行

### 🟢 最常用的流程（先照着做一遍）

这是实际工作中最常见的用法：有一个 Excel，就能做出一份 PPT。

**① 新建一个工作文件夹**

比如在桌面建一个 `q4-review` 文件夹，把 Excel 放进去：

```
q4-review/
└── 销售数据.xlsx
```

**② 在"这个文件夹里"打开 Claude Code**

在终端里输入：

```bash
cd ~/Desktop/q4-review
claude
```

> Windows：在文件夹空白处按住 Shift 点右键，选"在终端中打开"，再输入 `claude`。
> 关键是 **Claude 必须在这个文件夹里启动**，才能读到里面的 Excel，生成的 PPT 也会存在这里。

**③ 在聊天框里说一句话**

```
把文件夹里的 销售数据.xlsx 做成麦肯锡风格的 PPT。
```

也可以用斜杠命令，最稳定：

```
/mckinsey-deck 做一份Q4业务回顾，给高管看，营收1200亿，结论是申请追加投资
```

**④ 等 30 秒到 1 分钟**

Claude 会读取 Excel，挑选图表、摘要、结论等页面，在 `output/` 文件夹里生成
`.pptx` 文件。打开检查后就可以直接用于汇报。

---

### 更多需求示例

在 Claude Code 聊天框里**用中文描述你想要的 PPT**：

```
做一份季度业务回顾。营收 1200 亿（去年 1050 亿），
2 个 KPI 延误，正在评估 3 个新业务方向。
```

↓

Claude 会自动：

1. 按**故事结构**设计整份 PPT 的顺序（封面 → 摘要 → 图表 → 结论）
2. 从 40 个模板里为每一页挑选合适的模板
3. 说明**"为什么选这个模板"**
4. 把完成的 `.pptx` 保存到 `output/` 文件夹

### 这些说法它都能听懂

- "用麦肯锡风格做一份战略报告"
- "帮我做个业务回顾 PPT，面向管理层"
- "启动会 PPT，10 页，英文"
- "一页展示 5 年营收趋势的幻灯片"
- "用 BCG 矩阵对比 4 个业务"

### 完成后怎么查看

Claude 会告诉你文件路径，例如 `output/q4-review.pptx`。
在访达（Mac）或文件资源管理器（Windows）里找到它，双击即可用 PowerPoint / WPS / Keynote 打开。

---

## 中文字体与署名（本 fork 新增）

用中文提需求时，代理会自动使用**中文主题**：

- **字体：** 英文和数字用 Arial，中文用**微软雅黑**。
  PowerPoint 里中文字形用的是单独的"东亚字体"设置，本 fork 会把它写到每一段文字上，
  所以中文不会被替换成系统默认字体。
- **署名：** 原版页脚写的是 `Copyright of mckinsey-AX`，深蓝总结页右下角写的是
  `McKinsey & Company`。本 fork 把它们**默认改为空白**（只显示页码）。
  你在需求里提到公司名时，会显示成 `ⓒ 2026 你的公司`。
- **"资料来源"：** 页脚的来源前缀显示为"资料来源："，不再是英文 "Source:"。

在需求里这样说就行：

```
/mckinsey-deck 做一份出海战略汇报，公司名是"星海科技"，字体用苹方
```

| 想要的效果 | 怎么说 |
|---|---|
| 页脚显示公司名 | "公司名是 XX" 或 "页脚版权改成 ⓒ 2026 XX" |
| 换字体 | "字体用 苹方 / 思源黑体 / 等线"（默认微软雅黑） |
| 不要任何署名 | 什么都不说，默认就是空白 |

> 💡 Mac 上如果没装 Office 自带的微软雅黑，可以说"字体用苹方"（PingFang SC）。
> 文件发给别人时，对方电脑上没有这个字体的话，PowerPoint 会自动用相近字体替代。

---

## 实战指南：用 Excel / Word 等原始资料做 PPT

很少有工作是"一段话说完"就够的。通常手上会有 **Excel 销售数据**、
**Word 写的策划案**、**PDF 调研资料**等原始文件。按下面的方式整理好文件夹交给 Claude，
它会自动读取内容并放进 PPT。

### 文件夹整理方法（重要！）

在**你想做 PPT 的项目文件夹**里启动 Claude Code。
Claude 只能读取这个文件夹里的文件。

推荐结构：

```
我的项目文件夹/
├── inputs/                    ← 原始文件都放这里
│   ├── 销售数据.xlsx
│   ├── 策划案.docx
│   ├── 会议纪要.pdf
│   └── logo.png
└── output/                    ← 生成的 PPT 保存在这里（自动创建）
```

文件夹名用中文或英文都可以。关键是**把原始资料和成品分开**。

### 不同文件类型的用法

#### 📊 Excel / CSV 文件（营收、问卷、KPI 数据）

告诉 Claude 用**哪个工作表**的**哪些数字**：

```
用 inputs/销售数据.xlsx 里"月度销售"工作表的数据做一份 Q4 回顾 PPT。
用柱状图展示 1 到 12 月的月度营收，
再加一页 KPI 仪表盘。
```

Claude 会直接打开 Excel 读取数字并画成图表。
**它还会说明"哪个数字取自哪里"**，方便你核对。

> 💡 **提示：** 告诉它工作表名和单元格范围（比如"A1 到 F20"）会更准确。
> 如果工作表有几十个，只指出需要用的那几个。

#### 📝 Word 文档（`.docx`）

策划案、报告初稿、会议纪要等。Claude 会**读取正文并自动压缩成适合幻灯片的短要点**。

```
读一下 inputs/策划案.docx，做成给管理层看的 10 页战略报告。
结论是申请投资审批。
```

> ⚠️ 旧版 `.doc` 文件请先在 Word 里**另存为 `.docx`**。

#### 📄 PDF 文件

会议纪要、外部调研、董事会材料等。

```
总结 inputs/董事会备忘录.pdf 第 3–7 页，
做成一页给高管看的摘要幻灯片。
```

> 💡 如果 PDF 里**数字表格很多**，最好同时提供 Excel。PDF 里的表格有时读出来格式会乱。
> 有 Excel 的话 Claude 会优先使用 Excel。

#### 🗒 笔记 / Markdown（`.md`、`.txt`）

想法笔记、头脑风暴草稿——最轻松的方式。

```
看一下 notes.md，做一份项目启动会 PPT。
```

#### 🖼 Logo / 图片

想加 Logo 有两种方式：

1. **让 Claude 加：** "在封面放上 `inputs/logo.png`"
2. **自己加：** 用 PowerPoint 打开生成的 `.pptx`，把 Logo 拖进去

### 实际使用场景

#### 场景 A：月底准备季度业务回顾

```
项目文件夹/
└── inputs/
    ├── Q4财务.xlsx
    └── 风险清单.md
```

对 Claude 说：

```
用这个文件夹 inputs/ 里的资料做一份 7 页的 Q4 业务回顾。
面向管理层，结论是申请投资审批。
营收和营业利润用 Q4财务.xlsx 里"汇总"工作表的数字，
风险用重要性 × 紧急程度矩阵展示。
```

#### 场景 B：海外市场进入启动会

```
项目文件夹/
└── inputs/
    ├── 市场调研.pdf         （外部调研，15 页）
    ├── 目标客户.xlsx
    └── 路线图.md            （12 周计划）
```

对 Claude 说：

```
做一份进入印尼市场的启动会 PPT。英文，10 页。
包括 市场调研.pdf 的摘要、目标客户.xlsx 的客户画像，
以及把 路线图.md 做成甘特图。
```

#### 场景 C：只有数字，不知道该展示什么

```
项目文件夹/
└── inputs/
    └── 5年营收.csv
```

对 Claude 说：

```
只看 inputs/5年营收.csv，找出这些数字背后的故事，
做成 5 页。哪些信息重要由你来判断。
```

→ Claude 会自己找出趋势、拐点和异常值，并组织成一个故事。

### 不满意？直接改

第一次生成的是**初稿**。在同一个对话里继续说：

```
把第 4 页换个版式，让数字对比更明显。
```

```
把第 2 页的第三条要点改成"NPS 42 分（高于行业平均 15 分）"。
```

```
整体语气更正式一些，去掉所有表情符号和感叹号。
```

```
再做一份英文版，结构和数字保持一样。
```

像聊天一样不断打磨即可。

---

## 常见问题

**Q. 我从来没写过 Python、没写过代码，可以用吗？**
A. 可以，**完全不需要编程**。装好 Claude Code 后，全程用中文对话就行。

**Q. 数据是机密的，安全吗？**
A. 文件**只在你自己的电脑上**处理，Excel、Word 不会上传到云端。
   （不过和 Claude 的对话内容需要发送到 Anthropic 服务器才能得到 AI 回复，
   请按公司的安全规定自行判断。）

**Q. 不喜欢某页的版式。**
A. 说一句"这页换个版式"，它会从 40 个模板里换一个重新画。
   如果给出具体提示，比如"换成突出大数字的那种"，会更快得到好结果。

**Q. 想换成公司自己的品牌颜色和 Logo。**
A. 默认主题是麦肯锡风格（深海军蓝）。页脚公司名可以直接在需求里说（见上面"中文字体与署名"）。
   原作者 AX Labs 通过企业合作提供定制品牌模板，详见下方**企业咨询**。

**Q. 可以指定页数吗？**
A. 可以。说"做 7 页"或"10 页左右"即可。不指定的话，会根据内容一般做 5–10 页。

**Q. 能做英文 PPT 吗？**
A. 可以。用中文提需求时加一句"做英文版"就会生成英文 PPT；用英文提需求则直接生成英文版。

**Q. 生成的 PPT 能编辑吗？**
A. 能，就是**普通的 PowerPoint 文件**。用 PowerPoint / WPS / Keynote 打开随便改、直接演示。

---

## 能做哪些幻灯片？（40 个模板）

Claude 会自动挑选，你也可以直接指定。

### 🎯 摘要 / 结论类
- **一句话核心结论**（深海军蓝全屏）
- **管理层摘要**（加粗结论 + 要点）
- **段落式摘要**（标题 + 2–4 段文字）

### 📊 图表 / 数据可视化
- **时间序列增长图**（带增长箭头）
- **历史 + 预测图**（历史深色，预测浅色）
- **对比柱状图**（突出重点项）
- **气泡图**、**堆积柱状图**、**分组对比图**、**折线图**
- **KPI 仪表盘**（4–8 个指标卡，同比 ▲▼）

### 🧩 矩阵 / 分析框架
- **BCG 增长-份额矩阵**（2×2 象限）
- **优先级矩阵**（3×3，紧急程度 × 重要性）
- **对比表**（选项 × 标准，哈维球评分）
- **优劣势分析**（✓ 绿色 / ✗ 红色）
- **Before/After 对比**

### 🏢 组织 / 团队结构
- **组织架构图**（CEO → 负责人 → 成员）
- **团队圆形图**（负责人 + 成员）
- **职能团队矩阵**
- **议题树**（问题 → 原因 → 根本原因）

### 🗓 路线图 / 流程
- **三阶段箭头**
- **四阶段详细表**
- **四波次时间线**
- **甘特图**（按周 + 里程碑）
- **流程图**（4–6 个步骤）
- **漏斗**（TAM/SAM/SOM 等）

### 📋 结构类页面
- **封面**
- **章节分隔页**
- **目录**
- **大数字强调**
- **引言页**

### 🎨 其他
- **三大趋势**（图标 / 表格 / 编号 三种样式）
- **五大关键领域**
- **领域概览卡片**（5–7 个）
- **状态评估表**（红绿灯颜色）

> 完整详细清单见 [`mckinsey_pptx/agent/CATALOG.md`](mckinsey_pptx/agent/CATALOG.md)（英文）。
> 平时只要告诉 Claude **目的**，比如"业务对比页"，它会自己选。

---

## 插件由哪些部分组成？

安装后会有下面的文件夹结构。不懂开发的话，**知道"里面有这些东西"**就够了。
它们都是**必需组件**，请不要删除。

```
axlabs-mckinsey-pptx/
├── .claude-plugin/            ← 插件"名片"（Claude Code 读取的信息）
├── agents/                    ← ★ AI 助手的"大脑"（有它才能听懂你的话）
│   └── mckinsey-slide-agent.md
├── commands/                  ← 斜杠命令定义（比如 /mckinsey-deck）
│   └── mckinsey-deck.md
├── mckinsey_pptx/             ← 真正画 PPT 的引擎（40 个模板）
├── examples/                  ← 示例 PPT
└── requirements.txt           ← 自动安装用的依赖清单
```

**三个核心部分：**

- **`agents/` 文件夹**：里面是"麦肯锡幻灯片代理"这个 AI 助手的设定，包括它的知识和工作方式。
  Claude Code 读取这个文件后，才知道**"这个 AI 擅长什么、应该怎么干活"**。
  没有它的话，你说"帮我做 PPT"，回答你的只是普通 AI，专业代理不会启动。
- **`commands/` 文件夹**：定义 `/mckinsey-deck` 这类**斜杠命令**。
  在聊天框按 `/` 时弹出的命令补全就来自这里。
- **`mckinsey_pptx/` 文件夹**：真正生成 `.pptx` 文件的**绘图引擎**。
  40 种幻灯片模板（图表、矩阵、路线图等）的设计、配色、版式代码都在这里。
  代理做 PPT 时会在后台调用这个引擎。

三个文件夹**必须一起工作**插件才能运行。缺了任何一个，
就会变成"有代理但画不出来"或者"能画但没法通过对话调用"。

---

## 企业咨询（原作者 AX Labs）

以下服务由原作者 AX Labs 提供（与本 fork 无关）：

- **企业专属品牌模板**：按贵公司 Logo、配色、字体定制的 40 个专用模板
- **行业专属 AI 代理**：学习贵公司内部框架、方法手册和数据源
- **端到端 AX 落地**：从诊断到全职能部署
- **本地部署 / VPC 部署**：机密数据完全不出内网
- **团队培训与内化**：面向咨询、策划团队的工作坊

**AX = AI eXperience / AI Transformation。** 从把需要几天的咨询 PPT 缩短到几分钟出初稿开始，
把策划、调研、分析的整个工作流改造成 AI 原生方式。

→ 联系方式：**help@theuxlabs.com**
→ 网站：[theaxlabs.com](https://theaxlabs.com/)
→ 邮件标题格式：`[AX 문의] <公司名>`

---

## 贡献与反馈

- **原项目**：[seulee26/mckinsey-pptx](https://github.com/seulee26/mckinsey-pptx)，欢迎提交 Issue 和 Pull Request
- **企业咨询**：help@theuxlabs.com

---

## 许可证

[MIT](./LICENSE) © 2026 AX Labs — 이승필（Seungpil Lee）

开源插件采用 MIT 许可证。定制扩展、私有模板、企业部署另有商业条款，
请联系 AX Labs。

---

<details>
<summary>🛠 开发者参考（Python API、CLI、项目结构）</summary>

### 直接调用 Python API

```python
from mckinsey_pptx import PresentationBuilder, make_zh_theme

b = PresentationBuilder(theme=make_zh_theme("某某公司"),
                        default_section_marker="Q4 回顾")
b.add("dark_navy_summary", body="[核心结论]: 未来五年将决定全球领导地位。")
b.add("executive_summary_takeaways",
      sections=[{"takeaway": "市场同比增长 22%",
                 "bullets": ["北美份额上升", "欧洲增长停滞"]}])
b.add("column_historic_forecast",
      categories=[2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
      values=[1035, 1108, 1153, 1148, 1206, 1265, 1381, 1430, 1535],
      forecast_from_index=5, historic_growth="3%", forecast_growth="6%",
      description="营收趋势", takeaway_header="关键结论", source="公司财报")
b.save("output/deck.pptx")
```

### 中文主题参数

```python
from mckinsey_pptx import make_zh_theme

make_zh_theme()                                   # 微软雅黑，无署名
make_zh_theme("某某公司")                          # 页脚 "ⓒ 2026 某某公司"
make_zh_theme("某某公司", font="PingFang SC")      # 苹方
make_zh_theme("某某公司", font="Source Han Sans SC", year=2027)
```

`Theme` 上与署名相关的字段：

| 字段 | 作用 | 默认值 |
|---|---|---|
| `copyright_text` | 内容页右下角页脚 | `""`（只显示页码） |
| `brand_text` | 深蓝总结页右下角标记 | `""` |
| `source_label` | 页脚 `source=` 的前缀 | `"Source: "`（中文主题为 `"资料来源："`） |
| `typography.east_asian_family` | 中日韩字形使用的字体 | `None`（中文主题为 `"Microsoft YaHei"`） |

### 自适应 API（`add_specs`）

根据 dict 的字段自动推断模板：

```python
b.add_specs([
    {"body": "[核心结论]: ..."},                                  # dark_navy_summary
    {"sections": [...]},                                          # executive_summary_takeaways
    {"categories": [...], "values": [...], "forecast_from_index": 5},
                                                                  # column_historic_forecast
])
```

### CLI

```bash
python -m mckinsey_pptx.cli --list-types
python -m mckinsey_pptx.cli --demo -o output/demo.pptx
python -m mckinsey_pptx.cli specs.json -o deck.pptx --section-marker "Strategy review"
```

### 运行示例

```bash
python -m examples.demo           # 英文，覆盖所有模板
python -m examples.demo_chinese   # 中文，8 页
python -m examples.demo_korean    # 韩文，21 页
```

### 自定义主题

```python
from dataclasses import replace
from mckinsey_pptx import DEFAULT_THEME, PresentationBuilder

MY_THEME = replace(
    DEFAULT_THEME,
    typography=replace(DEFAULT_THEME.typography, east_asian_family="DengXian"),
    copyright_text="ⓒ 2026 某某公司",
    brand_text="某某公司",
)
b = PresentationBuilder(theme=MY_THEME)
```

### 完整项目结构

```
axlabs-mckinsey-pptx/
├── .claude-plugin/
│   ├── marketplace.json                   # 插件市场条目
│   └── plugin.json                        # 插件清单
├── agents/
│   └── mckinsey-slide-agent.md            # 子代理定义
├── commands/
│   └── mckinsey-deck.md                   # /mckinsey-deck 斜杠命令
├── mckinsey_pptx/                         # Python 引擎
│   ├── __init__.py
│   ├── theme.py                           # 配色、字体、版式参数，中文主题
│   ├── base.py                            # 通用图形/文字工具 + 页眉页脚
│   ├── builder.py                         # PresentationBuilder + add_specs 推断
│   ├── cli.py                             # 命令行接口
│   ├── agent/
│   │   └── CATALOG.md                     # 子代理使用的模板手册
│   └── slides/                            # 40 个模板（按类别分文件）
├── examples/
│   ├── demo.py                            # 英文示例
│   ├── demo_chinese.py                    # 中文示例
│   └── demo_korean.py                     # 韩文示例
├── LICENSE                                # MIT © 2026 AX Labs
├── README.md                              # 中文说明（本文件）
├── README.ko.md                           # 韩文原版说明
└── requirements.txt                       # python-pptx 等依赖
```

</details>
