# DeerFlow 2.0 从入门到精通

> 一本写给「想用起来、想看懂、想改得动」的人的书。
> 不是官方文档的翻译，是站在你肩膀上看过源码与规格后的白话拆解。

---

## 阅读指南

我自己用 DeerFlow 踩过的坑，总结成三条建议：

1. **先跑再读**。DeerFlow 是一个「产品级」的超级代理框架，不是纯库。它自带 Web UI、网关、沙箱和终端。先把 §02 跑起来，你才会有体感。
2. **分两层理解**。底层是 LangGraph 编排的 Agent 运行时；上层是 Gateway / Frontend / Provisioner 组成的服务栈。两边要分开看，合起来才是 DeerFlow。
3. **技能是灵魂**。DeerFlow 把「能做什么」几乎全部外置成 Skill 目录。看懂 §07，你就看懂了扩展性。

> **核心建议**：第一次读，先照 §02 把例子跑起来。等你有体感了，再回来看机制。

---

# 目录

**Part 1 起步**
- [§01 DeerFlow 到底是什么](#§01-deerflow-到底是什么)
- [§02 五分钟跑通](#§02-五分钟跑通)
- [§03 一次对话背后发生了什么](#§03-一次对话背后发生了什么)
- [§04 模型随便换](#§04-模型随便换)

**Part 2 核心能力**
- [§05 五大内置能力](#§05-五大内置能力)
- [§06 子代理与编排](#§06-子代理与编排)
- [§07 Skills 技能系统](#§07-skills-技能系统)
- [§08 长期记忆与历史](#§08-长期记忆与历史)
- [§09 沙箱与文件系统](#§09-沙箱与文件系统)
- [§10 MCP 工具接入](#§10-mcp-工具接入)
- [§11 人机协同](#§11-人机协同)
- [§12 护栏与权限沙箱](#§12-护栏与权限沙箱)
- [§13 流式与终端工作台](#§13-流式与终端工作台)

**Part 3 实战与进阶**
- [§14 生成与报告能力](#§14-生成与报告能力)
- [§15 定时任务](#§15-定时任务)
- [§16 上下文工程](#§16-上下文工程)
- [§17 可观测与生产部署](#§17-可观测与生产部署)
- [§18 选型对比](#§18-选型对比)
- [§19 避坑指南](#§19-避坑指南)

---

# Part 1: 起步

## §01 DeerFlow 到底是什么

DeerFlow 是一个开源的「超级代理框架」（super agent harness）。它能编排子代理、记忆和沙箱，去完成几乎任何任务，而驱动这一切的是一套可扩展的技能（Skills）。

名字拆开看：**D**eep **E**xploration and **E**fficient **R**esearch **F**low。它从「深度研究」起家，2.0 已经长成一个通用代理底座。

**2.0 是一次彻底重写**。它和 v1 没有任何代码共享。原来的 Deep Research 框架留在 `1.x` 分支维护。所以你看到的老文章，很多对 2.0 不适用——别拿 v1 的经验套 2.0。

几个关键事实，先钉死：

- **2026 年 2 月 28 日**，v2 发布后登上 GitHub Trending 榜首。
- 官方站点 `deerflow.tech` 有真实演示。
- 它集成了字节跳动火山引擎的智能搜索抓取工具集 **InfoQuest**。
- 官方推荐搭配 **Doubao-Seed-2.0-Code、DeepSeek v3.2、Kimi 2.5** 使用。

### DeerFlow 和你见过的框架不一样在哪

很多人第一反应是：「这不就是又一个 Agent 库？」不是。DeerFlow 的定位是**产品级 harness**，它交付的是一整套可运行的服务，而不只是一个 `import` 就能用的类。

| 维度 | 纯 Agent 库（如 deepagents） | DeerFlow 2.0 |
|------|------|------|
| 交付形态 | Python 包，代码里调用 | 服务栈：Gateway + Frontend + 沙箱 + 可选 Provisioner |
| 运行界面 | 你自己在代码里接 | 自带 Web UI、终端 TUI、IM 接入 |
| 编排内核 | 各家不同 | 基于 **LangGraph**（图、checkpointer、store） |
| 调度能力 | 一般没有 | 内置定时任务（§15） |
| 模型绑定 | 看库 | **模型中立**，OpenAI/OpenRouter/vLLM/Codex/Claude/MiniMax 通吃 |

**标叔的结论**：如果你只想在代码里嵌一个会调工具的 Agent，DeerFlow 重了；如果你想要一个「开箱即用的研究/自动化工作台」，DeerFlow 正中靶心。

下一章，我们不讲道理，先把服务跑起来。

---

## §02 五分钟跑通

DeerFlow 给了 `make` 一条龙脚本。照做，五分钟能看到界面。

### 第一步：克隆与初始化

```bash
git clone https://github.com/bytedance/deer-flow.git
cd deer-flow
make setup        # 交互向导，生成 config.yaml 和 .env（约 2 分钟）
```

`make setup` 是个交互式向导。它会问你 API Key、搜索源、沙箱偏好，最后吐出两份配置：

- `config.yaml` —— 模型、数据库、沙箱、调度等核心配置
- `.env` —— 密钥类环境变量

跑完用两个命令自检：

```bash
make doctor            # 验证依赖和配置是否就绪
make support-bundle    # 排障时生成隐私安全的打包信息
```

### 第二步：用 Docker 跑（推荐）

```bash
make docker-init    # 拉取沙箱镜像
make docker-start   # 启动开发用服务栈
```

开发栈起来后，访问 **http://localhost:2026** 就能用 Web UI 了。

### 第三步：生产栈（可选）

```bash
make up     # 构建并启动生产服务
make down   # 停止
```

### 本地开发模式

不想碰 Docker，也可以纯本地跑：

```bash
make dev
```

它对机器有要求，下面这张表照着配：

| 目标 | 起步 | 推荐 |
|------|------|------|
| 本地评估 `make dev` | 4C / 8G / 20G SSD | 8C / 16G |
| Docker 开发 | 4C / 8G / 25G | 8C / 16G |
| 长驻服务 `make up` | 8C / 16G / 40G | 16C / 32G |

**标叔的结论**：第一次玩，直接 `make setup` + `make docker-init` + `make docker-start`，别在资源配置上省。沙箱镜像不拉，后面代码执行会报错。

下一章，我们钻进「你在界面里发一句话」之后，系统内部到底走了什么路。

---

## §03 一次对话背后发生了什么

你点下发送，到答案回来，中间跨了四层服务、两套运行路径。先把拓扑画清楚。

### 服务拓扑

DeerFlow 2.0 的生产拓扑是这样的：

```
Nginx (2026)
  ├── /api/langgraph/*  → Gateway 的 LangGraph 兼容运行时
  └── /api/*            → Gateway REST API（端口 8001）
Frontend (Next.js，端口 3000)
Provisioner (可选，端口 8002，负责按需拉起沙箱)
```

注意：Nginx 在前，Gateway 在后。所有 `/api/*` 都进 Gateway，只有 `/api/langgraph/*` 走 LangGraph 兼容运行时。

### 两套运行路径，一个 Agent 工厂

这是 DeerFlow 架构里最容易被误解的点。现在代码里有**两条运行路径**，但它们共用同一个 Agent 工厂：

| 路径 | 触发方 | 运行方式 | 持久化 |
|------|------|------|------|
| Web/Gateway `run_agent()` | 浏览器/API | 异步 `astream` + `StreamBridge` 做 SSE | 写 `thread_meta` |
| `DeerFlowClient.stream()` | 终端 TUI / 嵌入 | 同步、进程内 | 只写 checkpointer |

两条路都通过同一个 `make_lead_agent` / `create_agent()` 工厂构建 Agent。也就是说，**Agent 行为一致，编排外壳不同**。

### 一次对话的完整生命周期

```
你的消息
  → Gateway 接收，注入已认证用户上下文
  → run-launch helper 启动一个 run
  → lead agent（主代理）拿到 prompt
      → 命中 Skill？加载对应技能
      → 需要子任务？拆给子代理并行跑
      → 要执行代码？进沙箱（bash / 写文件）
      → 要调外部能力？走 MCP 或内置工具
      → 工具调用前过护栏（GuardrailMiddleware）
  → 中间状态写 checkpointer + event store
  → 流式结果经 StreamBridge 回前端
  → 会话索引写 thread_meta，前端侧边栏可见
```

关键存储有两个，别混：

- **checkpointer**：LangGraph 的状态快照，记录「当前消息列表」。
- **event store（RunJournal）**：追加式事件流水，记录每一条 trace / message / lifecycle / middleware 事件。**它不受上下文压缩影响**——这点 §08、§16 会展开讲。

**标叔的结论**：理解 DeerFlow，先记住「Gateway 管调度和持久化，Agent 工厂管智能，LangGraph 管状态和流式」。三层职责分清，后面每章都不乱。

下一章，我们聊最容易让人兴奋也最容易踩坑的事：换模型。

---

## §04 模型随便换

DeerFlow 是**模型中立**的。这不是口号，是 `config.yaml` 里真能配出来的。

### 配置长什么样

模型在 `config.yaml` 里以列表形式声明，每一项是 `name` + `use`（LangChain 类路径）+ `model` + `api_key`：

```yaml
models:
  - name: gpt-4o
    use: langchain_openai:ChatOpenAI
    model: gpt-4o
    api_key: $OPENAI_API_KEY
```

`use` 字段决定用哪个 LangChain 聊天模型类。DeerFlow 已经接好了多家：

| 提供方 | 示例模型 | 接入方式 |
|------|------|------|
| OpenAI | `gpt-4o`、`gpt-5-responses`（Responses API） | `langchain_openai:ChatOpenAI` |
| OpenRouter | `gemini-2.5-flash-preview`（基址转发） | 转发基址 |
| vLLM 本地 | `Qwen/Qwen3-32B` | `VllmChatModel` |
| Codex CLI | Codex 命令行后端 | `CodexChatModel` |
| Claude Code | Claude Code OAuth | `ClaudeChatModel` |
| MiniMax | 文本/生成模型 | 自带 patched 适配 |

官方推荐搭配 **Doubao-Seed-2.0-Code、DeepSeek v3.2、Kimi 2.5** 当主力模型。

### 两个注意点

- **环境变量占位符**。上面 `$OPENAI_API_KEY` 会从环境或 `.env` 读取，别写死明文。
- **多模型共存**。你可以同时列五六个模型，运行时用 `/model`（终端）或界面切换。DeerFlow 默认就用第一个，但切模型是常态操作，不是改配置重启。

**标叔的结论**：DeerFlow 把「换模型」降到了改一行配置的事。但你真要稳定，建议先用官方推荐模型跑通，再试验本地 vLLM——本地模型的工具调用格式差异，是新手最常见的坑。

模型讲完，进入核心能力。下面九章，是 DeerFlow 真正的骨架。

---

# Part 2: 核心能力

## §05 五大内置能力

DeerFlow 把「代理能干什么」拆成了五个可独立理解、又能组合使用的能力。

| 能力 | 一句话 | 落地章节 |
|------|------|------|
| 子代理（Sub-Agents） | 把大任务拆给多个并行小代理 | §06 |
| 技能（Skills） | 可插拔的「怎么做某类事」目录 | §07 |
| 记忆（Memory） | 长期记忆 + 不可篡改的事件历史 | §08 |
| 沙箱（Sandbox） | 隔离的文件系统与代码执行环境 | §09 |
| MCP | 接外部工具/数据源的开放协议 | §10 |

再加两层横切能力，贯穿以上所有：

- **人机协同（HITL）**：代理不确定时主动问你（§11）。
- **护栏（Guardrails）**：工具调用前做权限与安全检查（§12）。

**标叔的结论**：这五个能力不是堆功能，是「智能 + 知识 + 记忆 + 执行 + 扩展」的完整闭环。后面九章，就是把这个闭环拆开给你看。

先讲智能的拆分方式——子代理。

---

## §06 子代理与编排

DeerFlow 的主代理（lead agent）不把所有活都自己干。遇到复杂任务，它进入**编排者模式（Orchestrator Mode）**，把任务拆成并行子任务，甩给多个子代理同时跑，最后自己只做综合。

官方 prompt 里写得很直白：

> You are a task orchestrator - decompose complex tasks into parallel sub-tasks and launch multiple subagents simultaneously. Synthesize results, don't execute directly.

翻译过来：**你是调度员，不是执行员。拆、派、合，三件事。**

### 两个内置纪律

主代理的 prompt 里还钉了两条铁律，对你写自己的代理很有参考：

1. **先澄清，再动手**（Clarification First）：
   > ALWAYS clarify unclear/missing/ambiguous requirements BEFORE starting work - never assume or guess

   代理在需求模糊时，会调用 `ask_clarification` 反问你，而不是直接猜。

2. **复杂任务先找技能**（Skill First）：遇到复杂任务，先加载相关 Skill，再动手。

### 轮次预算

子代理不是无限跑。系统有 `MAX_TURNS_REACHED` 这样的轮次上限做保护。任务太深、循环太久，会被预算打断，避免烧光 token 还不出结果。

**标叔的结论**：DeerFlow 的「编排」不是花活，是工程约束。并行 + 预算 + 先澄清，三件套把「代理跑飞」的概率压到了最低。你自定义代理时，这套纪律值得抄。

技能是 DeerFlow 扩展性的核心。下一章细说。

---

## §07 Skills 技能系统

DeerFlow 把「怎么做好某类事」外置成一个个 **Skill 目录**。这是它和很多框架最不一样的地方——能力不是写死在代码里的，是目录里读出来的。

### 一个 Skill 长什么样

每个 Skill 是自包含目录，典型结构：

```
skills/public/image-generation/
  SKILL.md          # frontmatter: name + description + 给代理的使用说明
  scripts/
    generate.py     # 纯 requests 调用外部 API 的 CLI（argparse）
  templates/        # 可选模板
```

`SKILL.md` 的 frontmatter 有 `name` 和 `description`，后面是给 Agent 看的操作说明。运行时，公共技能挂在 `/mnt/skills/public/<name>/`，产物写到 `/mnt/user-data/...`。

### public 与 custom，靠组合键区分

Skill 分两类：`public`（仓库自带）和 `custom`（你自己装）。早期有个坑：同名 public 和 custom 技能会互相串门。2.0 的解法是**组合键** `{category}:{name}`。

配置里这么写：

```json
{
  "skills": {
    "public:my-skill":  { "enabled": true },
    "custom:my-skill":  { "enabled": false }
  }
}
```

旧格式（只用 `name`）依然兼容——系统会自动识别。加载时还会在同一类别内查重，撞名直接抛 `ValueError`，把错误说在前面。

### 通过 API 管理技能

Gateway 暴露了技能管理端点：

| 端点 | 作用 |
|------|------|
| `GET /api/skills` | 列出技能 |
| `GET /api/skills/{skill_name}` | 查详情，可带 `?category=public` |
| `PUT /api/skills/{skill_name}` | 改启用状态，可带 `?category=` |
| `POST /api/skills/install` | 从 `.skill` 归档安装 |

同名时，API 会要求你补 `category` 参数，否则返回 400，把「到底改哪个」抛回给你。

### 用 skill-creator 造新技能

仓库里自带一个 `skill-creator` 公共技能，提供 `scripts/init_skill.py` 脚手架。想加自己的能力，先用它生成骨架，再填 `SKILL.md` 和 `scripts/`。

**标叔的结论**：Skill 目录化，是 DeerFlow 能「越用越聪明」的根本。你别急着改核心代码，先想「这事能不能做成一个 Skill」。能，就外置；外置了，就能热插拔、能隔离、能审计。

记忆是代理的「长期脑子」。下一章讲它怎么不丢历史。

---

## §08 长期记忆与历史

DeerFlow 的记忆分成两层，一定要分清：**长期记忆（Long-Term Memory）** 和 **事件历史（event store）**。

### 为什么需要两套

LangGraph 的 checkpointer 存的是「当前消息列表」的快照。问题是——当上下文太长，系统会做**压缩（summarization）**，把旧消息原地替换成摘要。结果就是：你去查历史，最早的用户原话不见了，只剩一段摘要。

DeerFlow 的解法：再加一条 **event store（RunJournal）**，追加式记录每一次事件，不覆盖、不压缩。

### RunJournal 记了什么

`RunJournal` 把运行过程写成 `run_events` 表，按类别分：

| category | 内容 |
|------|------|
| trace | LLM 请求、工具调用等链路追踪 |
| message | 每一条消息 |
| lifecycle | run 开始/结束/出错 |
| middleware | 中间件事件（如压缩发生点） |

关键点：**event store 不受 summarization 影响**。即使消息被压缩成摘要，原始 human 消息还在 event store 里。

### /history 读的是 event store

前端历史接口原本从 checkpointer 读，压缩后丢原话。2.0 改成了**优先读 event store 的 `list_messages()`**，覆盖 checkpointer 的 messages 字段。这样你在界面上能看到压缩之前的真实对话。

技术上还有两个细节值得记：

- 消息 ID 用 `uuid5(NAMESPACE_URL, f"{thread_id}:{seq}")` 确定性生成，稳定可复现。
- 历史分页不能用固定 `limit=1000`，长对话会丢头——必须 `count_messages()` 后全量拉，或游标翻页。

**标叔的结论**：DeerFlow 对「记忆不可丢」这件事很较真。checkpointer 管「当下状态」，event store 管「完整真相」。你做审计、做复盘，永远信 event store。

代码要执行，得有隔离环境。下一章讲沙箱。

---

## §09 沙箱与文件系统

DeerFlow 让代理写代码、跑命令，但这些动作必须关在**沙箱**里，不能碰你本机。

### 沙箱给你什么

沙箱提供两层能力：

- **Bash 访问**：代理能在隔离环境里执行命令。
- **文件写工具**：`write_file`、`str_replace`、`read_file` 等。

向导初始化时你会配置安全偏好，决定沙箱能碰多大范围。

### 沙箱后端可换

DeerFlow 支持多种沙箱 provider，在 `config.yaml` 里指定：

```yaml
sandbox:
  use: deerflow.community.aio_sandbox:AioSandboxProvider
```

可选后端包括：

| provider | 说明 |
|------|------|
| `aio_sandbox` | 社区版异步沙箱（provisioner 模式会自动拉起 provisioner） |
| `e2b` | E2B 云端沙箱 |
| `kubernetes` | K8s  Pod 沙箱 |
| `docker` | Docker 容器沙箱 |

### 技能目录互相隔离

每个 Skill 在沙箱里是独立目录，互不 import。MiniMax 那篇设计文档明确写了：MiniMax 代码在每个 skill 内各自内联，不做跨 skill 共享模块——少量重复可接受，换来的是强隔离。

**标叔的结论**：沙箱是 DeerFlow 敢让代理「动手」的底气。本地玩建议先用 `aio_sandbox`，别一上来就给代理裸 Bash 权限。

外部工具除了沙箱里跑，还能通过 MCP 接进来。下一章讲。

---

## §10 MCP 工具接入

MCP（Model Context Protocol）是接外部工具和数据源的开放标准。DeerFlow 原生支持 MCP Server。

### 怎么配

MCP 服务器在 `extensions_config` 里声明：

```json
{
  "mcpServers": {
    "my-server": {
      "tool_call_timeout": 30
    }
  }
}
```

几个要点：

- **每服务器超时**：`tool_call_timeout` 控制单个工具调用最长等多久。
- **会话池生命周期**：MCP 连接的会话池和 DeerFlow 会话生命周期同步，避免孤儿连接。
- **缓存重置端点**：提供端点手动清 MCP 缓存，改了外部工具后不用重启。

### 和 Skills 同居一个配置

注意 `extensions_config.json` 同时管两件事：**mcpServers** 和 **skills**。它是 DeerFlow 扩展能力的「总开关文件」。

**标叔的结论**：MCP 让 DeerFlow 能接任意兼容服务——数据库、内部 API、第三方 SaaS。但每接一个，记得设 `tool_call_timeout`，不然一个卡死的外部工具能拖垮整个 run。

代理要调工具、要问人，得有协同机制。下一章讲人机协同。

---

## §11 人机协同

DeerFlow 的代理不是闷头干。它会在关键节点停下来，找你确认。这就是 **Human-in-the-loop（HITL）**。

### 三种协同入口

1. **`ask_clarification`**：需求模糊时反问。注意官方强调过——**非内部调用方不能剥离澄清请求**。也就是说，你接 DeerFlow 做自己产品时，不能偷偷把「问用户」这一步删掉，否则代理会瞎猜。
2. **Session Goals**：给一次会话设目标，让代理知道「这次要做到哪」。
3. **手动上下文压缩（Manual Context Compaction）**：你主动触发压缩，控制上下文体积。

### 协同背后是归因

每次工具调用、每次澄清，系统都带着**归因信息**走。哪些信息？看 §12 的 `GuardrailRequest` 字段——`user_id`、`run_id`、`thread_id`、`tool_call_id` 都在。这让「谁、在哪次运行、调了什么」全程可追溯。

**标叔的结论**：HITL 不是「功能」，是信任机制。DeerFlow 把「问人」当成一等公民，而不是可选项。你做严肃场景，千万别为了「自动化」把澄清关了。

工具调用要安全，得有护栏守着。下一章讲。

---

## §12 护栏与权限沙箱

DeerFlow 在工具调用真正发生前，会过一道**护栏**。这是它敢默认放开工具调用的原因。

### GuardrailMiddleware + GuardrailProvider

架构是「中间件 + 可插拔 provider」：

- `GuardrailMiddleware`：在工具调用前拦截，构造 `GuardrailRequest`，交给 provider 判定。
- `GuardrailProvider`：你实现的判定逻辑，返回 `GuardrailDecision`。

`GuardrailRequest` 携带的字段（2.0 已补全运行时归因）：

```python
@dataclass
class GuardrailRequest:
    tool_name: str
    tool_input: dict
    agent_id: str | None = None
    thread_id: str | None = None
    is_subagent: bool = False
    timestamp: str = ""
    user_id: str | None = None        # DeerFlow 内部稳定用户 ID
    user_role: str | None = None      # admin / user
    oauth_provider: str | None = None # 未来 OAuth/SSO
    oauth_id: str | None = None
    run_id: str | None = None         # run 级审计
    tool_call_id: str | None = None   # 单次调用定位
```

`GuardrailDecision` 表达 `allow` / `deny`、原因、`policy_id`、元数据。

### 身份只信服务端

关键安全点：**Gateway 注入只信任服务端认证态 `request.state.user`**。客户端 body 里伪造的 `user_id` / `user_role` / `oauth_*` 不会覆盖服务端身份。这堵死了「假装是 admin」的越权路。

### 第二道护栏：ReadBeforeWriteMiddleware

代码写入还有一道**新鲜度护栏**。规则很硬：

1. `read_file` 成功 → 记一个 read-mark：`sha256(当前完整文件内容)`。
2. 改已存在文件（`write_file` 覆盖 / `append` / `str_replace`）前，校验「最新 read-mark 的 hash == 当前文件 hash」。
3. 不匹配 → **拦截，不执行写入**，返回「请先读该文件」。
4. 写入成功会立刻让上一次 read-mark 过期 → 连续改之间被逼着重读。
5. 写不存在的新文件 → 放行。

它**默认开启**，挂在中间件链尾、SandboxAudit 之后。对并行同文件写入，用 per-path 锁保证确定性拦截。

**标叔的结论**：DeerFlow 的安全是「双层 + 默认开」。护栏管「能不能调」，读写门管「改文件前看没看」。你做自己的 provider，至少把 `user_role` 用起来——比如 `admin:bash` 才放行危险工具。

能力讲完，来到界面与流式。下一章讲终端工作台。

---

## §13 流式与终端工作台

不是所有人都爱开浏览器。DeerFlow 给了**终端工作台（TUI）**，而且它和 Web 共享同一套会话。

### `deerflow` 命令

装好之后，控制台脚本叫 `deerflow`。默认交互路径：

```bash
deerflow            # TTY 下直接进交互界面
deerflow --tui      # 强制 TUI
deerflow chat       # 同上，进对话
deerflow --continue # 续上最近一次会话
deerflow --resume THREAD_ID   # 续指定会话
```

无头（脚本用）模式也保留着：

```bash
deerflow chat --print "summarize this repo"
deerflow models list --json
deerflow threads list --json
deerflow skills list|get|enable|disable|install
deerflow mcp list|export|apply
deerflow memory status|show|export|import|clear|fact add
```

### TUI 和 Web 怎么互通

这是设计上最巧的一点：TUI 跑在**嵌入式模式**，不需要 Gateway / 前端 / Nginx / Docker。但它**复用同一个 `thread_meta` 持久层**。

也就是说——你在终端建一个会话，关掉终端，打开 Web UI，那个会话出现在侧边栏里。因为它写的是同一个 `thread_meta` 表，而 Web UI 正是从这张表读会话列表的。**Web 可见性靠共享存储，不靠 Gateway 进程在跑。**

### 终端里的斜杠命令

TUI 支持一套 slash 命令，覆盖你能想到的所有操作：

| 命令 | 行为 |
|------|------|
| `/help` | 分类命令与快捷键 |
| `/new` | 新会话 |
| `/resume` `/threads` `/switch` | 会话切换 |
| `/model` | 模型选择器 |
| `/skills` | 浏览已启用/可用技能 |
| `/tools` `/mcp` | 工具与 MCP 状态 |
| `/memory` | 记忆状态与已注入事实 |
| `/uploads` `/artifacts` | 上传与产物 |
| `/details` `/usage` | 活动明细 / token 用量 |
| `/config` `/quit` | 配置路径 / 退出 |

**标叔的结论**：DeerFlow 的 TUI 不是「阉割版 CLI」，是和 Web 平起平坐的一等界面。它背后是同一个 `DeerFlowClient` 运行时。你习惯终端，就全程终端；习惯浏览器，就全程浏览器；两边会话还打通——这点很香。

核心能力到此讲完。进入实战与进阶。

---

# Part 3: 实战与进阶

## §14 生成与报告能力

DeerFlow 不只是「聊天 + 搜网页」。它自带一类**生成技能**，能出图、出视频、出播客、出音乐，还能写结构化研究报告。

### 四类生成技能

| 技能 | 现有 provider | 端点 |
|------|------|------|
| `image-generation` | Gemini（`gemini-3-pro-image-preview`） | `generativelanguage.googleapis.com` |
| `video-generation` | Gemini Veo（`veo-3.1`） | 长任务轮询 |
| `podcast-generation` | 火山引擎 TTS | `openspeech.bytedance.com` |
| `music-generation` | **MiniMax**（新增） | `api.minimaxi.com` |

### provider 怎么选

每个生成脚本里有 `_resolve_provider()`，判定顺序很讲理：

1. **显式覆盖**：环境变量 `IMAGE_GENERATION_PROVIDER` 等设了，直接用。
2. **现有 provider 优先**：原 provider 密钥齐全 → 用原来的，保证向后兼容。
3. **回退 MiniMax**：原 provider 没密钥但 `MINIMAX_API_KEY` 有 → 走 MiniMax。
4. 都没有 → 抛清晰错误，告诉你两套环境变量怎么配。

默认行为不变——你原来配了 Gemini，一切照旧；只配了 MiniMax 的用户自动走新路。

### 研究报告与「压缩标记」

DeerFlow 继承了 v1 的 Deep Research 血统，能产出带引用的研究报告。这里有个细节体验很好：当运行中触发了上下文压缩，前端历史里会插入一个 **`[N messages condensed]` 标记卡片**，点开能看到被压缩成的摘要。

实现上，它包装了 LangChain 的 `SummarizationMiddleware`，在每次真正压缩时 `adispatch_custom_event("summarization", ...)`，把 `replaced_count` 和摘要文本写进 event store，前端再在正确时间线位置渲染这张卡片。这样你不会疑惑「我前面的话怎么没了」。

**标叔的结论**：生成技能是 DeerFlow「产品感」的来源。你做个内容工作流，直接复用 `image-generation` / `podcast-generation` 比自己接 API 省太多事。记得用 `<SKILL>_PROVIDER` 锁定 provider，别让自动判断在半夜切了供应商。

定时跑任务，是自动化刚需。下一章讲。

---

## §15 定时任务

DeerFlow 2.0 有**定时任务 MVP**——注意是 MVP，有明确边界，但已经能打。

### 它解决什么

之前仓库里有内部定时器，但用户没法从产品里「创建、查看、暂停、触发、删除」常驻后台任务。MVP 先把这些管理面做出来，自然语言建任务留到后面。

### 支持的形态

| 维度 | 支持 | 不支持 |
|------|------|------|
| 任务类型 | `once`（一次性）、`cron`（周期） | `interval`（间隔） |
| 上下文模式 | `fresh_thread_per_run`（默认）、`reuse_thread` | —— |
| 触发 | 定时 + 手动 `trigger` | IM/Channel 派发 |

为什么不支持 `interval`？MVP 故意砍掉，因为它要多一套解析、多前端校验、多边界 case，而 `once` + `cron` 足以证明调度架构。

### 它靠 DB 租约保证安全

调度器**默认关闭**，要显式开：

```yaml
scheduler:
  enabled: false
  poll_interval_seconds: 5
  lease_seconds: 120
  max_concurrent_runs: 3
  min_interval_seconds: 60
```

核心保障是 **DB 租约（lease）**：每个轮询周期，调度器用一条 DB 事务原子地「认领」到期任务（设 `lease_owner` + `lease_expires_at` + 临时 `running`），避免多实例重复跑。任务 owner 隔离——别人的任务你列不到也改不了。

每次触发，都走**和手动触发相同的 run-launch helper**，不另搞一套运行时。重叠时按固定规则 `skip`，错过按 `run_once` 补最新一次。

REST 端点集中在 `/api/scheduled-tasks`：`GET / POST / PATCH`、`/pause` `/resume` `/trigger`、`/runs` 历史。

**标叔的结论**：定时任务的「工程克制」值得学——先管理面、后自然语言；先 `once`/`cron`、后 `interval`；默认关、显式开。每一刀都为了「第一个 PR 能被审、能被安全运维」。你做功能，也该这么切。

上下文会膨胀。下一章讲怎么管。

---

## §16 上下文工程

代理跑久了，上下文会爆。DeerFlow 在「上下文工程」上做了三件事：自动压缩、手动压缩、事件历史兜底。

### 自动压缩：SummarizationMiddleware

LangGraph 的 `SummarizationMiddleware` 会在消息超长时，把旧消息原地替换成一段摘要（前缀 `Here is a summary of the conversation to date:`）。这是 token 预算的刚需。

代价前面说过：checkpointer 里的原话没了。所以 DeerFlow 用 **event store 兜底**（§08）——原始消息在 event store 里一动没动，`/history` 改读 event store，前端还能插压缩标记卡片（§14）。

### 手动压缩：Manual Context Compaction

除了自动，你也能主动触发压缩，在长任务中段把上下文「瘦身」一次，控制成本和时延。

### Session Goals

给会话设目标，本质是给代理一个「这次要收敛到哪」的锚。目标明确，代理少跑弯路，上下文少走偏。

### 一个真实踩坑的启示

DeerFlow 自己修过一个有意思的 bug：summarize 之后，前端 feedback（点赞）的 `run_id` 映射会错位——因为 `/history`（checkpoint）和 `/messages`（event store）两条数据链的 AI 消息数量不一致。修法是让 `/history` 也读 event store，**两边对齐**，顺手把点赞打错 run 的隐藏 bug 也修了。

**标叔的结论**：上下文工程的本质是「在「记得住」和「装得下」之间找平衡。DeerFlow 的答案是——自动压缩管当下，event store 管真相，手动压缩管成本。三层一起用，长任务才稳。

东西写完了，得上线、要能看。下一章讲可观测与部署。

---

## §17 可观测与生产部署

### 可观测：LangSmith + Langfuse 双轨

DeerFlow 的追踪配置从「只支持 LangSmith」扩展成了**多 provider**。加了一个 tracing callback 工厂，按环境变量决定挂 0 个、1 个还是 2 个回调。

关键行为：**如果某个 provider 被显式启用但配置错了，模型创建阶段就直接报错**，明确点名是哪个 provider。不会「静默没追踪」让你以为正常。

### 部署：Docker 一条龙

生产部署就是前面 §02 的 `make up` / `make down`，访问 `http://localhost:2026`。

部署规模照这张表配（再贴一次，因为重要）：

| 目标 | 起步 | 推荐 |
|------|------|------|
| 长驻服务 `make up` | 8C / 16G / 40G | 16C / 32G |

### 数据库与配置

`config.yaml` 里 `database.backend` 设 `sqlite` 或 `postgres`。它**同时供 LangGraph checkpointer/store 和应用数据使用**——一套库，别分开建。

排障用 `make doctor` 和 `make support-bundle`（生成隐私安全的打包信息给社区求助）。

**标叔的结论**：DeerFlow 的「可观测」默认就接好了 LangSmith/Langfuse，你上生产前先把追踪 key 配上，不然出了问题只能盲调。数据库用 postgres 起，别拿 sqlite 扛并发——checkpointer 和 app 数据抢同一库，sqlite 会先跪。

选型是读者最关心的。下一章横向比。

---

## §18 选型对比

市面上代理框架不少。我用事实（不是情怀）横向比一下 DeerFlow 2.0 和另外两个常被拿来比的。

### DeerFlow vs deepagents

| 维度 | deepagents | DeerFlow 2.0 |
|------|------|------|
| 形态 | 轻量 Python 库 | 产品级服务栈 |
| 编排内核 | 各家（本书另一本讲过） | LangGraph |
| 界面 | 无，你自己接 | Web UI + TUI + IM |
| 定时任务 | 无 | 内置 MVP |
| 生成技能 | 无 | 图/视频/播客/音乐 |
| 护栏 | 看实现 | 内置 Guardrail + 读写门 |
| 模型 | 看库 | 模型中立，多家通吃 |

**标叔的结论**：deepagents 适合「我要在代码里嵌代理」；DeerFlow 适合「我要一个能直接给团队用的代理工作台」。需求决定选型，不是谁更先进。

### DeerFlow vs Claude Agent SDK

| 维度 | Claude Agent SDK | DeerFlow 2.0 |
|------|------|------|
| 模型绑定 | 偏 Claude 生态 | 模型中立 |
| 多租户 | 需自建 | 内建 user 隔离 + owner 作用域 |
| 调度 | 无 | 内置定时任务 |
| 终端 | 有 CLI | 有 TUI（共享持久层） |
| 上层服务 | 偏库/SDK | 完整服务栈 |

**标叔的结论**：如果你团队已经深度用 Claude、只要 SDK 接进去，Claude Agent SDK 顺。如果你要「模型随便换 + 多用户 + 调度 + 界面」一把梭，DeerFlow 更省事。

### 一句话总判断

DeerFlow 2.0 的定位是：**在「纯库」和「纯SaaS」之间，给你一个能自托管、能改、能扩的开源超级代理产品**。它重，但重得有道理。

最后一章，把文档里那些真实的坑，集中交给你。

---

## §19 避坑指南

这些坑不是我编的，来自 DeerFlow 自己的设计文档和代码改动记录。每一条都附正确姿势。

### 坑 1：同名 public/custom 技能互相串

**现象**：开 public 技能时，同名的 custom 技能也被开；配置键只用了 `skill_name`，两类技能分不清。

**正确姿势**：配置用组合键 `{category}:{name}`，如 `public:my-skill` 和 `custom:my-skill` 分开。同名时 API 补 `?category=`。

```json
{ "skills": { "public:my-skill": { "enabled": true }, "custom:my-skill": { "enabled": false } } }
```

### 坑 2：TUI 建的会话 Web 看不见

**现象**：终端跑的会话，开 Web 侧边栏不显示。

**根因**：早期 `DeerFlowClient` 只写 checkpointer，不写 `thread_meta`，而 Web 从 `thread_meta` 读列表。

**正确姿势**：用 2.0 的新版——TUI 复用同一 `thread_meta` 持久层，终端会话自动进 Web。老版本请升级，别自己补同步逻辑。

### 坑 3：改文件前没读，被读写门拦

**现象**：代理想改已存在文件，返回「请先读该文件」，写入失败。

**根因**：`ReadBeforeWriteMiddleware` 默认开，要求改前 read-mark 的 hash 和当前文件一致。

**正确姿势**：让代理先 `read_file` 再 `write_file` / `str_replace`。这是护栏不是 bug——它治的是「只追加不回读」导致的重复产物。别为了省事关掉它。

### 坑 4：护栏里客户端伪造身份

**现象**：有人试图在请求体里塞 `user_id=admin` 提权。

**正确姿势**：DeerFlow 注入**只信服务端认证态** `request.state.user`，客户端 body 里的身份字段不覆盖。你写自己的 provider，也别读客户端传的 user 字段——读 `runtime.context` 里 Gateway 注入的那个。

### 坑 5：定时任务租约和重叠

**现象**：多实例部署时任务重复跑；或上一个 run 没结束又触发。

**正确姿势**：调度器靠 **DB 租约**原子认领，强制 `enabled: true` 才跑；重叠按 `skip`、错过按 `run_once`。部署多实例时，别自己加 leader 开关——DB 租约就是护栏。注意 `min_interval_seconds` 默认 60，短于它的用户任务会被拒。

### 坑 6：生成 provider 被自动切走

**现象**：半夜生成突然走了不同的供应商，产物风格变了。

**根因**：`_resolve_provider()` 自动判断，两套密钥都在时按「现有 provider 优先」，但你若只配了覆盖变量又改了名，行为会偏。

**正确姿势**：想锁定，显式设 `IMAGE_GENERATION_PROVIDER=gemini` 这类环境变量，覆盖自动判断。别依赖「自动」做生产决策。

### 坑 7：历史被压缩后 feedback 错位

**现象**：给历史消息点赞，赞到了错误的 run。

**根因**：`/history`（checkpoint）和 `/messages`（event store）两条数据链 AI 消息数不一致。

**正确姿势**：2.0 已让 `/history` 改读 event store，两边对齐，顺手修好。确保你用的是新版本；老版本别在压缩后的长对话里依赖点赞归属。

**标叔的结论**：这七个坑，本质都指向 DeerFlow 的设计哲学——**默认安全、显式优先、持久层单一真相**。你顺着这三条走，坑基本都绕得开。

---

## 写在最后

DeerFlow 2.0 不是一个「又一个小代理库」。它是字节把内部研究代理产品化后，开源出来的**完整工作台**：底层 LangGraph 编排，上层 Gateway/Frontend/TUI/Provisioner 服务栈，中间用 Skills 做扩展、用护栏做安全、用 event store 做不可篡改的历史。

你如果只想嵌个代理，它重；你想给团队一个「能搜、能写、能生成、能定时、能审计」的代理平台，它刚好。

书到这里。下一步建议：把 §02 跑起来，照 §07 写一个自己的 Skill，再用 §12 加一道你业务的护栏。动起手，比读十遍都管用。

> 本文所有事实均来自 DeerFlow 官方仓库（README、CLAUDE.md 摘要、规格与代码改动文档）。2.0 为重写版本，v1 经验不照搬。
