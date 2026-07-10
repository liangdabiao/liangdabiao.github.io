# Flue 框架从入门到精通

A Complete Guide from Beginner to Master — 用 Harness 驱动的架构搭建可部署到任何平台的 AI Agent

**创建者**: 标叔
**为谁创建**: 会写 TypeScript、想自己搭 AI Agent 的开发者
**基于**: Flue Agent Framework v0.9.1
**最后更新**: 2026-07-07
**适用场景**: 用同一套代码，把自主 Agent 跑在本地、CI、Node 服务器或 Cloudflare

---

## Part 1: 起步

从零到一。读完这 Part，你能跑通自己的第一个 Agent，并给它装上"手"。

## §01 为什么是 Flue：Agent 是被"套上马具"的模型

### 01.1 我踩过的最疼的坑

去年我帮一个朋友搭客服机器人。他用官方 SDK 直接调模型 API，把"先查库存、再判断意图、最后回复"全写死成代码。

写了 800 行流程控制。改一个需求，全要重写。

模型越强，这套写死的逻辑越脆。现实一变，脚本就崩。

> **标叔的经验**：手写流程只适合窄而固定的活。
>
> 我做过一个文档分类脚本，写死 5 步。上线第 3 天，用户传了个格式异常的文档，整个流程报错。模型其实能处理，但被我的脚本卡死了。

### 01.2 旧方案 vs 新方案

Flue 的思路完全相反。你不再写"怎么干"，而是给模型一个"环境"，让它自己找路。

| 维度 | 手写流程脚本 | Flue（Harness 驱动） | 标叔的结论 |
|------|------------|---------------------|-----------|
| 谁决定步骤 | 你写死 | 模型自己选 | 让模型掌舵 |
| 改需求成本 | 重写流程 | 改指令/工具 | Flue 省 10 倍 |
| 抗意外能力 | 弱，一变就崩 | 强，模型能绕路 | 现实不按脚本走 |
| 适合场景 | 窄而固定 | 开放、长尾 | 看你的活儿 |

> **重点看**：最后一列"标叔的结论"。
>
> 这些数字背后的信号就一个：你越想让 Agent 干复杂活，越不能写死流程。

### 01.3 一个公式讲清 Flue

先给结论：**Agent = 模型 + 马具（Harness）**。

模型你熟。马具是啥？英文叫 harness，原意是"给马套上的挽具"。

类比级联一下：

- 模型是**马的大脑**。它只想事，不会动。
- 马具是**缰绳、鞍、眼罩**。它决定马能去哪、能看啥、能拉啥。
- 没有马具的马，是**罐子里的大脑**。再聪明，也动不了。

Flue 就是那套马具。它用 TypeScript 写成，给你现成的：记忆、工具、技能、沙箱。

> **核心建议**：先把"模型"和"马具"分开想。
>
> 很多人学 Agent 框架卡住，是因为把"模型能力"和"运行环境"混在一起。分开后，Flue 一切都顺了。

### 01.4 适合谁，不适合谁

- 你是 TypeScript 开发者，想用代码搭 Agent → **适合**。
- 你要一个开箱即用的聊天界面 → 不太适合，Flue 是 headless（无界面）。
- 你只想要一句话调模型 → 太重了，直接用 SDK 更轻。

下一章，我带你 10 分钟跑通第一个 Agent。不讲虚的。

---

## §02 十分钟跑通你的第一个 Agent

### 02.1 你需要什么

上周我重装环境。Node 22.18.0、一条命令、30 秒，对话就跑起来了。

清单很简单：

- **Node.js ≥ 22.18.0**（低于这个版本会报错）
- **一个模型 API Key**（我用 Anthropic，你用哪家电都行）
- **15 分钟**和一杯咖啡

### 02.2 我们最终要做成什么

一个会讲"hello world"冷笑话的 Agent。跑通后，你能在终端跟它对话。

为啥从笑话开始？因为它能验证整条链路：模型通了、会话通了、输出通了。

### 02.3 安装和第一次对话

**第一步**：建目录，装依赖。

```bash
# 装运行时和命令行工具
npm install @flue/runtime
npm install --save-dev @flue/cli

# 把密钥写进 .env，别提交到 git
echo 'ANTHROPIC_API_KEY="你的key"' > .env

# 初始化 Node 目标，生成 flue.config.ts
npx flue init --target node
```

预期结果：目录里多出 `flue.config.ts`，`package.json` 多了两个依赖。

**第二步**：写第一个 Agent 文件。

```typescript
// src/agents/hello-world.ts
import { createAgent } from '@flue/runtime';

// 文件名就是 Agent 名：hello-world
export default createAgent(() => ({
  model: 'anthropic/claude-sonnet-4-6',        // 模型用 provider/model 格式
  instructions: 'Tell a funny "hello world" engineering joke.',
}));
```

预期结果：文件保存即可，无需编译。Flue 会自动发现它。

**第三步**：连上去，开聊。

```bash
# hello-world 是模块名，local 是这次实例的 id
npx flue connect hello-world local
```

预期结果：终端显示已连接。你敲一句回车，它就回一段冷笑话。

> **注意**：模型写法必须是 `provider/model-id`。
>
> 写成 `deepseek-v4-flash` 会报 `Invalid model`。正确是 `deepseek/deepseek-v4-flash`。斜杠不能省。

### 02.4 两个新手必踩的坑

第一坑：`valibot` 版本。

```bash
# 必须 1.x，用 0.x 会报 TypeError: Cannot read properties of undefined
npm install valibot@^1.0.0
```

