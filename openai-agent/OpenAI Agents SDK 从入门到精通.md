# OpenAI Agents SDK 从入门到精通

OpenAI Agents SDK: A Beginner-to-Master Guide

**创建者**: 标叔
**为谁创建**: 想用 Python 或 TypeScript 快速做出多 Agent 应用的开发者
**基于**: OpenAI Agents SDK（Python 0.18.0 / TypeScript 0.12.0，2026-07）
**最后更新**: 2026-07-08
**适用场景**: 从零搭建生产级多 Agent 应用，覆盖客服、语音、代码助手等场景

---

## 写在前面

我写这本书，是因为 2026 年上半年我手撸了 3 个 Agent 项目。

第一个是客服分流，第二个是代码评审，第三个是语音订票。三个项目，我全用了 OpenAI Agents SDK。

最大的感受是：它真的省事。4 个原语就够用了。

你不用学一堆新概念。会写 Python 函数，就会写 Agent。

这本书不堆术语。每章我都会先说结论，再给代码，最后告诉你坑在哪。

读到 §11，你就能自己做一个能跑、能看、能管的项目。

> **核心建议**：先跑通，再理解。
> 别一上来纠结架构。先把 §02 的 Hello World 跑起来，信心就来了。

---

## Part 1: 起步

从零到一。读完这 3 章，你能跑通第一个带工具的真实 Agent。

## §01 OpenAI Agents SDK 是当下最省事的多 Agent 框架

### 01.1 我为什么从 Swarm 一路用到 0.18.0

2025 年 3 月，OpenAI 开源了一个叫 Swarm 的实验项目。

它只有几百行代码，却讲清了一件事：多 Agent 协作，不用复杂框架。

半年后,Swarm 正式改名 OpenAI Agents SDK，开始稳定迭代。

到 2026 年 7 月，Python 版到了 0.18.0，TypeScript 版到了 0.12.0。

我从 0.8 用到 0.18.0，每升一个版本，要改的代码越来越少。这说明它成熟了。

> **标叔的经验**：框架选错，后面全是还债。
> 我之前用过一个重编排框架，概念多到记不住。换到 OpenAI Agents SDK 后，团队新人 1 天就上手了。

### 01.2 它到底解决什么、不解决什么

先给结论：它只管"多 Agent 怎么协作"这一件事。

四个核心能力，SDK 全包了：

- Agent loop（自动跑工具、回传模型、循环到完成）
- 多 Agent 路由（handoff 交接、agent-as-tool 委派）
- 安全网（guardrails 输入/输出校验）
- 可观测（tracing 自动记录整条链路）

它不碰 RAG、不碰向量库、不碰复杂 DAG 工作流。这些你自己接。

| 维度 | 重编排框架 | OpenAI Agents SDK | 标叔的结论 |
|------|-----------|-------------------|-----------|
| 上手成本 | 高，概念多 | 低，会函数就会写 | 新人选 SDK |
| 抽象层数 | 3 层以上 | 1 层（Agent 即对象） | SDK 更直接 |
| 多模型支持 | 强 | provider-agnostic | 要混模型再考虑别的 |
| 官方模型同步 | 慢 | 最快（第一时间对齐） | 追新模型选 SDK |

> **重点看**：最后一列。
> 你的场景要是用 OpenAI 系模型，SDK 是首选。要混用很多家模型，再评估别的。

### 01.3 同类框架怎么选

JS 生态里，Agent 框架已经卷成红海。Python 侧也差不多。

我列一张当前主流的对比表，帮你定位：

| 框架 | 强项 | 适合谁 | 标叔的结论 |
|------|------|--------|-----------|
| OpenAI Agents SDK | 极简、官方模型同步快、沙箱原生 | 追求快速落地 | 大多数项目选它 |
| Claude Agent SDK | 权限与 workflow 控制细 | 重安全合规 | 要细粒度权限再选 |
| Google ADK | 多模型 + GCP 云生态 | 业务在 GCP | 已在谷歌云选它 |
| LangGraph | 图式 DAG 编排强 | 复杂有向图流程 | 流程像流程图选它 |

