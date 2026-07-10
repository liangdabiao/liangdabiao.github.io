# LangGraph 从入门到精通

Build Resilient AI Agents with LangGraph

**创建者**: 标叔
**为谁创建**: 会一点 Python、懂大模型基本概念，想亲手做出"可控、可持久化、能上线"的 AI Agent 的开发者
**基于**: LangGraph 1.2.8（2026-07-06 发布）
**最后更新**: 2026-07-08
**适用场景**: 从零跑通第一个 Agent，到部署一个生产可用的智能体系统

---

## 目录

- Part 1 起步
  - §01 LangGraph 不是"链"，是"图"
  - §02 5 分钟跑通你的第一个 Agent
  - §03 手搭一个会调用工具的客服助手
- Part 2 核心能力
  - §04 图的三要素：节点、边、状态
  - §05 工具调用代理：让 AI 自己选工具
  - §06 记忆系统：短期 + 长期
  - §07 人机协同：在关键节点按暂停
- Part 3 进阶实战
  - §08 多智能体：用 supervisor 组建团队
  - §09 Functional API：少写图的另一种写法
  - §10 从本地到生产：部署与可观测
  - §11 写这本书时，我对 Agent 框架的认知变了
- 附录 A 版本与生态速查（2026-07）
- 附录 B 常见坑与排查
- 阅读指南

---

## Part 1: 起步

从零到一。读完这部分，你能跑通第一个 Agent，并手搭一个带工具的助手。

## §01 LangGraph 不是"链"，是"图"

### 01.1 我是怎么被"链"劝退的

2024 年我第一次用 LangChain 写客服。流程是线性的：调模型、抽实体、查库、再调模型。

链路一长，问题就来了。用户改了主意，我得回头重跑前面几步。代码里全是 if-else 绕来绕去。

我当时就想：这哪是智能体，这是一根不能回头的面条。

2025 年 10 月，LangGraph 发布 1.0。我重写了那个客服。循环、分支、回溯，全成了"图"上的自然动作。

> **标叔的经验**：一次真实故障
>
> 有回客服 Agent 查库失败，旧链路直接崩给用户。换成图之后，我加了一个"失败→重试→人工"的分支。同样的故障，用户只看到一句"正在为您转人工"。这一下，我就回不去了。

### 01.2 LangGraph 在 2026 生态里到底算什么

很多人以为 LangGraph 是 LangChain 的一个"升级版"。这话不对，得重新说清楚。

2026 年的官方定位是四层：

| 层 | 角色 | 一句话 |
|------|------|--------|
| LangGraph | 编排运行时 | 负责持久化、流式、人机协同、状态 |
| LangChain | 框架 | 管模型、工具、Agent 循环的抽象与集成 |
| Deep Agents | 上层封装（harness） | 在 LangGraph 上做规划、子代理、文件系统 |
| LangSmith | 平台 | 追踪、评估、部署，跨框架通用 |

你看，LangGraph 不替你写提示词，也不规定 Agent 架构。它只管一件事：把"长流程、有状态"跑稳。

这就是它和"链"的本质区别。链是固定的线。图是可以循环、可以分叉、可以暂停的网络。

> **重点看**：上表第一列。
> LangGraph 只做"编排运行时"。这句话理解了，后面全通。

### 01.3 为什么是"图"

我把 Agent 的工作方式分成三类，类比一下你就懂：

- 脚本是你的菜谱，一步一步照做。
- 链是你的传送带，串好就走。
- 图是你的城市地铁网，可以换乘、可以绕路、可以原路返回。

Agent 的真实任务从来不是直线的。它会："查一下→不对→再查→问人→总结"。

只有图能自然表达这种"带循环和判断"的流。

### 01.4 你适不适合用 LangGraph

我先给结论：

- 你要做"对话机器人"、单次问答 → 用 LangChain 的 `create_agent` 就够了，别上 LangGraph。
- 你要做"跑很久、要记住上下文、中途要人审批、会循环自己纠错"的系统 → LangGraph 是正解。