第二坑：`init()` 不收普通配置对象。这个我们 §08 细讲，先记住结论。

> **标叔的经验**：环境对，一切顺。
>
> 我第一次卡了 40 分钟，最后发现是 Node 版本是 20。升到 22.18.0，秒通。版本这关，先过。

### 02.5 回顾

我们装了依赖，写了 8 行代码，在终端跟 Agent 聊上了。

> **核心建议**：先跑通再优化。
>
> 别在第一天纠结"prompt 怎么写才完美"。先让它跑起来，看输出，再迭代。卡在完美主义是新手通病。

装完了，账号登了，第一次对话也跑通了。下一章，做个真能干活的项目。

---

## §03 第一个真实项目：会调 API 的搜索助手

### 03.1 项目需求

去年帮朋友搭完客服机器人后，我想做个能查热搜的小助手。光会讲笑话不够，得让它真的去调接口。

需求很具体：用户说"微博热搜 Top3"，Agent 调接口、拿数据、整理成列表。

这就是 Agent 和"聊天机器人"的分水岭——**它会动手调外部服务**。

### 03.2 思路：先想清楚三件事

动手前，先定三件事：

- 用什么模型？（我用 deepseek，便宜又快）
- 给它什么工具？（一个查热搜的 HTTP 工具）
- 在哪运行？（`local()` 沙箱，能直接发请求）

类比一下：Agent 是员工，工具是他的办公软件。你不写他每一步点哪，只把软件装好。

### 03.3 写工具和 Agent

```typescript
// src/agents/social-search.ts
import { createAgent, defineTool, Type, local } from '@flue/runtime';
import type { AgentRouteHandler, AgentWebSocketHandler } from '@flue/runtime';

// 定义一个工具：调外部 API
const apiCall = defineTool({
  name: 'api_call',
  description: 'Call an external API',
  parameters: Type.Object({
    method: Type.Union([Type.Literal('GET'), Type.Literal('POST')]),
    path: Type.String({ description: 'API path' }),
  }),
  execute: async ({ method, path }) => {
    // 这行是关键：直接返回字符串给模型
    return JSON.stringify({ method, path });
  },
});

const agent = createAgent(() => ({
  model: 'deepseek/deepseek-v4-flash',
  instructions: 'You are a social media search assistant.',
  sandbox: local(),          // 让它能碰主机网络
  tools: [apiCall],
}));

// 这两个导出是 HTTP/WS 访问必须的
export const route: AgentRouteHandler = agent.route;
export const websocket: AgentWebSocketHandler = agent.websocket;
export default agent;
```

预期结果：保存后，`flue dev` 启动，访问 `POST /agents/social-search/我的会话` 就能对话。

> **注意**：工具参数用 `Type`（TypeBox），不是 `valibot`。
>
> 这是 Flue 一个反直觉点。工具用 Type，工作流的 `result` 才用 valibot。混用会报错。

### 03.4 让它真正联网

上面 `apiCall` 我简化了。真实场景里，`execute` 直接用 Node 的 `https` 发请求：

```typescript
import https from 'node:https';

execute: async ({ path }) => {
  // 直接调 Node API，不用沙箱里的 shell
  return new Promise((resolve) => {
    const req = https.request(
      { hostname: 'api.example.com', path },
      (res) => {
        let data = '';
        res.on('data', (c) => (data += c));
        res.on('end', () => resolve(data));
      },
    );
    req.end();
  });
}
```

> **标叔的经验**：工具的 `execute` 就是普通 Node 函数。
>
> 我一开始以为要在沙箱里跑，绕了弯路。其实它跑在 Node 运行时，啥 Node API 都能用：`fs`、`https`、`child_process`。这点自由度很大。

### 03.5 回顾

我们给 Agent 装了"手"（工具）和"工作间"（沙箱）。它能调外部 API 了。

> **核心建议**：第一个项目，工具越简单越好。
>
> 别一上来搞 MCP、多工具联动。先跑通"一个工具 + 一次调用"，建立手感最重要。

会动手了。下一 Part，我拆开 Harness 的五个零件，让你真正看懂 Flue。

---

## Part 2: 核心能力

深入 Flue 的关键能力。每章一个核心概念，原理 + 实战。

## §04 Agent = 模型 + 马具：Harness 的五个零件

### 04.1 一个公式，反复用

我刚学 Flue 时，最懵的就是"马具里到底有啥"。翻完文档才懂，其实就五个零件。

今天拆开讲。Flue 的马具有五个零件，各有各的活：

| 零件 | 它干啥 | 类比 |
|------|--------|------|
| 文件系统 | 让 Agent 存东西 | 员工的笔记本 |
| 工具 | 让 Agent 动手 | 员工的软件 |
| 沙箱 | 让 Agent 安全地动 | 员工的工作间 |
| 会话 | 让 Agent 记得上下文 | 员工的记忆 |
| 子智能体 | 让 Agent 会分工 | 员工的同事 |

> **重点看**：最右一列"类比"。
>
> 把 Agent 当成一个被你雇来的员工。你不用教他每步点哪，你给他工具和工位。

### 04.2 五个零件怎么装

它们都写在一个 `createAgent(() => ({...}))` 里。看这个真实例子：

```typescript
// src/agents/repository-reviewer.ts
import { createAgent } from '@flue/runtime';
import { local } from '@flue/runtime/node';
import reviewChecklist from '../skills/review-checklist/SKILL.md' with { type: 'skill' };
import { repositoryTools } from '../shared/repository-tools.ts';

export default createAgent(() => ({
  model: 'anthropic/claude-sonnet-4-6',
  instructions: 'Review the change and report only evidence-based findings.',
  cwd: '/srv/repositories/catalog-service', // 工作目录
  tools: repositoryTools,                  // 零件：工具
  skills: [reviewChecklist],               // 零件：技能
  sandbox: local(),                        // 零件：沙箱
}));
```

