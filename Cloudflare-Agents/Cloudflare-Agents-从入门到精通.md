# Cloudflare Agents 从入门到精通

Ship a Stateful AI Agent on the Global Edge in One Afternoon

**创建者**: 标叔

**为谁创建**: 想把想法变成可上线 AI Agent 的独立开发者、产品经理、AI 副业玩家

**基于**: Cloudflare Agents（`agents` SDK，含 `McpAgent`/`AIChatAgent`/`AgentWorkflow`/`runFiber`），GitHub `cloudflare/agents`

**最后更新**: 2026-07-08

**适用场景**: 从 0 部署一个有状态、能记忆、能定时、能接真实世界的生产级 AI Agent。只写业务逻辑，运行时、存储、调度、观测 Cloudflare 兜底

---

> 这本书讲一件事：怎么用 Cloudflare Agents，把你脑子里的 Agent 想法，变成一个个"活着的"、有身份、有记忆、能自己跑任务的对象。
>
> 我研究这个 SDK 的第一天下午，就跑通了一个断电重启还能接着聊的 Agent。没填任何大模型 Key。这件事值得写一本书。

## 阅读指南

| 时间 | 章节 | 目标 |
|------|------|------|
| Day 1 | §01-§03 | 从零到第一次跑通 |
| Day 2-3 | §04-§07 | 掌握核心能力（模型、状态、工具、观测） |
| Day 4-5 | §08-§14 | 进阶实战（聊天、部署、调度、持久执行） |
| Day 6 | §15-§23 | 工具与渠道（浏览器、沙箱、MCP、RAG、支付、邮件、语音） |
| Day 7 | §24-§28 | 生产化、对比与思维转变 |

---

## Part 1: 起步

从零到一。读完这 Part，你能不写一行业务代码，把一个有状态 Agent 部署上线。

## §01 Cloudflare Agents 把"有状态 Agent"这件事托住了

### 01.1 我帮朋友搭客服 Agent 那三周

去年我帮一个朋友做客服 Agent。第一周全花在搭骨架。要写 SSE 流式输出。要处理会话存储。要接模型 Key。要管工具调用状态。

真正写业务逻辑，是第三周的事。最气的是：这套骨架，每个做 Agent 的人都得过一遍。

### 01.2 它到底托住了什么

先给结论：Cloudflare Agents 把"运行沙箱、对话状态、实时连接、任务调度、模型调用、MCP、可观测"这些通用能力提前打通了。你只填业务逻辑。

但它托住的方式，和 EdgeOne Makers 不一样。这一节先把这层说清。

| 维度 | EdgeOne Makers | Cloudflare Agents | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| 形态 | 托管平台（控制台点一点） | SDK + 全球运行时 | 一个偏"用"，一个偏"写" |
| 状态 | 平台托管记忆 | 每个 Agent 自带 SQLite | Cloudflare 把状态焊死在对象里 |
| 模型 | 统一模型网关 | Workers AI 免 Key + AI Gateway | 都不锁死供应商 |
| 框架 | 不锁框架 | `agents` SDK，TS 一等公民 | Cloudflare 更"代码优先" |
| 调度 | 平台定时任务 | `schedule()` 内建 | Cloudflare 调度在对象内 |
| 支付 | 无内建 | x402 / MPP 内建 | Cloudflare 独一份 |
| 国内访问 | 腾讯云，备案友好 | 全球网络，国内需加速器 | 看你的用户在哪 |

> **重点看**：最后两行"支付"和"国内访问"。
>
> 这两件事决定了你该选哪个平台。用户在国内、要备案，EdgeOne 更顺。要全球分发、要 Agent 自己付钱，Cloudflare 更狠。

### 01.3 它最核心的一句定义

文档原话：Agents are **persistent, stateful execution environments**，powered by Cloudflare Durable Objects。

翻译成人话：每个 Agent 是一个"长命的、有状态的对象"。它有身份证（name）、有私有数据库（SQLite）、有实时连接、会自己定时干活、空闲了就休眠、不占你一分钱。

> **标叔的经验**：我见过太多人把 Agent 当成"一个函数"。在 Cloudflare 上，Agent 是一个"对象"。这个认知差，决定了你能不能写出真正会记忆的东西。

### 01.4 它不是什么

它不锁你的模型框架。AI SDK、OpenAI SDK、Anthropic SDK、Workers AI 都能用。TS、JS 都能写。

但它是代码优先的。你要会 `npm`、会 `wrangler`。这点和 EdgeOne 的"控制台点一点"不同。

> **核心建议**：如果你连命令行都抗拒，先去 EdgeOne Makers。如果你享受写代码、要全球部署、要深度控制，Cloudflare Agents 更对味。

装好认知，下一章我们 10 分钟跑通第一个 Agent。

## §02 10 分钟跑通你的第一个 Agent

上周我第一次点开官方 Starter。三行命令，一个能计数、能实时同步的 Agent 就上线了。我当场决定，这一章就讲这个最快的路。

### 02.1 你需要什么

装好 Node 24+。有一个 Cloudflare 账号（免费层够跑通）。不用装任何 IDE 插件。不用写代码。

### 02.2 我们最终要做成什么

一个能打开链接就对话、点击按钮就改数字、多人同时看到变化、断电重启数字还在的计数器 Agent。

### 02.3 用 Starter 模板起项目

```bash
# 这一行拉取官方 agents-starter 模板
npm create cloudflare@latest -- --template cloudflare/agents-starter
cd my-agent
npm install
```

预期结果：目录里出现 `src/server.ts`（你的 Agent 代码）、`src/client.tsx`（前端）、`wrangler.jsonc`（配置）。

### 02.4 把 server.ts 换成计数器

```typescript
import { Agent, routeAgentRequest, callable } from "agents";

// 定义状态的形状
type CounterState = { count: number };

export class Counter extends Agent<Env, CounterState> {
  // 新实例的默认状态
  initialState: CounterState = { count: 0 };

  // @callable 标记的方法，客户端能直接调
  @callable()
  increment() {
    this.setState({ count: this.state.count + 1 });
    return this.state.count;
  }

  @callable()
  decrement() {
    this.setState({ count: this.state.count - 1 });
    return this.state.count;
  }
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext) {
    // 路由请求到对应的 Agent 实例
    return (
      (await routeAgentRequest(request, env)) ??
      new Response("Not found", { status: 404 })
    );
  }
};
```

### 02.5 在 wrangler.jsonc 里登记 Agent

```jsonc
{
  "name": "my-agent",
  "main": "src/server.ts",
  "compatibility_date": "2025-01-01",
  "compatibility_flags": ["nodejs_compat"],
  "durable_objects": {
    "bindings": [{ "name": "Counter", "class_name": "Counter" }]
  },
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["Counter"] }]
}
```

> **注意**：`Counter` 必须同时出现在 `durable_objects.bindings` 和 `migrations.new_sqlite_classes`。漏一个，运行时报 `No such Durable Object class`。这是新手第一坑。

### 02.6 启动，看它活过来

```bash
npm run dev
```

打开 `http://localhost:5173`。点按钮，数字变。开两个浏览器标签，一个加，另一个也跟着变。这就是实时同步。

> **标叔的经验**：第一次看到两个标签页数字同步的那一刻，我明白了 Cloudflare Agents 的精髓——状态是"对象级"的，不是"请求级"的。

### 02.7 发生了什么