> **核心建议**：先问自己"流程会不会回头"
> 不会回头，别用图。会回头，LangGraph 省你一半代码。

[向前桥接] 概念清楚了。下一章，我们 5 分钟真跑一个 Agent。

---

## §02 5 分钟跑通你的第一个 Agent

### 02.1 你需要什么

- Python 3.10 以上（我用的是 3.13）。
- 一个支持"函数调用"的大模型 API Key（OpenAI、通义、智谱都行）。
- 预计时间：5 分钟。

### 02.2 装好依赖

```bash
# 这行装的是 LangGraph 本体，会自动带上核心依赖
pip install -U langgraph
# 装模型集成（以 OpenAI 为例，换厂商就换这个包）
pip install langchain-openai
```

预期结果：命令行跑完，没有红色报错。

> **注意**：版本会变
> 本书写于 2026-07，LangGraph 稳定版是 1.2.8。装完跑 `pip show langgraph` 看一眼版本，别低于 1.0。

### 02.3 二十行跑通第一个 Agent

```python
# 这行导入统一的模型入口，2026 年推荐这么写
from langchain.chat_models import init_chat_model
# 预置 Agent 工厂，最简用法就靠它
from langgraph.prebuilt import create_react_agent

# 初始化模型。把 key 换成你自己的，模型名也能换
llm = init_chat_model("openai:gpt-4o-mini", api_key="你的KEY")

# 核心一步：模型 + 工具（这里先不给工具，纯对话）
agent = create_react_agent(llm, tools=[])

# 直接对话，输入是 messages 列表
result = agent.invoke({"messages": "用一句话介绍 LangGraph"})
# 取最后一条消息的内容
print(result["messages"][-1].content)
```

预期结果：屏幕上打印出一段关于 LangGraph 的介绍文字。

就成了。你没写任何"循环"代码，但 `create_react_agent` 内部已经是一个完整的图：调模型 → 判断 → 回答。

### 02.4 给它一个工具，让它"动手"

```python
from langchain_core.tools import tool

# 用装饰器定义一个工具，docstring 就是给 AI 看的说明书
@tool
def get_time() -> str:
    """返回当前时间。用户问时间时调用。"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M")

# 把工具交给 Agent
agent = create_react_agent(llm, tools=[get_time])

# 问时间，Agent 会自己决定调用 get_time
result = agent.invoke({"messages": "现在几点了？"})
print(result["messages"][-1].content)
```

预期结果：Agent 不再瞎编，而是调用 `get_time` 后告诉你真实时间。

> **标叔的经验**：docstring 是半条命
> 我早期踩过坑：工具描述写"获取信息"，AI 死活不调用。改成"返回当前时间。用户问时间时调用。"，命中率立刻上来了。AI 是按你的描述选工具的。

### 02.5 小结

这一章你跑通了：
- 安装 LangGraph
- 用 `create_react_agent` 造一个 Agent
- 给它加工具，看它自己调用

> **核心建议**：从 `create_react_agent` 起步
> 它封装好了"思考—调工具—再思考"的循环。等你想完全掌控流程，再回到 StateGraph。

[向前桥接] 预置 Agent 省事，但黑盒。下一章，我带你手搭一个图，看清里面每一块。

---

## §03 手搭一个会调用工具的客服助手

### 03.1 我们最终做成什么

做一个客服助手：能聊天、能查天气、能把用户信息存库。

做完你就能看清一张图的骨架：节点、边、状态。后面所有复杂系统都是这个骨架长出来的。

### 03.2 定义状态：图里的"共享白板"

```python
from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage
import operator

# State 是节点之间传递的数据，messages 用 add 做累加
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
```

`operator.add` 是"归约器"（reducer）。新消息加到旧列表后面，不是覆盖。这点很关键。

### 03.3 搭节点和边