这五行，就是给员工配齐了脑子、指令、工具、技能、工位。

> **标叔的经验**：写 Agent 更像"搭环境"而不是"写代码"。
>
> 我最初总想写逻辑。后来明白，难的不是代码，是"给 Agent 什么样的上下文"。上下文给对了，它自己干得比你写的还好。

### 04.3 两个模式，别用错

Flue 有**两种 Agent 模式**，用错会报错。这个坑我踩过，单独提一下：

| 模式 | 用途 | 怎么写 | 标叔的结论 |
|------|------|--------|-----------|
| 交互式 Agent | 网页聊天、SSE、WebSocket | 直接 `createAgent()`，导出 route/websocket | 持续对话选它 |
| 工作流 Agent | `flue run` 一次性任务 | handler 里 `createAgent()` 再 `init()` | 干完即走选它 |

> **核心建议**：长聊用交互式，干完就走用工作流。
>
> 分不清时，问自己：这个活要持续对话吗？要，就是 Agent；不要，就是工作流（§08）。

零件讲完了。下一章，先把"工具"这个最关键的零件讲透。

---

## §05 工具（Tools）：给 Agent 一双会干活的手

### 05.1 模型只会说话，工具让它动手

我第一次给 Agent 接工具时，激动得不行。因为那一刻它从"只会聊"变成"真能干活"。

模型本身只能"想"和"说"。查数据库、发短信、改文件，它一样都干不了。

工具就是它的手。这是 Flue 里**最关键的一步**——把你的业务能力交给 Agent。

### 05.2 一个工具的四部分

我用 `defineTool` 定义工具。它有四个零件：

```typescript
// src/shared/order-tools.ts
import { Type, defineTool } from '@flue/runtime';

export const lookupOrderStatus = defineTool({
  name: 'lookup_order_status',   // 1. 模型调用的名字
  description: 'Look up order fulfillment status.', // 2. 帮模型判断何时用
  parameters: Type.Object({      // 3. 输入参数（用 Type，非 valibot）
    orderId: Type.String({ description: 'Order ID like order_1234' }),
  }),
  execute: async ({ orderId }) => {  // 4. 真正干活的代码
    // 这行是关键：返回字符串给模型
    return `Order ${orderId} is packed.`;
  },
});
```

四部分拆开看：名字、说明、参数、执行体。

> **注意**：`execute` 必须返回字符串。
>
> 返回对象会出错。要返回结构化数据，用 `JSON.stringify(...)` 包一层。

### 05.3 工具不是鉴权边界

这点特别重要。模型的输入不可信，但凭证必须由你的代码给。

```typescript
// 正确：客户 id 由代码定，模型只能选订单号
export default createAgent(({ id: customerId }) => ({
  model: 'anthropic/claude-haiku-4-5',
  tools: [
    defineTool({
      name: 'lookup_customer_order',
      parameters: Type.Object({ orderId: Type.String() }),
      execute: async ({ orderId }) => {
        // 模型选订单号，但查哪个客户由代码定
        return await orders.getStatus(customerId, String(orderId));
      },
    }),
  ],
}));
```

模型能选订单号，但**选不了客户**。凭证和越权防护，永远握在你代码手里。

> **标叔的经验**：工具里别放密钥。
>
> 我见过有人把 API Key 写进工具参数描述，想让模型自己带。危险。密钥在 `env` 里，代码注入，模型只传业务参数。

### 05.4 接 MCP 生态

你不用自己写所有工具。MCP 服务器能提供远程工具：

```typescript
const inventory = await connectMcpServer('inventory', {
  url: env.INVENTORY_MCP_URL,
  headers: { Authorization: `Bearer ${env.INVENTORY_MCP_TOKEN}` },
});
// 连上后，工具名会变成 mcp__inventory__lookup_item
const harness = await init(agent, { tools: inventory.tools });
```

| 方式 | 适合 | 标叔的结论 |
|------|------|-----------|
| 自己写 defineTool | 业务逻辑、内部 API | 最灵活，首选 |
| 接 MCP 服务器 | 现成生态工具 | 省事，但多一跳网络 |

工具讲透了。下一章讲"技能"和"子智能体"，让 Agent 既专业又会分工。

---

## §06 技能与子智能体：让 Agent 既专业又会分工

### 06.1 一个人干所有活，会累

上个月我做客服 Agent，把查库存、写工单全塞一个 prompt。它开始胡说。我才懂要分工。

Agent 也一样。一个客服 Agent，又要查库存、又要写工单、又要判断情绪，全塞一个 prompt，它会乱。

Flue 给两种解法：**技能**让它变专业，**子智能体**让它会分工。

### 06.2 技能（Skills）：可复用的"操作手册"

技能是 Agent Skills 规范：一批指令和参考文件，Agent 按需加载。它**不执行代码**，只指导怎么干。

```typescript
// 用 skill 导入属性加载 SKILL.md
import review from '../skills/review/SKILL.md' with { type: 'skill' };
import triage from '../skills/triage/SKILL.md' with { type: 'skill' };

export default createAgent(() => ({
  model: 'anthropic/claude-sonnet-4-6',
  skills: [review, triage],  // 两个技能随时可用
}));
```

技能也能放在沙箱里，Agent 自己发现：`<cwd>/.agents/skills/review/`。