你点按钮时：客户端经 WebSocket 调 `agent.stub.increment()` → Agent 跑 `increment()`，`setState()` 把数字写进 SQLite → 状态广播给所有连接 → React 重渲染。

```
┌─────────────┐         ┌─────────────┐
│   Browser   │◄───────►│    Agent    │
│  (React)    │   WS    │  (Counter)  │
└─────────────┘         └──────┬──────┘
                               │
                        ┌──────▼──────┐
                        │   SQLite    │
                        │  (State)    │
                        └─────────────┘
```

关掉页面，再打开。数字还在。这就是休眠与唤醒。

装好第一个 Agent，下一章我们把开发环境配齐。

## §03 装好你的开发环境

### 03.1 三个硬前提

第一，Node 要 24+。Cloudflare Agents 的 dev 工具链认新版本。

第二，`wrangler` 是命令行核心。它负责本地开发、配置校验、部署上线。

第三，装饰器。Agent 用 `@callable()` 这类 TC39 标准装饰器。别开 `experimentalDecorators`，会静默破坏它。

### 03.2 tsconfig 与 vite 必配项

Starter 已经配好。手动建项目时，这两段不能少：

```json
// tsconfig.json —— 继承 agents 的推荐配置
{ "extends": "agents/tsconfig" }
```

```typescript
// vite.config.ts —— agents() 插件处理装饰器转译
import { cloudflare } from "@cloudflare/vite-plugin";
import react from "@vitejs/plugin-react";
import agents from "agents/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [agents(), react(), cloudflare()]
});
```

> **注意**：如果看到 `@callable()` 方法调不动、报 `Method X is not callable`，九成是装饰器没转译对。检查 `agents()` 插件在不在、tsconfig 有没有继承 `agents/tsconfig`。

### 03.3 本地配置与密钥

本地开发，`wrangler dev` 读 `.env`。生产密钥用：

```bash
wrangler secret put OPENAI_API_KEY
```

非敏感变量放 `wrangler.jsonc` 的 `vars`，值必须是字符串，代码里自己 `parseInt`。

> **核心建议**：`.env` 一定加进 `.gitignore`。密钥进了 Git 历史，比 Agent 崩了还难收拾。

环境配齐了。下一章进核心能力——先讲模型怎么接。

---

## Part 2: 核心能力

深入 Cloudflare Agents 的关键能力，每章一个核心概念。

## §04 模型接入：Workers AI 免 Key，AI Gateway 路由任意供应商

### 04.1 免 Key 是第一步惊喜

Cloudflare 自带 Workers AI。Starter 默认就用它。你不用申请任何 Key，直接调。

```typescript
import { Agent } from "agents";
import { streamText } from "ai";
import { createWorkersAI } from "workers-ai-provider";

export class MyAgent extends Agent {
  async onRequest(request: Request) {
    const workersai = createWorkersAI({ binding: this.env.AI });
    const { text } = await generateText({
      model: workersai("@cf/moonshotai/kimi-k2.7-code"),
      prompt: "Build me an AI agent on Cloudflare Workers",
    });
    return Response.json({ modelResponse: text });
  }
}
```

wrangler 里加一个 `ai` binding 就行：

```jsonc
{ "ai": { "binding": "AI" } }
```

### 04.2 想换供应商？AI SDK 一行搞定

Workers AI 不够用？换 OpenAI、Anthropic、Gemini 都行。底层用 AI SDK 统一接口。

```typescript
import { openai } from "@ai-sdk/openai";

const { text } = await generateText({
  model: openai("gpt-4o"),
  prompt: "Build me an AI agent on Cloudflare Workers",
});
```

### 04.3 真正的杀手锏：AI Gateway 路由

这一层和 EdgeOne 的"统一模型网关"思路一致。你可以在 AI Gateway 里做供应商路由、评估、限流、缓存。

```typescript
const response = await this.env.AI.run(
  "@cf/deepseek-ai/deepseek-r1-distill-qwen-32b",
  { prompt: "Build me a Cloudflare Worker that returns JSON." },
  {
    gateway: {
      id: "{gateway_id}",   // 你的网关 ID
      skipCache: false,
      cacheTtl: 3360,
    },
  }
);
```

| 维度 | Workers AI 直连 | 走 AI Gateway | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| 配置 | 加 `ai` binding | 加 gateway id | 都要配 |
| 路由 | 写死模型 | 按规则换供应商 | Gateway 更灵活 |
| 缓存/限流 | 无 | 内建 | 生产用 Gateway |
| 适用 | 快速验证 | 正式上线 | 先直连后 Gateway |

> **重点看**：最后一行。我建议先用 Workers AI 跑通，再接 AI Gateway 上生产。别一上来就配网关，容易卡在配置上。

### 04.4 流式输出

大模型慢，别缓冲。直接流式吐给客户端。WebSocket 或 SSE 都行。

```typescript
const result = streamText({
  model: workersai("@cf/zai-org/glm-4.7-flash"),
  prompt: userPrompt,
});
for await (const chunk of result.textStream) {
  if (chunk) connection.send(JSON.stringify({ type: "chunk", content: chunk }));
}
```

模型这块讲完了。下一章讲状态——Cloudflare Agents 最硬的底子。

## §05 对话状态：每个 Agent 自带 SQLite，断线续跑

### 05.1 先给结论

Cloudflare Agents 的状态，存在每个 Agent 实例私有的 SQLite 里。它自动持久化、跨客户端实时同步、重启后还在。

这点比 EdgeOne 的"平台托管记忆"更底层——你拿到的不是黑盒记忆，而是一整张能写 SQL 的表。

### 05.2 三种操作

```typescript
export class ChatAgent extends Agent<Env, { messages: any[]; count: number }> {
  // 1. 初始状态：新实例的默认值
  initialState = { messages: [], count: 0 };

  // 2. 读状态
  onRequest() {
    return Response.json(this.state);
  }

  // 3. 改状态：自动落盘 + 广播
  addMessage(msg: any) {
    this.setState({ ...this.state, messages: [...this.state.messages, msg] });
  }
}
```

### 05.3 状态不是普通变量

`setState` 会：写进 SQLite、广播给所有连接、触发 `onStateChanged`。直接改 `this.state` 不生效。

```typescript
// 对的
this.setState({ count: this.state.count + 1 });

// 错的：改动不会落盘，也不会广播
this.state.count = this.state.count + 1;
```

| 维度 | `this.state` 直改 | `this.setState()` | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| 持久化 | 否 | 是 | 永远用 setState |
| 广播 | 否 | 是 | setState 才同步 |
| 类型安全 | 有（泛型） | 有（泛型） | 都用泛型 |

### 05.4 直接写 SQL

状态是 JSON 存的。要复杂查询？直接用 `this.sql`，模板标签，类型安全。

```typescript
type User = { id: string; name: string };
const [user] = this.sql<User>`SELECT * FROM users WHERE id = ${userId}`;
```

> **标叔的经验**：小状态用 `setState`，结构化数据用 `this.sql`。我做一个游戏房 Agent，玩家列表用 setState，排行榜用 SQL 表。各司其职。

### 05.5 校验状态

敏感状态，加一道关卡。`validateStateChange` 在落盘前跑，抛错就拒绝。

```typescript
validateStateChange(next: GameState) {
  if (next.score < 0) throw new Error("score cannot be negative");
}
```

状态这块是 Cloudflare Agents 的立身之本。下一章讲工具——让 Agent 真的能"动手"。