```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage

# 三个工具，定义略，和上一章一样的写法
tools = [get_weather, save_user_info]
tool_node = ToolNode(tools)
llm_with_tools = llm.bind_tools(tools)

# 节点一：调模型，让它决定要不要调工具
def call_model(state):
    resp = llm_with_tools.invoke(state["messages"])
    return {"messages": [resp]}

# 建图，绑定状态结构
g = StateGraph(AgentState)
g.add_node("agent", call_model)   # AI 决策节点
g.add_node("tools", tool_node)    # 工具执行节点
g.add_edge(START, "agent")        # 入口
# 条件边：有 tool_calls 去 tools，否则结束
g.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
g.add_edge("tools", "agent")      # 工具跑完回到 AI 总结
graph = g.compile()
```

`tools_condition` 是 LangGraph 预置的路由函数。它看最后一条消息有没有 `tool_calls`，有就走 `tools`，没有就 `END`。

### 03.4 跑一下

```python
# 这一行设置递归上限，防止 AI 无限调工具
out = graph.invoke(
    {"messages": [HumanMessage(content="北京今天天气怎么样？")]},
    {"recursion_limit": 10},
)
print(out["messages"][-1].content)
```

预期结果：Agent 调 `get_weather`，再总结成一句人话。

> **注意**：一定要设递归上限
> 没设 `recursion_limit`，AI 一旦陷进"调工具—不满意—再调"的循环，进程就卡死。我默认设 10。

### 03.5 回顾

我们从零搭了一张带循环的真图。你看到了图的三个核心零件：节点（算什么）、边（走哪条）、状态（存什么）。

> **核心建议**：先手搭，再偷懒
> 手搭一遍，你就懂 `create_react_agent` 内部在干嘛。之后用预置的，心里才有底。

[向前桥接] 这张图还很简单。下一章，我把"节点、边、状态"拆开讲透。

---

## Part 2: 核心能力

深入四块关键能力。每章一个，读完你能掌控 Agent 的内部。

## §04 图的三要素：节点、边、状态

### 04.1 节点就是一个普通函数

2025 年我带新人，最爱用这句话开场："节点没那么神，它就是一个函数。"

```python
# 节点接收 state，返回要更新的字段
def my_node(state: AgentState):
    last = state["messages"][-1].content
    return {"messages": [f"你说了：{last}"]}
```

节点返回什么，就更新状态的哪部分。返回 `{"messages": [...]}` 就往白板贴新消息。

### 04.2 边决定"下一步去哪"

普通边是无条件走：

```python
g.add_edge("agent", "tools")  # 永远从 agent 走到 tools
```

条件边看情况走，背后是个路由函数：

```python
def route(state):
    if state["messages"][-1].tool_calls:
        return "tools"   # 要走这条路
    return END           # 否则结束

g.add_conditional_edges("agent", route, {"tools": "tools", END: END})
```

> **重点看**：`route` 返回的字符串。
> 它必须和字典的 key 对上。对不上，图编译直接报错。

### 04.3 状态：图的"共享白板"

最省事的状态是 `MessagesState`：

```python
# 一句话搞定消息累加，不用自己写 reducer
from langgraph.graph import MessagesState

g = StateGraph(MessagesState)
```

`MessagesState` 内部就一个 `messages` 字段，自带 `add_messages` 归约。90% 的场景用它足够。

要加自定义字段也简单：

```python
from langgraph.graph import MessagesState
from typing import Annotated
import operator

class MyState(MessagesState):
    # 在消息之外，再加一个累计分数
    score: Annotated[int, operator.add] = 0
```

### 04.4 三种"图"的对比

| 维度 | 手写函数 | LangChain 链 | LangGraph 图 |
|------|---------|-------------|-------------|
| 循环 | 自己写 while | 不支持 | 原生支持 |
| 暂停恢复 | 极难 | 不支持 | 原生支持 |
| 可视化 | 无 | 弱 | LangGraph Studio |
| 标叔的结论 | 玩具级 | 线性任务 | 真实 Agent |

