# Vercel Eve 从入门到精通

Vercel's Agent Framework, Explained Like a Friend

**创建者**: 标叔
**为谁创建**: 想用工程化方式构建生产级 AI Agent 的前端 / 全栈开发者与技术负责人
**基于**: Vercel Eve（eve npm 0.22.0，2026-07）
**最后更新**: 2026-07-08
**适用场景**: 从零认识 Eve，直到搭出可部署、可暂停恢复、可审批、可评测的 Agent 团队

---

这本书用大白话讲清楚 Vercel Eve 是什么、为什么值得看、怎么上手、怎么进阶。我会用一个 SpringXX内容团队的真实例子，把它的全部能力串起来。

---

## Part 1: 起步

从零到一。读完这部分，你能跑通第一个 Agent。

## §01 Eve 解决的根本不是"怎么调模型"

### 01.1 2026 年 6 月 17 日，Vercel 把 Eve 开源了

2026 年 6 月 17 日，Vercel 把 Eve 开源了。我当天就翻完了发布文章和仓库。

先说我的判断：Eve 值得关注。但原因不是它又提供了一种调大模型的新写法。

它真正有意思的地方，是把 Agent 跑起来之后那一大堆没人愿意重复造的基础设施，收进了一个文件系统优先的框架里。

> **标叔的经验**：Agent Demo 很好做
>
> 写个系统提示词，备几个工具，调模型循环几轮，一个能查数据、搜网页的 Agent 半天就能跑起来。我做过不下十个这样的 Demo。但没一个真正上线过。

### 01.2 Agent 上生产后，七个真问题来了

Demo 跑起来不难。可一旦准备放进真实业务，问题马上就来：

- 任务跑了半小时，进程重启了怎么办？
- Agent 等用户批准时，连接要一直挂着吗？
- 模型生成的脚本，敢不敢直接在应用服务器上执行？
- 回滚生产版本，也能自动做吗？
- 同一 Agent 要接 Web、Slack、API，每入口都要重写吗？
- Agent 出错后，怎么知道它当时看了什么、调了什么工具？
- 改了一句 instructions，怎么确认旧能力没悄悄退化？

这些问题，没有一个能靠"再优化下 Prompt"解决。

### 01.3 Eve 切入的位置

过去大家要自己拼：模型 SDK、工作流引擎、任务队列、状态存储、沙箱、OAuth、审批页、日志系统、评测框架。Demo 几百行，包住它的生产基建却膨胀成另一个项目。

| 维度 | 自己拼装 | 用 Eve | 标叔的结论 |
|------|---------|--------|-----------|
| 持久执行 | 自己写队列 | 框架默认 Durable | 省掉最难的 30% |
| 沙箱隔离 | 自己接容器 | 内置 Sandbox | 安全观开箱即用 |
| 人工审批 | 自己写页面 | 内置 Approvals | 边界显式化 |
| 子 Agent | 自己调度 | 目录即子 Agent | 结构更清晰 |
| 可观测 | 自己接 ELK | OpenTelemetry | 复用现有平台 |
| 评测 | 自己写脚本 | 内置 Evals | 接 CI 挡回归 |

重点看最后一列。Eve 不是给你更多模型调用方式，而是把"生产 Agent 该有的样子"固定成约定。

> **核心建议**：先想清楚要不要框架
>
> 如果你只是给接口加一次模型问答，直接用 AI SDK 更轻。为了两步流程引入整套框架，不划算。

[向前桥接] 装好它，跑通第一个 Agent。下一章，我们动手。

## §02 十分钟跑通第一个 Agent

### 02.1 你需要什么

- Node.js 24 或更新（这是硬要求，2026-07 的 0.22.0 版本会把 engines.node 钉在 24.x）
- npm（Node 自带）
- 一个模型凭据：Vercel AI Gateway 的 `AI_GATEWAY_API_KEY`，或任意 AI SDK 支持的直连 Key

> **注意**：Node 版本不够会直接失败
>
> 我见过有人用 Node 20 跑 `eve init`，卡在引擎检查。先 `node -v`，低于 24 就用 nvm 切：`nvm install 24 && nvm use 24`。

### 02.2 用 eve init 创建项目

```bash
# 创建项目，同时装依赖、初始化 Git
npx eve@latest init my-agent
cd my-agent
```

预期结果：`my-agent/` 目录生成，`agent/` 里已有 `instructions.md` 和 `agent.ts`，还带一个内置 Eve channel。