## §06 工具调用：把能力拆成工具

### 06.1 聊天 Agent 的工具三态

`AIChatAgent` 上，工具分三种：服务端工具（有 `execute`）、客户端工具（无 `execute`）、审批工具（服务端 + `needsApproval`）。

```typescript
import { AIChatAgent } from "@cloudflare/ai-chat";
import { streamText, tool, convertToModelMessages, stepCountIs } from "ai";
import { z } from "zod";

export class ChatAgent extends AIChatAgent {
  async onChatMessage() {
    const workersai = createWorkersAI({ binding: this.env.AI });
    const result = streamText({
      model: workersai("@cf/moonshotai/kimi-k2.7-code"),
      messages: await convertToModelMessages(this.messages),
      tools: {
        getWeather: tool({
          description: "Get weather for a city",
          inputSchema: z.object({ city: z.string() }),
          execute: async ({ city }) => fetchWeather(city), // 服务端执行
        }),
      },
      stopWhen: stepCountIs(5), // 最多 5 步，防止死循环
    });
    return result.toUIMessageStreamResponse();
  }
}
```

### 06.2 客户端工具：让浏览器动手

有些事只能在浏览器做，比如拿定位。服务端只声明 schema，不写 `execute`。

```typescript
// 服务端：只描述，不实现
tools: {
  getLocation: tool({
    description: "Get the user's location from the browser",
    inputSchema: z.object({}),
    // 没有 execute —— 客户端处理
  });
}
```

```tsx
// 客户端：用 onToolCall 补上实现
const { messages, sendMessage } = useAgentChat({
  agent,
  onToolCall: async ({ toolCall, addToolOutput }) => {
    if (toolCall.toolName === "getLocation") {
      const pos = await new Promise((r) => navigator.geolocation.getCurrentPosition(r));
      addToolOutput({ toolCallId: toolCall.toolCallId, output: { lat: pos.coords.latitude } });
    }
  },
});
```

| 类型 | 在哪执行 | 典型用途 | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| 服务端工具 | Worker | 查库、调 API | 主力 |
| 客户端工具 | 浏览器 | 定位、DOM | 善用浏览器能力 |
| 审批工具 | 服务端 | 付款、删号 | 危险操作必加 |

### 06.3 消息历史自动持久化

`AIChatAgent` 把聊天记录存进 SQLite，`maxPersistedMessages` 只限制存多少条，不影响发给模型的消息数。

```typescript
export class ChatAgent extends AIChatAgent {
  maxPersistedMessages = 200; // 仅限存储，不裁剪发给 LLM 的
}
```

> **注意**：想控制发给模型的 token，用 AI SDK 的 `pruneMessages()`，不是这个字段。这俩经常被人搞混。

工具讲完一半。MCP 这种"工具的标准化形态"，我们放到 §17 专章讲。下一章先讲怎么看清 Agent 在干什么。

## §07 可观测性：内置追踪、指标、日志

### 07.1 先给结论

Cloudflare Agents 内置了一套事件系统。RPC 调用、状态变更、调度执行、工作流流转、MCP 连接——全有结构化的事件。没人听的时候零开销。

### 07.2 事件长什么样

```typescript
{
  type: "rpc",            // 发生了什么
  agent: "MyAgent",       // 哪个类
  name: "user-123",       // 哪个实例（DO name）
  payload: { method: "getWeather" },
  timestamp: 1758005142787
}
```

### 07.3 本地订阅看事件

```typescript
import { subscribe } from "agents/observability";

const unsub = subscribe("rpc", (event) => {
  if (event.type === "rpc") console.log(`RPC call: ${event.payload.method}`);
  if (event.type === "rpc:error") console.error(`RPC failed: ${event.payload.error}`);
});
```

### 07.4 生产用 Tail Worker

生产环境不用在 Agent 里写订阅。挂一个 Tail Worker，自动收到所有诊断事件。

```typescript
export default {
  async tail(events) {
    for (const event of events) {
      for (const msg of event.diagnosticsChannelEvents) {
        // msg.channel 是 "agents:rpc"、"agents:workflow" ...
        console.log(msg.timestamp, msg.channel, msg.message);
      }
    }
  },
};
```

| 维度 | 本地 subscribe | 生产 Tail Worker | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| 接入成本 | 改代码 | 挂一个 Worker | 生产用 Tail |
| 热路径开销 | 零（没人听就静默） | 零（平台转发） | 都不拖慢 |
| 适用 | 调试 | 监控告警 | 两个都配 |

> **核心建议**：开发期用 `subscribe` 抓 bug，上线用 Tail Worker 接日志系统。别把调试代码留生产。

可观测这块讲完。下一 Part 进进阶实战，先拆一个真实聊天 Agent。

---

## Part 3: 进阶实战

从模板到真实项目，把能力串起来。

## §08 从模板到真实项目：聊天 Agent 拆解

### 08.1 我们要做什么

做一个能聊天、有记忆、会调天气工具、危险操作要你确认的 Agent。这就是 Starter 模板里 `ChatAgent` 的真身。

### 08.2 服务端骨架

```typescript
import { AIChatAgent } from "@cloudflare/ai-chat";
import { createWorkersAI } from "workers-ai-provider";
import { streamText, convertToModelMessages, tool, stepCountIs } from "ai";
import { z } from "zod";

export class ChatAgent extends AIChatAgent {
  async onChatMessage() {
    const workersai = createWorkersAI({ binding: this.env.AI });
    const result = streamText({
      model: workersai("@cf/moonshotai/kimi-k2.7-code"),
      messages: await convertToModelMessages(this.messages),
      tools: {
        getWeather: tool({
          description: "Get weather for a city",
          inputSchema: z.object({ city: z.string() }),
          execute: async ({ city }) => fetchWeather(city),
        }),
        processPayment: tool({
          description: "Process a payment",
          inputSchema: z.object({ amount: z.number(), recipient: z.string() }),
          needsApproval: async ({ amount }) => amount > 100, // 超 100 要批
          execute: async ({ amount, recipient }) => charge(amount, recipient),
        }),
      },
      stopWhen: stepCountIs(5),
    });
    return result.toUIMessageStreamResponse();
  }
}
```

### 08.3 wrangler 配置

```jsonc
{
  "ai": { "binding": "AI" },
  "durable_objects": {
    "bindings": [{ "name": "ChatAgent", "class_name": "ChatAgent" }]
  },
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["ChatAgent"] }]
}
```

> **注意**：`AIChatAgent` 用 SQLite 存消息和流式缓冲，`new_sqlite_classes` 是必选项。漏了，对话历史不落盘。

### 08.4 客户端连上

```tsx
import { useAgentChat } from "@cloudflare/ai-chat/react";

const { messages, sendMessage, addToolApprovalResponse } = useAgentChat({ agent: "ChatAgent" });
```

`useAgentChat` 返回 `messages`、`sendMessage`、`clearHistory`、`addToolOutput`、`addToolApprovalResponse` 等。一个 hook 管全了。

> **标叔的经验**：我第一次把 `needsApproval` 加上去，看到前端弹出"是否批准付款"的按钮，才真正觉得这是生产级。安全不是事后补，是内建的。

聊天 Agent 拆完了。下一章讲怎么把它配好、部署到全球。

## §09 配置与部署：wrangler.jsonc 与全球网络

### 09.1 配置是地基

`wrangler.jsonc` 一个文件管全部。我把它拆成必填和可选。