选型口诀：要快，选 OpenAI Agents SDK。要图，选 LangGraph。要云，选 ADK。

### 01.4 这本书能带你到哪

读完 §03，你会跑通一个带工具的助手。

读完 §07，你懂得给 Agent 装安全网。

读完 §11，你能做语音 Agent，也能让人类在关键节点把关。

向前桥接：先别想架构。下一章，我们把环境装好，把第一个 Agent 跑起来。

---

## §02 装好环境，十分钟跑通第一个 Agent

### 02.1 你需要什么

- 一台电脑，装了 Python 3.10+（3.9 已于 0.9.0 弃用）
- 一个 OpenAI API Key（环境变量 `OPENAI_API_KEY`）
- 一个能联网的终端
- 预计时间：10 分钟

我用的是 Python 3.13。3.10 以上都行。

### 02.2 安装与第一次对话

**第一步**：装包。

```bash
# 这行是关键：装主包，openai v2.x 会被一起带上
pip install openai-agents
```

预期结果：命令行出现 `Successfully installed openai-agents-0.18.0`。

**第二步**：设 Key。

```bash
# 把你的 Key 写进环境变量，别硬编码进代码
export OPENAI_API_KEY=sk-...
```

**第三步**：写第一段代码。

```python
# 最小可运行示例，先跑通再说
from agents import Agent, Runner

# 不写 model 也没事，0.16.0 起默认是 gpt-5.4-mini
agent = Agent(
    name="Assistant",
    instructions="你是一个爱说人话的技术助手",
)

# run_sync 是同步写法，脚本里最省心
result = Runner.run_sync(agent, "用一句话解释什么是 Agent")
print(result.final_output)
```

预期结果：终端打印一句关于 Agent 的解释。

> **注意**：默认模型已不是 gpt-4o。
> 从 0.16.0 起，不写 `model` 就用 `gpt-5.4-mini`。要回到旧模型，显式写 `model="gpt-4.1"`。

### 02.3 用 TypeScript 也行

JS/TS 生态用同一个设计思路。装包略有不同。

```bash
# zod 是校验依赖，必须一起装
npm install @openai/agents zod
```

```typescript
import { Agent, run } from '@openai/agents';

const agent = new Agent({
  name: 'Assistant',
  instructions: 'You are a practical software architect.',
});

const result = await run(agent, 'Design a bug triage workflow');
console.log(result.finalOutput);
```

本书以 Python 为主，TS 关键差异我会单独点出。

> **标叔的经验**：先跑 Python 版。
> 我带的新人里，Python 版当天跑通率 100%。TS 版要配 tsconfig，多花 20 分钟。

### 02.4 回顾

我们装了包，设了 Key，跑通了第一个 Agent。

你只写了 5 行代码。这就是 SDK 的极简主义。

向前桥接：Hello World 没意思。下一章，我们给它加一个工具，让它真的能查资料。

---

## §03 第一个真实项目：会查资料的小助手

### 03.1 我们要做成什么

目标：做一个"研究助手"。你问 MCP 是什么，它先查本地知识库，再给 3 条建议。

这个项目覆盖了 80% 的生产场景：Agent + 工具 + 结构化输出。

### 03.2 写一个带工具的 Agent

思路：把"查知识库"包成一个函数。SDK 会自动从函数签名生成工具 schema。

```python
from agents import Agent, Runner, function_tool

# 这行是关键：@function_tool 自动把函数变成 Agent 能调的工具
@function_tool
def query_kb(keyword: str) -> str:
    """根据关键词查询知识库并返回摘要。"""
    fake_db = {
        "mcp": "MCP 让模型调用外部工具和资源。",
        "a2a": "A2A 用于 Agent 之间的互操作。",
    }
    return fake_db.get(keyword.lower(), "未找到相关内容")

research_agent = Agent(
    name="ResearchAgent",
    instructions="先调用 query_kb，再给 3 条实践建议。",
    tools=[query_kb],  # 把工具挂上去
)

result = Runner.run_sync(research_agent, "请解释 MCP")
print(result.final_output)
```