> **注意**：技能目录别放密钥。
>
> Flue 打包技能时会拒绝常见敏感文件。凭证走 `env`，别塞进 SKILL.md。

### 06.3 子智能体（Subagents）：会分工的同事

子智能体是一个"专家档案"，父 Agent 能把活派给它。

```typescript
// src/agents/policy-assistant.ts
import { createAgent, defineAgentProfile } from '@flue/runtime';
import { local } from '@flue/runtime/node';

// 定义一个专家：政策检索员
const policyResearcher = defineAgentProfile({
  name: 'policy_researcher',
  description: 'Finds relevant policy text and quotes it.',
  instructions: 'Read the policy workspace and return quoted passages.',
});

export default createAgent(() => ({
  model: 'anthropic/claude-sonnet-4-6',
  instructions: 'Delegate source lookup to policy_researcher first.',
  sandbox: local(),
  cwd: '/srv/company-policies',
  subagents: [policyResearcher],  // 挂上专家
}));
```

子智能体在**独立的子会话**里干活，不污染父 Agent 的对话历史。

### 06.4 技能 vs 子智能体

| 维度 | 技能（Skill） | 子智能体（Subagent） | 标叔的结论 |
|------|--------------|---------------------|-----------|
| 本质是 | 指令/手册 | 另一个 Agent | 轻的用技能 |
| 是否执行代码 | 否 | 是，有自己的会话 | 重的派子体 |
| 适合 | 复用流程、规范 | 委派研究、分类 | 看是否独立 |
| 调用方式 | 模型自动或 `session.skill()` | 模型自动或 `session.task()` | 都不用手动 |

> **标叔的经验**：先技能，后子智能体。
>
> 我一开始啥都用子智能体，结果开销大、调试难。能写成"操作手册"的，用技能更轻。真要独立研究的，才派子智能体。

分工讲完。下一章讲"沙箱"和"模型"——Agent 的工作间和大脑。

---

## §07 沙箱与模型：Agent 的工作间和大脑

### 07.1 模型是大脑，沙箱是工作间

我第一次用 `local()` 沙箱，Agent 直接把我主机文件改了。吓一跳。才认真研究沙箱。

选错了，要么跑不动（沙箱太弱），要么不安全（沙箱太宽）。这章把这两个旋钮讲清。

### 07.2 沙箱三选一

| 沙箱 | 用途 | 隔离性 | 标叔的结论 |
|------|------|--------|-----------|
| 虚拟沙箱（默认） | 轻量工作，内存文件系统 | 中，非网络隔离 | 起步首选，够用 |
| local() | 直接碰主机文件/命令 | 无隔离 | 只信主机时才用 |
| 远程沙箱 | 不信任/多租户任务 | 强 | 上云或跑代码时用 |

虚拟沙箱是默认的，无需配置。一个工作流能先塞文件进去，再让 Agent 处理：

```typescript
const harness = await init(reviewer);
// 这行是关键：应用代码先放好输入文件
await harness.fs.writeFile('document.md', payload.document);
const session = await harness.session();
await session.prompt('Review document.md and write findings to review.md.');
// 收结果
return { review: await harness.fs.readFile('review.md') };
```

> **注意**：`harness.fs` 在工作流里用，`harness.env` 在 Agent 里用。
>
> 没有 `harness.fs` 这个 API。在 Agent 会话里读写，走 `harness.env.writeFile`。别记反。

### 07.3 模型：用字符串选大脑

模型用 `provider/model-id` 格式指定。Flue 内置多家：

```typescript
createAgent(() => ({
  model: 'anthropic/claude-sonnet-4-6',  // Anthropic
  // model: 'deepseek/deepseek-v4-flash', // DeepSeek，内置，免注册
  thinkingLevel: 'high',                 // 推理强度：off→xhigh
}));
```

`thinkingLevel` 控制模型花多少心思。默认 `medium`。简单活设 `low` 省钱。

### 07.4 关于 DeepSeek 的一个坑

DeepSeek 是**内置** provider。设个环境变量就能用，不用注册。

但有人想把 DeepSeek 当 Anthropic 用，走它的 Anthropic 兼容端点。这时要改 `baseUrl`：

```bash
# .env 里设这两个，让 anthropic provider 指向 DeepSeek
ANTHROPIC_API_KEY=sk-your-deepseek-key
ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
```

> **标叔的经验**：`registerProvider` 必须写在 `app.ts`。
>
> 我把它写在 Agent 文件里，死活不生效。后来才懂：Flue 构建只抽取 handler 函数，顶层副作用会被丢掉。`app.ts` 才是注册 provider 的地方。

工作间和大脑都讲清了。下一 Part 进入进阶实战。

---

## Part 3: 进阶实战

多场景、多工具、多 agent 的复杂用法。从工作流到部署，一章一个实战。

## §08 工作流（Workflows）：一次性的确定性任务

### 08.1 不是所有事都要长聊

上周我要批量总结 50 篇文档。开 50 个对话太傻。用工作流，一条命令全搞定。

有些活，干完就走。比如：收到一篇文档，总结它；收到一张工单，分类它。

你不想为它开一个"持续对话"。这就是**工作流**。

### 08.2 Agent 还是工作流？

| 维度 | 交互式 Agent | 工作流 Workflow | 标叔的结论 |
|------|------------|----------------|-----------|
| 对话 | 持续多轮 | 一次性，干完即走 | 多轮选 Agent |
| 触发 | HTTP/WS 实时 | `flue run` 或 CI | CI 选工作流 |
| 适合 | 客服、聊天 | 总结、分类、CI 任务 | 看是否长聊 |
| 有 runId | 否 | 是，可查运行记录 | 要查账用工作流 |