```jsonc
{
  "name": "my-agent-app",
  "main": "src/server.ts",
  "compatibility_date": "2025-01-01",
  "compatibility_flags": ["nodejs_compat"],   // 必需！

  "durable_objects": {
    "bindings": [
      { "name": "Counter", "class_name": "Counter" },
      { "name": "ChatAgent", "class_name": "ChatAgent" }
    ]
  },
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["Counter", "ChatAgent"] }],

  "ai": { "binding": "AI" },
  "vars": { "API_BASE_URL": "https://api.example.com" }
}
```

### 09.2 多 Agent 怎么配

入口文件 export 多个类，每个类一条 binding + 一条 `new_sqlite_classes`。

```jsonc
"durable_objects": {
  "bindings": [
    { "name": "Counter", "class_name": "Counter" },
    { "name": "ChatRoom", "class_name": "ChatRoom" }
  ]
},
"migrations": [{ "tag": "v1", "new_sqlite_classes": ["Counter", "ChatRoom"] }]
```

### 09.3 迁移三件套

类改名、删类，靠 migrations 版本号管。

```jsonc
"migrations": [
  { "tag": "v1", "new_sqlite_classes": ["OldName"] },
  { "tag": "v2", "renamed_classes": [{ "from": "OldName", "to": "NewName" }] },
  { "tag": "v3", "deleted_classes": ["AgentToDelete"] }
]
```

| 字段 | 用途 | 标叔的提醒 |
| ---- | ---- | ---- |
| new_sqlite_classes | 新建带存储的类 | 漏了不落盘 |
| renamed_classes | 改名 | 代码/binding/导出三处同步改 |
| deleted_classes | 删除 | 数据永久没，谨慎 |

### 09.4 部署与区域

```bash
npm run deploy
```

一条命令，Agent 上线到 Cloudflare 全球网络。你可以给实例指定运行区域，降延迟：

```typescript
const agent = await getAgentByName(env.MyAgent, "instance", {
  locationHint: "enam", // wnam|enam|sam|apac ...
});
```

要数据驻留欧盟？加 `jurisdiction: "eu"`。GDPR 合规直接满足。

> **核心建议**：默认让它全球跑。只有延迟敏感或合规要求，才显式指定区域和辖区。别过度优化。

部署讲完。下一章聊一个心态：你只写业务逻辑。

## §10 你只写业务逻辑，这事本身就是生产力

### 10.1 脚手架不是业务

回头看 §02 的计数器。真正的业务逻辑，只有 `increment` 和 `decrement` 两行。其余——WebSocket、状态落盘、广播、休眠唤醒——全是 SDK 的。

### 10.2 对比一下成本

| 活儿 | 自己从零 | Cloudflare Agents | 省下 |
| ---- | ------- | -------------- | ---- |
| 流式对话 | 自己写 SSE | `toUIMessageStreamResponse()` | 几天 |
| 对话记忆 | 自己接 DB | SQLite 内建 | 一个 DB |
| 模型切换 | 改代码重部署 | 改 binding | 一次发布 |
| 定时任务 | 自己搭调度 | `schedule()` | 一套 cron 服务 |
| 全球部署 | 自己买机器 | `npm run deploy` | 运维人力 |

> **重点看**：最后一列。这些不是"功能多"，是"你不用做的事多"。Agent 开发的生产力，藏在"不写"里。

### 10.3 标叔的结论

平台不锁框架，比"功能多"更值钱。Cloudflare Agents 把运行时、存储、调度、观测解耦了，你就剩业务逻辑。这才是它最狠的地方。

心态定了。下一 Part 进更深一层：边缘运行时与持久执行。

---

## Part 4: 进阶篇

Durable Objects、调度、子 Agent、长任务。这一 Part 是 Cloudflare 的护城河。

## §11 Durable Objects 与边缘运行时：在离用户最近的地方算

### 11.1 Agent 的本质

`Agent` 继承自 Durable Object。它就是一个有状态、单实例、全球可寻址的对象。

每个 `name` 对应一个实例。`Counter:user-123` 和 `Counter:user-456` 是两个独立对象，各有各的 SQLite。

### 11.2 生命周期方法

```typescript
class MyAgent extends Agent {
  async onStart() { /* DO 启动，fetch/RPC 之前 */ }
  async onRequest(request: Request) { return new Response("hi"); }
  async onConnect(conn, ctx) { conn.send("connected"); }
  async onMessage(conn, msg) { /* WebSocket 消息 */ }
  async onStateChanged(state, source) { /* 状态变了 */ }
  onError(e) { console.error(e); }
  async cleanup() { await this.destroy(); }
}
```

### 11.3 休眠与唤醒

没客户端连、没定时任务时，Agent 休眠，不占资源不花钱。下次请求唤醒，状态从 SQLite 读回。

> **标叔的经验**：我做一个"每日星座"Agent，平时零成本躺着。只有用户打开或 cron 触发才醒。账单好看。

### 11.4 边缘的含义

你的 Agent 跑在离用户最近的 Cloudflare 节点。状态也在那。计算和状态同置，延迟极低。

| 维度 | 传统服务器 | Cloudflare DO | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| 位置 | 单区域 | 全球边缘 | 用户就近 |
| 扩缩 | 手动 | 自动到百万实例 | 省心 |
| 成本（空闲） | 照收 | 零 | 真零 |

运行时讲完。下一章让 Agent 会"自己定时干活"。

## §12 调度与队列：让 Agent 真正自动跑起来

### 12.1 四种调度模式

底层用 Durable Object alarm，任务持久化进 SQLite，重启不丢。

| 模式 | 语法 | 用例 |
| ------ | ------ | ------ |
| 延迟 | `schedule(60, ...)` | 60 秒后 |
| 定时 | `schedule(new Date(...), ...)` | 指定时刻 |
| Cron | `schedule("0 8 * * *", ...)` | 每天 8 点 |
| 间隔 | `scheduleEvery(30, ...)` | 每 30 秒 |

### 12.2 一个提醒 Agent

```typescript
export class ReminderAgent extends Agent {
  async onRequest(request: Request) {
    // 30 秒后发提醒
    await this.schedule(30, "sendReminder", { message: "Check email" });
    // 每天 8 点发日报
    await this.schedule("0 8 * * *", "dailyDigest", { userId: "u1" });
    return new Response("Scheduled!");
  }

  async sendReminder(payload: any) { console.log(payload.message); }
  async dailyDigest(payload: any) { /* 生成并发送 */ }
}
```

### 12.3 管理调度

```typescript
const all = await this.listSchedules();              // 全部
const cron = await this.listSchedules({ type: "cron" }); // 只 cron
await this.cancelSchedule(scheduleId);               // 取消
```

### 12.4 队列：瞬时高并发

调度是"未来某刻跑一次"。队列是"现在塞进去，按顺序跑"。

```typescript
await this.queue("processTask", { taskId: "123" });
// 回调：async processTask(payload) { ... }
```

| 维度 | schedule | queue | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| 语义 | 定时/延迟 | 异步入队 | 看要不要定时 |
| 重叠保护 | 间隔内建 | 顺序消费 | 队列防挤兑 |
| 典型 | 日报、提醒 | 批量任务 | 各用各的 |

> **核心建议**：cron 放 `onStart()` 里设，利用幂等避免重启重复创建。调度是 Agent 自动化的起点。

调度讲完。下一章讲怎么把一个大 Agent 拆成一群小 Agent。