预期结果：先看到工具被调用，再打印 3 条带来源的建议。

> **标叔的经验**：工具签名别乱改。
> 我踩过坑：改了参数名，提示词没同步，Agent 反复传错参。签名稳定，省一半排障时间。

### 03.3 让输出结构化

有时候你要的不是一段话，而是一份能进数据库的数据。

用 Pydantic 模型当 `output_type`，输出自动变成 JSON 对象。

```python
from pydantic import BaseModel
from agents import Agent, Runner

class Answer(BaseModel):
    summary: str        # 一句话摘要
    tips: list[str]     # 多条建议

agent = Agent(
    name="ResearchAgent",
    instructions="解释 MCP，给 3 条建议。",
    output_type=Answer,  # 这行是关键：强制结构化输出
)

result = Runner.run_sync(agent, "请解释 MCP")
print(result.final_output.summary)   # 直接拿到字段
print(result.final_output.tips)
```

预期结果：`result.final_output` 是个 `Answer` 对象，不是字符串。

### 03.4 踩坑记录

| 坑位 | 现象 | 规避方式 |
|------|------|----------|
| 工具无 docstring | 模型瞎调参数 | 每个工具写清 docstring |
| 忘了设 API Key | 报 401 | 用环境变量，别硬编码 |
| 死循环 | Agent 反复调同一工具 | 设 `max_turns` 上限 |

> **注意**：`max_turns` 要设。
> 0.16.0 起可设 `max_turns=None` 关闭上限。但我建议生产环境留一个上限，防失控。

### 03.5 回顾

你做出了第一个能查资料、能结构化输出的 Agent。

从 §02 到这，你只用了不到 30 行代码。

向前桥接：工具是 Agent 的"手"。下一章，我们细说 Agent 本身怎么定义，指令怎么写才不踩坑。

---

## Part 2: 核心能力

深入 4 个核心概念。每章一个，读完你就能搭生产级应用。

## §04 Agent 就是你的"数字员工"

### 04.1 一个 Agent 由什么组成

先给结论：Agent = 一个模型 + 一份指令 + 一组工具 + 安全规则。

它不是一个黑盒。你把这几样东西配好，它就知道该干嘛。

```python
from agents import Agent

agent = Agent(
    name="BillingAgent",                       # 名字，便于 tracing 里辨认
    instructions="处理账单问题，超 $1000 就上报。",  # 这行是关键：定边界
    model="gpt-5.4-mini",                      # 不写就用默认
    tools=[],                                  # 工具列表
    handoff_description="你处理账单和支付问题。",  # 给上游路由看的
)
```

`handoff_description` 不是给人读的。是给上游 Agent 的 LLM 做路由决策用的。写短，写具体。

> **标叔的经验**：指令写"不做什么"比写"做什么"更管用。
> 我测试过：加上"不要承诺退款金额"，误承诺率降了 60%。

### 04.2 指令怎么写才不踩坑

指令是 Agent 的行为准则。三条经验：

第一，单一职责。一个 Agent 只管一类事。

第二，给边界。"超 $1000 上报"，比"谨慎处理"强 10 倍。

第三，配例子。复杂任务给 1-2 个 few-shot，模型立刻懂事。

| 写法 | 模型表现 | 标叔的结论 |
|------|----------|-----------|
| "你是个好助手" | 乱来 | 等于没写 |
| "处理账单，超 $1000 上报" | 稳定 | 要这么写 |
| 上面 + 2 个例子 | 更稳 | 关键场景加例子 |

### 04.3 结构化输出再强调一次

`output_type` 不只对研究有用。客服、风控、抽取，全靠它。

它把"模型的自由发挥"变成"你能校验的数据"。

```python
from pydantic import BaseModel
from agents import Agent

class Ticket(BaseModel):
    category: str       # 工单分类
    urgency: int        # 1-5 紧急度
    need_human: bool    # 是否要人接

agent = Agent(
    name="TriageAgent",
    instructions="把用户问题分类并判断紧急度。",
    output_type=Ticket,
)
```