> **重点看**：最后一行"有 runId"。
>
> 工作流每次执行都有独立 `runId`，能查历史、查事件。Agent 的对话没有这个。

### 08.3 写一个工作流

```typescript
// src/workflows/summarize.ts
import { createAgent, type FlueContext } from '@flue/runtime';

const summarizer = createAgent(() => ({
  model: 'anthropic/claude-haiku-4-5',
  instructions: 'Summarize the supplied document clearly.',
}));

// 文件名就是工作流名：summarize
export async function run({ init, payload }: FlueContext<{ text: string }>) {
  const harness = await init(summarizer);  // 这行初始化
  const session = await harness.session();
  const response = await session.prompt(payload.text);
  return { summary: response.text };        // 返回值就是结果
}
```

跑它：

```bash
pnpm exec flue run summarize --payload '{"text":"要总结的内容"}'
```

### 08.4 结构化结果，别让模型自由发挥

工作流常被别的代码调用。你要的是字段，不是散文。用 `result` 要结构化数据：

```typescript
import * as v from 'valibot';
const response = await session.prompt(payload.ticket, {
  result: v.object({
    priority: v.picklist(['low', 'medium', 'high']),
    summary: v.string(),
  }),
});
// 注意：直接拿数据，不是 response.data
return response.data;
```

> **标叔的经验**：`init()` 只要 `createAgent()` 的结果。
>
> 我最常报的错就是 `init() requires an agent created with createAgent(...)`。把配置对象直接丢给 `init`，不行。必须 `const agent = createAgent(...); init(agent)`。这条记死。

工作流讲完。下一章，把 Agent 接到你自己的服务里，并加上鉴权。

---

## §09 路由与安全：把 Agent 接到你的服务里

### 09.1 没加鉴权，被人刷了

去年一个项目，Agent 直接暴露在公网，没加鉴权。一周被刷掉 200 刀 API 费。

Agent 写好了，不能谁都能调。这章讲怎么把它接进你的服务，并守好门。

### 09.2 app.ts：你的 Hono 应用