默认模型是 `anthropic/claude-sonnet-5`，走 Vercel AI Gateway。想换模型或直连别家，改 `agent/agent.ts` 即可。

### 02.3 加一个工具

工具就是一个 TypeScript 文件。文件名就是工具名，必须 snake_case。

```typescript
// agent/tools/get_weather.ts
// 文件名 get_weather 直接变成模型看到的工具名
import { defineTool } from "eve/tools";
import { z } from "zod";

export default defineTool({
  description: "Get the current weather for a city.",
  inputSchema: z.object({ city: z.string().min(1) }), // 入参用 zod 约束
  async execute({ city }) {
    return { city, condition: "Sunny", temperatureF: 72 };
  },
});
```

这里要注意：工具跑在你的应用进程里，带完整 `process.env`，不在沙箱里。敏感操作要自己加保护。

### 02.4 两种方式对话

方式一，CLI 聊天：

```bash
# 启动本地运行时，打开交互式终端
npm run dev
```

在终端里输入一句话，你会先看到 `get_weather` 被调用，再看到结果，最后是回答。

方式二，HTTP 接口（Eve 每个应用都暴露同一套稳定 API）：

```bash
# 开一个持久会话
curl -X POST http://127.0.0.1:2000/eve/v1/session \
  -H 'content-type: application/json' \
  -d '{"message":"What is the weather in Brooklyn?"}'
```

返回里有 `continuationToken`（续聊用）和 `x-eve-session-id`（流式用）。

```bash
# 挂着看流式事件：session.started → actions.requested → action.result → message.completed
curl http://127.0.0.1:2000/eve/v1/session/<sessionId>/stream
```

> **标叔的经验**：先验证模型入口
>
> 社区里有朋友接入自定义网关，一上来就报错。后来发现是 base URL 或 Key 错了，不是 instructions 的问题。先在 `npm run dev` 之外单独 ping 一下模型入口，能省半天排查。

[向前桥接] 第一个 Agent 跑通了。但它到底长什么样？下一章讲核心架构。

## §03 一个目录就是一个 Agent

### 03.1 filesystem-first 是什么

Eve 的第一个特点是 filesystem-first（文件系统优先）。官方一句话："The filesystem is the authoring interface"。

翻成白话：别把 Agent 藏在某控制台的一堆配置项里，把它当成普通软件项目来管理。

最小项目长这样：

```
my-agent/
└── agent/
    ├── agent.ts          # 模型与运行时配置（可选）
    ├── instructions.md   # 常驻系统提示（必需）
    ├── tools/            # 类型化工具
    ├── skills/           # 按需加载的操作手册
    ├── channels/         # HTTP、Slack、Discord 入口
    ├── subagents/        # 可委派任务的子 Agent
    ├── sandbox/          # 隔离执行环境配置
    ├── connections/      # 外部 MCP/OpenAPI 连接
    ├── schedules/        # 定时任务
    ├── hooks/            # 生命周期钩子
    └── lib/              # 共享代码
```

最小的 Agent，甚至可以从一份 `instructions.md` 开始。

### 03.2 为什么这设计舒服

因为 Agent 的角色、工具、技能、入口都落在普通文件里，它们就能：

- 进 Git 做版本管理；
- 走 Pull Request 审查；
- 看 instructions 改前改后的 diff；
- 对不同版本建 Preview 环境；
- 出问题时回滚到上一个提交。

| 维度 | 控制台配置型平台 | Eve 文件型 | 标叔的结论 |
|------|----------------|-----------|-----------|
| 版本管理 | 导出导入 / 无 | Git 原生 | 文件赢 |
| 审查 | 截图或录屏 | PR diff | 文件赢 |
| 回滚 | 手动备份 | git revert | 文件赢 |
| 上手成本 | 低 | 需会 TS/Markdown | 平台略赢 |
| 多环境 | 平台功能 | Preview 分支 | 平手 |

重点看"版本管理"那行。Agent 也是一种软件，该用软件的方式管。

### 03.3 默认就给你的能力

你以为只写了两份文件？其实 Eve 默认 harness 已经给了 Agent 四类工具：文件、Shell、Web、委派。所以哪怕不加任何工具，Agent 也能读文件、跑命令、搜网页、调子 Agent。