## §13 子 Agent 与 Agent 工具：分而治之

### 13.1 什么是子 Agent（facet）

子 Agent 是和父同机的子 Durable Object。它有自己的 SQLite、自己的 WebSocket，但由父派生、列举、销毁。像"主聊天室"下的"每个会话"。

### 13.2 创建与回连父

```typescript
export class Inbox extends Agent {
  @callable()
  async createChat() {
    const id = crypto.randomUUID();
    await this.subAgent(Chat, id); // 惰性、幂等地建子
    return id;
  }

  @callable()
  listChats() { return this.listSubAgents(Chat); }
}

export class Chat extends Agent {
  async say(text: string) {
    const inbox = await this.parentAgent(Inbox); // 回连直接父
    await inbox.recordTurn(this.name, text);
  }
}
```

### 13.3 客户端直连子

```tsx
const chat = useAgent({
  agent: "Inbox", name: userId,
  sub: [{ agent: "Chat", name: chatId }], // URL: /agents/inbox/{uid}/sub/chat/{cid}
});
```

### 13.4 Agent 工具：把子 Agent 当工具调

除 facet 外，Agents SDK 还能把一个聊天型子 Agent 注册成"工具"，父在 agentic loop 里调用它，子流的思考过程可流式回传。适合"研究员 Agent 被主 Agent 调度"这类编排。

| 维度 | facet 子 Agent | Agent 工具 | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| 关系 | 父子对象 | 工具调用 | 看要不要回传过程 |
| 状态 | 独立 SQLite | 独立 SQLite | 都隔离 |
| 典型 | 多租户隔离 | 多专家协作 | 编排选工具 |

> **注意**：父可用 `onBeforeSubAgent` 钩子拦截 `/sub/` 请求做鉴权。别让任意子路径都能建。

子 Agent 讲完。下一章讲长任务怎么不断点。

## §14 长任务与持久执行：Fiber 断点续跑

### 14.1 问题：DO 会被驱逐

Durable Object 会因闲置（约 70–140 秒）、代码更新、alarm 超时（15 分钟）被赶走。长任务跑一半被踢，怎么办？

### 14.2 runFiber：可中断可恢复

`runFiber` 执行前在 SQLite 登记，执行中持有心跳，用 `ctx.stash()` 写检查点。被驱逐后，下次激活触发 `onFiberRecovered`。

```typescript
class MyAgent extends Agent {
  async doWork() {
    await this.runFiber("my-task", async (ctx) => {
      const step1 = await expensiveOperation();
      ctx.stash({ step1 });                 // 检查点
      const step2 = await anotherOp(step1);
      this.setState({ ...this.state, result: step2 });
    });
  }

  async onFiberRecovered(ctx) {
    if (ctx.name !== "my-task") return;
    const snap = ctx.snapshot as { step1: unknown } | null;
    if (snap) {
      const step2 = await anotherOp(snap.step1); // 从检查点续
      this.setState({ ...this.state, result: step2 });
    }
  }
}
```

### 14.3 长任务不丢进度

客户端断开？Agent 继续跑。重连？从 SQLite 读回进度接着发。AIChatAgent 的流式输出也有自动续传。

```typescript
// 长效任务：启动-休眠-回调 模式
await this.runFiber("research", async (ctx) => {
  const steps = ["search", "analyze", "synthesize"];
  const completed: string[] = [];
  for (const step of steps) {
    await executeStep(step);
    completed.push(step);
    ctx.stash({ completed }); // 每步存盘
  }
});
```

| 维度 | 普通 async | runFiber | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| 被驱逐 | 进度丢 | 检查点续 | 长任务必用 |
| 客户端断开 | 可能中断 | 继续跑 | 体验好 |
| 复杂度 | 低 | 中 | 值 |

> **注意**：`stash()` 每次完全替换快照（不是 merge）。恢复逻辑必须写在 `onFiberRecovered`，原 lambda 不可重放。

持久执行讲完。下一 Part 进工具与渠道：浏览器、沙箱、MCP、RAG、支付。

---

## Part 5: 最佳实践篇

把 Agent 的能力往外扩：让它真的会"看"、会"跑代码"、会"接外部世界"。

## §15 浏览器工具：让 Agent 真的会"看"网页

### 15.1 问题：静态 HTML 抓不到

很多内容要 JS 跑完才出现。Agent 不能只发个 HTTP GET。它得开真浏览器。

### 15.2 browser_execute：让模型写 CDP 代码

Cloudflare 的浏览器工具不给你固定的"点击/截图"动作集。它让模型写代码，经沙箱跑 CDP 命令操作真实浏览器。

```typescript
import { createBrowserTools } from "agents/browser/ai";

const browserTools = createBrowserTools({
  ctx: this.ctx,
  browser: this.env.BROWSER,
  loader: this.env.LOADER,
});

const result = streamText({
  model, system: "You can browse the web and inspect pages.",
  messages: await convertToModelMessages(this.messages),
  tools: { ...browserTools },
  stopWhen: stepCountIs(10),
});
```

wrangler 要加两个 binding，入口导出运行时类：

```jsonc
{ "browser": { "binding": "BROWSER" }, "worker_loaders": [{ "binding": "LOADER" }] }
```

```typescript
export { CodemodeRuntime } from "agents/browser";
```

### 15.3 三种会话模式

| 模式 | 含义 | 标叔的建议 |
| ---- | ---- | ---- |
| one-shot | 每次新会话 | 默认，最干净 |
| reuse | 命名共享 | 要登录态持续用 |
| dynamic | 可提升为共享 | 要登录后再继续 |

### 15.4 无状态快读

只要 `browser` binding，不用 DO，就能做 markdown/extract/links/scrape：

```typescript
import { createQuickActionTools } from "agents/browser/ai";
const tools = createQuickActionTools({ browser: this.env.BROWSER });
// browser_markdown, browser_extract, browser_links, browser_scrape
```

> **注意**：沙箱里禁止 `fetch` 外部网络；CDP 调用必须顺序（不能 `Promise.all`），否则重放日志乱序。Live View 链接约 5 分钟有效，可配合人工登录/CAPTCHA 审批。

浏览器讲完。下一章让 Agent 能跑任意代码。

## §16 沙箱与代码执行：跑任意代码

### 16.1 什么时候要沙箱

模型生成的代码、Python 脚本、要装包的数据分析——这些不能跑在 Worker 隔离区里。要隔离容器。

### 16.2 getSandbox：容器里跑命令

沙箱基于 Cloudflare Containers，暴露文件系统、shell、语言运行时。

```typescript
import { getSandbox } from "@cloudflare/sandbox";
export { Sandbox } from "@cloudflare/sandbox";

export class CodeAgent extends Agent {
  @callable()
  async runPython(code: string) {
    const sandbox = getSandbox(this.env.Sandbox, this.name);
    await sandbox.writeFile("/workspace/script.py", code);
    const r = await sandbox.exec("python3 /workspace/script.py");
    this.setState({ lastOutput: r.stdout });
    return { stdout: r.stdout, stderr: r.stderr, exitCode: r.exitCode };
  }
}
```

```jsonc
"containers": [{ "class_name": "Sandbox", "image": "./Dockerfile", "instance_type": "lite", "max_instances": 1 }],
"durable_objects": { "bindings": [{ "name": "Sandbox", "class_name": "Sandbox" }] },
"migrations": [{ "tag": "v1", "new_sqlite_classes": ["Sandbox"] }]
```