`src/app.ts` 是可选的入口。它本质是个 [Hono](https://hono.dev/) 应用。你把自己的路由、中间件和 Flue 拼一起。

```typescript
// src/app.ts
import { flue } from '@flue/runtime/routing';
import { Hono, type MiddlewareHandler } from 'hono';
import { authenticate } from './auth.ts';

// 这行是关键：先验证用户
const requireUser: MiddlewareHandler = async (c, next) => {
  const user = await authenticate(c.req.raw);
  if (!user) return c.json({ error: 'Unauthorized' }, 401);
  await next();
};

const app = new Hono();
app.get('/health', (c) => c.json({ ok: true }));
app.use('/agents/*', requireUser);     // 给 Agent 路由加锁
app.use('/workflows/*', requireUser);
app.route('/', flue());                // 挂载 Flue
export default app;
```

### 09.3 暴露哪种传输，你自己定

每个 Agent 文件用导出决定"怎么被访问"：

| 导出 | 暴露方式 |
|------|---------|
| `route` | `POST /agents/名/:id` 的 HTTP |
| `websocket` | `GET /agents/名/:id` 的 WebSocket |
| 都不导 | 只通过 `dispatch()` 内部调用 |

只接 webhook、不对外暴露的 Agent，两个都不用导。安全。

### 09.4 异步事件用 dispatch

聊天平台、队列消息，用 `dispatch` 异步喂给 Agent：

```typescript
app.post('/webhooks/support-comments', async (c) => {
  const event = await verifySupportWebhook(c.req.raw);
  // 这行是关键：异步投递，不等回复
  const receipt = await dispatch(supportAssistant, {
    id: event.ticketId,
    session: 'customer-follow-up',
    input: { type: 'support.comment.created', text: event.text },
  });
  return c.json(receipt, 202);
});
```

> **注意**：provider 注册只在 `app.ts` 有效。
>
> 这是 §07 提过的坑，在路由里再强调一次：`registerProvider` 放 Agent 文件里会被丢弃。所有顶层副作用，都进 `app.ts`。

> **标叔的经验**：鉴权别只挂在 Agent 上。
>
> 我吃过亏，只在 Agent 的 `route` 里校验，结果工作流路由漏了。现在统一在 `app.ts` 用中间件锁 `/agents/*` 和 `/workflows/*`，一处管全站，省心。

门守住了。下一章，让 Agent 的运行"看得见"。

---

## §10 流式输出与可观测：让 Agent 的运行看得见

### 10.1 用户盯着空白屏，以为卡了

我第一次上线 Agent，用户说"它卡了"。其实它在思考。我才明白要流式输出。

Agent 思考要几秒。你只回最终答案，用户面对空白，会以为挂了。

解决两件事：**流式输出**让用户看到过程，**可观测**让你看到运行。

### 10.2 SSE：把思考过程推给前端

加一个 `Accept: text/event-stream` 头，就能收到实时事件：

```bash
curl -N -X POST http://localhost:3583/agents/social-search/my-session \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"message":"微博热搜Top3"}'
```

事件类型一览：

| 事件 | 含义 |
|------|------|
| `thinking_start` / `thinking_delta` / `thinking_end` | Agent 推理过程 |
| `tool_execution_start` / `tool_execution_end` | 工具开始/结束 |
| `text_delta` | 最终回答的片段流 |
| `agent_end` | Agent 结束 |

每个事件都是 `data: <JSON>\n\n` 格式。前端边收边渲染，体验立刻不一样。

### 10.3 可观测：用 observe 看全局

上线后，你要知道"哪个工作流慢了、哪个失败了"。在 `app.ts` 注册观察者：

```typescript
import { observe } from '@flue/runtime';

observe((event) => {
  // 这行是关键：慢操作告警
  if (event.type === 'operation' && event.durationMs > 5000) {
    console.warn('Slow operation', event.operationKind, event.durationMs);
  }
});
```

工作流内部还能写结构化日志：

```typescript
export async function run({ init, log, payload }: FlueContext<{ text: string }>) {
  log.info('Summarization requested', { characters: payload.text.length });
  // ... 干活 ...
  log.info('Completed', { tokens: response.usage.totalTokens });
}
```

> **标叔的经验**：先盯"结果类"信号。
>
> 失败的工作流、慢操作、模型用量，这三样先接上。嵌套的工具报错别全都当事故，Agent 常常自己恢复了，全告警会吵死人。

看得见运行了。下一章，把它部署到任何地方。

---

## §11 部署到任何地方：Node、Cloudflare 与 CI

### 11.1 写一次，到处跑

去年我把一个 Agent 从 Node 迁到 Cloudflare。原本以为要重写，结果只改了 `target`。

这是 Flue 的承诺：同一套 Agent，跑本地、跑 Node 服务器、跑 Cloudflare、跑 CI。

我把它在 Node 和 Cloudflare 都试过。同一份代码，换 `target` 就部署。

### 11.2 构建与启动

```bash
npm run build   # 构建到 dist/
npm start       # 启动生产服务器
```

生产启动脚本要显式加载环境变量和端口：

```json
{
  "scripts": {
    "start": "bash -c 'set -a && source .env && set +a && PORT=3583 node dist/server.mjs'"
  }
}
```

### 11.3 开发 vs 生产

| 模式 | 命令 | 行为 | 标叔的结论 |
|------|------|------|-----------|
| 开发 | `flue dev` | 热重载，但一改文件就断连 | 只本地调试用 |
| 生产 | `npm start` | 稳定，不断连 | 上线必须用 |

> **重点看**："开发"那一行的"断连"。
>
> `flue dev` 监听项目根目录**所有文件**。你改个 `.md`，它都重启，正在流的 SSE 直接断。线上服务用生产模式。

### 11.4 部署目的地

| 目的地 | 适合 | 说明 |
|--------|------|------|
| Node.js | 普通长驻服务器/容器 | 最通用 |
| Cloudflare | Worker，免运维 | 用 `cloudflare/` 模型免 Key |
| Render | 托管 Node 服务 | 带可选持久化 |
| GitHub Actions | CI 里跑一次性任务 | `--target node` |

Cloudflare 有个爽点：用 `cloudflare/@cf/...` 模型，靠 Worker 的 `AI` 绑定，连 API Key 都不用配。

> **标叔的经验**：部署前先 `flue build`。
>
> 我偷懒直接 `dev` 上线过，遇到文件监听把连接搞挂。构建一次能提前抓出"Agent 没被发现"这类问题，省心。

四处都能跑了。最后两章，聊点虚但重要的——思维转变和框架选型。

---

## Part 4: 收束与选型

不是新功能，是回头看。这一 Part 一章讲思维，一章讲选型。读完你就能收工了。

## §12 思维转变：你不是写代码的人，你是搭舞台的人

### 12.1 三个月，最大的变化

用 Flue 三个月，我最大的变化不是代码写得好。是**思考问题的方式**变了。

以前接需求，我第一反应是"写个函数"。现在第一反应是"给 Agent 配个什么环境"。

### 12.2 你是导演，不是打字员

从现在开始，你是**导演**。

- 模型是演员，你选它演谁。
- 工具是道具，你决定给它什么。
- 沙箱是片场，你划好能动的边界。

你不再写"第 1 步调 A，第 2 步判断 B"。你搭好舞台，让演员自己走位。

> **核心建议**：把"控制"换成"给上下文"。
>
> 越想精确控制 Agent，越容易写死逻辑、越脆。把边界和工具给足，让它自己找路，反而稳。

### 12.3 三个思维切换

| 旧思维 | 新思维 | 为什么 |
|--------|--------|--------|
| 写流程脚本 | 配运行环境 | 现实不按脚本走 |
| 精确控制每步 | 给足上下文 | 模型比你会找路 |
| 绑死一家模型/云 | 开放可替换 | Flue 每层都能换 |

这三换，是 Flue 教我最重要的东西。它不只是一个框架，是一种搭 Agent 的方法论。

> **标叔的经验**：从"写代码"到"搭舞台"，省下的时间最多。
>
> 我一个原本 800 行的客服流程，用 Flue 重写成"环境配置"，核心代码不到 100 行。剩下的活，交给模型在马具里自己跑。

> **一句话总结**：Flue 让你从"写代码的"，变成"搭舞台的"。
>
> | 维度 | 写代码的人 | 搭舞台的人 |
> |------|-----------|-----------|
> | 关注点 | 步骤对不对 | 环境够不够 |
> | 抗变能力 | 弱 | 强 |
> | 你的角色 | 打字员 | 导演 |

书到这里。Agent 会跑了，手会动了，舞台会搭了。接下来，去搭你自己的那个吧。

---

## §13 Flue vs Claude Agent SDK：怎么选

### 13.1 为什么这一章要单写

三个月前我带团队做 Agent 选型。会议室里摆了三个方案，最后吵的不是"用不用 LLM"，是"用 Flue 还是 Claude Agent SDK"。

当时没人能把两边讲透。我把这三个月踩的坑整理成这一章。如果我一句话总结：轻量级功能和部署，优先试试flue!

你看完，应该能在 5 分钟内做选择。

### 13.2 先把两边摆上台

Flue 是"通用马具"。它**不绑模型**，Anthropic、DeepSeek、OpenAI 谁都能上，部署到 Node、Cloudflare、CI 都行。Claude Agent SDK 是 Anthropic 官方出品，**深度绑定 Claude**，CLI 场景里最舒服。

一个像"乐高"，一个像"主题套装"。都能搭 Agent，但手感不同。

### 13.3 五个维度比一比

我把两边用同一把尺子量过。下表是结论，每行下面会展开讲。

| 维度 | Flue | Claude Agent SDK | 标叔的结论 |
|------|------|------------------|-----------|
| 语言 | TypeScript | Python、TypeScript | 团队语言定 |
| 模型绑定 | 不绑，多家可换 | 绑 Claude 系列 | 跨家选 Flue |
| 部署目标 | Node / Cloudflare / CI | 终端、CLI、服务端 | 上 Cloudflare 选 Flue |
| 适合场景 | 多端统一、生产服务 | 本地编码助手、CLI 工具 | 看场景 |
| 学习成本 | 中（要懂 Harness 五个零件） | 低（CLI 直接用） | 快速落地选 SDK |

> **重点看**：最后一行"学习成本"。
>
> 这是新人最容易忽略的。Claude Agent SDK 装上 `claude` 命令就能聊。Flue 要先懂沙箱、工具、技能子智能体，再写代码。

### 13.4 Flue 的优点与缺点

**优点**

- **不绑模型**。我有个项目上午用 DeepSeek（便宜），下午切 Claude（质量好），只改 `model` 字符串。这是 SDK 做不到的。
- **部署自由**。同一份代码，Node 服务器、Cloudflare Worker、GitHub Actions 都跑。SDK 主要服务 CLI。
- **TypeScript 优先**。前端团队直接上手，类型推断、IDE 跳转都顺。
- **Harness 显式可配**。五个零件（文件系统、工具、沙箱、会话、子智能体）写在 `createAgent` 里，一目了然。
- **生产特性全**。SSE 流式、Observe 可观测、工作流 runId、App 路由鉴权——都是 SDK 默认没有的。

**缺点**

- **学习曲线高**。新手要吃透 Harness、TypeBox、沙箱三选一，门槛不低。
- **生态年轻**。遇到坑基本要自己查或问作者，没有大社区背书。
- **没有官方 CLI 体验**。`flue connect` 是个能用的 REPL，但和 `claude` 命令那种丝滑度比，还有差距。
- **文档偏少**。这本指南其实是文档的延伸，外面能查到的资料有限。

> **标叔的经验**：Flue 的真正门槛不是 API，是"思维转变"。
>
> 我团队有个写 Python 五年的同事，第一次用 Flue 写 Agent，老想 `if/else` 控制流程。两周后才转过来。

### 13.5 Claude Agent SDK 的优点与缺点

**优点**

- **上手极快**。`npm install -g @anthropic-ai/claude-code`，一条命令开聊。10 分钟就有产出。
- **Claude 深度优化**。所有 Claude 模型特性（extended thinking、prompt caching、tool use）都打通，你不用配。
- **内置工具强**。Read、Edit、Bash、Grep、Glob、WebSearch、WebFetch 都是现成的，写代码场景开箱即用。
- **权限系统成熟**。allow / deny / ask 三档，可按工具、按路径细粒度控制，企业可用。
- **Hooks 系统完整**。PreToolUse、PostToolUse、Stop 都能挂回调，做审计、做安全扫描、做日志都对口。
- **Skills 与 Subagents 一等公民**。markdown 写技能、Task 派子体，模型自己协调。

**缺点**

- **绑死 Claude**。想换 GPT、Gemini、DeepSeek？不行。这是最大硬伤。
- **CLI 优先**。服务化部署没那么顺，要自己包一层才能上生产。
- **Python 体验明显好于 TypeScript**。TypeScript 版本是后来补的，文档和示例都少。
- **定制空间小**。沙箱、文件系统这些底层，能改的有限。
- **大上下文贵**。长会话不裁剪，Token 烧起来心疼。
- **中文场景偶有水土不服**。复杂中文指令偶尔会跑偏。

> **标叔的经验**：把 Claude Agent SDK 当"瑞士军刀"，别当"生产线"。
>
> 我用它写过 CI 里的 PR Reviewer Bot、好用过。但要做一个对客的客服 Agent 跑在 Cloudflare 上，不行——它天生不是干这个的。

### 13.6 决策树：5 分钟做选择

我把这三个月的判断画成一张决策图。你照着走，基本不会错。

| 你的情况 | 选 Flue | 选 Claude Agent SDK |
|----------|---------|---------------------|
| 团队主力是 TypeScript | ✓ | |
| 团队主力是 Python | | ✓ |
| 要部署到 Cloudflare Workers | ✓ | |
| 写本地编码助手、CLI 工具 | | ✓ |
| 必须能换模型（成本/合规考虑） | ✓ | |
| 模型就钉死 Claude | | ✓ |
| 要对接现有 Hono / Node 服务 | ✓ | |
| 要做 PR Review / Code Agent / 终端自动化 | | ✓ |
| 要做对客的多端产品 | ✓ | |
| 团队没人懂 Agent 概念，要最快出活 | | ✓ |

> **核心建议**：先想"在哪跑"，再想"用什么模型"。
>
> 很多人选框架反着来——先挑模型，再想部署。结果 Claude Agent SDK 跑 Cloudflare 写得很痛苦。**部署目标先定，框架就定一半。**

### 13.7 并存：两边都用

这不是二选一。我现在的项目，**两个都用**。

- **Claude Agent SDK** 跑在开发者本地，做代码审查、脚本生成、CI 里的 PR 分析。
- **Flue** 跑在 Cloudflare，做对客的客服 Agent、数据处理工作流。

两边用一致的 prompt 模板、共享 SKILL.md。模型层互不依赖。

```typescript
// Flue 这边：导入和 SDK 同样的 SKILL.md
import reviewChecklist from '../skills/review/SKILL.md' with { type: 'skill' };

// Claude Agent SDK 那边的 settings.json 也指向同一份
// { "skills": ["./skills/review/SKILL.md"] }
```

Agent Skills 规范是 Anthropic 推的，Flue 原生兼容。一份技能，两边用，省维护。

> **标叔的经验**：别把鸡蛋放一个篮子。
>
> 我以前只用 Claude Agent SDK，结果一次 Claude API 抖动，整个研发流程卡了两小时。现在核心流程 Flue 兜底，SDK 做增强。安全感不一样。

### 13.8 迁移路径

如果以后想从一边迁到另一边，也不难。它们的"心智模型"高度相似：

| 概念 | Flue | Claude Agent SDK |
|------|------|------------------|
| Agent 本身 | `createAgent(() => ({...}))` | `claude --agent xxx` |
| 工具 | `defineTool({...})` | `tools: [{name, input_schema, ...}]` |
| 技能 | `import skill from 'X/SKILL.md'` | `.claude/skills/.../SKILL.md` |
| 子智能体 | `defineAgentProfile({...})` | Task tool 派发 |
| 会话 | `harness.session()` | 内置 session |
| 流式 | SSE `text_delta` | `stream: true` |

两边都遵循 [Agent Skills 规范](https://agentskills.io)。技能文件、提示词、心智模型是通的。

> **标叔的经验**：先 Flue 后 SDK，比反过来舒服。
>
> 我团队有个逆向走法：先 SDK 后 Flue，一直骂 Harness 复杂。原因是 SDK 把复杂度藏在内部，先用 SDK 的人不习惯"显式配置"。先 Flue 后 SDK 的人，反倒觉得 SDK 简洁。

### 13.9 一句话总结

> **Flue 是给"搭舞台的人"用的，Claude Agent SDK 是给"演员"用的。**
>
> | 你是谁 | 选谁 |
> |--------|------|
> | 写产品、写服务、跨多端 | Flue |
> | 写工具、写脚本、自动化 | Claude Agent SDK |
> | 两个都干 | 都装，按场景切换 |

---

## 附录

### A 常见错误与排查速查表

| 报错/现象 | 原因 | 解法 |
|----------|------|------|
| `init() requires an agent created with createAgent(...)` | 把配置对象直接丢给 `init()` | 先 `createAgent()`，再 `init(agent)` |
| `Invalid model "xxx"` | 少了 `provider/` 前缀 | 用 `deepseek/deepseek-v4-flash` |
| `403 Forbidden`（Anthropic + DeepSeek） | 端点不兼容 | 用内置 `deepseek` provider 或改 `baseUrl` |
| `registerProvider` 不生效 | 写在 Agent 文件里 | 移到 `src/app.ts` |
| `Agent "xxx" not found`（`flue run`） | 文件在 `workflows/` | `flue run` 只认 `agents/` |
| dev 服务器老断连 | 监听所有根文件 | 用生产模式 `npm start` |
| `TypeError: Cannot read properties of undefined` | valibot 0.x | 升到 `valibot@^1.0.0` |
| `harness.fs is not a function` | Agent 里用了 `harness.fs` | 改用 `harness.env.writeFile` |

### B 核心 API 速查表

| API | 作用 | 关键注意 |
|-----|------|---------|
| `createAgent(fn)` | 定义 Agent | 返回函数，文件名即 Agent 名 |
| `defineTool({...})` | 定义工具 | 参数用 `Type`，`execute` 返字符串 |
| `defineAgentProfile({...})` | 定义子智能体/档案 | `name`、`instructions` 必填 |
| `init(agent, opts?)` | 初始化运行环境 | 只接 `createAgent()` 结果 |
| `session.prompt(msg, {result})` | 发消息 | 带 result 直接返数据 |
| `session.task(msg, {agent})` | 派给子智能体 | 在独立子会话执行 |
| `connectMcpServer(name, {...})` | 接 MCP | 工具名前缀 `mcp__名__工具` |
| `dispatch(agent, {id, input})` | 异步投递 | 不等回复，返回 receipt |
| `observe(fn)` | 全局可观测 | 写在 `app.ts` |
| `local()` | 本地沙箱 | 从 `@flue/runtime/node` 导入 |

### 阅读指南

| 时间 | 章节 | 目标 |
|------|------|------|
| Day 1 | §01-§03 | 从零到第一个会干活的 Agent |
| Day 2-3 | §04-§07 | 吃透 Harness 五个零件与核心能力 |
| Day 4-5 | §08-§11 | 工作流、路由安全、可观测、部署 |
| Day 6 | §12 + 附录 | 思维转变，查错与速查 |

> **标叔出品** | AI Native Coder · 独立开发者
> 公众号「标叔」 
> 代表作：github.com/liangdabiao


### 参考文档：

 https://mp.weixin.qq.com/s/-QaD5vDZ13v2NXf2rTR7zg?scene=1&click_id=320