> **核心建议**：从最小开始，逐步加目录
>
> 先只有 `instructions.md` + `agent.ts`。需要工具加 `tools/`，需要流程加 `skills/`，需要接 Slack 加 `channels/`。每加一个目录，对应解决一个明确问题。

[向前桥接] 架构清楚了。下面进核心能力。先讲最反直觉也最关键的：Durable。

---

## Part 2: 核心能力

深入 Eve 的关键能力，每章一个核心概念。

## §04 Durable：Agent 不害怕重启

### 04.1 普通请求扛不住长任务

普通聊天接口一问一答，请求结束任务就结束。Agent 却经常不是这样。

它可能等一个慢查询，可能让用户补材料，可能在危险操作前等审批。一次任务持续几小时甚至几天，不奇怪。

把这种任务绑在普通 HTTP 请求上，超时、断线、进程重启迟早找上门。

### 04.2 会话即工作流

Eve 把每段会话作为 durable workflow 运行。底层用开源的 Workflow SDK。工作流步骤会被 checkpoint；任务等待消息时可以暂停，收到新消息从原位置恢复。

按官方说法，中间崩溃或重新部署，会话也能继续推进。

类比一下：

- 普通对话像打电话，挂了就断。
- Agent 会话像寄快递，中途可以停，收到新信息接着走。
- Durable workflow 像带 checkpoint 的流水线，任何一步断了，从断点重来，不重做前面。

> **标叔的经验**：Durable 不是免费魔法
>
> 框架能存执行状态，但决定不了"这笔退款能不能再调一次"。工具有没有副作用、恢复后会不会重复执行、操作是否幂等，仍要你设计。

### 04.3 实战：一个跨天的会话

```bash
# 第一天：开会话，Agent 跑到一半等你补材料
curl -X POST http://127.0.0.1:2000/eve/v1/session \
  -d '{"message":"帮我分析上季度日志，缺的部分告诉我"}'
# 返回 continuationToken，进程重启也不怕

# 第二天：拿 token 续聊，从停的地方继续
curl -X POST http://127.0.0.1:2000/eve/v1/session/<id> \
  -d '{"continuationToken":"<token>","message":"数据补上了，继续"}'
```

| 维度 | 普通 HTTP Agent | Eve Durable | 标叔的结论 |
|------|---------------|-------------|-----------|
| 进程重启 | 会话丢失 | 从 checkpoint 恢复 | Durable 赢 |
| 等审批 | 连接常驻 | 暂停后恢复 | Durable 赢 |
| 实现成本 | 自己写队列 | 框架默认 | Durable 赢 |
| 幂等责任 | 你自己管 | 还是你自己管 | 平手 |

[向前桥接] 能恢复还不够。Agent 跑出来的代码，得关进笼子里。下一章讲 Sandbox。

## §05 Sandbox：给 Agent 一台隔离的电脑

### 05.1 真实计算能扩大能力，也扩大风险

很多复杂任务无法提前备好所有工具。让 Agent 分析陌生日志，它可能临时写段 Python；处理 CSV，它可能生成聚合脚本。

模型生成的命令和代码，应被视为不可信输入。直接放进应用运行时执行，一次错误路径判断就可能把 Agent 问题变成生产事故。

### 05.2 默认就有的隔离

Eve 给每个 Agent 提供隔离沙箱。本地开发可用 Docker、microsandbox 等适配器；部署到 Vercel 后可切到 Vercel Sandbox，不改业务逻辑。

注意一个关键区别：你在 `tools/` 里写的工具跑在应用进程（带 `process.env`）；而文件读写、Shell 执行、代码运行，默认进沙箱。

配置沙箱很简单：

```typescript
// agent/sandbox/sandbox.ts
import { defineSandbox, vercelSandboxBackend } from "eve/sandbox";

export default defineSandbox({
  backend: vercelSandboxBackend({ runtime: "node24" }), // 选运行时
});
```

### 05.3 安全观：默认不信任

我很喜欢这个设计背后的态度：不是禁止 Agent 写代码，而是默认它写出的代码不值得信任。

> **核心建议**：文件产物别污染源码
>
> Agent 在 `/workspace` 下写的研究笔记、草稿、临时文件，是沙箱工作区，不是你的项目源码。把运行产物和 Agent 定义代码分清楚。