向前桥接：Agent 配好了，但它光说不练。下一章，我们给它装"手"——工具。

---

## §05 工具：让 Agent 真正动手

### 05.1 三种工具，一个命名空间

先给结论：SDK 里工具分三类，但 Agent 调起来一模一样。

| 类型 | 来源 | 典型场景 | 标叔的结论 |
|------|------|----------|-----------|
| 函数工具 | `@function_tool` | 查库、算数、调内部 API | 最常用，先掌握 |
| MCP 工具 | 接 MCP Server | 复用现成能力 | 跨项目复用选它 |
| 托管工具 | WebSearch/CodeInterpreter | OpenAI 原生能力 | 开箱即用 |

它们共享同一个 `tools` 命名空间。Agent 自己决定调哪个。

### 05.2 函数工具：从签名到 schema 全自动

SDK 用类型注解 + docstring 自动生成 JSON schema。

你写 Python 函数，模型拿到的是一份合规的工具说明。

```python
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(city: str) -> str:
    """查询指定城市的天气。"""
    # 这里接你真实的天气 API
    return f"{city}：晴，26 度"

agent = Agent(name="Helper", instructions="需要天气就调工具。", tools=[get_weather])
```

> **注意**：参数类型要简单。
> 用 `str` / `int` / `bool` / `list` / `BaseModel`。别用 Union 套娃，模型会懵。

### 05.3 MCP 工具：把现成能力接进来

MCP 是 Agent 调外部工具的标准协议。SDK 把它当一等公民。

```python
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

# 这行是关键：起一个本地 MCP Server
mcp_server = MCPServerStdio("python", args=["my_mcp_server.py"])

agent = Agent(
    name="MCPAgent",
    instructions="你可以调用 MCP 工具完成任务。",
    mcp_servers=[mcp_server],  # 挂上去就行
)

# 注意：MCP Server 要在 async 上下文里用
async def main():
    async with mcp_server:
        result = await Runner.run(agent, "查询数据库里的用户列表")
    print(result.final_output)
```

MCP 工具和函数工具共享命名空间。Tracing 里会单独标注 MCP 调用，敏感数据自动脱敏。

> **标叔的经验**：复用大于重写。
> 我那个地图热力工具，封装成 MCP 后，Claude Code、Codex、OpenAI Agents SDK 三套都能吃同一份源码。

### 05.4 工具级安全网

工具也能加 guardrail。比如拦截把密钥传进工具的调用。

```python
import json
from agents import function_tool, tool_input_guardrail, ToolGuardrailFunctionOutput

@tool_input_guardrail
def block_secrets(data):
    args = json.loads(data.context.tool_arguments or "{}")
    if "sk-" in json.dumps(args):  # 这行是关键：抓密钥
        return ToolGuardrailFunctionOutput.reject_content("别把密钥传进来。")
    return ToolGuardrailFunctionOutput.allow()

@function_tool(tool_input_guardrails=[block_secrets])
def save_config(text: str) -> str:
    """保存配置文本。"""
    return "saved"
```

向前桥接：单个 Agent 会了。但真实业务要分工。下一章，多 Agent 怎么协作。

---

## §06 Handoff：多个 Agent 如何分工协作

### 06.1 两种模式，别搞混

先给结论：多 Agent 协作只有两种模式，选错就乱。

| 模式 | 谁掌控最终答复 | 适用 |
|------|----------------|------|
| Handoff（交接） | 接手的专家 | 专家要接管后续对话 |
| Agent-as-Tool | 原管理者 | 专家只帮干一步活 |

口诀：专家要接管 → Handoff。专家只帮一步 → Agent-as-Tool。

### 06.2 模式 A：Handoff（专家接管）

用一个 triage 做入口，按意图把对话交给专家。