> **核心建议**：状态要"可序列化"
> State 里的东西最终要存进数据库。别塞不能 JSON 化的对象，否则中断恢复会炸。

[向前桥接] 节点会了。下一章讲 Agent 怎么"自己挑工具"。

---

## §05 工具调用代理：让 AI 自己选工具

### 05.1 AI 怎么知道调哪个

老实说，第一次看到 AI 自己选工具，我还挺惊讶。原理其实就三步：

第一，把工具清单和说明给模型。
第二，模型返回"我想调 X，参数是 Y"。
第三，你执行 X，把结果还回去，模型再总结。

```python
# bind_tools 把工具说明塞进模型上下文
llm_with_tools = llm.bind_tools([search_web, get_weather])

resp = llm_with_tools.invoke("北京天气？")
# resp.tool_calls 里就有模型的决定
print(resp.tool_calls)
```

### 05.2 ToolNode 帮你执行

你不用自己写"查字典调函数"的循环。`ToolNode` 包好了：

```python
from langgraph.prebuilt import ToolNode

tool_node = ToolNode([search_web, get_weather])
# 它接收一个带 tool_calls 的 state，返回 ToolMessage 结果
```

配合 `tools_condition` 做路由，就是 §03 那张图的完整逻辑。

### 05.3 工具描述写得好，AI 才听得懂

这是实战里最值钱的一条经验：

```python
# ❌ 差的写法，AI 看不懂何时用
@tool
def f(x):
    """一个函数"""
    ...

# ✅ 好的写法，讲清用途和参数
@tool
def search_flights(dep: str, arr: str, date: str):
    """查航班。

    Args:
        dep: 出发城市，如"北京"
        arr: 到达城市，如"上海"
        date: 日期，格式 YYYY-MM-DD
    """
    ...
```

> **标叔的经验**：描述决定命中率
> 我测过一个客服：把工具描述从"查询"改成"当用户询问订单、物流时调用"，无效调用少了七成。

### 05.4 给工具加容错

工具会失败。在工具里自己接住：

```python
@tool
def get_weather(city: str):
    """查询天气。"""
    try:
        return api.get(city)
    except Exception as e:
        # 返回友好信息，让 AI 自己圆场
        return f"查 {city} 天气出错：{e}"
```

> **核心建议**：工具里吞异常
> 别让异常冒泡到图外。返回一段说明文字，AI 会自己跟用户解释。

[向前桥接] 工具会选了。可 Agent 一重启就忘事，下一章解决"记忆"。

---

## §06 记忆系统：短期 + 长期

### 06.1 先给结论：记忆分两层

2026 年的 LangGraph，记忆是两套互补的机制：

| 机制 | 存什么 | 范围 | 用途 |
|------|--------|------|------|
| Checkpointer | 图的状态快照 | 单个会话（thread） | 续聊、人机协同、时光回溯 |
| Store | 应用自定义数据 | 跨会话 | 用户偏好、长期事实 |

很多人只知其一。两者一起用，Agent 才又"记得刚才聊啥"，又"记得你是谁"。

### 06.2 短期记忆：Checkpointer

```python
# 开发用内存版，重启即丢
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()

# 编译时挂上，并给每个会话一个 thread_id
graph = g.compile(checkpointer=checkpointer)

cfg = {"configurable": {"thread_id": "user-001"}}
graph.invoke({"messages": "我叫小明"}, cfg)
# 下一次用同一个 thread_id，它记得你是小明
graph.invoke({"messages": "我叫什么？"}, cfg)
```

生产换持久化的：

```python
# 本地文件，开发够用
from langgraph.checkpoint.sqlite import SqliteSaver
cp = SqliteSaver.from_conn_string("sqlite:///state.db")

# 正式上线用 Postgres，记得先 setup() 建表
from langgraph.checkpoint.postgres import PostgresSaver
cp = PostgresSaver.from_conn_string("postgresql://user:pwd@host/db")
cp.setup()
```

