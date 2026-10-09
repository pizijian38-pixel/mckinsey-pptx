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

> 🪐 **使用 Google Antigravity？** 本仓库同时也是一个 Antigravity Skill，
> 安装方法见 [在 Google Antigravity 中使用](#在-google-antigravity-中使用)。

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

## 在 Google Antigravity 中使用

本仓库根目录有一个 `SKILL.md`，所以**整个仓库文件夹就是一个 Antigravity Skill**。
把它放进 Antigravity 的 skills 文件夹就能用，用法和 Claude Code 版一样：用中文说出需求即可。

### 安装（二选一）

**方式 1：全局安装（所有项目都能用，推荐）**

Mac / Linux（终端）：

```bash
git clone https://github.com/pizijian38-pixel/mckinsey-pptx.git ~/.gemini/antigravity/skills/mckinsey-pptx
```

Windows（PowerShell）：

```powershell
git clone https://github.com/pizijian38-pixel/mckinsey-pptx.git "$env:USERPROFILE\.gemini\antigravity\skills\mckinsey-pptx"
```

**方式 2：只给当前项目用**

在项目根目录执行：

```bash
git clone https://github.com/pizijian38-pixel/mckinsey-pptx.git .agent/skills/mckinsey-pptx
```

> 💡 没装 git？在 GitHub 页面点 **Code → Download ZIP**，解压后把文件夹改名为
> `mckinsey-pptx`，放到上面任意一个路径下即可。确认 `SKILL.md` 在
> `mckinsey-pptx/SKILL.md` 这一层，不要多套一层文件夹。

装好后重新打开 Antigravity（或新开一个对话），让它加载新的 skill。

### 安装依赖（只需一次）

在 Antigravity 对话里说：

```
安装 mckinsey-pptx skill 需要的 Python 库
```

它会执行 `pip install python-pptx`。想让 AI 渲染预览图自检排版，再装 LibreOffice（可选）。

### 使用

在 Antigravity 里打开放着资料的项目文件夹，然后直接说：

```
用 inputs/销售数据.xlsx 做一份麦肯锡风格的 Q4 业务回顾 PPT，8 页，公司名是"星海科技"
```

Antigravity 会根据 skill 的描述自动启用它。如果没有触发，可以明确说
"使用 mckinsey-pptx skill 做……"。生成的文件在项目的 `output/` 文件夹里。

模型按 skill 的流程只用两个固定命令：`scripts/catalog.py`（按名称查模板）和
`scripts/run_deck.py`（构建 + 检查 + 渲染预览，一条命令），不再临时拼写
`python -c` 命令，所以需要审批的命令种类大幅减少；如果终端设置支持允许列表，
把这两个脚本加进去即可。附件请直接拖进对话，
模型会按附件路径读取，不再手抄大纲。

### 更新

```bash
git -C "$HOME/.gemini/antigravity/skills/mckinsey-pptx" pull
```

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

## 根据大纲 / 文档出稿（"按大纲出稿"模式）

给它一份现成的大纲（比如 Word 写的"Slide 1: … Slide 2: …"）或方案文档时，
它会自动进入**按大纲出稿模式**，遵守下面这些规则：

- **大纲就是需求本身**：每个章节至少一页，顺序不变；要删减或合并会先问你。
- **数据全部保留**：源文件里的每张表、每个数字都会出现在 PPT 里，用表格或图表呈现。
- **不编造**：只用源文件里的数字和来源；缺的地方标"[待补充]"并列成清单。
- **语言跟源文件一致**：英文大纲做英文 PPT，除非你明确说"做成中文版"。
- **只扩写，不新增**：可以解释和串联源文件内容，但不能新增目标、合作方、
  产品形态、渠道、技术或医学主张。
- **出稿后自检**：用 `scripts/deck_check.py` 把 PPT 和源文件逐项对照，报告：
  疑似编造的数字、源数据覆盖率、内容过稀的页面、残留占位符、
  源文件里没有的主张或引号词、同一版式连续过多或缺少图表、字号过小、页脚来源写法错误，
  以及文字版式占比（仅提醒）。

示例：

```
根据 inputs/大纲.docx 做一份完整的营销方案 PPT，给管理层预读。
```

你也可以自己运行检查：

```bash
python scripts/deck_check.py output/xxx.pptx --source inputs/大纲.docx
# 或一条命令完成构建 + 检查 + 预览图（Windows 自动找 LibreOffice）
python scripts/run_deck.py output/build_xxx.py --source inputs/大纲.docx
```

第 [11] 项"版式构成"只是提醒：文字版式（卡片、表格）超过内容页一半时提示你
复查哪些页其实是关系（流向、占比、变化、排名、因果、交集），不会判为不通过。

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

## 能做哪些幻灯片？（80 个模板 + 复合版式）

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
- **Marimekko**（细分 × 玩家，面积 = 占比）、**Treemap**（面积 = 数值）、**桑基图**（流向与转化）
- **斜率图**（两个时点的变化）、**哑铃图**（每类两个值的差距）、**排名变化图**（3–6 期排名）
- **热力图**（行 × 列数值）、**雷达图**（多选项多维度画像，原生可编辑）

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
- **鱼骨图**（一个问题现象的分类原因）、**客户旅程**（阶段 × 行为 × 情绪曲线）
- **泳道图**（跨角色流程与交接）、**分层堆叠**（技术 / 能力栈）、**韦恩图**（2–3 个条件的交集）

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

### ⭐ 新一代"富版式"模板（新稿默认优先使用）
- **卡片网格** `card_grid`：2–8 张卡片，每张有图标、小标题、要点或大数字；
  字号会自动适配空间，内容少时卡片自动收紧，不再出现大片空白
- **通用数据表** `data_table`：任意行列，可高亮某行或某列，右侧带 Key Insight 框，可在 PowerPoint 里直接编辑
- **原生图表** `chart`：柱状、条形、折线、堆积、饼图、环形图；能在 PowerPoint 里"编辑数据"，
  可突出某个系列或某根柱子，并带洞察面板
- **SWOT** `swot`：四象限，固定配色和图标
- **价格 / 服务阶梯** `tier_ladder`：基础 → 专业 → 企业这类逐级上升的分层
- **横排列表** `card_rows`：决策事项、风险与应对、建议等需要一两句话说明的条目
- **瀑布图 / 桥图** `waterfall`：营收、利润、成本从起点到终点的变动拆解（可编辑原生图表）
- **计分卡** `scorecard`：KPI 目标 vs 实际 + 红黄绿状态
- **路线图** `roadmap`：多条工作流 × 时间段，带里程碑
- **时间线** `timeline`：3–7 个按时间排列的事件
- **2×2 矩阵** `matrix_2x2`：影响 × 难度、可能性 × 严重度等两维度排序
- **方案概览** `option_profiles`：2–4 个方案 / 产品 / 供应商并列，同样的维度（定位、关键数字、优劣势）
- **决策矩阵** `decision_matrix`：标准 × 权重 × 方案，原始分 + 加权分，每行最高分标金色，加权总分
- **风险登记** `risk_register`：风险卡片 + 等级标签（高 / 中 / 低）+ 应对措施
- **复合版式** `composite`：在一页里自由组合"流程图、指标表、大数字、卡片、优劣势、编号清单、分阶段路线、图表、表格"，
  做出咨询公司式的"方案详解页"（左边商业模式和数字，右边 Why / How / 优劣势，底部结论）
- **逻辑链网格** `logic_grid`：每行一个主题，按"外部情境 → 自身能力 → 竞争优势"或"客户需求 → 我们怎么做 → 表现 → 启示"
  逐列推进，最后一列是深色结论框；`direction="down"` 变成 PEST / 五力分析的"现状 → 对公司的影响"
- **战略挑战收敛** `strategic_challenge`：多个驱动因素 → 各自后果 → 汇聚成一个核心威胁 → "How can X …, given …?" 关键问题
- **故事线执行摘要** `storyline_summary`：情境 → 关键问题 → 备选方案（推荐方案高亮）→ 建议，一页讲完整份 deck
- **复合版式的逻辑升级**：列标题（箭头 / 横线 / 色条）、列间箭头、区块间向下箭头，以及新组件
  `callout`（新价值主张）、`pyramid`（定位金字塔）、`sections`（可行性 / 优点 ✓ / 缺点 ✗）
- **因果飞轮 / 循环** `cycle`：起点 → 多条并行影响链 → 结果，虚线反馈回起点；或 3–6 步的恶性循环
- **风险热力图** `risk_heatmap`：按发生概率 × 影响程度分区摆放编号风险，右侧按编号列出应对措施
- **竞争定位刻度** `positioning_scale`：每个指标一行，写出含义，各家在"低 → 高"刻度上的位置一目了然
- **价值链 + KSF** `value_chain`：箭头环节 + 每段关键成功要素，标出公司自己做的环节，可加价格/成本
- **分阶段落地网格** `phase_grid`：行（合作伙伴 / 行动 / 资源）× 阶段，可跨年份合并、加 KPI 行和右侧风险应对栏
- **评分矩阵（带理由）** `evaluation_matrix`：每格"分数 + 理由"、圆点评分、按维度分组、顶部公式横幅、优先级标签
- **商业模式画布** `business_model_canvas`、**战略三角** `strategic_triangle`、**中心辐射图** `hub_spoke`
- **章节导航条**：`PresentationBuilder(nav=[...])` 后每页传 `nav="当前章节"`，顶部显示面包屑
- **标签自动跟随语言**：`make_theme(lang="zh")` 时，"Key insight / 推荐 / 加权总分 / SWOT 标题"等默认标签全部显示为中文
- 每页都可以加 `kicker`（标题上方的小字定位标签），并列页面用 `group` 标记，保证版式一致
- 文字中可以用 `**加粗**`、`{red|标红}`、`{green|标绿}` 强调关键词，内置 88 个商务图标
- **品牌配色**：说"用品牌色 #103B8C"即可，整套配色会自动换成你的品牌色

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
from mckinsey_pptx import PresentationBuilder, make_theme

b = PresentationBuilder(theme=make_theme("某某公司", lang="zh"),
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
from mckinsey_pptx import make_theme

make_theme(lang="zh")                                  # 中文页面，微软雅黑，无署名
make_theme("某某公司", lang="zh")                       # 页脚 "ⓒ 2026 某某公司"
make_theme("某某公司", lang="zh", font="PingFang SC")   # 苹方
make_theme("Acme", brand="103B8C")                     # 英文页面 + 品牌色
```

`Theme` 上与署名相关的字段：

| 字段 | 作用 | 默认值 |
|---|---|---|
| `copyright_text` | 内容页右下角页脚 | `""`（只显示页码） |
| `brand_text` | 深蓝总结页右下角标记 | `""` |
| `source_label` | 页脚 `source=` 的前缀 | `"Source: "`（中文主题为 `"资料来源："`） |
| `typography.east_asian_family` | 中日韩字形使用的字体 | `None`（中文主题为 `"Microsoft YaHei"`） |

`lang` 是**幻灯片的语言**，不是你聊天用的语言。旧的 `make_zh_theme` / `make_brand_theme` 仍可使用。

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

### 冒烟测试

```bash
python tests/smoke/run.py            # 构建 5 个不同场景的 PPT 并逐个检查
python tests/smoke/run.py --render   # 同时渲染预览图（需要 LibreOffice）
```

每次修改引擎或规则后跑一遍，避免只对某一类 PPT 有效。

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
├── scripts/
│   └── deck_check.py                      # 把 PPT 和源文件对照检查
├── tests/smoke/                           # 多场景冒烟测试（财务回顾 / 项目汇报 / 中文战略 / 现场路演 / 方案评估）
├── examples/
│   ├── demo.py                            # 英文示例
│   ├── demo_chinese.py                    # 中文示例
│   └── demo_korean.py                     # 韩文示例
├── SKILL.md                               # Google Antigravity Skill 定义（仓库即 skill）
├── LICENSE                                # MIT © 2026 AX Labs
├── README.md                              # 中文说明（本文件）
├── README.ko.md                           # 韩文原版说明
└── requirements.txt                       # python-pptx 等依赖
```

</details>