### 16.3 Code Mode：让模型写可执行 TS

更高一层的玩法：模型不直接调工具，而是生成一段可执行 TypeScript，调用你的工具。这叫 Code Mode（`@cloudflare/codemode`）。适合"多工具编排"场景，模型自己决定怎么组合。

| 维度 | Sandbox 容器 | Code Mode | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| 用途 | 跑任意代码/装包 | 模型编排工具 | 看要跑啥 |
| 隔离 | 容器级 | Worker 沙箱 | 都隔离 |
| 典型 | 数据分析、构建 | 复杂多步任务 | 各取所需 |

> **核心建议**：临时文件、生成代码、日志放沙箱文件系统；用户可见进度和小元数据放 Agent 状态。别把大文件塞状态里。

沙箱讲完。下一章用 MCP 把能力接到外部世界。

## §17 用 MCP 把能力接到外部世界

### 17.1 MCP 是什么

Model Context Protocol，让 Agent 用标准方式接外部工具。Cloudflare Agents 两种都支持：当客户端、当服务器。

### 17.2 当客户端：连别人的 MCP

```typescript
export class ToolAgent extends Agent {
  async onStart() {
    await this.addMcpServer("github", "https://mcp.github.com/mcp");
  }
  async onRequest(request: Request) {
    const workersai = createWorkersAI({ binding: this.env.AI });
    const { text } = await generateText({
      model: workersai("@cf/zai-org/glm-4.7-flash"),
      prompt: "Summarize latest issue activity.",
      tools: this.mcp.getAITools(), // 把远程工具喂给模型
    });
    return Response.json({ text });
  }
}
```

要鉴权？`addMcpServer` 返回授权状态，连接持久化进 Agent 的 SQL。

### 17.3 当服务器：把自己的 Agent 暴露成 MCP

最简有状态 MCP Server，约 20 行：

```typescript
import { McpAgent } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

export class TinyMcp extends McpAgent {
  server = new McpServer({ name: "", version: "v1.0.0" });
  async init() {
    this.server.registerTool(
      "square",
      { description: "Squares a number", inputSchema: { number: z.number() } },
      async ({ number }) => ({ content: [{ type: "text", text: String(number ** 2) }] })
    );
  }
}
export default TinyMcp.serve("/"); // 整个 Worker 就这么一行
```

| 维度 | 当客户端 | 当服务器 | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| 目的 | 用别人工具 | 暴露自己能力 | 双向都重要 |
| 配置 | `addMcpServer` | `McpAgent.serve` | 都简单 |
| 状态 | 连接存 SQL | 每会话一个 DO | 都持久 |

> **注意**：无状态的 `createMcpHandler` 每次请求必须 `new` 一个 `McpServer` 实例——已连接的 server 不能重复挂 transport。这是新手第二坑。

MCP 讲完。下一章把知识库/RAG 交给托管。

## §18 AI 搜索与知识库：RAG 交给托管

### 18.1 你不用自己搭检索

想让 Agent 查产品文档、用户文件、内部知识库？AI Search 把索引、检索、可选的聊天补全全托管了。

### 18.2 两种用法

```typescript
// 1. 只检索
const instance = this.env.AI_SEARCH.get("my-instance");
const results = await instance.search({ messages: [{ role: "user", content: query }] });

// 2. 检索 + 生成答案
const resp = await instance.chatCompletions({
  messages: [{ role: "user", content: "How do I deploy an Agent?" }],
  model: "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
  ai_search_options: { retrieval: { max_num_results: 5 } },
});
```

wrangler 用 namespace binding：

```jsonc
"ai_search_namespaces": [{ "binding": "AI_SEARCH", "namespace": "default", "remote": true }]
```

| 维度 | 自己搭 RAG | Cloudflare AI Search | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| 向量库 | 自己装 | 托管 | 省一个组件 |
| 索引 | 自己写 | 托管 | 省心力 |
| 适用 | 极致定制 | 标准检索 | 先托管后自研 |

> **核心建议**：先做托管 AI Search，跑通再考虑自己接 Vectorize 做精细控制。别一上来就自建向量库。

RAG 讲完。下一 Part 进模型与智能体深潜：密钥、鉴权、工作流、支付。

---

## Part 6: 模型与智能体深潜

模型密钥、会话鉴权、工作流、人类在环、支付。

## §19 模型厂商密钥：用你自己的 Key 接任意大模型

### 19.1 自带 Key 的姿势

Workers AI 免 Key。但要调 OpenAI 的 GPT、Anthropic 的 Claude，用自己的 Key 就行。

```typescript
import { openai } from "@ai-sdk/openai";

const { text } = await generateText({
  model: openai("gpt-4o"),
  prompt: "Build me an AI agent.",
});
```

### 19.2 密钥存哪

生产：`wrangler secret put OPENAI_API_KEY`。本地：`.env`。别硬编码。

### 19.3 OpenAI 兼容端点

任何暴露 OpenAI 兼容 API 的服务都能调。比如直接调 Gemini：

```typescript
import { OpenAI } from "openai";
const client = new OpenAI({
  apiKey: this.env.GEMINI_API_KEY,
  baseURL: "https://generativelanguage.googleapis.com/v1beta/openai/",
});
```

| 维度 | Workers AI | 自带 Key 供应商 | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| Key | 无 | 你自己的 | 起步用内置 |
| 模型池 | Cloudflare 托管 | 全宇宙 | 要强的用自带 |
| 成本 | 按量 | 按供应商 | 看预算 |

> **重点看**：最后一行。我起步用 Workers AI 验证想法，要质量或特殊模型再换自带 Key。切换只改模型名，业务逻辑不动。

密钥讲完。下一章讲怎么记得住、管得严。

## §20 会话存储与鉴权：记得住、管得严

### 20.1 状态就是你的会话存储

前面 §05 讲了，Agent 状态存 SQLite，天然就是会话存储。每个 `name` 一个会话。

### 20.2 只读连接

不想让客户端改状态，只让看？用只读连接。客户端连上只能读，不能 `setState`、不能调 `@callable`。

### 20.3 跨域鉴权

Agent 要接外部系统（比如你的后端）？`cross-domain-authentication` 让你安全地让 Agent 代表用户调外部 API，用令牌转发。

### 20.4 安全清单

| 风险 | 做法 | 标叔的提醒 |
| ---- | ---- | ---- |
| 状态被乱改 | 只读连接 | 展示页用只读 |
| 子 Agent 乱建 | `onBeforeSubAgent` 校验 | 严格注册表 |
| 密钥泄露 | `wrangler secret` | 别进 Git |
| MCP 未授权 | OAuth / token | 公开 server 加鉴权 |

> **核心建议**：公开暴露的 Agent 和 MCP，默认当"会被攻击"来设计。最小权限，显式鉴权。

鉴权讲完。下一章讲工作流——多步、可恢复、可审批的管线。

## §21 工作流与人工审批：可恢复的多步管线

### 21.1 什么时候用 Workflow

任务超过 30 秒、多步、要自动重试、中间要人批一道——上 Workflow。

### 21.2 定义工作流

```typescript
import { AgentWorkflow } from "agents/workflows";

export class ProcessingWorkflow extends AgentWorkflow<MyAgent, TaskParams> {
  async run(event: AgentWorkflowEvent<TaskParams>, step: AgentWorkflowStep) {
    const params = event.payload;
    const result = await step.do("process-data", async () => processData(params.data)); // 持久+重试
    await this.reportProgress({ step: "process", status: "complete", percent: 0.5 });
    await step.do("save-results", async () => this.agent.saveResult(params.taskId, result));
    await step.reportComplete(result);
    return result;
  }
}
```

