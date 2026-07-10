# DeepAgents 从入门到精通

## 用 LangChain 的"智能体工具套件"构建能规划、会委派、记得住的 AI 代理

**创建者**: 标叔
**为谁创建**: 想用 DeepAgents 构建 AI 代理的 Python 开发者（懂点 LangChain 更好，不懂也能读）
**基于**: DeepAgents（LangChain 团队的 `deepagents` Python 库）
**最后更新**: 2026-07-07
**适用场景**: 从零认识 DeepAgents，到能独立写出可生产的深度代理应用

***

## 阅读指南

这本书分三部分。

第一部分带你跑通第一个 Agent。别跳。
第二部分拆开 DeepAgents 的内置机制。这是骨架。
第三部分给实战、CLI 工具和上线要点。这是血肉。

我的写法很直接：先说结论，再给证据，最后上代码。
短句为主。能断言就不含糊。

> **核心建议**：第一次读，先照第二部分把例子跑起来。等你有体感了，再回来看机制。

***

## 目录

**Part 1 起步**

- [§01 DeepAgents 是套在 LangChain 上的工具套件](#§01-deepagents-是套在-langchain-上的工具套件)
- [§02 五分钟跑通你的第一个 Agent](#§02-五分钟跑通你的第一个-agent)
- [§03 一次调用背后，框架帮你干了四件事](#§03-一次调用背后框架帮你干了四件事)
- [§04 模型随便换，是 DeepAgents 的底层优势](#§04-模型随便换是-deepagents-的底层优势)

**Part 2 核心能力**

- [§05 五大内置能力，你写代码前就已经在了](#§05-五大内置能力你写代码前就已经在了)
- [§06 中间件是 DeepAgents 的灵魂](#§06-中间件是-deepagents-的灵魂)
- [§07 后端系统决定数据存在哪](#§07-后端系统决定数据存在哪)
- [§08 子代理：把脏活分给干净上下文](#§08-子代理把脏活分给干净上下文)
- [§09 Skills：随用随取的技能包](#§09-skills随用随取的技能包)
- [§10 长期记忆：AGENTS.md 让代理记得住](#§10-长期记忆agentsmd-让代理记得住)
- [§11 流式输出：看清代理在干嘛](#§11-流式输出看清代理在干嘛)
- [§12 人机协同：关键操作必须你点头](#§12-人机协同关键操作必须你点头)
- [§13 权限与沙箱：给代理划好边界](#§13-权限与沙箱给代理划好边界)

**Part 3 实战与进阶**

- [§14 实战：搭一个会写报告的研究助手](#§14-实战搭一个会写报告的研究助手)
- [§15 Deep Agents Code：开箱即用的终端编程代理](#§15-deep-agents-code开箱即用的终端编程代理)
- [§16 上下文工程：别让窗口爆掉](#§16-上下文工程别让窗口爆掉)
- [§17 生产部署：多租户、安全与扩展](#§17-生产部署多租户安全与扩展)
- [§18 和 Claude Agent SDK 怎么选](#§18-和-claude-agent-sdk-怎么选)
- [§19 避坑指南：从一个真实重构说起](#§19-避坑指南从一个真实重构说起)

***

# Part 1: 起步

从零到一。读完这part，你能跑通第一个 Agent，并看懂它背后发生了什么。

## §01 DeepAgents 是套在 LangChain 上的工具套件

先给结论：DeepAgents 不是新框架，是 LangChain 之上的"有主见的默认配置"。

2025 年底，我第一次读它的源码。一句话记住它：**它是一个 agent harness（智能体工具套件）**。

什么意思？看这三层关系。

```
LangChain  → 基础构件（model、tool、prompt）
LangGraph  → 运行时（持久化、流式、中断、状态图）
DeepAgents → 工具套件（规划、文件系统、子代理、记忆）
```

LangChain 给你积木。LangGraph 给你跑积木的跑道。
DeepAgents 直接把积木拼好，还配好了说明书。

你看，它不替代 LangGraph。它站在 LangGraph 肩膀上。
核心函数只有一个：`create_deep_agent()`。
它返回一个编译好的 LangGraph 状态图（`CompiledStateGraph`）。

> **标叔的经验**：我踩过最大的坑，是把 DeepAgents 当普通 LangGraph wrapper 用。结果 HITL 失效、子代理不注册、Skills 用不上。后面 §19 我会细讲。先记住：用框架，就按框架的设计意图用。

为什么需要它？因为成功的"深度 Agent"都有四个共同点：
规划工具、子代理、文件系统、精细提示词。

Claude Code 有。Deep Research 有。Manus 也有。
DeepAgents 把这套模式，做成开箱即用的默认能力。

所以你写几行代码，就拥有别人要自己搭很久的东西。

**标叔的结论**：如果你要做多步骤、长任务、要记忆的 Agent，DeepAgents 值得一试。简单的一次性调用，它反而重了。

> **注意**：DeepAgents 需要支持 tool calling 的模型。纯文本模型跑不了。

下一章，我带你 5 分钟跑通第一个 Agent。

## §02 五分钟跑通你的第一个 Agent

先给结论：装一个包，写十行代码，你的第一个深度代理就活了。

我用一个天气助手做例子。够简单，一眼看懂。

### 第一步：安装

```bash
pip install deepagents tavily-python
# 或用 uv
uv add deepagents tavily-python
```

`tavily-python` 是搜索工具，第三章实战会用到。先不装也行。

### 第二步：设 API Key

```bash
export ANTHROPIC_API_KEY="你的key"
# 用 OpenAI 就设 OPENAI_API_KEY
```

### 第三步：写第一个 Agent

```python
from deepagents import create_deep_agent

def get_weather(city: str) -> str:
    """查询某个城市的天气。"""
    return f"{city} 永远是晴天！"   # 这里是假数据

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",  # provider:model 格式
    tools=[get_weather],                  # 挂上你的工具
    system_prompt="你是个乐于助人的助手",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "旧金山天气怎么样？"}]}
)
print(result["messages"][-1].content)
```

跑一下。它会输出："旧金山永远是晴天！"

就这？就这。

你没写任何规划逻辑。没写文件系统。没写上下文管理。
但这些能力，已经在那儿了。只是这个例子用不上。

> **标叔的经验**：我第一次跑通时，愣了一下。十行代码，连 `write_todos` 都不用调，就有了一个能扩展的 Agent 底座。这种"默认即强大"的感觉，是 DeepAgents 最值钱的地方。

### model 怎么写

注意 `model="anthropic:claude-sonnet-4-6"` 这个写法。
`provider:model`，冒号分隔。这是 DeepAgents 的约定。

它支持一大票模型：

```python
model="anthropic:claude-sonnet-4-6"   # Anthropic
model="openai:gpt-5.4"                 # OpenAI
model="google_genai:gemini-3.1-pro-preview"  # Google
model="ollama:devstral-2"              # 本地 Ollama
model="deepseek:deepseek-v4-flash"     # DeepSeek
```

换模型，只改这一行。不用动其他代码。

**标叔的结论**：能用字符串写模型，就别手动 `ChatOpenAI(...)`。让框架替你初始化。后面 §19 会讲为什么。

下一章，我们看一次调用背后，框架到底帮你做了什么。

## §03 一次调用背后，框架帮你干了四件事

先给结论：你只调了一次 `invoke()`，框架在背后跑了规划、搜索、存文件、委派、压缩。

2026 年初，我用 DeepAgents 搭了个研究助手。
我让它"研究 2025 年的 agentic 框架，写份报告"。
我以为就一句 LLM 调用。结果它干了五件事。

它自动做了这些：

1. 调 `write_todos` 把任务拆成步骤。
2. 调 `internet_search` 搜资料。
3. 把大段搜索结果存进虚拟文件系统。
4. 必要时 spawn 子代理处理分支。
5. 回读文件，综合成报告。

全程我没写一行调度代码。

> **标叔的经验**：最让我意外的是第 3 步。一次搜索返回几千字，直接塞进上下文会爆窗。DeepAgents 自动把大结果"驱逐"到文件系统，只在上下文留个指针。这是我手动写 LangGraph 时最头疼的事——它默认就处理了。

这背后是五个内置能力的配合：

| 能力       | 内置工具                                                    | 作用                   |
| -------- | ------------------------------------------------------- | -------------------- |
| 规划       | `write_todos`                                           | 任务分解，状态存 agent state |
| 文件系统     | `read_file` `write_file` `edit_file` `ls` `glob` `grep` | 大结果自动 offload        |
| Shell 执行 | `execute`                                               | 仅在沙箱后端可用             |
| 子代理      | `task`                                                  | 上下文隔离的任务委派           |
| 上下文压缩    | `compact_conversation`                                  | 窗口到 85% 自动摘要         |

**标叔的结论**：你写的是"做什么"，框架管的是"怎么做"。这正是 harness 的价值。

> **注意**：`execute`（跑 shell）默认不可用。它只在沙箱后端开启。别在本地直接指望它。详见 §13。

下一章，我把"模型随便换"这件事讲透。

## §04 模型随便换，是 DeepAgents 的底层优势

先给结论：DeepAgents 是模型中立的。Anthropic、OpenAI、Google、DeepSeek、本地 Ollama，通吃。

这点和 Claude Agent SDK 形成直接对比。
Claude Agent SDK 绑死在 Anthropic 模型上。
DeepAgents 不挑。你用谁家的模型都行。

写法统一成 `provider:model`：

```python
agent = create_deep_agent(
    model="openai:gpt-5.4",   # 想换就换
    tools=[get_weather],
)
```

我做过一个实验。同一个研究助手，下午用 Claude，晚上换 GPT。
代码一行没改，只动了 model 字符串。
报告质量有差异，但工程层完全不用动。

> **标叔的经验**：这种"模型可插拔"在生产里太重要了。供应商涨价、某个模型抽风，你当天就能切。绑死一家，迁移成本以周计。

如果你要传额外参数（temperature、thinking 开关），可以手动初始化模型：

```python
from langchain.chat_models import init_chat_model

llm = init_chat_model(model="openai:gpt-5.4", temperature=0.2)
agent = create_deep_agent(model=llm, tools=[get_weather])
```

但注意！别把 `callbacks` 挂模型上。
那会和 DeepAgents 的中间件打架。日志要用中间件写，见 §06。

**标叔的结论**：能用字符串，就别手动实例化。要额外参数，才手动建。手动建就别挂 callback。

> **注意**：模型必须支持 tool calling。纯补全模型（不带工具调用）跑不了 Agent。

到这里，起步 part 结束。下一 part，我们拆骨架。

***

# Part 2: 核心能力

这 part 是 DeepAgents 的骨架。读懂它，你才算是真会用。

## §05 五大内置能力，你写代码前就已经在了

先给结论：规划、文件系统、Shell、子代理、压缩，是出厂自带。不写代码就有。

我刚用时有个错觉：这些是"可选功能"。
错了。它们是默认中间件塞进来的。你不用，它们在；你用，它们更强。

### 规划（write\_todos）

Agent 自己把大任务拆成小步骤。
状态：`pending` → `in_progress` → `completed`。
存在 agent state 里，跨轮次不丢。

### 文件系统（6 个工具）

```text
ls          列出目录
read_file   读文件（带行号，支持分页）
write_file  写文件（冲突即报错，不覆盖）
edit_file   精确字符串替换
glob        模式匹配找文件
grep        搜文件内容
```

关键能力：**大结果自动驱逐**。
超过 20k token 的工具结果，会被写到文件系统，上下文只留 `read_file` 指针。

### Shell 执行（execute）

跑 shell 命令。默认 120 秒超时。
但只有沙箱后端才开。本地默认没有。

### 子代理（task）

把子任务派给一个"干净上下文"的新 Agent。
主 Agent 的上下文不被污染。详见 §08。

### 上下文压缩（compact\_conversation）

上下文用到 85%，自动摘要老消息。
让长任务不爆窗。详见 §16。

**标叔的结论**：这五个能力，单独看都不稀奇。稀奇的是它们默认协同、默认开箱。你省下的，是搭脚手架的时间。

> **标叔的经验**：我手动搭 LangGraph 时，光"大结果 offload"和"上下文压缩"就写了两百行。DeepAgents 默认就有了。这二百行，我永远不想再写。

下一章，讲这五个能力背后的真正灵魂：中间件。

## §06 中间件是 DeepAgents 的灵魂

先给结论：中间件拦截每一次 LLM 请求。它能改提示词、筛工具、跨轮追踪、注入上下文。

普通工具是"被调用的函数"。中间件是"包裹整个流程的层"。
这是两回事。

我用一个类比级联说清：

- 工具 = 员工的双手，干具体活。
- 中间件 = 主管，在员工动手前定规矩、动手后做检查。

### 默认中间件栈（从底层到高层）

```text
FilesystemMiddleware     文件工具 + 大结果驱逐(>20k token)
SubAgentMiddleware       task 工具 + 子代理管理
SummarizationMiddleware  上下文压缩(85% 阈值触发)
MemoryMiddleware         AGENTS.md 注入(每轮)
SkillsMiddleware         SKILL.md 渐进式披露
TodoListMiddleware       任务追踪
AnthropicPromptCachingMiddleware  省 token
PatchToolCallsMiddleware 修中断的工具调用
```

设了 `interrupt_on`，还会加 `HumanInTheLoopMiddleware`。

### 自己写一个中间件

日志需求，别用 callback。用 `@wrap_tool_call`：

```python
from langchain.agents.middleware import wrap_tool_call

@wrap_tool_call
def log_tool_calls(request, handler):
    print(f"调用工具: {request.name}")   # 动手前
    result = handler(request)            # 真正执行
    return result                        # 动手后

agent = create_deep_agent(model="...", middleware=[log_tool_calls])
```

每个中间件能挂四个钩子：

```text
before_agent   整体预处理
before_model   LLM 调用前
after_model    LLM 调用后
after_agent    整体后处理
```

**标叔的结论**：要改提示词、跨轮追踪、动态注入——用中间件。无状态、自包含的函数——用普通工具。这个分水岭要清楚。

> **注意**：别把日志挂模型 `callbacks` 上。会和默认中间件冲突。这是 §19 里一个真实踩坑。

下一章，讲数据存在哪：后端系统。

## §07 后端系统决定数据存在哪

先给结论：所有文件操作都走 `BackendProtocol` 抽象层。换后端，不换业务代码。

我第一次没搞懂后端，直接上了 `FilesystemBackend` + `CompositeBackend`。
结果 `.agent_data/` 目录不透明、不持久、gitignore 忽略。
其实我那个场景，用默认的 `StateBackend` 就够了。

### 后端全家福

| 后端                  | 范围            | execute | 适合                               |
| ------------------- | ------------- | ------- | -------------------------------- |
| `StateBackend`      | 线程作用域         | 否       | 默认；中间结果草稿纸                       |
| `FilesystemBackend` | 本地磁盘          | 否       | 本地开发、CI                          |
| `StoreBackend`      | 跨线程           | 否       | 长期记忆、多会话                         |
| `ContextHubBackend` | LangSmith Hub | 否       | 不要单独 store 的持久化                  |
| `LocalShellBackend` | 本地+Shell      | 是       | 本地开发带命令行                         |
| 沙箱后端                | 隔离环境          | 是       | Modal/Daytona/Runloop/LangSmith  |
| `CompositeBackend`  | 按路径前缀路由       | 按路由     | 混合：默认 State + /memories/ 用 Store |

### 最常用的 CompositeBackend

```python
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.store.memory import InMemoryStore

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    backend=CompositeBackend(
        default=StateBackend(),                      # 默认走内存
        routes={"/memories/": StoreBackend(...)},    # /memories/ 走持久
    ),
    store=InMemoryStore(),
)
```

一句话理解：默认存内存，特定路径存长久。

**标叔的结论**：开发用 `StateBackend` 或 `FilesystemBackend`。生产用 `CompositeBackend`（内存 + Store 持久）。代码执行才上沙箱。别像我一样过度设计。

> **标叔的经验**：StateBackend 把数据存在 LangGraph state 里，线程隔离，无外部依赖。对纯内存场景，它是首选。我后来把那个项目从 FilesystemBackend 退回 StateBackend，清爽很多。

下一章，讲子代理——DeepAgents 最被低估的能力。

## §08 子代理：把脏活分给干净上下文

先给结论：子代理是"上下文隔离的任务委派"。主 Agent 不被子任务的细节淹没。

我做长研究时吃过亏。所有中间步骤塞进一个上下文，读到后面，前面的重点全被挤掉。
子代理的解法很妙：主 Agent 把活派给一个**全新、干净上下文**的 Agent。
子代理干完，只回一个总结给主 Agent。

### 最简单的字典定义

```python
research_subagent = {
    "name": "researcher",          # 必需：唯一标识
    "description": "深度搜索网络信息",  # 必需：触发条件
    "system_prompt": "你是搜索大师",  # 必需：不继承主代理
    "tools": [internet_search],    # 可选：写了就全覆盖
    "model": "openai:gpt-5.4",     # 可选：换模型
}
```

三个字段是必需的：`name`、`description`、`system_prompt`。
`description` 要写**触发条件**，不是功能介绍。这很关键。

> **标叔的经验**：我见过一个真实 bug：`description` 写得太模糊，主 Agent 不知道何时委派，子代理从没被调用。把描述改成"用户要生成任何图片时调用"，委派准确率立刻上来了。

### 多专家协作

```python
subagents = [
    {"name": "data-collector", "description": "收集原始数据",
     "system_prompt": "全面收集数据", "tools": [web_search]},
    {"name": "data-analyzer", "description": "分析数据",
     "system_prompt": "提取洞察", "tools": [statistical_analysis]},
    {"name": "report-writer", "description": "撰写报告",
     "system_prompt": "写专业报告", "tools": [format_document]},
]
agent = create_deep_agent(system_prompt="你协调多专家", subagents=subagents)
```

### 其他两种形态

- `CompiledSubAgent`：传预编译的 LangGraph 图，要完全控制拓扑时用。
- `AsyncSubAgent`：后台长任务，`start`/`check`/`update`/`cancel` 管理。

默认会有一个 `general-purpose` 子代理。你不定义也会自动加。
想关掉：`GeneralPurposeSubagentProfile(enabled=False)`。

**标叔的结论**：子代理的核心价值是"上下文隔离"。复杂任务不拆，上下文迟早爆。拆，就干净。

> **注意**：子代理不继承父代理的工具（除非不写 `tools`）。不继承 middleware、skills。要用的，显式传。详见 §19 配置规范。

下一章，讲随用随取的技能包：Skills。

## §09 Skills：随用随取的技能包

先给结论：Skill 是带 `SKILL.md` 的目录。用到才加载全文，平时只占元数据。这叫渐进式披露。

传统做法是把所有提示词塞进 system prompt。
我见过一个 `IMAGE_GENERATOR_PROMPT`，是包含所有规则的巨型字符串。
每次对话都消耗大量 token。浪费。

DeepAgents 的 Skills 不这么干。

### 三步机制

1. **匹配**：看 skill 的 name + description 是否对上任务。
2. **加载**：用 `read_file` 读完整 `SKILL.md`。
3. **执行**：按指令调工具或脚本。

平时只加载 frontmatter（name + description）。
相关时才读全文。省 token，也省上下文。

### SKILL.md 长这样

```markdown
---
name: location-detector
description: 获取用户所在城市。需要基于位置的服务时调用。
---

# 位置检测器
## 使用方法
python scripts/location_detector.py
## 响应格式
当前位置：{城市名}
```

### 目录结构

```text
skills/
└── my-skill/
    ├── SKILL.md          # 必需
    ├── scripts/          # 可选：脚本
    ├── references/       # 可选：模板/文档
    └── assets/           # 可选：输出资源
```

### 挂到 Agent 上

```python
agent = create_deep_agent(
    model="...",
    skills=["/skills/"],          # 指向含 SKILL.md 的目录
    backend=StateBackend(),
    checkpointer=MemorySaver(),
)
```

> **标叔的经验**：我把一个电商图片生成的硬规则，从巨型 prompt 迁到 `SKILL.md`。每次对话 token 消耗降了一大截。而且 rules 改了只动一个文件，不再翻巨型字符串。这就是渐进式披露的好处。

**标叔的结论**：长提示词、领域知识、固定流程——都该做成 Skill。别堆在 system prompt 里。

> **注意**：Skill 的 `description` 决定它何时被触发。写清楚"何时用"，比写"它能干啥"更重要。

下一章，讲让代理记得住的长期记忆。

## §10 长期记忆：AGENTS.md 让代理记得住

先给结论：用 `AGENTS.md` 文件存"持久偏好"。它每轮都加载——和 Skills 的渐进式披露不同。

我一开始把 AGENTS.md 和 Skills 搞混了。
区别一句话：Skills 用到才加载，AGENTS.md 每轮都加载。

AGENTS.md 该放什么？放"身份、约定、偏好"这种恒定信息。

```python
agent = create_deep_agent(
    model="...",
    memory=["/AGENTS.md"],    # 每轮加载
    checkpointer=MemorySaver(),
)
```

### 它和 Skills 的关键差别

| 维度     | AGENTS.md (memory) | SKILL.md (skills) |
| ------ | ------------------ | ----------------- |
| 加载时机   | 每轮都加载              | 用到才加载             |
| 适合内容   | 身份、偏好、约定           | 领域知识、流程           |
| 是否可被忽略 | 否                  | 模型自行判断是否触发        |

### 两种后端的播种方式

```python
# StateBackend：用 files 参数播种
agent = create_deep_agent(
    model="...",
    memory=["/AGENTS.md"],
    backend=StateBackend(),
)

# StoreBackend：用 store.put() 预填
store.put(("namespace",), key="AGENTS.md", value=content)
```

> **标叔的经验**：我曾把"运行时指令"塞进 AGENTS.md，比如"严格保留原图外观"。结果每轮都占上下文，还很怪。运行时指令该放 Skill 或 system\_prompt。AGENTS.md 只放真正持久的东西。

**标叔的结论**：AGENTS.md 是代理的"性格与习惯"。少而精，别当垃圾桶。

> **注意**：AGENTS.md 每轮加载。内容越长，每轮越费 token。只放恒定信息。

下一章，讲怎么看清代理在干嘛：流式输出。

## §11 流式输出：看清代理在干嘛

先给结论：DeepAgents 内建流式。三种模式，对应三种观察粒度。

我第一次跑长任务，终端一片静默。十几秒没输出，我以为它挂了。
后来开了流式，才看到它在一步步调工具、写文件。安心多了。

### 三种模式

| 模式         | 粒度      | 适合     |
| ---------- | ------- | ------ |
| `updates`  | 节点级进度   | 宏观进度追踪 |
| `messages` | token 级 | 聊天式打字机 |
| `custom`   | 自定义事件   | 进度百分比等 |

### updates 模式：看节点

```python
for event in agent.stream(
    {"messages": [{"role": "user", "content": "你好"}]},
    config={"configurable": {"thread_id": "123"}},
    stream_mode="updates",
    subgraphs=True,        # 看子代理
    version="v2",
):
    print(event)
```

### messages 模式：打字机

```python
for chunk in agent.stream(input, stream_mode="messages",
                           subgraphs=True, version="v2"):
    if chunk["type"] == "messages":
        token, _ = chunk["data"]
        if token.type == "tool":          # 工具结果
            print(f"\n工具结果: {str(token.content)[:150]}")
        elif token.type == "ai" and token.content:  # 文本
            print(token.content, end="", flush=True)
```

### v2 格式与命名空间

新版本用 `version="v2"`。每个 chunk 带 `ns`（命名空间）：

```text
()                        → 主 Agent
("tools:abc123",)         → task 创建的子 Agent
("tools:abc123", "...")   → 子 Agent 内部节点
```

这样你能分清：这段输出，是主代理还是子代理说的。

**标叔的结论**：做 UI 用 `messages`，做后台监控用 `updates`，做进度条用 `custom`。按需选。

> **注意**：看子代理细节，必须 `subgraphs=True`（旧版 `stream_subgraphs=True`）且 `version="v2"`。漏了就只见主代理。

下一章，讲最该认真对待的能力：人机协同。

## §12 人机协同：关键操作必须你点头

先给结论：敏感工具执行前，可以让代理停下来等人类批准。这叫 Human-in-the-Loop（HITL）。

删除文件、发邮件、部署代码——这些不能让 Agent 自作主张。
DeepAgents 用 `interrupt_on` 配置哪些工具要人确认。

### 配置中断

```python
from langgraph.checkpoint.memory import MemorySaver

agent = create_deep_agent(
    tools=[delete_file, send_email],
    interrupt_on={
        "delete_file": True,   # 全部决策都允许
        "send_email": {"allowed_decisions": ["approve", "reject"]},
    },
    checkpointer=MemorySaver(),   # 必须！否则恢复不了
)
```

### 中断与恢复（v2 格式）

```python
result = agent.invoke(
    {"messages": [{"role": "user", "content": "删掉 temp.txt"}]},
    config=config, version="v2",
)

if result.interrupts:                    # v2：属性访问
    action = result.interrupts[0].value["action_requests"][0]
    print(f"要执行: {action['name']}, 参数: {action['args']}")

    decisions = [{"type": "approve"}]    # approve/edit/reject
    result = agent.invoke(
        Command(resume={"decisions": decisions}),  # 恢复执行
        config=config, version="v2",
    )
```

四种决策：`approve`（批准）、`edit`（改参数再执行）、`reject`（拒绝）、`respond`（回复）。

### 风险分级建议

| 风险 | 工具       | 允许决策                   |
| -- | -------- | ---------------------- |
| 高  | 删除/发送/部署 | approve、edit、reject    |
| 中  | 写文件/改配置  | approve、reject（禁 edit） |
| 低  | 读/列      | 不打断                    |

> **标叔的经验**：我见过的真实 bug：在父 Agent 层面对 `generate_image` 设中断。但那是子代理的工具，父 Agent 的中断传不到它。正确做法是去子代理自己的 `interrupt_on` 里设。这个坑后面 §19 会展开。

**标叔的结论**：敏感操作，宁可多问一次。HITL 配置错，比不配置更危险——因为它给你"已保护"的错觉。

> **注意**：HITL 必须配 `checkpointer`。中断恢复靠它。没有 checkpointer，流程断不了也续不上。

下一章，讲给代理划边界：权限与沙箱。

## §13 权限与沙箱：给代理划好边界

先给结论：用 `FilesystemPermission` 声明"能读哪、能写哪"。用沙箱隔离代码执行。边界在工具层强制。

DeepAgents 的安全哲学很明确：**信任 LLM，但在工具/沙箱层强制边界**。
靠"请你别删重要文件"这种提示词设防，没用。

### 文件权限

```python
from deepagents import create_deep_agent, FilesystemPermission

agent = create_deep_agent(
    model="...",
    permissions=[
        FilesystemPermission(operations=["write"], paths=["/policies/**"], mode="deny"),
        FilesystemPermission(operations=["read", "write"], paths=["/workspace/**"], mode="allow"),
    ],
)
```

规则是**首匹配生效**。没匹配上的，默认允许。
模式：`allow` 放行，`deny` 拒绝。操作：`read` / `write`。

### 沙箱：代码执行的隔离舱

`execute` 跑 shell，只在沙箱后端开。
沙箱把代码执行关进隔离环境，不碰你本机。

支持的后端：Daytona、Modal、Runloop、LangSmith、AgentCore。

```python
agent = create_deep_agent(
    model="...",
    backend=LocalShellBackend(root_dir="./workspace", virtual_mode=True),
)
```

`virtual_mode=True` 限制路径，本地开发更安全。

> **标叔的经验**：一个真实项目把 `generate_image` 工具内部写成轮询 180 秒。结果 Agent 被冻住 180 秒，啥也干不了。长任务别在工具里轮询。要么直接 `await`，要么用 AsyncSubAgent。详见 §19。

**标叔的结论**：安全不是一句"请注意"。是声明式规则 + 隔离执行环境。两层都要有。

> **注意**：`permissions` 对沙箱后端不生效。沙箱要用后端自己的策略钩子（如 `PolicyWrapper`）来限制。

Part 2 结束。下一 part 进实战。

***

# Part 3: 实战与进阶

从"能用"到"用好"。这 part 给实战、CLI、上线和选型。

## §14 实战：搭一个会写报告的研究助手

先给结论：把前 13 章串起来，你就能搭一个"搜索→存储→委派→出报告"的研究助手。

我用"研究 2026年 agentic 框架"做例子。这是 DeepAgents 最经典的用法。

### 完整代码

```python
import os
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.store.memory import InMemoryStore

tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def internet_search(query: str, max_results: int = 5) -> dict:
    """运行网络搜索。"""
    return tavily.search(query, max_results=max_results)

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[internet_search],
    subagents=[
        {"name": "data-collector", "description": "收集数据",
         "system_prompt": "全面收集数据", "tools": [internet_search]},
        {"name": "report-writer", "description": "撰写报告",
         "system_prompt": "写专业报告", "tools": []},
    ],
    store=InMemoryStore(),
    backend=CompositeBackend(
        default=StateBackend(),
        routes={"/memories/": StoreBackend(namespace=lambda rt: (rt.server_info.user.identity,))},
    ),
    system_prompt="""你是研究助手。把进度存到 /memories/research/:
- sources.txt   来源列表
- notes.txt     关键发现
- report.md     报告草稿""",
)
```

### 四大机制如何配合

| 能力    | 实现    | 组件                                   |
| ----- | ----- | ------------------------------------ |
| 任务规划  | 自动拆任务 | `write_todos` + `TodoListMiddleware` |
| 上下文管理 | 大结果卸载 | 文件系统 + 自动驱逐(>20k)                    |
| 专业化   | 上下文隔离 | `task` + 子代理                         |
| 持久记忆  | 混合存储  | `CompositeBackend` + `StoreBackend`  |

### 跑它

```python
result = agent.invoke(
    {"messages": [{"role": "user",
     "content": "研究 2026 年的 agentic 框架，写份报告"}]},
    config={"configurable": {"thread_id": "research-001"}},
)
print(result["messages"][-1].content)
```

> **标叔的经验**：第一次跑这种多子代理流程，我盯着流式输出看。主 Agent 规划完，把"收集"派给 data-collector，把"写"派给 report-writer。主上下文始终干净。那一刻我真正懂了 §08 说的"隔离"是什么感觉。

**标叔的结论**：研究助手是 DeepAgents 的"hello world 进阶版"。吃透它，你就吃透了框架。

下一章，介绍开箱即用的终端编程代理：dcode。

## §15 Deep Agents Code：开箱即用的终端编程代理

先给结论：`dcode` 是官方用 Deep Agents SDK 做的终端编程 Agent。装好就能用，像 Claude Code。

你不想写代码，只想有个能帮你写代码的命令行工具？`dcode` 就是答案。
它和 DeepAgents SDK 是同一套内核。

### 安装

```bash
curl -LsSf https://langch.in/dcode | bash
dcode
```

默认支持 OpenAI、Anthropic、Google。其他家（Ollama、Groq、xAI）是可选扩展：

```bash
DEEPAGENTS_EXTRAS="fireworks,nvidia" curl -LsSf https://langch.in/dcode | bash
```

### 给任务

```text
Create a Python script that prints "Hello, World!"
```

它会用 diff 形式提修改方案，等你批准再动文件。
还能跑 shell 测代码、查文档、搜网页。

### 常用斜杠命令

| 命令          | 作用          |
| ----------- | ----------- |
| `/model`    | 切换模型        |
| `/auth`     | 管理 API key  |
| `/remember` | 更新记忆与技能     |
| `/offload`  | 压缩上下文腾空间    |
| `/mcp`      | 看 MCP 服务与工具 |
| `/threads`  | 浏览历史会话      |

### 非交互模式（CI 友好）

```bash
git diff | dcode -n "审查这些改动"
dcode -n "修复失败的测试" --max-turns 10
```

`-n` 跑单任务即退出。`-S` 设命令白名单。`--max-turns` 防死循环。

### 远程沙箱

```bash
dcode --sandbox modal "部署这个服务"
```

支持 langsmith、agentcore、modal、daytona、runloop。

> **标叔的经验**：`dcode` 让我最快验证了 DeepAgents 的能力。不用写一行 SDK 代码，就体验了子代理、记忆、HITL、Skills。想快速感受框架，先装 dcode。

**标叔的结论**：要落地能力，写 SDK。要马上用，装 dcode。两者同源，学一个懂两个。

> **注意**：`dcode` 官方不支持 Windows。Windows 用户用 WSL 跑。另外 `-S all` 会放开任意 shell 命令，慎用。

下一章，讲一个深层话题：上下文工程。

## §16 上下文工程：别让窗口爆掉

先给结论：DeepAgents 把"上下文管理"做成默认流水线。你理解它，长任务才稳。

我做过一个超长研究任务。没管上下文，跑到一半，Agent 开始"失忆"——前面搜的重点全丢了。
后来我懂了：上下文窗口是稀缺资源，得主动管。

DeepAgents 的上下文管理靠三件套：

1. **大结果驱逐**：>20k token 的工具结果，写文件系统，留指针。
2. **自动压缩**：窗口到 85%，摘要老消息。
3. **子代理隔离**：把脏活丢给干净上下文。

### 手动触发压缩

```python
# 代理自己或你手动调用
compact_conversation()
```

85% 是阈值。到了就自动摘要。
老消息被压缩，原文 offload 到后端存储，上下文只留摘要。

### 给开发者的建议

| 做法                | 效果      |
| ----------------- | ------- |
| 大结果写文件，不全塞上下文     | 省窗口     |
| 长任务拆子代理           | 主上下文干净  |
| 用 Skills 渐进披露     | 不预载长提示词 |
| 用 AGENTS.md 放恒定信息 | 不重复注入   |

> **标叔的经验**：我那个"失忆"的任务，改成"每步结果写 /memories/ 文件 + 拆子代理"后，跑到两万字上下文也没丢重点。上下文工程不是玄学，是这几条具体动作。

**标叔的结论**：上下文窗口是有限的。会管理上下文的 Agent，才跑得动长任务。

下一章，讲上线：生产部署。

## §17 生产部署：多租户、安全与扩展

先给结论：DeepAgents 为生产而设计。多租户、RBAC、自带 Agent Server，开箱有。

我帮一个团队上线 Agent 服务时，最怕两件事：多用户隔离、服务可运维。
Claude Agent SDK 这两件都要自己搭。DeepAgents 默认带了不少。

### 多租户

DeepAgents 内建多租户：

- 按用户/助手隔离的沙箱
- 作用域化的 thread
- 运行历史隔离
- RBAC（基于角色的访问控制）

用 LangSmith Sandbox，还自带 auth 代理。
用户从沙箱调第三方 API，你不用每人配凭证。

### Agent Server 开箱即用

自托管 Claude Agent SDK，你要自己写 HTTP/WebSocket/SSE 服务。
DeepAgents 部署自带 Agent Server：流式端点、thread 管理、运行历史、webhook、鉴权。

### 两种部署模式（无代码改动）

| 模式  | 做法                                    |
| --- | ------------------------------------- |
| 托管  | LangSmith 的 Managed Deep Agents       |
| 自托管 | `langgraph build` 生成独立 Docker 镜像，到处部署 |

### 生产要点清单

```text
☐ checkpointer 必配（HITL、多轮都靠它）
☐ store 配好（跨线程记忆）
☐ 权限规则声明（FilesystemPermission）
☐ 沙箱隔离代码执行
☐ 流式用 version="v2"
☐ 监控接 LangSmith tracing
```

> **标叔的经验**：上线前我漏了 checkpointer。结果 HITL 恢复不了，多轮对话也串了。生产环境，checkpointer 不是可选项，是必选项。

**标叔的结论**：DeepAgents 把生产该有的骨架都备好了。你填业务，别重造轮子。

> **注意**：多租户隔离靠后端 + 沙箱配置。配错，用户数据会串。上线前务必测隔离。

下一章，讲选型：和 Claude Agent SDK 怎么选。

## §18 和 Claude Agent SDK 怎么选

先给结论：要模型/基础设施灵活、要内置多租户——选 DeepAgents。深度绑 Anthropic 且愿自建——选 Claude Agent SDK。

这俩都是 harness，但取舍不同。我做了张对比表。

| 维度        | Deep Agents                      | Claude Agent SDK      |
| --------- | -------------------------------- | --------------------- |
| Agent 在哪跑 | 沙箱内或外用沙箱当工具                      | 只在沙箱内                 |
| 模型供应商     | 任意（Anthropic/OpenAI/Google/100+） | 仅 Anthropic 系         |
| 多租户       | 内建（隔离 thread、沙箱、RBAC）            | 自己搭                   |
| 部署        | 托管或自托管镜像                         | 自托管（自己写服务）            |
| 许可证       | MIT                              | MIT（Claude Code 本身闭源） |

### 关键差异一：执行位置

Claude Agent SDK 只支持"Agent 跑在沙箱里"。
DeepAgents 两种都行，还能"Agent 跑外面，把远程沙箱当工具用"。
这叫"两种连接沙箱的模式"。生产架构正往这个方向走。

### 关键差异二：多租户

给每个用户隔离环境，Claude Agent SDK 要你写 API 包装层：
每用户起沙箱、追踪归属、用完销毁。
DeepAgents 在 harness 里直接配：按用户/助手隔离沙箱，带 thread 隔离和 RBAC。

### 谁在用

DeepAgents 已在生产使用：OpenSWE、LangSmith Fleet。
这不是玩具框架。

**标叔的结论**：模型中立 + 内建多租户 + 托管/自托管任选——这三个是 DeepAgents 的硬优势。你若已深绑 Anthropic 且愿自建，Claude Agent SDK 也行。

> **标叔的经验**：我给客户选型时，先问一句"模型锁死 Anthropic 了吗？"。没锁，基本选 DeepAgents。锁了，再看团队能不能扛多租户自建。这一问，省了三天纠结。

下一章，收尾：从一个真实重构，讲避坑。

## §19 避坑指南：从一个真实重构说起

先给结论：绝大多数 DeepAgents 问题，是"没按框架设计意图用"。下面 6 个坑，我都亲眼见过。

我手头有个真实案例：一个图片生成系统，把 DeepAgents 当普通 LangGraph wrapper 用。
结果 HITL 失效、子代理不注册、Skills 架空、工具冻结。
我把它重构了一遍。下面这些坑，都来自那次。

### 坑 1：HITL 用了旧格式

错误：检查 `__interrupt__`（v1 格式），调用没传 `version="v2"`。
后果：中断信息取不到，恢复不了。

正确：

```python
result = await agent.ainvoke(input_data, config=config, version="v2")
# 检查用属性
if getattr(result, "interrupts", None):
    ...
# 恢复
await agent.ainvoke(Command(resume={"decisions": decisions}), config=config, version="v2")
```

### 坑 2：子代理配置缺字段

错误：`description` 太模糊，没 `skills`，没 `response_format`。
后果：主 Agent 不知何时委派；返回自由文本要靠脆弱正则解析。

正确：`description` 写触发条件；用 `response_format` 拿结构化 JSON：

```python
class ImageGenResult(BaseModel):
    status: str
    task_id: str
    file_url: str | None = None

{"name": "image-generator",
 "description": "用户要生成任何电商/营销图片时调用",
 "system_prompt": "...",
 "tools": [generate_image],
 "skills": ["skills/ecom-details-image"],
 "response_format": ImageGenResult}
```

### 坑 3：Skills 被架空

错误：模板硬编码进巨型 prompt，没有 `SKILL.md`。
后果：`SkillsMiddleware` 完全不介入；每轮白烧 token。

正确：建 `skills/xxx/SKILL.md`，用渐进式披露。删掉硬编码函数。

### 坑 4：工具内部轮询冻住 Agent

错误：`generate_image` 内部 `for i in range(180): sleep(1)` 轮询。
后果：Agent 被冻 180 秒。

正确：直接 `await run_generation(task, ...)`。要真异步，用 AsyncSubAgent。

### 坑 5：每线程新建 Agent 实例

错误：`_agent_sessions` 对每个 thread\_id 建新 Agent + 新 checkpointer。
后果：实例浪费，checkpointer 不共享。

正确：全局只建一次 Agent + checkpointer，用 `thread_id` 区分会话：

```python
_checkpointer = MemorySaver()
_agent = None

def get_agent():
    global _agent
    if _agent is None:
        _agent = create_deep_agent(model=..., checkpointer=_checkpointer)
    return _agent
```

### 坑 6：模型手动初始化 + 挂 callback

错误：`ChatDeepSeek(... callbacks=[...])`。
正确：用 `"provider:model"` 字符串；日志走中间件：

```python
agent = create_deep_agent(model="deepseek:deepseek-v4-flash", ...)

@wrap_tool_call
def log_tool_calls(request, handler):
    print(f"[TOOL] {request.name}")
    return handler(request)
```

### 一张表记住

| 坑            | 现象       | 修法                                |
| ------------ | -------- | --------------------------------- |
| HITL 旧格式     | 中断取不到    | 加 `version="v2"`，用 `.interrupts`  |
| 子代理缺字段       | 不委派/脆弱解析 | 写好 description + response\_format |
| Skills 架空    | token 浪费 | 建 SKILL.md，渐进披露                   |
| 工具轮询         | Agent 冻结 | 直接 await / AsyncSubAgent          |
| 每线程建实例       | 资源浪费     | 全局单例 + thread\_id                 |
| 模型挂 callback | 中间件冲突    | 用字符串 + 中间件日志                      |

> **标叔的经验**：这 6 个坑，根子都是一个——"我没按框架的意思用"。DeepAgents 给了默认最佳实践。你绕过它自己造，往往造出它已经解决的问题。先用默认，遇到真瓶颈再改。

**标叔的结论**：学框架，先信它的默认。踩坑大多来自"我以为这样写也行"。

***

## 写在最后

DeepAgents 不是又一个 Agent 框架。
它是 LangChain 把"成功的深度 Agent"长什么样，做成默认配置。

你只要写 `create_deep_agent()`，就拿到：
规划、文件系统、子代理、记忆、压缩、HITL、Skills。

从五分钟跑通，到生产部署。
这本书的 19 章，是一条完整路径。

我最想说的就一句：
**先用默认，跑起来，再谈优化。**
别像我一样，先造轮子，再发现轮子框架早就给了。

> 标叔出品 | AI Native Coder · 独立开发者
> 公众号「标叔」| B站「AI进化论-花生」

***

## 附录：核心 API 速查

### create\_deep\_agent 常用参数

| 参数                | 作用                       |
| ----------------- | ------------------------ |
| `model`           | `"provider:model"` 或模型实例 |
| `tools`           | 自定义工具列表                  |
| `system_prompt`   | 自定义指令（置顶）                |
| `middleware`      | 额外中间件                    |
| `subagents`       | 子代理定义                    |
| `skills`          | SKILL.md 目录路径            |
| `memory`          | AGENTS.md 路径（每轮加载）       |
| `permissions`     | 文件权限规则                   |
| `backend`         | 存储后端                     |
| `interrupt_on`    | HITL 配置                  |
| `response_format` | 结构化输出 schema             |
| `checkpointer`    | 持久化层（HITL/多轮必配）          |
| `store`           | 跨线程存储                    |

### 五大内置能力工具

```text
规划：write_todos
文件：ls read_file write_file edit_file glob grep
Shell：execute（沙箱）
子代理：task
压缩：compact_conversation
```

### 常用命令

```bash
pip install deepagents          # 装 SDK
curl -LsSf https://langch.in/dcode | bash   # 装 dcode
dcode                            # 启动终端编程代理
```