> **重点看**：`thread_id` 必须稳定。
> 同一用户的每次对话用同一个 `thread_id`，记忆才连得上。用 UUID 最稳。

### 06.3 长期记忆：Store

短期记忆跟着会话走。长期记忆要跨会话保留：

```python
from langgraph.store.memory import InMemoryStore
store = InMemoryStore()

graph = g.compile(checkpointer=cp, store=store)
```

节点里读写长期记忆：

```python
def remember(state, *, store):
    # 按 user_id 存一条偏好
    store.put(("prefs",), state["user_id"], {"like": "足球"})
    return {}
```

跨会话、跨线程都能读到。这就是"它记得你是球迷"的来源。

### 06.4 更高级的记忆：langmem

如果你不想自己设计抽取逻辑，官方有 `langmem` 库：

- 自动从对话里抽取重要信息
- 维护长期记忆，和 Store 打通
- 还能反哺优化 Agent 的提示词

> **核心建议**：Store 管"存"，langmem 管"学"
> 简单偏好用 Store 直接存。要"越用越懂用户"，上 langmem。

[向前桥接] 记忆有了。可有些事不能全信 AI，下一章讲"人何时插手"。

---

## §07 人机协同：在关键节点按暂停

### 07.1 什么是 HITL

HITL 是 Human-in-the-Loop，人机协同。

一句话：让 Agent 在关键决策点停下来，等人拍板，再继续。

金融风控、医疗诊断、合同审批——这些地方，AI 说了不算，得人签字。

### 07.2 核心就一个：interrupt

```python
from langgraph.types import interrupt

def approve_node(state):
    # 关键：在这里暂停，把待审信息交出去
    decision = interrupt({"plan": state["plan"], "msg": "请审批"})
    # 恢复后，decision 就是人传回来的结果
    if decision["type"] == "accept":
        return {"ok": True}   # 普通返回，更新状态即可
    return {"ok": False}
```

`interrupt()` 一调用，图立刻冻结。状态存进 Checkpointer。人审批完，用同一个 `thread_id` 带着结果回来，代码从这一行往下接着跑。

### 07.3 恢复也简单

```python
from langgraph.types import Command

# 人审批后，用 Command(resume=...) 把决定塞回 interrupt
graph.invoke(
    Command(resume={"type": "accept"}),
    {"configurable": {"thread_id": "user-001"}},
)
```

> **注意**：interrupt 必须配 Checkpointer
> 没挂 checkpointer，`interrupt()` 用不了。图编译时会直接报错提醒你。

### 07.4 一句话讲清"为什么能冻结"

Checkpointer 在每次到节点或触发 `interrupt` 时，把整个 State 序列化存库。

恢复时，它不重跑函数，而是重放历史状态，把 `resume` 的值直接注入 `interrupt()` 的返回值。

所以一个 Python 函数能像按了暂停键，几小时甚至几天后再醒。

> **标叔的经验**：审批要留痕
> 生产环境，每一次 interrupt→resume 都要记审计日志：谁、什么时间、基于什么数据、做了啥决定。出事能溯源。

[向前桥接] 单智能体够强了。但任务太大，下一章讲"多智能体怎么分工"。

---

## Part 3: 进阶实战

多智能体、另一种写法、上线部署，以及我对框架的认知转变。

## §08 多智能体：用 supervisor 组建团队

### 08.1 先泼盆冷水

我见过太多人，需求明明一个 Agent 能搞定，非要上多智能体。

结果：调试翻倍，成本翻倍，效果没好多少。

先给结论：90% 的场景，单智能体够用。只有下面三种情况才考虑多智能体：

- 任务要不同专业知识（研究 + 写作）
- 要并行处理多个子任务
- 需要不同角色扮演

### 08.2 层级式：一个主管带几个专家

2025 年底，官方出了 `langgraph-supervisor`。它把"主管（supervisor）+ 多个专家"的层级结构封装好了。