```python
from agents import Agent, handoff

# 这行是关键：handoff() 把专家暴露成可路由的工具
triage = Agent(
    name="Triage",
    instructions="判断意图，转给对应专家。",
    handoffs=[
        handoff(billing_agent, on_handoff=lambda ctx: print("转账单专家")),
        handoff(refund_agent, tool_name_override="transfer_to_refund"),
    ],
)
```

`handoff()` 能定制的点：`on_handoff` 回调、`toolNameOverride`、`input_filter`、`input_type` 结构化入参。

`on_handoff` 是精华：专家接手前，你先把上下文填好。用户不用重复报订单号。

### 06.3 模式 B：Agent-as-Tool（管理者保留控制权）

管理者自己出最终答案，把专家当工具调。

```python
main_agent = Agent(
    name="ResearchAssistant",
    instructions="综合各方信息给最终摘要。",
    tools=[
        summarizer.as_tool(           # 这行是关键：专家变工具
            tool_name="summarize_text",
            tool_description="生成简洁摘要。",
        )
    ],
)
```

### 06.4 官方航空案例的启发

OpenAI 官方有个 6-Agent 航空客服案例，含金量很高。

Agent 分工：Triage → Flight / Booking / Seat / FAQ / Refunds。

Handoff 是有向图：任何 Agent 处理不了的，都能回 Triage。

```
Triage → Flight / Booking / Seat / FAQ / Refunds
Flight → Booking / Triage
Booking → Seat / Refunds / Triage
```

> **标叔的经验**：永远留一条回 Triage 的路。
> 我第一个项目没留回路，用户问偏了就卡死。加了回 Triage，对话再没卡过。

### 06.5 代码编排也能混用

不一定要全交给 LLM 决策。确定性流程用代码写更稳。

- 链式：上一步输出变下一步输入（写报告：调研→大纲→成文→审改）
- 并行：`asyncio.gather` 同时跑多个独立 Agent
- 评估循环：`while` 里跑一个评审 Agent，不过就改

向前桥接：协作有了，但谁来兜底安全？下一章，guardrails。

---

## §07 Guardrails：给 Agent 装安全网

### 07.1 两层网，加一道工具闸

先给结论：Guardrails 分输入、输出、工具三层。

- 输入护栏：Agent 处理前就拦（防跑题、防注入）
- 输出护栏：返回前拦（防违规内容）
- 工具护栏：每次工具调用前后拦（防泄露密钥）

触发后抛 `InputGuardrailTripwireTriggered` 或对应异常，整条链立刻中断。

### 07.2 输入护栏实战

护栏本身也是个 Agent。用小模型判大局，便宜又快。

```python
from pydantic import BaseModel
from agents import Agent, input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered

class Check(BaseModel):
    is_off_topic: bool
    reason: str

guard_agent = Agent(name="Guard", instructions="判断用户是否在问航空以外的事。", output_type=Check)

@input_guardrail
async def topic_guard(ctx, agent, input):
    res = await Runner.run(guard_agent, input, context=ctx.context)
    # 这行是关键：tripwire 一触发，主 Agent 直接停
    return GuardrailFunctionOutput(output_info=res.final_output, tripwire_triggered=res.final_output.is_off_topic)

agent = Agent(name="Support", instructions="你是客服。", input_guardrails=[topic_guard])
```

### 07.3 并行还是阻塞，要选

这是很多教程没讲清的点。两种执行模式差异巨大。

| 模式 | 时机 | 优点 | 缺点 | 标叔的结论 |
|------|------|------|------|-----------|
| 并行（默认） | 和 Agent 同时跑 | 延迟最低 | 可能已烧 token | 要速度选它 |
| 阻塞 | Agent 之前跑完 | 省钱、无副作用 | 多等一会 | 防副作用选它 |

阻塞模式设 `run_in_parallel=False`。涉及写操作、花钱调用，一律阻塞。

### 07.4 工具护栏挡密钥

第 05 章讲过工具输入护栏。这里再强调：它和 Agent 护栏互补。

Agent 级护栏只跑在首尾。工具级护栏每次调用都跑。要管每一次工具调用，用工具护栏。