| 维度 | 直接跑应用进程 | 进沙箱 | 标叔的结论 |
|------|--------------|--------|-----------|
| 文件删除风险 | 高 | 隔离 | 沙箱赢 |
| 依赖污染 | 可能 | 干净 | 沙箱赢 |
| 执行延迟 | 低 | 略高 | 进程略赢 |
| 配置成本 | 无 | 一个文件 | 平手 |

[向前桥接] 沙箱解决了"乱跑"的问题。可有些事，不该让它自己跑。下一章讲 Approvals。

## §06 Approvals：成熟的 Agent 知道何时停手

### 06.1 human-in-the-loop

Agent 能调工具，不代表每个工具都该自动执行。查订单和取消订单不是一回事；看部署记录和回滚生产也不是一回事。

Eve 内置 human-in-the-loop approval。遇到要人确认的动作，工作流暂停；你批准或拒绝后，从当前状态继续。

审批不只存在于专用后台。channel 能把审批映射到真实界面，比如在 Slack 里显示按钮。

### 06.2 风险分级

一个实用起点：

- 读取与分析：自动执行；
- 修改外部系统：需要审批；
- 删数据、回滚生产、大额付费：更严格确认。

| 动作类型 | 是否自动 | 标叔的建议 |
|---------|---------|-----------|
| 查日志、读文档 | 自动 | 放心跑 |
| 发消息、建 Issue | 审批 | 人点一下 |
| 删库、回滚、付费 | 强确认 | 双重确认 |

### 06.3 实战：把审批放进流程

> **标叔的经验**：失败的子 Agent 别偷偷补完
>
> 内容团队里，如果 researcher 挂了，让 root Agent 悄悄把活自己干完，界面上看着流程完整，实际那人没参与。我更愿看到"researcher 这步失败了，是否缩小任务重试"。可观察比假装完整重要。

[向前桥接] 哪些动作要人批，清楚了。可一个人干不完所有活。下一章讲 Subagents。

## §07 Subagents：一支分工明确的团队

### 07.1 子 Agent 的价值

子 Agent 本身也是个目录，可以有自己的 instructions、tools、skills、模型、沙箱。主 Agent 把它当工具调用，子 Agent 在干净上下文里干完，把结果交回。

它的价值不是把一个头像变五个，而是两件事：

第一，复杂任务拆成边界更清楚的子任务；第二，不同任务用不同上下文和最小权限工具。

举例一次线上事故：

- 日志分析 Agent 只读日志与指标；
- 代码调查 Agent 只看 GitHub 变更；
- 影响评估 Agent 只查订单和用户数据；
- 主 Agent 综合证据做决定。

这种隔离减少上下文污染，也缩小每个 Agent 的权限范围。

### 07.2 一个边界细节

注意：声明的子 Agent 不会继承 root 的 authored slots。

root 有 `agent/skills/topic_planning.md`，不代表 researcher 自动拥有它。每个子 Agent 是独立 agent root，只发现自己目录下的内容。想让子 Agent 用某 skill，就把它放进子 Agent 自己的 `skills/`。

### 07.3 实战：三个角色

```typescript
// agent/subagents/researcher/agent.ts
import { defineAgent } from "eve";

export default defineAgent({
  description: "Research topics, collect source plans, return briefs.", // 父 Agent 据此判断何时调用
  model: "anthropic/claude-sonnet-5",
});
```

> **核心建议**：能拆不等于应该拆
>
> 子 Agent 增加模型调用、延迟和汇总成本。一个工具调用就能搞定的事，别为了"多 Agent"三个字绕一圈。

| 维度 | 单 Agent | 子 Agent 团队 | 标叔的结论 |
|------|---------|--------------|-----------|
| 上下文干净 | 易污染 | 隔离 | 团队赢 |
| 权限最小化 | 难 | 易 | 团队赢 |
| 成本 | 低 | 高 | 单 Agent 赢 |
| 适用 | 简单任务 | 复杂任务 | 看场景 |

[向前桥接] 子 Agent 各管一摊。它们怎么知道每一步该怎么做？下一章讲 Skills。

## §08 Skills 与 Channels：操作手册与多入口

### 08.1 Skills：按需翻看的手册

skill 是 Markdown 写成的操作手册。关键是 frontmatter 里的 `description`：

```markdown
---
description: Use when planning article topics or scoring candidate ideas.
---
```

Eve 把 description 暴露给模型。任务匹配时，模型再通过 load_skill 把完整 skill 加进上下文。这样 Agent 不用每次都背着所有流程细节。