### 21.3 从 Agent 启动

```typescript
// Agent 内
const instanceId = await this.runWorkflow("PROCESSING_WORKFLOW", { taskId, data });

// wrangler 注册 workflow
"workflows": [{ "name": "processing-workflow", "binding": "PROCESSING_WORKFLOW", "class_name": "ProcessingWorkflow" }]
```

### 21.4 人工审批闸门

```typescript
const approvalData = await this.waitForApproval<{ approvedBy: string }>(step, { timeout: "7 days" });
// Agent 端：this.approveWorkflow(id, {...}) / this.rejectWorkflow(id, {...})
```

| 维度 | Schedule | Workflow | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| 语义 | 定时触发 | 多步持久管线 | 复杂流程用流 |
| 重试 | 回调级 | 步骤级幂等 | 流更稳 |
| 审批 | 无 | `waitForApproval` | 流有闸门 |

> **注意**：工作流可在子 Agent 内启动，但追踪记录在子 Agent 自己的 SQLite，父看不到。需要全局视图要自己汇总。

工作流讲完。下一章把"人类在环"四种模式一次讲清。

## §22 人类在环：审批流与四种模式

### 22.1 先给决策树

文档给了清晰的选型：

```
是Workflow多步？ ──是──▶ waitForApproval
   │否
是MCP服务器？ ──是──▶ elicitInput
   │否
是聊天交互？ ──是──▶ 要浏览器能力？ ──是──▶ onToolCall（客户端）
                         │否
                         └──▶ needsApproval（服务端）
    │否
简单确认 ──▶ State + WebSocket
```

### 22.2 聊天工具审批

```typescript
processPayment: tool({
  description: "Process a payment",
  inputSchema: z.object({ amount: z.number(), recipient: z.string() }),
  needsApproval: async ({ amount }) => amount > 100, // 超 100 要批
  execute: async ({ amount, recipient }) => charge(amount, recipient),
}),
```

客户端用 `addToolApprovalResponse` 回应批准或拒绝。被拒可改 `addToolOutput({ state: "output-error", errorText })` 给模型自定义原因。

### 22.3 MCP 内请求结构化输入

```typescript
const userInput = await this.server.server.elicitInput({
  message: "By how much do you want to increase the counter?",
  requestedSchema: { type: "object", properties: { amount: { type: "number" } }, required: ["amount"] },
}, { relatedRequestId: extra.requestId });
```

> **核心建议**：危险操作（付款、删号）一律加审批。审批不是体验负担，是上线底线。四种模式按决策树选，别混用。

人类在环讲完。下一章讲一个 Cloudflare 独一份的能力：让 Agent 自己付钱。

## §23 支付：让 Agent 自己付钱

### 23.1 为什么 Agent 要会付钱

传统接入要注册账号、绑卡、拿 API Key。Agent 程序化消费资源，这套流程卡死。Cloudflare 用 HTTP `402 Payment Required` 解决。

### 23.2 x402 与 MPP

两套都基于 `402`：

- **x402**（Coinbase 创立）：链上稳定币（USDC），三个 HTTP 头带挑战/凭证/回执。可甩给 facilitator 服务验单，服务器不用直连链。
- **MPP**（Stripe 等参与，IETF 标准轨道）：除链上，还支持卡、Lightning、稳定币，引入 session 做流式按量付。向后兼容 x402。

### 23.3 服务端收费

SDK 提供 `withX402`、`paidTool`（MCP 服务端）、`x402-hono`（HTTP Worker）。客户端 `withX402Client` 自动处理 402 并重试，可选人工确认。

| 维度 | x402 | MPP | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| 结算 | 稳定币 | 卡/币/稳定币 | MPP 更宽 |
| 标准 | x402 基金会 | IETF 轨道 | MPP 更正式 |
| 流式 | 无 | session 按量 | 流式选 MPP |

> **标叔的经验**：这是 Cloudflare Agents 区别于几乎所有同类平台的点。Agent 能自己付钱，意味着"Agent 经济"真能跑——你的 Agent 调别人的 Agent，自动结算。这块值得长期关注。

支付讲完。下一 Part 进高级功能：邮件、Webhook、语音、对比与思维转变。

---

## Part 7: 高级功能篇

接入真实世界事件，做最终选型，完成思维转变。

## §24 邮件 Agent：收发回复邮件

### 24.1 Agent 能管邮箱

Cloudflare Email Service 让 Agent 收邮件、发邮件、回复邮件。`routeAgentEmail` 把邮件路由到对应 Agent。

### 24.2 收邮件

```typescript
import { routeAgentEmail } from "agents/email";

export default {
  async email(message: EmailMessage, env: Env, ctx: ExecutionContext) {
    // 按收件人路由到 Agent
    return routeAgentEmail(message, env, ctx);
  }
};
```

### 24.3 在 Agent 里处理

```typescript
export class SupportAgent extends Agent {
  async onEmail(message: EmailMessage) {
    const from = message.from;
    const text = await message.text();
    // 调模型生成回复，再 reply
    await message.reply(`收到你的邮件：${from}`);
  }
}
```

wrangler 加 `email` binding 与路由配置。三种 resolver 决定"哪个 Agent 收哪类邮件"。

| 维度 | 普通邮件转发 | Agent 收邮件 | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| 处理 | 手动/规则 | 模型理解后回 | Agent 更聪明 |
| 状态 | 无 | 有 SQLite 上下文 | 能续聊 |
| 典型 | 通知 | 智能客服邮箱 | 客服场景香 |

> **核心建议**：做"会看邮件上下文、能续聊"的智能邮箱，用 Agent 收。纯转发规则，别上 Agent。

邮件讲完。下一章用 Webhook 和推送接更多事件源。

## §25 Webhook 与推送通知：接入真实世界事件

### 25.1 Webhook：让外部系统打 Agent

GitHub 推送、Stripe 支付、表单提交——都能用 Webhook 打到 Agent。

```typescript
export default {
  async fetch(request: Request, env: Env) {
    // 用 HMAC-SHA256 校验签名，防伪造
    const valid = verifySignature(request, env.WEBHOOK_SECRET);
    if (!valid) return new Response("bad signature", { status: 401 });

    const payload = await request.json();
    const agent = await getAgentByName(env.MyAgent, payload.userId);
    await agent.handleEvent(payload); // 转给 Agent 处理
    return new Response("ok"); // 快速响应，重活在 Agent
  }
};
```

> **注意**：Webhook 端点要"快进快出"。校验完立刻返回 200，重活交给 Agent 异步跑。外部系统超时重试会让你重复处理。

### 25.2 推送通知：客户端关了也能达

用户关了页面？用 Web Push（VAPID）把消息推到浏览器。Agent 配合 service worker 订阅，定时或事件触发时推送。

```typescript
// 订阅 + 定时提醒的 Agent 内逻辑
await this.schedule("0 9 * * *", "sendPush", { title: "早报", body: "点开看今日摘要" });
```

| 维度 | WebSocket | Web Push | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| 客户端在线 | 实时双向 | 不需要在线 | 互补 |
| 离线可达 | 否 | 是 | 推送补离线 |
| 典型 | 聊天 | 提醒/告警 | 两个都配 |