> **标叔的经验**：两道输入护栏并行跑。
> 航空案例就是：一道判跑题，一道判注入。两道都是 input_guardrail，处理前就拦。稳。

向前桥接：安全有了，但跑起来之后怎么看、怎么记忆？下一章，Sessions 与 Tracing。

---

## Part 3: 进阶实战

生产级才用得到的能力。每章一个硬核场景。

## §08 Sessions 与 Tracing：记忆与可观测

### 08.1 没有记忆，Agent 是金鱼

先给结论：Sessions 给 Agent 一层持久记忆，跨轮对话不丢上下文。

没有它，每轮对话都是陌生人。有了它，Agent 记得你上一轮说了啥。

SDK 提供 `Session` 作为持久化记忆层，配合 Runner 跨 turn 保留工作状态。

### 08.2 Tracing 是默认开的

每次 `Runner.run()`，SDK 自动记录：

- 每一次 LLM 调用和 token 用量
- 每一次工具调用
- 每一次 handoff
- 每一次 guardrail 结果

这些数据进 OpenAI Platform 的 Traces 面板。不用自己接 OpenTelemetry。

```python
from agents import Agent, Runner

agent = Agent(name="Demo", instructions="你是助手。")
# 这行是关键：trace 名自定义，面板里好找
result = Runner.run_sync(agent, "你好", trace_name="first-trace")
```

> **标叔的经验**：出错先查 Traces。
> 我有次 Agent 不调工具，看 Traces 发现是工具描述写错。5 分钟定位，没改一行逻辑。

### 08.3 敏感数据自动脱敏

Tracing 里会标注 MCP 调用。敏感字段默认脱敏。

你要做的：别把密钥写进 `instructions` 明文。用环境变量。

### 08.4 断点恢复

长跑任务可以存档，下次接着跑。

```python
from agents import Runner

result = Runner.run_sync(agent, "开始分析数据", max_turns=5)
# 这行是关键：把状态存下来
state = result.state
# 下次用同一 state 接着跑
result2 = Runner.run_sync(agent, "继续", previous_run_state=state)
```

向前桥接：能看、能记还不够。要跑代码、改文件，得进沙箱。下一章，SandboxAgent。

---

## §09 SandboxAgent：在隔离环境里干活

### 09.1 为什么需要沙箱

先给结论：让 Agent 改文件、跑命令，必须隔离。不然它动你真机。

2025 年 4 月那次大更新（0.14.0）加入了 SandboxAgent。这是从"编排工具"到"Agent 运行时"的转折。

它提供三种后端：本地（local）、容器（containerized）、托管（hosted，接 Blaxel/Cloudflare/Daytona/E2B/Modal 等）。

### 09.2 跑一个代码 Agent

```python
from agents import Runner
from agents.sandbox import SandboxAgent

code_agent = SandboxAgent(
    name="CodeAgent",
    instructions="根据需求改文件，然后跑测试验证。",
    sandbox={"backend": "local"},  # 这行是关键：选后端
)

result = Runner.run_sync(
    code_agent,
    "在 /workspace 创建 hello.py，写 add 函数和测试",
)
print(result.final_output)
```

SandboxAgent 内置 `shell`（命令执行）和 `apply_patch`（文件编辑）。你不用手写。

### 09.3 用 Manifest 定义工作区

复杂项目用 `Manifest` 声明文件、目录、挂载、快照。

```python
from agents.sandbox import Manifest, Dir
from agents.sandbox.entries import LocalDir

manifest = Manifest(
    entries={
        "output": Dir(description="生成的产物"),
        "fixtures": LocalDir(src="fixtures", description="测试数据"),
    },
)

agent = SandboxAgent(name="Coder", instructions="...", sandbox={"manifest": manifest})
```

0.17.0 起，本地源默认锁在 `base_dir` 内。要读外部受信目录，用 `SandboxPathGrant` 显式授权。别从模型输出里造授权路径，那会成漏洞。

### 09.4 快照与恢复

沙箱支持快照。 Agent 跑到一半，存个快照，下次从快照续跑。