```python
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

# 先造两个专家 Agent
research = create_react_agent(llm, tools=[search_web], name="researcher")
writer = create_react_agent(llm, tools=[draft_doc], name="writer")

# 主管来协调，决定派给谁
workflow = create_supervisor(
    [research, writer],
    model=llm,
    prompt="你是主管，按需把任务派给研究员或写手。",
)
graph = workflow.compile()
```

`create_supervisor` 返回的是 `StateGraph`，`.compile()` 后就能跑。它内置流式、记忆、人机协同。

### 08.3 主管怎么"派活"

主管靠"交接工具"（handoff）把任务转给专家：

```python
graph.invoke({
    "messages": "先查一下 LangGraph 最新版本，再写一段介绍。"
})
# 主管会先调 researcher，再调 writer，最后汇总
```

你可以控制历史怎么保留：

```python
create_supervisor(
    [research, writer],
    model=llm,
    output_mode="last_message",  # 只留专家最终回复，省 token
)
```

### 08.4 对比：单 vs 多

| 维度 | 单智能体 | 多智能体（supervisor） |
|------|---------|----------------------|
| 上手难度 | 低 | 中 |
| 调试成本 | 低 | 高 |
| 并行能力 | 弱 | 强 |
| 标叔的结论 | 默认选它 | 真复杂才上 |

> **核心建议**：从单智能体长出来
> 别一上来就多智能体。先把单 Agent 玩透，需要时才加主管。

[向前桥接] 图写腻了？下一章给你一种"少写图"的写法。

---

## §09 Functional API：少写图的另一种写法

### 09.1 图不是唯一写法

2026 年我最大的惊喜，是 Functional API。

它让你用普通 Python 写流程，照样拿到持久化、记忆、人机协同。

不用声明节点和边。if、for 直接用。

### 09.2 最小例子

```python
from langgraph.func import entrypoint, task
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt

# @task 包住一个工作单元，结果会被 checkpoint
@task
def write(text: str) -> str:
    return f"文章：{text}"

# @entrypoint 是整个流程的入口
@entrypoint(checkpointer=InMemorySaver())
def flow(topic: str):
    essay = write(topic).result()        # 调 task，等结果
    ok = interrupt({"essay": essay})     # 照样能暂停等人
    return {"essay": essay, "ok": ok}

# 用法和图一模一样
flow.invoke("LangGraph 是什么", {"configurable": {"thread_id": "t1"}})
```

### 09.3 两种 API 怎么选

| 维度 | Graph API | Functional API |
|------|-----------|----------------|
| 控制流 | 声明式图 | 原生 Python |
| 可视化 | 强（Studio） | 无 |
| 改动成本 | 要重构 | 加俩装饰器 |
| 标叔的结论 | 复杂状态用 | 老代码加能力用 |

> **核心建议**：两个都能混用
> 底层是同一个运行时。复杂模块用图，轻量逻辑用函数，放一起跑没毛病。

[向前桥接] 本地能跑不算完。下一章讲怎么上线。

---

## §10 从本地到生产：部署与可观测

### 10.1 三种部署路径

| 路径 | 适合 | 难度 |
|------|------|------|
| LangGraph Platform（云） | 想省心 | 低 |
| Self-host（自托管） | 数据不出内网 | 中 |
| 纯代码嵌入 | 做别人产品的零件 | 低 |

### 10.2 自托管：langgraph.json + CLI

自托管要一个 `langgraph.json` 描述图：

```json
{
  "dependencies": ["."],
  "graphs": {
    "my_agent": "./agent.py:graph"
  },
  "env": ".env"
}
```

然后一条命令起服务：

```bash
# 装 CLI
pip install langgraph-cli
# 本地起服务，默认 8123 端口
langgraph dev
```

预期结果：终端打印本地地址，浏览器打开能看到你的图。

### 10.3 可视化：LangGraph Studio

Studio 是官方可视化工具。它能：

- 把图结构画出来，节点边一眼看清
- 单步执行，看每一步状态怎么变
- 直接对话调试 Agent