> **核心建议**：实时交互用 WebSocket，离线提醒用 Push。一个 Agent 两种通道都接，体验才完整。

Webhook 讲完。下一章讲语音——让 Agent 开口说话。

## §26 语音 Agent：实时语音对话

### 26.1 语音是另一种通道

Cloudflare 提供语音能力：连续语音转写（STT）、流式语音合成（TTS）、语音活动检测（VAD）、打断、SFU 工具。可用 `withVoice` 和 `VoiceClient` 接入。

### 26.2 典型链路

麦克风 → STT 转文字 → Agent 推理 → TTS 合成语音 → 扬声器。全程流式，用户能打断。

### 26.3 前端用 VoiceClient

```typescript
import { VoiceClient } from "@cloudflare/voice/client";

const client = new VoiceClient({ agent: "VoiceAgent" });
// 连上后，麦克风音频自动走 STT → Agent → TTS 回传
```

> **标叔的经验**：语音 Agent 的"打断"体验最考验工程。Cloudflare 的 VAD 把这块内建了，比我自己接省太多。做语音客服、语音助手，这个通道直接拉满。

语音讲完。下一章做最终选型：Cloudflare Agents vs EdgeOne Makers。

## §27 Cloudflare Agents vs EdgeOne Makers：怎么选

### 27.1 先说清楚它们是两类东西

EdgeOne Makers 是"托管平台"——你点控制台、填业务逻辑、它搞定模型/记忆/工具/观测。Cloudflare Agents 是"SDK + 全球运行时"——你写代码，它兜底运行时/存储/调度/观测。

一个是"用产品"，一个是"写代码"。

### 27.2 能力对照

| 维度 | EdgeOne Makers | Cloudflare Agents | 标叔的结论 |
| ---- | ------- | -------------- | ------- |
| 上手 | 控制台点一点 | 写 TS + wrangler | 怕代码选 EdgeOne |
| 状态 | 平台托管记忆 | 每实例 SQLite | Cloudflare 更底层 |
| 模型 | 统一网关 | Workers AI + Gateway | 都不锁 |
| 调度 | 平台定时 | `schedule()` 内建 | Cloudflare 在对象内 |
| 工具 | 平台工具框架 | 浏览器/沙箱/MCP/RAG/支付 | Cloudflare 工具更野 |
| 支付 | 无 | x402/MPP | Cloudflare 独 |
| 语音/邮件 | 视平台 | 内建通道 | Cloudflare 通道全 |
| 国内 | 腾讯云备案友好 | 全球，国内需加速 | 看用户在哪 |
| 边缘 | 腾讯边缘 | 全球 300+ 节点 | Cloudflare 更广 |

### 27.3 我怎么选

- 用户在**国内**、要**备案**、不想碰命令行 → **EdgeOne Makers**。
- 要**全球分发**、爱**写代码**、要** Agent 自己付钱/会看网页/跑代码** → **Cloudflare Agents**。
- 两个都想要？EdgeOne 管国内用户，Cloudflare 管海外和 Agent 经济。不冲突。

> **重点看**：最后一行。它们不是非此即彼。我见过团队国内走 EdgeOne、海外和 Agent 间结算走 Cloudflare。按用户 geography 分。

选型讲完。最后一章，聊一个根上的认知转变。

## §28 思维转变：Agent 不是函数，是对象

### 28.1 最大的认知坑

我刚接触 Cloudflare Agents 时，把它当成"一个 API 函数"。写个 `handler`，调模型，返回。结果状态全丢，每次请求像陌生人。

### 28.2 换一个比喻

函数是无状态的。你打一次，它算一次，算完就忘。

Agent 是**有身份的对象**。它有名字、有记忆、有私有数据库、会自己定时醒来。你不是在"调用"它，是在"和它打交道"。

### 28.3 这个转变带来的设计差异

| 旧思维（函数） | 新思维（对象） | 标叔的体会 |
| ---- | ------- | -------------- |
| 每次请求重新取上下文 | 上下文在对象里常驻 | 不用反复喂历史 |
| 状态放外部 DB | 状态在 Agent 内 | 少一个组件 |
| 调度靠外部 cron 服务 | 调度在对象内 | 自包含 |
| 并发靠自己加锁 | DO 单实例串行 | 天然线程安全 |

> **核心建议**：设计 Agent 时，先问"它的身份是什么、它记得什么、它什么时候自己醒"。别问"这个请求怎么处理"。这一句，值整本书。

### 28.4 写在最后

Cloudflare Agents 把"有状态的 Agent"这件最难的事，焊进了 Durable Object。你拿到的是对象，不是函数。

剩下的，只是业务逻辑。

---

## 附录

### A 速查表

| 能力 | 入口 | 关键 API |
| ---- | ---- | ---- |
| 定义 Agent | `class X extends Agent` | `initialState`, `setState`, `this.sql` |
| 实时方法 | `@callable()` | `agent.stub.xxx()` |
| 路由 | `routeAgentRequest` | `getAgentByName` |
| 聊天 | `AIChatAgent` | `onChatMessage`, `useAgentChat` |
| 调度 | `this.schedule` | `scheduleEvery`, `listSchedules` |
| 子 Agent | `this.subAgent` | `parentAgent`, `onBeforeSubAgent` |
| 持久执行 | `runFiber` | `ctx.stash`, `onFiberRecovered` |
| 工作流 | `AgentWorkflow` | `step.do`, `waitForApproval` |
| MCP 客户端 | `addMcpServer` | `this.mcp.getAITools()` |
| MCP 服务器 | `McpAgent` | `MyMcp.serve("/")` |
| 浏览器 | `createBrowserTools` | `cdp.send` |
| 沙箱 | `getSandbox` | `sandbox.exec` |
| AI 搜索 | `AI_SEARCH` | `search`, `chatCompletions` |
| 支付 | x402/MPP | `withX402`, `paidTool` |
| 观测 | `subscribe` | Tail Worker |

### B 常见错误与解决

| 错误 | 原因 | 解决 |
| ---- | ---- | ---- |
| `No such Durable Object class` | 类没同时进 binding 和 migration | 两处都加 |
| `@callable` 方法调不动 | 装饰器没转译 | 检查 `agents()` 插件、别开 `experimentalDecorators` |
| 状态不广播 | 直接改 `this.state` | 用 `setState` |
| 历史不落盘 | 漏 `new_sqlite_classes` | 补 migration |
| MCP 连接报已连接 | 复用 McpServer 实例 | 每次请求 `new` 一个 |
| Fiber 恢复乱 | 恢复逻辑写在 lambda 里 | 移到 `onFiberRecovered` |
| 浏览器重放乱 | CDP `Promise.all` | 改顺序调用 |

### C 学习路径建议

第一步：跑通 §02 计数器，理解状态与广播。
第二步：做 §08 聊天 Agent，接工具和审批。
第三步：加 §12 调度，让 Agent 自动跑。
第四步：试 §15 浏览器 / §17 MCP，接外部世界。
第五步：读源码 `cloudflare/agents` 的 `examples/`，每个 demo 都是宝藏。

---

**标叔出品** | AI Native Coder · 独立开发者
公众号「标叔」| B站「Liangdabiao」
代表作：Claude Code从入门到精通 · OpenClaw橙皮书 · Hermes Agent从入门到精通 · EdgeOne Makers从入门到精通 · Cloudflare Agents从入门到精通