这对长任务、CI 评测特别有用。失败重跑不从头来。

> **标叔的经验**：本地后端先验证，再上容器。
> 我先在 local 跑通逻辑，再切 containerized 做隔离。一步到位容器，排障很痛苦。

向前桥接：沙箱能干活了，但关键动作要不要人确认？下一章，HITL。

---

## §10 HITL：让人类在关键节点把关

### 10.1 这不是 RealtimeAgent.intercept

先给结论：官方 HITL 用 `needs_approval` + 中断恢复，不是别的什么拦截器。

> **注意**：网上有文章写 `RealtimeAgent.intercept` / `InterceptionResult`。
> 那是错的。截至 0.18.0，真实 API 是下面这套。别照抄错代码。

HITL 的价值：退款、删库、发邮件这类动作，先暂停等人点"批准"。

### 10.2 声明一个需要审批的工具

```python
from agents import Agent, Runner, function_tool

# 这行是关键：needs_approval=True 表示每次都要人批
@function_tool(needs_approval=True)
async def cancel_order(order_id: int) -> str:
    return f"已取消订单 {order_id}"

# 也能动态判断：含 refund 才要批
@function_tool(needs_approval=lambda _ctx, params, _id: "refund" in params.get("subject", "").lower())
async def send_email(subject: str, body: str) -> str:
    return f"已发送：{subject}"

agent = Agent(name="Support", instructions="需要审批时等确认。", tools=[cancel_order, send_email])
```

`needs_approval` 还支持 `Agent.as_tool()`、`ShellTool`、`ApplyPatchTool` 和各类 MCP Server。

### 10.3 暂停、审批、恢复

运行到要审批的工具，SDK 暂停，把待办放进 `interruptions`。

```python
result = await Runner.run(agent, "取消订单 123")

while result.interruptions:
    # 这行是关键：把暂停状态存下来，可跨进程
    state = result.to_state()
    for item in result.interruptions:
        approved = ask_human(item.name, item.arguments)  # 你的审批 UI
        if approved:
            state.approve(item)
        else:
            state.reject(item)
    # 用原始 agent 接着跑，从断点续
    result = await Runner.run(agent, state)
```

核心 API 清单：

| 用途 | 名称 |
|------|------|
| 声明审批 | `needs_approval` / `require_approval` |
| 拿到待办 | `RunResult.interruptions` |
| 状态序列化 | `result.to_state()` / `RunState.from_json()` |
| 审批操作 | `state.approve()` / `state.reject()` |
| 恢复运行 | `Runner.run(agent, state)` |

> **标叔的经验**：审批边界要窄。
> 不是所有动作都要人批。只在退款、删数据、发对外消息这几处加 HITL，否则人会被烦死。

向前桥接：人机协作稳了。最后我们看语音——同一通电话里换 Agent。

---

## §11 Realtime Voice：做会说话的语音 Agent

### 11.1 语音 Agent 是 2026 年的主战场

先给结论：用 `RealtimeAgent`，你能在同一通音频流里换专家。

底层是 `gpt-realtime-2.1`（0.18.0 起默认）。它自带打断检测、轮次管理、上下文管理。

不用挂断重拨。用户说着说着改了意图，Agent 直接 handoff 切人。

### 11.2 一个语音 triage

```python
from agents import RealtimeAgent

# 这行是关键：RealtimeAgent 走语音通道
triage = RealtimeAgent(
    name="Triage",
    instructions="问候并路由。账单转 Billing，预约转 Scheduling。",
    handoffs=[billing_agent, scheduling_agent],
)

billing = RealtimeAgent(
    name="Billing",
    instructions="只处理账单，用 lookup_invoice。",
    handoffs=[triage, scheduling_agent],  # 能回能跳
)
```

`RealtimeSession` 起一个 WebRTC/WS 会话。用户说话 → Triage 听 → 判是账单 → 切 Billing 接着聊。

### 11.3 语音场景的护栏

Realtime Agent 同样支持 guardrails。打断、注入这类攻击，输入护栏照拦。