我排错基本靠它。比盲目加 print 强十倍。

### 10.4 可观测：LangSmith

图跑起来，你得知道它为啥这么走。

```bash
# 开追踪，把过程发到 LangSmith
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=你的KEY
```

LangSmith 能看完整调用链、每步耗时、Token 消耗。还能自动发现异常、提议修复。

> **核心建议**：上线前先接 LangSmith
> 没追踪的 Agent 像黑盒。出了问题你只能猜。接上追踪，问题看得见。

[向前桥接] 讲到这，技术都齐了。最后一章，聊聊认知。

---

## §11 写这本书时，我对 Agent 框架的认知变了

### 11.1 我以为框架越多越好

早些年我追新框架。这个火学这个，那个火学那个。

写这本书时我停下来想：框架解决的真的是"写不写得出来"吗？

不是。是"跑不跑得稳"。

### 11.2 我现在怎么看 LangGraph

它不替你想架构。它只保证：长流程不丢状态、能暂停、能恢复、能追。

这四点，恰恰是生产环境最贵的那部分。

我现在的判断很直接：

- 玩具 Demo，别用。
- 要上线的长流程 Agent，它是我首选。

### 11.3 给读者的三句话

第一，先把单智能体玩透，别急着多智能体。

第二，记忆和人机协同，是 Agent 和"脚本"的分界线。

第三，框架是工具，不是目的。能稳定解决问题的，就是好方案。

> **一句话总结**：最好的 Agent 不是用了最炫的框架，是用最合适的零件，真把事办成了。

---

## 附录 A 版本与生态速查（2026-07）

| 项目 | 版本 / 事实 | 备注 |
|------|-----------|------|
| langgraph 稳定版 | 1.2.8 | 2026-07-06 发布 |
| langgraph 1.0 | 2025-10 发布 | 首个稳定大版本 |
| langgraph 1.1 | 2026-03 | 类型安全流式/调用 v2 |
| langgraph 1.2 | 2026-05 | DeltaChannel、节点超时、错误恢复 |
| langgraph-supervisor | 0.0.31 | 多智能体层级编排 |
| langmem | 活跃维护 | 长期记忆与自我优化 |
| Deep Agents | 0.7.0（2026-07） | 上层 harness |
| Checkpointer | InMemory / Sqlite / Postgres | 短期记忆 |
| Store | InMemory / Postgres | 长期记忆 |

> **重点看**：第一行。
> 装依赖后先 `pip show langgraph` 确认 ≥ 1.0。

---

## 附录 B 常见坑与排查

**坑1：AI 不调工具**
原因：工具 docstring 太模糊。
解决：写清"何时调用 + 参数格式"，并在系统提示里强调"必须调工具"。

**坑2：无限循环调工具**
原因：工具返回信息 AI 看不懂，又去调。
解决：设 `recursion_limit`，工具返回写清"请用以上结果回答"。

**坑3：interrupt 用不了**
原因：没挂 Checkpointer。
解决：`compile(checkpointer=...)` 后再用 `interrupt()`。

**坑4：重启后记忆没了**
原因：用了 `InMemorySaver`。
解决：生产换 `SqliteSaver` 或 `PostgresSaver`。

**坑5：Postgres 报 thread_id 过长**
原因：thread_id 超 255 字符。
解决：用 `str(uuid.uuid4())`。

---

## 阅读指南

| 时间 | 章节 | 目标 |
|------|------|------|
| Day 1 | §01-§03 | 从零到跑通第一个 Agent |
| Day 2-3 | §04-§07 | 掌握图、工具、记忆、人机协同 |
| Day 4-5 | §08-§10 | 多智能体、Functional API、部署 |
| Day 6 | §11 + 附录 | 沉淀认知，查坑 |

---

**标叔出品** | AI Native Coder · 独立开发者
公众号「标叔」| B站「Liangdabiao」
代表作：Claude Code 从入门到精通 · OpenClaw 橙皮书 · Hermes Agent 从入门到精通