> **注意**：别内置静态选题列表
>
> 内容 Agent 最容易凭空编"看起来像热点"的标题。skill 必须写清该查哪些真实来源；查不到就列待人工核验项，别把猜测包装成事实。

### 08.2 Channels：一份逻辑，多入口

Eve 默认提供 HTTP API，也能通过 channel adapter 接 Slack、Discord、Teams、Telegram、GitHub、Linear 等。同一份 Agent 逻辑服务多个渠道，不用每接一个聊天工具重写业务流程。

接 Slack 大致这样：

```typescript
// agent/channels/slack.ts
import { connectSlackCredentials } from "@vercel/connect/eve";
import { slackChannel } from "eve/channels/slack";

export default slackChannel({
  credentials: connectSlackCredentials("slack/my-agent"), // Connect 管 OAuth
});
```

Vercel Connect 负责 OAuth 授权、同意页和 token 刷新，模型不直接看到连接地址和凭据。

| 维度 | 每渠道重写 | Eve channel | 标叔的结论 |
|------|-----------|-------------|-----------|
| 接入成本 | 高 | 一个文件 | channel 赢 |
| 凭据管理 | 自己管 | Connect 接管 | channel 赢 |
| 渠道覆盖 | 看人力 | Slack/Discord/Teams… | channel 赢 |

[向前桥接] 能力都齐了。把它们拼成一支真实团队。下一章实战。

---

## Part 3: 进阶实战

多场景、多工具、多 Agent 的复杂用法。

## §09 实战：用 Eve 搭一支内容运营团队

### 09.1 我们要做成什么

我有一个面向 Java 开发者的 SpringXX社区，一直没空维护。这一章用 Eve 从零搭一支 AI 内容团队：研究员、撰稿人、审核人，加一个当主编的主 Agent。

（这个例子改编自社区教程，已按 0.22.0 的 API 简化。）

目录结构：

```
agent/
  instructions.md          # 主编身份与协作规则
  skills/                  # 选题/写作/审稿流程
    topic_planning.md
    article_writing.md
    review_checklist.md
  subagents/
    researcher/            # 研究员，自带 topic_planning
    writer/                # 撰稿人，自带 article_writing
    reviewer/              # 审核人，自带 review_checklist
  channels/
    eve.ts
```

### 09.2 主编怎么分活

root agent 的 instructions 只做判断：当前任务属于哪一步、加载哪个 skill、把什么上下文交给哪个子 Agent、返回后怎么整合、哪些还要人确认。

研究员负责选题与来源计划；撰稿人负责大纲和草稿；审核人负责风险检查。三者各自独立上下文，互不打扰。

### 09.3 关键边界

researcher 想用 `topic_planning` skill，得在自己目录放一份。因为子 Agent 不继承 root 的 skills——这是 Eve 反复强调的边界。

```bash
# 验证 Eve 是否发现了 skills 和 subagents
npm exec -- eve info
# 它会列出发现的 skills、subagents 和编译产物
```

> **标叔的经验**：先跑通再扩展
>
> 这个拆法主要是说明 Eve 的 skills、subagents、协作边界，不代表内容团队最佳实践。真实项目你完全可按自己的业务重新设计角色。

[向前桥接] 团队搭好了。可上线后才是真正的开始。下一章讲可观测与评测。

## §10 Tracing 与 Evals：上线才是真正的开始

### 10.1 Tracing：出错后能复盘

Agent 运行后，每次模型调用、工具调用、沙箱命令都能进 trace。Eve 用 OpenTelemetry，可接入现有可观测平台；部署在 Vercel 上时，还能在 Agent Runs 里看会话执行过程。

这回答了 Demo 常忽略的问题：Agent 出错后，怎么知道它当时看了什么、调了什么工具？

### 10.2 Evals：升级前先验证

instructions、skills、tools 都是仓库里的文件。一次看似无害的修改，也可能改变 Agent 行为。

Eve 提供评测能力：你可以定义带评分标准的测试集，在本地运行，也能接入 CI，把行为回归挡在部署之前。具体命令和配置随版本演进，以你安装版本的文档为准。

> **核心建议**：把 evals 接进 CI
>
> 我建议每次改 instructions 都跑一遍评测。比上线后发现"旧能力退化了"便宜得多。