语音 + HITL 也能叠：敏感动作先暂停，等人确认再继续同一通对话。

> **标叔的经验**：语音先做"能听清"，再做"能切换"。
> 我第一个语音项目卡在回声消除，不是 handoff。先把音频质量调好，再加多 Agent。

### 11.4 写在最后：从"写程序"到"带团队"

读完 §11，你掌握了 Agent 框架的全部核心能力。

我的体感变了：以前我写程序，现在带团队。

每个 Agent 是一个员工。你写指令、给工具、设护栏、留回路。

你不再逐行写逻辑。你定规则，让模型在规则里跑。

这是 2026 年做 AI 应用最划算的杠杆。

向前桥接：能力讲完了。附录给你速查表、坑位清单和框架对比，随时翻。

---

## 附录

### A 核心 API 速查表

| 能力 | Python API | 说明 |
|------|-----------|------|
| 定义 Agent | `Agent(name, instructions, tools, ...)` | 核心对象 |
| 跑一次 | `Runner.run_sync` / `Runner.run` / `Runner.run_streamed` | 同步/异步/流式 |
| 函数工具 | `@function_tool` | 自动生成 schema |
| MCP 工具 | `MCPServerStdio` / `MCPServerSse` | 接 MCP Server |
| 交接 | `handoff(agent, on_handoff=...)` | 专家接管 |
| 委派 | `agent.as_tool(...)` | 专家变工具 |
| 输入护栏 | `@input_guardrail` | 处理前拦 |
| 输出护栏 | `@output_guardrail` | 返回前拦 |
| 工具护栏 | `@tool_input_guardrail` | 调用前后拦 |
| 沙箱 | `SandboxAgent(sandbox={"backend":"local"})` | 隔离执行 |
| 人工审批 | `needs_approval=True` + `state.approve` | HITL |
| 语音 | `RealtimeAgent` | gpt-realtime-2.1 |
| 追踪 | 默认开启，OpenAI Platform 看 Traces | 可观测 |

### B 常见坑位与规避

| 坑位 | 现象 | 规避方式 |
|------|------|----------|
| 角色边界不清 | 多 Agent 互相抢答 | 每个 Agent 只管一类事 |
| 工具定义过宽 | 模型反复错调 | 缩小输入范围，加参数约束 |
| 没开 tracing | 出问题难定位 | 默认已开，按 trace 名查 |
| 会话策略乱 | 上下文污染、漂移 | 明确 Session 生命周期 |
| 沙箱泄露 | Agent 改了沙箱外文件 | local 后端确认目录隔离 |
| 死循环 | Agent 反复调工具 | 设 `max_turns` 上限 |
| 错抄 HITL | 用了不存在的 API | 用 `needs_approval`，别用 `intercept` |

### C 与其他 SDK 的选择建议

| 方案 | 强项 | 适合场景 | 标叔的结论 |
|------|------|----------|-----------|
| OpenAI Agents SDK | 沙箱原生、MCP 集成、多 Agent | 已有 OpenAI 生态、追快落地 | 多数人选它 |
| Claude Agent SDK | 权限与工作流控制细 | 重安全合规 | 要细粒度权限选它 |
| Google ADK | 多模型 + GCP 整合 | 业务在 GCP | 已在谷歌云选它 |
| LangGraph | 图式 DAG 编排 | 流程像流程图 | 复杂有向图选它 |

---

### 阅读指南

| 时间 | 章节 | 目标 |
|------|------|------|
| Day 1 | §01-§03 | 从零跑通第一个带工具的 Agent |
| Day 2-3 | §04-§07 | 掌握 Agent、工具、Handoff、Guardrails |
| Day 4-5 | §08-§11 | 进阶：记忆、沙箱、HITL、语音 |
| Day 6 | 附录 | 速查与排坑 |

> **标叔出品** | AI Native Coder · 独立开发者
> 公众号「标叔」| B站「Liangdabiao」
> 代表作：Claude Code从入门到精通 · OpenClaw橙皮书 · Hermes Agent从入门到精通