| 维度 | 没可观测/评测 | 有 Tracing + Evals | 标叔的结论 |
|------|-------------|-------------------|-----------|
| 出错复盘 | 靠猜 | 看 trace | 评测赢 |
| 行为回归 | 上线才发现 | CI 挡住 | 评测赢 |
| 接入成本 | 无 | 需写用例 | 平手 |

[向前桥接] 能跑、能看、能评测，就差判断了。下一章做总结。

## §11 Eve 是 Agent 时代的 Next.js 吗

### 11.1 类比合理，但为时过早

Vercel 的类很大胆：像 Next.js 之于 Web App，但这次面向 Agent。

这个类比有道理。Next.js 当年没发明 React，也没发明服务端渲染，它把路由、构建、渲染、数据获取、部署装进一套约定里。Eve 走相似路线：没发明大模型、Tool Calling、工作流、沙箱或 OAuth，而是把 Agent 反复出现的结构固定下来。

但截至 2026-07，Eve 仍处 Beta（npm 0.22.0，受 Vercel beta 条款约束）。框架、API、文档、行为都可能变。说它已成"Agent 时代的 Next.js"，太早。

### 11.2 哪些团队现在就能试

如果你做这几类项目，Eve 值得进技术验证名单：

- 任务会持续很久，需要暂停和恢复；
- Agent 需要跑脚本或处理文件；
- 要接 GitHub、Slack、Linear 等团队系统；
- 有必须人工确认的高风险动作；
- 想用 Git、Preview、CI 管 Agent 变更；
- 项目已用 Vercel 技术栈。

强依赖私有化部署、已有成熟工作流平台、或暂时接受不了 beta API 变化的团队，先别把核心业务押上去。

| 团队类型 | 现在试 Eve？ | 标叔的建议 |
|---------|------------|-----------|
| Vercel 栈 + 长任务 | 可以 | 直接验证 |
| 已有成熟 Agent 平台 | 暂缓 | 对比后再说 |
| 纯接口加一次问答 | 不必 | 用 AI SDK 更轻 |
| 强私有化部署 | 暂缓 | 等 GA 或自托管 |

> **一句话总结**：Eve 提出了一套很有 Vercel 风格的 Agent 工程答案。它能不能成事实标准，看开发者愿不愿意把真实 Agent 放上去跑。

[向前桥接] 书写到这里。下面给你一份速查表和常见坑。

---

## 附录

### A 核心概念速查表

| 概念 | 一句话 | 文件位置 |
|------|--------|---------|
| instructions.md | 常驻系统提示 | agent/instructions.md |
| agent.ts | 模型与运行时配置 | agent/agent.ts |
| tools/ | 类型化工具，文件名即工具名 | agent/tools/*.ts |
| skills/ | 按需加载的操作手册 | agent/skills/*.md |
| subagents/ | 子 Agent，独立上下文 | agent/subagents/*/ |
| channels/ | 多入口（Slack/Discord/Web） | agent/channels/*.ts |
| sandbox/ | 隔离执行环境 | agent/sandbox/sandbox.ts |
| connections/ | 外部 MCP/OpenAPI 连接 | agent/connections/ |
| schedules/ | 定时任务 | agent/schedules/*.ts |
| hooks/ | 生命周期钩子 | agent/hooks/ |

### B 常见错误与解决方案

| 问题 | 原因 | 解决 |
|------|------|------|
| `eve init` 报引擎错误 | Node 低于 24 | `nvm install 24 && nvm use 24` |
| 工具不被调用 | 文件名非 snake_case | 改成 `get_weather.ts` |
| 子 Agent 看不到 skill | 子 Agent 不继承 root skills | 在子 Agent 目录放一份 |
| 改了 instructions 行为变了 | 没跑评测 | 把 evals 接进 CI |
| 沙箱里删了项目文件 | 没区分 /workspace 与源码 | 产物写进 /workspace |

### 阅读指南

| 时间 | 章节 | 目标 |
|------|------|------|
| Day 1 | §01-§03 | 从零到第一次跑通 |
| Day 2-3 | §04-§08 | 掌握核心能力 |
| Day 4 | §09-§10 | 进阶实战与评测 |
| Day 5 | §11 + 附录 | 做判断与查漏 |

---

> **标叔出品** | AI Native Coder · 独立开发者
> 公众号「标叔」| B站「Liangdabiao」
> 基于 Vercel Eve 0.22.0（2026-07）撰写，框架仍在 Beta，API 可能变化，请以官方文档为准。
