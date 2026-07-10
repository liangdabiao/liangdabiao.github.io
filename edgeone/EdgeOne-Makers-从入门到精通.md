# EdgeOne Makers 从入门到精通

Ship Your AI Agent from Idea to Production in One Afternoon

**创建者**: 标叔

**为谁创建**: 想把想法变成可上线 AI Agent 的独立开发者、产品经理、AI 副业玩家

**基于**: EdgeOne Makers（原 EdgeOne Pages）Agent 托管能力上线版本

**最后更新**: 2026-07-07

**适用场景**: 从 0 部署一个生产级 AI Agent，只写业务逻辑，平台搞定模型、记忆、工具、观测

---

> 这本书讲一件事：怎么用 EdgeOne Makers，把你脑子里的 Agent 想法，变成一个别人能打开链接就用的服务。
>
> 我研究这个平台的第一天下午，就跑通了第一个能对话的 Agent。没填任何大模型 Key。这件事值得写一本书。

## Part 1: 起步

从零到一。读完这 Part，你能不写一行业务代码，把一个 Agent 部署上线。

## §01 EdgeOne Makers 把 Agent 基础设施一次性托住了

### 01.1 我帮朋友搭客服 Agent 那三周

去年我帮一个朋友做客服 Agent。第一周全花在搭骨架。要写 SSE 流式输出。要处理会话存储。要接模型 Key。要管工具调用状态。

真正写业务逻辑，是第三周的事。最气的是：这套骨架，每个做 Agent 的人都得过一遍。

### 01.2 它到底托住了什么

先给结论：EdgeOne Makers 把"运行沙箱、对话记忆、流式响应、工具链路、模型网关、观测"这些通用能力提前打通了。你只填业务逻辑。

| 维度   | 自己从零搭   | EdgeOne Makers | 标叔的结论   |
| ---- | ------- | -------------- | ------- |
| 流式对话 | 自己写 SSE | 模板自带           | 新手省 1 周 |
| 对话记忆 | 自己接数据库  | 平台零配置          | 不用开 DB  |
| 模型切换 | 改代码重部署  | 改环境变量          | 省一次发布   |
| 链路观测 | 自己搭日志   | 面板自带           | 按链路看    |

> **重点看**：最后两行"模型切换"和"链路观测"。
>
> 这两件事自己搞最烦。Makers 直接平台化了。

### 01.3 它不是什么

它不锁定你的框架。OpenAI SDK、Claude SDK、LangGraph、CrewAI 都支持。JS、Python 都能用。

> **标叔的经验**：平台不锁框架，比"功能多"更值钱。
>
> 我见过太多团队被某个 PaaS 绑死，换模型要重写。Makers 的模型网关把这件事解耦了，这点我给好评。

### 01.4 适合谁，不适合谁

适合：想快速验证 Agent 想法的独立开发者。想做 MVP 的产品经理。

不适合：要深度改运行时内核的团队。要私有化部署到大内网的场景。

装好认知，下一章我们 5 分钟跑通第一个 Agent。

## §02 5 分钟跑通你的第一个 Agent

上周我第一次点开 Makers 控制台。三下鼠标，一个能对话的 Agent 就上线了。我当场决定，这一章就讲这个最快的路。

### 02.1 你需要什么

一个腾讯云账号。一个 GitHub 账号。不用装任何东西。不用写代码。

### 02.2 我们最终要做成什么

一个能打开链接就对话的 AI Agent。你不用填大模型 Key，平台已经帮你接好了。

### 02.3 控制台风模板部署

**第一步**：进 EdgeOne Makers 的 Agent 面板。

预期结果：看到一堆官方模板。OpenAI SDK、Claude SDK、LangGraph、CrewAI 都有。

**第二步**：选一个 OpenAI Agent 模板，关联你的 GitHub 仓库。

预期结果：点"创建部署"，什么都别改。

**第三步**：等它自动跑完。

预期结果：平台自动建仓库、装依赖、构建部署。点"预览"，拿到一个临时测试域名。

> **注意**：临时链接只有 3 小时。
>
> 3 小时后链接失效。要长期用，得加自定义域名，见 §09。先体验，不急。

### 02.4 为什么没填 Key 也能聊

你可能会问：我没填大模型 API Key，它怎么就能对话了？

进 Makers 控制台的 Models 面板，你会发现：平台默认帮你对接了主流大模型，限时赠送每个用户 **50 万 Token/月**。还自动建了一个默认密钥，创建项目时注入到了环境变量里。

> **核心建议**：先体验模板，再决定要不要写代码。
>
> 很多新手一上来就写，结果卡在环境。先点三下鼠标跑通，信心就来了。

### 02.5 回顾

我们花了大概 5 分钟。没写代码。拿到一个能对话的 Agent。下一章，装好你的开发环境，准备写真东西。

## §03 装好你的开发环境

3 天前我装这套环境，把"全局安装"那个选项漏看了。折腾了一会才顺。这坑我帮你先踩了。

### 03.1 你需要什么

装好 Node.js（跑 npx 用）。准备 10 分钟。我们装一套官方 Skill 包。

### 03.2 装官方 Skill 包

**第一步**：打开终端，装 EdgeOne 官方 Skills。

```bash
# 装官方技能包，含 /makers-agents 和 /makers-deploy
npx skills add TencentEdgeOne/edgeone-makers-tools
```

预期结果：提示让你选要装的 Skill。选「智能体开发 /makers-agents」和「部署 /makers-deploy」。

**第二步**：安装范围选"全局安装"。

预期结果：之后所有项目都能用这两个 Skill。不用每个项目重装。

> **标叔的经验**：全局安装省了我很多重复操作。
>
> 我第一回装到项目级，第二个项目又装一遍。后来全改全局，一条命令通吃。

### 03.3 登录授权

**第一步**：用 `/makers-deploy` 触发首次部署。

预期结果：浏览器弹出腾讯云登录页。登录即授权。

**第二步**：特殊环境弹不出浏览器？

预期结果：自动切到 Token 登录。去 Makers 控制台设置里生成 API Token，粘贴回来就行。

### 03.4 验证环境

**第一步**：让 AI 用 `/makers-agents` 建个空项目。

预期结果：它按平台规范生成入口函数、联网搜索和对话记忆的调用骨架。

> **注意**：本地没配大模型 Key，跑不通完整对话。
>
> 别慌。这步只是验证骨架对不对。配 Key 是部署后的事，见 §04。

### 03.5 回顾

环境装好了。Skill 装好了。账号登了。下一章开始，我们一个一个拆它的核心能力。

---

## Part 2: 核心能力

深入产品的关键能力。每章一个核心概念，读完你能讲清楚"它为什么好用"。

## §04 模型网关：换模型不用改一行代码

3月前我接手一个老 Agent 项目，模型 ID 写死在代码里。换一次模型，我得改代码、测试、重部署，半天没了。我越想越不对。

### 04.1 我见过最蠢的耦合

之前有个项目，模型 ID 写死在业务代码里。换模型要改代码、测试、重新部署。一次切换，半天没了。

标叔的结论：模型选择是产品策略，不该是工程事件。

### 04.2 它是怎么解耦的

Makers 底层接了 AI 网关。代码里只留统一的接入方式。用哪个模型、哪家厂商、哪个版本，都在网关侧配。

看两个**自动注入**的环境变量：

```bash
# 网关地址，所有模型调用都走这里
AI_GATEWAY_BASE_URL=https://ai-gateway.edgeone.link/v1
# 平台自动生成的密钥，创建项目时已注入
AI_GATEWAY_API_KEY=sk-xxx
```

这两个是平台在创建项目时**自动注入**的，你不用管。模型名你自己在代码或环境变量里指定（很多模板读 `AI_GATEWAY_MODEL`）。

内置模型用 `@makers/` 前缀，比如 `@makers/hy3-preview`、`@makers/deepseek-v4-flash`。换模型就改这一个值，业务代码一行都不用动。

### 04.3 实战：从默认模型切到 DeepSeek

鱼皮做"AI 投资人 Agent"时，默认模型效果一般。他切到 DeepSeek，只做了两件事：

**第一步**：去控制台「模型与密钥」页，绑定你自己的 DeepSeek API Key。

预期结果：DeepSeek 出现在可选厂商里。

> **注意**：平台不提供厂商密钥。
>
> 内置模型免 Key，但要用 DeepSeek、OpenAI 这类厂商模型，得自己备 Key 并绑定。详情见 §19。

**第二步**：把 model 改成厂商写法，重新部署。

```bash
# 内置免 Key，开箱即用
AI_GATEWAY_MODEL=@makers/deepseek-v4-flash
# 绑定 DeepSeek Key 后，用厂商写法
AI_GATEWAY_MODEL=deepseek/deepseek-v4-pro
```

预期结果：对话质量明显变好，代码零改动。

> **重点看**：整个过程零代码改动。
>
> 业务代码始终稳定，模型能力跟着平台走。这就是网关的价值。
>
>

### 04.4 适合谁来切

产品早期追效果，用强模型。量上来追成本，切轻量模型。新模型上线想灰度，加一个环境变量的事。

换模型这件事，不该惊动你的代码。下一章讲对话记忆。

## §05 对话记忆：多轮上下文零配置

2月前我上线第一个 Agent，第二天用户就吐槽它"记性差"。我查了半天才明白，是记忆没接对。我把这个过程拆给你看。

### 05.1 我踩过的"失忆"坑

鱼皮第一次跑通 AI 投资人 Agent，发现多轮对话记不住。用户第二轮补充的信息，Agent 当没听见。

这坑不怪他。记忆是最容易被忽略的基础能力。

### 05.2 它是怎么做的

Makers 默认提供对话存储。同一次会话里，Agent 能承接前面的上下文。

关键三点：

- 零配置，开箱即用。
- 平台管理每个用户的对话历史。
- 不同用户之间互不干扰。

| 维度 | 自己接数据库 | EdgeOne Makers | 标叔的结论  |
| -- | ------ | -------------- | ------ |
| 隔离 | 自己写逻辑  | 平台托管           | 不用开 DB |
| 配置 | 改代码    | 零配置            | 省一次发布  |
| 多轮 | 自己拼上下文 | 自动承接           | 新手友好   |

> **重点看**："隔离"那一行。
>
> 多用户场景，内存管理错一点就串号。平台托管，你省心。

### 05.3 实战：让记忆生效

**第一步**：让 AI 提交一版代码，先留底。

```bash
# 先提交，改出问题好回滚
git add . && git commit -m "feat: before memory fix"
```

预期结果：代码进了仓库。

**第二步**：要求 AI 修多轮记忆，重新部署并自测。

预期结果：用户第二轮补充的信息，Agent 能接住。不会再"失忆"。

> **标叔的经验**：记忆不生效，先查是不是没走平台会话接口。
>
> 我见过有人自己另接了一套存储，结果和平台冲突。直接用平台给的，最稳。

### 05.4 回顾

记忆零配置，是 Makers 最被低估的能力。下一章，讲怎么把业务能力拆成工具。

## §06 工具调用：把能力拆成工具

6月前我做摄影师智能体那阵，一开始把经验全塞进 Prompt。结果上下文爆了，模型还用错。我白忙活一阵。我后来才学会拆工具。

### 06.1 别把知识塞进 Prompt

摄影师智能体的作者讲得很对：摄影知识别写进系统提示。系统提示适合定义角色和规则，不适合承载大量经验资料。

塞多了，上下文越来越长，模型还不一定用对。

### 06.2 拆成三类工具

摄影师智能体拆了三类工具：

- 摄影经验工具：返回构图、参数、后期建议。
- 实时天气工具：查天气、云量、日出日落。
- 说明书检索工具：从相机说明书找菜单路径和原文。

工具调用时，前端能用流式事件展示状态："正在查实时天气"。用户等待时不空白。

### 06.3 一个隐蔽的好设计

Makers 模板有个约定：文件名带下划线的，不暴露为公开路由。

```python
# _knowledge.py 是内部知识模块，用户访问不到
# 放核心经验、场景规则、参数建议
agents/_knowledge.py
```

这个设计很实用。你的核心经验放在 `_knowledge.py`，不会被用户直接访问，也不影响对外接口结构。

| 维度  | 写进 Prompt | 拆成工具 + 文件 | 标叔的结论 |
| --- | --------- | --------- | ----- |
| 上下文 | 越来越长      | 按需读取      | 工具胜   |
| 维护  | 改提示很乱     | 改一个文件     | 文件胜   |
| 安全  | 经验外泄风险    | 下划线隔离     | 文件胜   |

> **核心建议**：经验先沉淀成文件，再让工具读。
>
> MVP 阶段不用先搭向量库。加个 `_knowledge.py` 就够轻量。

### 06.4 回顾

工具是 Agent 的"手脚"。拆得好，Agent 才不空谈。下一章，讲怎么看清它到底干了什么。

## §07 观测面板：Metrics 加 Traces 看清链路

上个月我那个 Agent 答非所问，我猜了一晚上 Prompt。后来开了 Traces，十分钟定位是工具挂了。我太需要一个看清链路的办法。

### 07.1 普通日志救不了 Agent

普通 Web 应用出事，看接口日志、错误栈就行。Agent 不行。

一次对话，模型先理解，再调工具，工具返回后模型再组织回答。中间哪一步异常，光看最终回复，你根本不知道坏在哪。

### 07.2 两个面板怎么用

Makers 的观测分两块：

**Metrics**：看整体。被调用多少次、模型调用多少次、平均耗时、Token 消耗、有没有报错。适合判断服务整体正不正常。

**Traces**：看单次。每次请求一条完整链路。展开能看到：模型调了几次、调了哪些工具、入参是什么、返回了什么、每步耗时多久。

| 维度  | Metrics | Traces | 标叔的结论 |
| --- | ------- | ------ | ----- |
| 看什么 | 整体状态    | 单次细节   | 两个都要  |
| 适合  | 判断健不健康  | 定位哪步坏  | 配合用   |
| 频率  | 每天看     | 出事看    | 出事必看  |

> **重点看**："出事必看"那格。
>
> 早期用户反馈很碎。只有把链路看清，才知道是 Prompt 要改、工具要改、还是外部依赖要换。

### 07.3 实战：一次链路排查

假设用户说 Agent 答非所问。

**第一步**：开 Traces，找那次请求。

预期结果：看到模型调了两次工具，第二次入参是空的。

**第二步**：顺藤摸瓜，发现是天气工具超时。

预期结果：问题不在 Prompt，在外部接口。换数据源或加超时重试。

> **标叔的经验**：别靠猜修 Agent。
>
> 我之前猜了半天 Prompt，其实是工具挂了。有 Traces 后，十分钟定位。

### 07.4 回顾

能观测，才敢迭代。下一章，我们拿真实项目练手。

---

## Part 3: 进阶实战

多场景、多工具、多步骤的复杂用法。每章一个完整项目思路。

## §08 从模板到真实项目：摄影师智能体拆解

上周我研究腾讯云那篇实战时，最打动我的是"从模板出发"。我照着走了一遍，确认这条路能复用到任何场景。

### 08.1 它要解决什么

一个摄影师，攒了一堆构图、光线、参数的经验。用户问"今天鼓浪屿日落值不值得拍"，它要能答。

腾讯云那篇实战，把这件事拆成了七步。我们抓关键的。

### 08.2 第一步：从模板出发

最实际的第一步，不是写业务代码。是先有个能跑的骨架：用户能对话、模型能流式返回、工具调用前端有状态。

Makers 模板把这些准备好了：`/chat` 入口、SSE 流式、工具事件、中断接口、基础日志。你替换业务层，不是重搭水管。

> **核心建议**：MVP 别从空项目开始。
>
> 空项目那些基础工程，比想象中更占时间。从模板改，把精力压到业务验证上。

### 08.3 第二步到第六步：一层层接进去

- 接工具：经验、天气、说明书，三类拆开。
- 建知识库：`_knowledge.py` 沉淀摄影经验。
- 开记忆：多轮对话零配置承接。
- 接网关：模型随时换，不改代码。
- 本地测：逻辑通了再上线。

### 08.4 第七步：部署上线

这一套走完，摄影师智能体就从一个本地代码，变成了用户能访问的服务。

| 步骤 | 做了什么  | 平台替你做的     |
| -- | ----- | ---------- |
| 模板 | 业务骨架  | 对话/流式/工具链路 |
| 知识 | 经验沉淀  | 文件隔离不暴露    |
| 部署 | 填环境变量 | 构建/加速/观测   |

> **重点看**：右边"平台替你做的"那列。
>
> 开发者真正要管的，是自己的业务：用户问什么、哪些经验值得沉淀。

### 08.5 回顾

把"摄影"换成任何场景，方法都一样。下一章，讲上线后的域名和长期可用。

## §09 自定义域名与版本回滚

去年我第一次把 Agent 绑到自己域名，卡在 ICP 备案上三天。我后来才搞懂区域的门道。

### 09.1 3 小时之后怎么办

临时预览链接只给 3 小时。要长期用，必须加自定义域名。

### 09.2 绑定自定义域名

**第一步**：进"域名管理"，添加你的域名。

预期结果：看到 EdgeOne 给的默认临时域名。

**第二步**：改 CNAME 解析。

```bash
# 腾讯云注册的域名，可一键加 CNAME
# 其他注册商，去控制台手动改解析记录
# 等约 1 分钟生效
```

预期结果：解析生效，域名指向 EdgeOne。

**第三步**：配 HTTPS。

预期结果：选"申请免费证书"，EdgeOne 自动申请、续签、部署。或托管你已有的 SSL 证书。

> **注意**：加速区域含中国大陆，有硬要求。
>
> 腾讯云账号必须实名认证，且域名必须完成 ICP 备案。没这需求，选「全球可用区（不含中国大陆）」省事。

### 09.3 版本回滚

每次改动都可能引入新问题。Makers 的构建版本和回滚，让你在新版本异常时，先恢复到上一个稳定版。

| 触发方式        | 适用场景     | 标叔的结论 |
| ----------- | -------- | ----- |
| 推 main 自动构建 | Git 仓库部署 | 省心，推荐 |
| 手动新建部署      | 本地上传     | 灵活可控  |

> **标叔的经验**：回滚救过我一次。
>
> 有回改了工具逻辑，线上直接报错。一键回滚到上一版，用户无感，我再慢慢查。

### 09.4 回顾

域名和回滚，是"能演示"和"能生产"的分界线。下一章，讲最重要的思维转变。

## §10 你只写业务逻辑，这事本身就是生产力

3 天前写这本书前，我把三个资料读了一遍。我最大的感受是：平台把脏活全接了，你只剩业务逻辑。我想把这事讲透。

### 10.1 鱼皮那 20 分钟

鱼皮做"AI 投资人 Agent"，从写代码到上线，不到 20 分钟。他全程只关注业务逻辑：怎么评估一个副业想法。

联网搜索、对话记忆、模型网关、链路追踪，Makers 全帮他搞定了。

### 10.2 模型强，不够

模型再强，没有靠谱的工程化支撑，Agent 只能停在本地 Demo。

能让开发者把精力全放业务逻辑上，而不是重复造轮子，这事本身就有价值。

> **核心建议**：把"造轮子"列成清单，逐项交给平台。
>
> 流式、记忆、网关、观测——这四件 Makers 都接了。你剩下的，只有你的想法。

### 10.3 从 idea 到 MVP 的公式

我研究完两个案例，总结出一个朴素公式：

```
模板骨架 + 你的业务逻辑 + 平台基础设施 = 可上线 Agent
```

左边你写，中间你写，右边平台给。你真正拥有的，是中间那块。

### 10.4 写在最后

AI 时代，大模型能力重要。但给模型配的那套能力，同样重要。

Makers 没把开发者锁死在某种框架、语言或模型里。它把通用能力提前打通，让你只管自己的业务场景。

把一个 Agent 做成能稳定承接问题、调用工具、被观测、可部署的服务，它就不再是个聊天窗口。它是一个能持续迭代的业务。

去写你的业务逻辑吧。不过能跑只是第一步——下一章，我们进入进阶篇，把它从 demo 做成能扛流量的生产级工程。

---

## Part 4: 进阶篇

从"能跑"到"能打"。读完这 Part，你能用边缘函数、缓存策略、CLI 流水线和定时任务，把 Agent 与 Web 服务做成生产级工程，而不只是又一个 demo。

## §11 边缘函数 Pages Functions：在离用户最近的地方算

### 11.1 我为什么不再自己买服务器

2月前我接了个需求：给一个活动页加"实时倒计时 + 区域限流"。第一反应是自己开台 CVM，写个 Go 服务。算下来：机器钱、运维、扩容、被攻击的担心。我后来想，这种"请求来了算一下就返回"的逻辑，凭什么要我养一台服务器？

Makers 的边缘函数正好吃这个场景。

### 11.2 它怎么把代码铺到 3200+ 节点

先给结论：Pages Functions 运行在 EdgeOne 3200+ 边缘节点上，你的代码不用落在一台固定服务器，而是被调度到离用户最近的节点执行。

| 维度   | 自建服务器 | Pages Functions | 标叔的结论  |
| ---- | ----- | --------------- | ------ |
| 部署位置 | 单区域一台 | 3200+ 边缘节点      | 就近响应   |
| 扩容   | 自己加机器 | 平台弹性            | 不用操心峰值 |
| 延迟   | 跨地域高  | 就近低             | 体验直接好  |
| 运维   | 自己盯   | 平台管             | 省一个人   |

> **重点看**：最后一列"运维"。边缘函数把"机器"这件事从你的待办里删了。

### 11.3 路由就是目录：/functions 约定优于配置

Makers 不让你写路由表。你在项目根目录建一个 `functions/` 文件夹，里面每个 `.js` 文件自动变成一条路由。

```js
// functions/index.js          ->  example.com/
// functions/hello-pages.js    ->  example.com/hello-pages
// functions/api/users/list.js ->  example.com/api/users/list
```

文件结构即路由表。没匹配到的请求，自动回退到静态资源。

> **标叔的经验**：约定优于配置，省的是你维护路由文件的心智。新手最容易犯的错，是去翻"路由配置在哪"，其实根本没那个东西。

### 11.4 动态路由：[id] 与 [[default]]

真实 API 不可能每个 ID 写一个文件。Makers 支持两种动态段：

```js
// functions/api/users/[id].js      ->  匹配 /api/users/1024（单级）
// functions/api/[[default]].js     ->  匹配 /api/books/list（多级 catch-all）
```

```js
// functions/api/users/[id].js
export function onRequestGet({ params }) {
  return new Response(`用户 ID 是 ${params.id}`);
}
```

注意：`[id]` 只吃一级路径，`/api/users/vip/1024` 它接不住；`[[default]]` 能吞多级。选错会 404，我踩过。

### 11.5 Handlers：按 HTTP 方法分派

一个文件能同时处理多种方法，也能只认一种：

```js
export function onRequest(context) { /* 所有方法 */ }
export function onRequestGet(context) { /* 只认 GET */ }
export function onRequestPost(context) { /* 只认 POST */ }
// 还有 Put / Delete / Patch / Head / Options
```

`context` 里你能拿到：`request`（请求对象）、`params`（动态路由参数）、`env`（环境变量）。

> **警告**：边缘函数**不支持** `addEventListener`，别拿传统 Service Worker 那套来写。它只认 Function Handlers。我第一次写就栽在这。

### 11.6 三个真实示例：geo / KV / supabase

**（1）拿客户端地理位置**——`context.request.eo.geo` 直接给你：

```js
export function onRequest({ request }) {
  const geo = request.eo.geo;
  return new Response(JSON.stringify({ geo }), {
    headers: { 'content-type': 'application/json; charset=UTF-8' },
  });
}
```

**（2）用 KV 存访问数**——`my_kv` 是你在项目里绑定的命名空间变量名：

```js
export async function onRequest({ env }) {
  const n = Number(await my_kv.get('visitCount')) + 1;
  await my_kv.put('visitCount', String(n));
  return new Response(JSON.stringify({ visitCount: n }));
}
```

**（3）连三方数据库 supabase**：

```js
import { createClient } from '@supabase/supabase-js';
export async function onRequest({ env }) {
  const supabase = createClient(env.supabaseUrl, env.supabaseKey);
  const { data } = await supabase.from('users').select('*');
  return new Response(JSON.stringify({ users: data }));
}
```

> **标叔的建议**：示例三连三方库，记得把依赖装进项目，别以为边缘节点自带。详见 §13 的环境变量与 §14 的 includeFiles。

### 11.7 边缘函数不是银弹

它跑的是 V8、ES6、标准 Web API（Fetch / Cache / Crypto / Stream 都有）。但单函数有运行时长上限，重计算别往里塞。

能在边缘算的"轻逻辑"——鉴权、改写、限流、拼装——用它；要算半天的重活，留给云函数或你的后端。

下一章，我们让这些静态资源和函数响应"快到极致"。

---

## §12 缓存与 edgeone.json：把性能和规则配出来

### 12.1 浏览器缓存与边缘缓存是两件事

3 天前我帮人调一个"更新了但用户看不到新页面"的 bug。根因是他把浏览器缓存和边缘缓存混为一谈。

- **浏览器缓存**：存在用户浏览器里。Makers 对带哈希的文件（如 `main.a1b2c3.js`）给 `max-age=31536000`（一年）长期缓存；对 `index.html` 给 `max-age=0`，保证新鲜。
- **边缘缓存**：存在 EdgeOne 节点上，静态资源首次请求后缓存，最长三个月。每次新部署自动失效。

> **重点看**：边缘缓存"新部署自动失效"这件事，意味着你不用手动清缓存。改完推上去，用户自然拿到新的。

### 12.2 默认规则够用，但你要懂

大部分项目用默认就够。但当你要改响应头、做重定向、自定义构建，就得上 `edgeone.json`——放在项目根目录，覆盖控制台的项目设置。

### 12.3 用 edgeone.json 改缓存与加安全头

```json
{
  "headers": [
    {
      "source": "/*",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "Cache-Control", "value": "max-age=7200" }
      ]
    },
    {
      "source": "/assets/*",
      "headers": [
        { "key": "Cache-Control", "value": "max-age=31536000" }
      ]
    }
  ]
}
```

> **标叔的提醒**：`headers` 最多 30 条；key 限 1-100 字符、value 限 1-1000 字符且**不支持中文**。我见过有人把中文塞进 value，部署直接挂。

### 12.4 重定向与重写：redirects / rewrites

```json
{
  "redirects": [
    { "source": "/articles/:id", "destination": "/news-articles/:id", "statusCode": 301 },
    { "source": "/old-path", "destination": "/new-path", "statusCode": 302 }
  ],
  "rewrites": [
    { "source": "/assets/*", "destination": "/assets-new/:splat" }
  ]
}
```

| 能力           | 行为             | 数量上限  | 标叔的结论    |
| ------------ | -------------- | ----- | -------- |
| redirect     | 换 URL（301/302） | 100 条 | 改路径用它    |
| rewrite      | 内部改写，URL 不变    | 100 条 | 静态资源迁移用它 |
| 两者 source 长度 | ≤500 字符        | -     | 别写超长     |

> **警告**：`rewrites` 只适用于静态资源，不支持 SPA 前端路由重写。SPA 的重写得用框架自己的路由系统，别在 edgeone.json 里硬配。

### 12.5 自定义构建：buildCommand / nodeVersion

```json
{
  "buildCommand": "next build",
  "installCommand": "npm install",
  "outputDirectory": "./build",
  "nodeVersion": "22.11.0"
}
```

> **标叔的建议**：`nodeVersion` 只认预装版本（14.21.3 / 16.20.2 / 18.20.4 / 20.18.0 / 22.11.0）。填别的号，部署直接失败。这坑我替你记着。

### 12.6 配置即代码，别只在控制台点

上面这些，控制台都能点。但写在 `edgeone.json` 里，它随仓库版本走，回滚跟着代码回滚。

下一章，我们用 CLI 把这些"点出来的配置"变成"敲出来的命令"。

---

## §13 CLI 与 CI/CD：把部署写进流水线

### 13.1 双命令体系：makers 与 pages

3月前我把 CI 脚本从 `edgeone pages deploy` 改成 `edgeone makers deploy`。不是闲得慌，是新产品名（Pages 升级成 Makers）有了新命名空间。

先给结论：现在有两套命令，`edgeone makers <command>`（推荐）和 `edgeone pages <command>`（过渡期可用）。**两者等价**，老命令暂时不会下线，但新功能只在 `makers` 下提供（比如 `edgeone makers create`）。

> **标叔的建议**：新项目直接用 `makers`；存量脚本过渡期内不急着改，但别拖到老命令真下线那天。

### 13.2 本地开发：init / link / dev

```bash
npm install -g edgeone     # 装 CLI
edgeone -v                 # 看版本
edgeone login              # 登录，选 Global 或 China
edgeone whoami             # 看当前账号

edgeone makers init        # 在现有项目初始化，生成 edge-functions/ 等
edgeone makers link        # 关联控制台已建的项目，拉环境变量到本地
edgeone makers dev         # 本地 8088 端口起服务，热更新调试
```

> **警告**：`edgeone makers dev` 默认读 `edgeone.json` 的 `devCommand`；**千万别在 edgeone.json 或 package.json 里把 dev 命令配成 `edgeone makers dev`**，会套娃。dev 服务有启动次数限制，别频繁重启。

### 13.3 部署：deploy 与多环境

```bash
edgeone makers deploy            # 生产环境
edgeone makers deploy -e preview # 预览环境
edgeone makers deploy ./dist     # 部署本地已构建产物
```

`-e preview` 出来的就是 §09 讲过的那个临时预览链接（3 小时有效）。生产部署才进正式域名。

### 13.4 CI/CD：API Token + deploy

把部署写进流水线，核心就一句：用 API Token 代替登录。

```bash
# 生产
edgeone makers deploy -n project-name -t $EDGEONE_API_TOKEN
# 预览
edgeone makers deploy -n project-name -e preview -t $EDGEONE_API_TOKEN
```

Token 在 Makers 控制台生成。这样你的 GitHub Actions / 任意 CI 推完代码就自动部署，零人工。

| 方式                 | 适合        | 标叔的结论    |
| ------------------ | --------- | -------- |
| Git 推送自动构建         | 大多数项目     | 默认就用它    |
| CLI deploy + Token | CI/CD 流水线 | 要自动化必选   |
| 控制台手动点             | 临时验证      | 能脚本化就别手点 |

### 13.5 环境变量管理：env ls/pull/set/rm

```bash
edgeone makers env ls              # 列出控制台所有环境变量
edgeone makers env pull            # 拉到本地 .env
edgeone makers env pull -f .env.prod
edgeone makers env set KEY value   # 新增/修改
edgeone makers env rm KEY          # 删除
```

> **标叔的经验**：环境变量别写死在代码里（§04 讲过模型网关解耦）。用 `env pull` 把生产变量拉到本地调试，和线上保持一致，少踩"我本地好的"那种坑。

### 13.6 能脚本化的都别手点

部署、环境变量、预览——凡是能敲命令的，都写进脚本和流水线。控制台点一遍很爽，点第十遍就烦了，而且人点容易错。

下一章，我们用定时任务和函数微调，把"自动跑"这件事补上。

---

## §14 定时任务与组合实战：让 Agent 真正自动跑起来

### 14.1 schedules：cron 触发函数

3月前我想做个"每天凌晨清理一次临时数据"的活。以前得养个 cron 服务器。现在 Makers 的 `schedules` 直接在 edgeone.json 里配：

```json
{
  "schedules": [
    {
      "name": "daily-cleanup",
      "cron": "0 2 * * *",
      "path": "/api/cron/cleanup",
      "timezone": "Asia/Shanghai"
    }
  ]
}
```

`cron` 是标准 5 段（分 时 日 月 周），不支持秒级。`timezone` 用 IANA 时区，不填就取构建机时区——**跨时区团队务必显式写**，不然构建机在美国，任务半夜跑你国内白天。每次部署平台自动比对新配置，移除的任务会自动停。

### 14.2 cloudFunctions 微调

函数不止能写，还能调：

```json
{
  "cloudFunctions": {
    "nodejs": {
      "maxDuration": 60,
      "includeFiles": ["assets/**", "!assets/**/*.tmp"],
      "externalNodeModules": ["svg-captcha"]
    },
    "mainlandRegions": ["ap-beijing"],
    "overseasRegions": ["ap-tokyo"]
  }
}
```

| 配置                       | 作用                  | 标叔的结论    |
| ------------------------ | ------------------- | -------- |
| maxDuration              | 单次最长 10-120s，默认 30s | 重活调大     |
| includeFiles             | 把文件打进产物让函数读         | 读文件必配    |
| externalNodeModules      | 含原生模块的依赖            | 编译型依赖必配  |
| mainland/overseasRegions | 指定部署地域              | 国内/海外分别定 |

> **警告**：`includeFiles` 用相对路径（别以 `./` 或 `/` 开头），支持 glob。函数里用相对路径 `readFileSync('assets/your-file.png')` 读取。我第一次忘了配，部署后读不到文件，排查半天。

### 14.3 组合实战：geo + KV + 缓存的"访问画像" API

把前面学的串起来。一个边缘函数，记录每个访客的地区和累计访问数，并加缓存减轻 KV 压力：

```js
// functions/api/profile.js
export async function onRequest({ request, env }) {
  const geo = request.eo.geo;
  const region = geo.country || 'unknown';

  let n = Number(await my_kv.get(`visits:${region}`)) || 0;
  n += 1;
  await my_kv.put(`visits:${region}`, String(n));

  return new Response(JSON.stringify({ region, visits: n }), {
    headers: {
      'content-type': 'application/json; charset=UTF-8',
      'Cache-Control': 'max-age=60',
    },
  });
}
```

边缘函数就近算、KV 存状态、Cache-Control 兜底——三件事一次讲完。

> **标叔的结论**：进阶篇学的不是"更多功能"，是"把功能拼成工程"。边缘函数管计算、缓存管速度、CLI 管交付、定时任务管自动——你手里这套，已经够做一个正经产品。

### 14.4 你手里已经是生产级工具箱

到这，从第一个 Agent 到边缘函数、缓存、流水线、定时任务，链路通了。平台把脏活接了，你只写业务。

附录里我整理了环境变量速查表、edgeone.json 字段清单和常见报错，需要时翻一下。去把你的想法做成能自动跑的服务吧。接下来，Part 5 我们换到实战模板视角——用 8 个真实案例，看别人怎么把 Makers 的 Agent 能力直接做成产品。

---

## Part 5: 最佳实践篇

## §15 给网站加一个会"看"页面的 AI 对话助手

3天前我帮一个做技术博客的朋友接 AI 助手。他最怕两件事：一是要改一大堆后端代码，二是 AI 答非所问。我用 EdgeOne Makers 的 **AI Assistant 模板**给他半小时搞定，零后端改动。这一章我就把这事拆给你看。

> 经验：很多人以为"给网站加 AI 客服"得自己搭 RAG、向量库、检索服务。在 Makers 上不用——模板把脏活全接了，你只写业务 API 的 Schema。

### 15.1 它到底解决什么

你给网站加一段 `<script>`，右下角就多一个聊天气泡。用户问"这篇文章讲了什么"，AI 能根据**当前页面内容**回答；问"搜一下 React 相关的文章"，AI 会调用你的搜索接口返回真实数据。支持嵌到任何站点：React、Vue、WordPress、纯静态 HTML 都行。

### 15.2 部署：一行代码的事

先在 Makers 控制台用 AI Assistant 模板部署一个 Agent。配置环境变量：

| 变量                    | 必填 | 说明                                       |
| --------------------- | -- | ---------------------------------------- |
| `AI_GATEWAY_MODEL`    | 否  | 模型 ID，默认 `@makers/deepseek-v3`           |
| `DATA_API_BASE_URL`   | 否  | 你的后端 API 根地址，如 `https://api.example.com` |
| `DATA_API_KEY`        | 否  | 后端认证 Token，会加到 `Authorization: Bearer` 头 |
| `AI_GATEWAY_API_KEY`  | 是* | 模型网关 Key，一键部署时自动注入                       |
| `AI_GATEWAY_BASE_URL` | 是* | 模型网关地址，一键部署时自动注入                         |

> 标叔的结论：`AI_GATEWAY_API_KEY` / `AI_GATEWAY_BASE_URL` 标星是因为**一键部署会自动注入**，你根本不用管；只有本地调试才手动填。别被"必填"吓到。

部署完绑定自定义域名（如 `chat.example.com`），然后在网站 `</body>` 前加一行：

```html
<script src="https://chat.example.com/embed.js" async></script>
```

刷新页面，气泡就出现了。完事。

### 15.3 外观与提示词都能改

气泡颜色、位置、名字靠 `data-*` 属性：

```html
<script
  src="https://chat.example.com/embed.js"
  data-color="#10b981"
  data-position="bottom-left"
  data-name="小助手"
  async></script>
```

AI 的人设、欢迎语、推荐问题写在项目根目录的 `ai-chat-assistant.config.json`：

```json
{
  "name": "我的助手",
  "welcome": "你好！有什么可以帮你的？",
  "systemPrompt": "你是一个专业的电商客服助手。回答要简洁友好，优先推荐店铺商品。",
  "suggestedQuestions": ["有哪些热门商品？", "如何查询订单状态？"]
}
```

> 建议：`systemPrompt` 别写"你是万能助手"。越具体（行业 + 语气 + 优先动作），AI 越不跑偏。

### 15.4 让 AI 查你的业务数据：API Schema

光靠页面内容不够，得让 AI 调你的接口。写 `api-schema.json`：

```json
{
  "endpoints": [
    {
      "path": "GET /api/posts/{id}",
      "description": "Get the full content of a single blog post by its ID. Use search_posts first if you don't know the ID."
    }
  ]
}
```

| 写法                                   | 效果                         |
| ------------------------------------ | -------------------------- |
| `GET /api/posts/{id}` + `{"id":"5"}` | 变成 `GET /api/posts/5`      |
| `GET` 多余参数                           | 拼成 query string `?q=react` |
| `POST` 多余参数                          | 放进 JSON body               |

> 警告：`description` 写"获取数据"这种模糊话，AI 根本不知道什么时候该调。写成"功能 + 使用时机"才灵。AI 只能调你 Schema 里定义的接口，不会自己乱造请求——这是安全边界，不是缺陷。

后端要开 CORS：

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

### 15.5 它怎么工作的

`embed.js` 注入气泡 + 一个同源 iframe（加载 `/widget`）。iframe 提取页面内容，通过 `postMessage` 发给 Agent；Agent 调 `/chat`，把页面内容塞进上下文，判断要不要查你的 API，最后用 **SSE 流式**把答案推回来。

> 经验：用 iframe 是因为它和 Agent 同域，内部请求同源，没有跨域麻烦。你后端在哪都行（AWS、阿里云、自建），只要 `DATA_API_BASE_URL` 指过去。

### 15.6 本地调试与常见坑

```bash
git clone https://github.com/你的用户名/ai-assistant.git
cd ai-assistant
npm install
cp .env.example .env   # 填入 AI_GATEWAY_API_KEY 等
edgeone makers dev     # 本地开发服务器
```

| 问题               | 答案                                        |
| ---------------- | ----------------------------------------- |
| 后端不在 Makers 上能用吗 | 能，只要公网可达                                  |
| 不配 Schema 能用吗    | 能，AI 只看页面内容                               |
| 支持哪些模型           | 所有 OpenAI 兼容的：DeepSeek、GPT-4o、Claude、通义千问 |
| SPA 支持吗          | 支持，路由切换自动重新提取页面                           |

> 标叔的结论：每轮对话 AI 最多调 4 次工具，频率限制在**你后端**做。Agent 本身不替你限流。

下一章，我们换个角度——不碰 UI，直接用一句话让 AI 把整个项目部署上线。

## §16 AI 对话式部署：用 Skill 一句话部署项目

2周前我在地铁上突然想做个小游戏发给朋友。没带电脑，我就对着手机里的 AI 说了一句"帮我做个贪吃蛇小游戏，部署到 EdgeOne Makers"，几分钟后拿到一个能玩的链接。这就是 **Makers Deploy Skill** 的威力——对话即部署。

> 经验：Skill 不是插件、不是脚本，而是一份交给 AI 的"操作手册"（Anthropic 提出的开放规范）。它告诉 AI 该做什么、怎么做、出错怎么办。AI 加载后，就变成了一位会自动判断环境、选策略、执行部署的运维工程师。

### 16.1 先装 Skill

三种方式，挑顺手的：

| 方式       | 操作                                                                                |
| -------- | --------------------------------------------------------------------------------- |
| 自然语言（推荐） | 在 AI 工具里说："帮我安装这个 skill：<https://github.com/TencentEdgeOne/edgeone-pages-skills>" |
| 命令行      | `npx skills add TencentEdgeOne/edgeone-pages-skills`                              |
| 手动       | 下载仓库，把 `skills/edgeone-pages-deploy/` 放进 AI 工具的 skills 目录                         |

> 标叔的结论：我一般用自然语言装，因为 AI 会自己拉仓库、解析、落盘，全程不用我动手。CodeBuddy / Claude Code / Cursor 都原生支持这套规范。

### 16.2 一句话触发部署

装完之后，部署就是一句话的事。

**场景一：在 CodeBuddy 里加功能并预览**

我对 AI 说："帮我新增个暗黑模式，然后部署一个预览环境到 EdgeOne Makers"。CodeBuddy 加载 Skill 后自动走四步：

1. **环境检查**：检测 EdgeOne CLI 是否装好、版本对不对，没装就自动 `npm install -g edgeone`
2. **登录认证**：没登录就引导浏览器完成认证
3. **项目构建**：自动识别框架（如 Vue.js）执行构建
4. **部署上传**：把产物推到 Makers

全程我只在它提问时确认少量信息（比如选中国站/国际站），其余全自动。从发指令到拿到线上 URL，通常 1–2 分钟。

**场景二：在 OpenClaw 里从零造**

OpenClaw 是开源 AI Agent 框架，能接企业微信、飞书、Telegram。我在 IM 里说"帮我做一个贪吃蛇小游戏，部署到 EdgeOne Makers"，AI 从零生成代码 → 检查环境 → 登录 → 构建 → 上线，返回一个可访问链接。有 bug 就再让它修、再部署。

> 建议：部署到 Makers 的项目是**持久化**的——每次部署更新同一个站点 URL，你能不断迭代，就像传统 CI/CD。项目也能在 Makers 控制台管理：绑域名、看部署历史。

### 16.3 远程 / CI 环境怎么登录

浏览器登录在远程服务器、SSH、CI/CD 里走不通，Skill 会自动切到 **API Token** 方式。Token 在中国站 / 国际站控制台创建。Agent 首次用 Token 后会问你要不要存到本地 `.edgeone/.token`，之后自动复用。

| 要点       | 说明                                             |
| -------- | ---------------------------------------------- |
| Token 权限 | Makers 账户级别，请妥善保管                              |
| 切勿提交     | 别把 `.edgeone/.token` 推进代码仓库                    |
| 错误处理     | Skill 内置修复逻辑：CLI 版本不对自动重装、登录过期引导重登、构建失败分析日志给建议 |

> 警告：API Token 等于你账号的钥匙。我用它时只放在本地或 CI 的 secret 里，绝不写进 `.env` 还 `git add`。

### 16.4 支持哪些框架

EdgeOne CLI 会自动识别框架并选对构建策略，你不用手动配：

| 类别       | 框架                     |
| -------- | ---------------------- |
| 全栈 / SSR | Next.js、Nuxt、SvelteKit |
| 静态生成     | Astro、Vite             |
| 前端库      | React、Vue              |

> 标叔的结论：你只管写业务代码，部署的脏活交给 Skill。它和 Makers 的 Agent 原生能力是一套思路——把"怎么部署"这件事，从人的记忆里挪进机器的操作手册。

下一章，我们正面看 AI 应用本身：怎么用通用大模型，几分钟搭出一个能对话、能生图的站点。

## §17 用通用大模型快速搭建 AI 应用

4周前有个读者问我："我想做个 AI 聊天 + AI 生图的小站，但怕被某个模型绑死。"我给他指了 Makers 的 AI 应用模板——原生接口和 SDK 封装两条路都给好了，模型想换就换。这一章讲清楚这两条路怎么选。

> 经验：搭 AI 应用最怕两件事——一是被某家模型 API 绑架，二是为接模型写一堆胶水代码。Makers 的模板把 API Key 收口到环境变量，把调用收口到两套标准模板，你换模型只改一个变量。

### 17.1 两条技术路径

| 路径          | 适合谁         | 灵活度 | 开发量 |
| ----------- | ----------- | --- | --- |
| 原生接口调用      | 要深度定制、自己控请求 | 高   | 中   |
| AI SDK 封装调用 | 想快速集成、少写代码  | 中   | 低   |

模板清单：

| 能力    | 原生接口模板                       | AI SDK 模板                        |
| ----- | ---------------------------- | -------------------------------- |
| AI 对话 | `ai-chatbot-starter`         | `ai-sdk-chatbot-starter`         |
| AI 生图 | `ai-image-generator-starter` | `ai-sdk-image-generator-starter` |

### 17.2 先拿 API Key

API Key 是访问模型的身份凭证，类似账号密码。不是所有都要申请，用到哪个申哪个。

**对话模型**：DeepSeek、OpenAI、Google、Anthropic/Claude、xAI

**图片模型**：HuggingFace、Replicate、FAL、Nebius、Fireworks、DeepInfra、Luma、Together AI

> 标叔的结论：新手先拿 DeepSeek 或 OpenAI 的 Key 跑通对话，生图等真要用了再申。别一上来把八家 Key 全申请一遍。

### 17.3 一键部署

进模板详情页，点左侧蓝色 **Deploy** 按钮 → 进 Makers 控制台。配置面板本质就是在填 API Key：不同模板按它支持的模型列出不同变量，你至少填一个能用的 Key。

```bash
# 以 ai-sdk-chatbot-starter 为例
git clone https://github.com/${your-github-account}/vercel-ai-sdk-chatbot.git
cd vercel-ai-sdk-chatbot
```

填好环境变量，点 "start deployment"，完事就能开预览地址。

### 17.4 本地调试

部署后关联的 GitHub 账号下会多一个项目。把它拉到本地改：

```bash
git clone https://github.com/${your-github-account}/vercel-ai-sdk-chatbot.git
cd vercel-ai-sdk-chatbot
edgeone makers link   # 关联 Makers 项目，把云端环境变量同步到本地 .env
edgeone makers dev    # 本地 DEV 模式，访问 localhost:8088
```

> 建议：`edgeone makers link` 会在本地生成 `.env` 并同步云端变量，省得你手动抄。改完代码推 GitHub，Makers 自动监听、自动重新部署——你看到 "Deploying" 状态就是在跑了。

```bash
git add .
git commit -m "调整对话界面"
git push origin main
```

### 17.5 模型怎么换

因为 Key 全在环境变量里，换模型就是改 `AI_GATEWAY_BASE_URL` / `AI_GATEWAY_API_KEY` / `AI_GATEWAY_MODEL` 这几个值，代码一行不动。Makers 的模型网关走 OpenAI 兼容协议，DeepSeek、GPT-4o、Claude、通义千问都能接。

> 警告：生图模型的返回格式差异大（有的返 URL，有的返 base64）。用 AI SDK 模板能少踩这类坑，因为它把不同厂商的差异都封装了。

下一章，我们把模型再往前推一步——不调云端大模型，直接用**边缘节点**上的 DeepSeek，体验毫秒级响应。

## §18 用边缘 AI 模型快速搭建对话型 AI 站点

5天前我点开 `deepseek-r1-edge.edgeone.app` 试了下，问一句话，答案几乎是秒回。它背后不是"前端调云端大模型"，而是**边缘节点直达大模型**——模型算力下沉到离用户最近的边缘，延迟自然低。这一章讲怎么用 Makers 的「AI 聊天模板」一分钟搭出这种站点。

> 经验：我测过好几次，普通 AI 应用是"浏览器 → 你的服务器 → 云端大模型"，多跳一次就多一份延迟。边缘 AI 是"浏览器 → 边缘节点上的模型"，链路短了一大截。对对话这种要流式、要快的交互，体感差别很明显。

### 18.1 为什么用边缘模型

Makers 免费开放边缘部署 DeepSeek 系列模型，配合「AI 聊天模板」，1 分钟上线，零成本体验毫秒级响应。

| 对比   | 云端大模型      | 边缘 AI 模型            |
| ---- | ---------- | ------------------- |
| 调用方式 | 需要 API Key | 边缘函数内**免 Key** 免费调用 |
| 延迟   | 多跳，偏高      | 边缘节点直达，低            |
| 架构   | 传统服务端      | 完全 Serverless       |
| 协议   | 各厂商不一      | 兼容 OpenAI API 标准    |

> 标叔的结论：边缘模型适合"快、轻、免运维"的对话场景。要复杂推理或私有数据，还是走网关接云端大模型（见 §17）。两条路不冲突，按场景选。

### 18.2 四步上线

1. 进模板页 `templates/deepseek-r1-edge`，点"部署" → Makers 控制台配置项目 → "立即创建"
2. 创建后自动进入部署流程，可在详情页看构建日志
3. 部署成功，点项目概览的预览按钮生成预览链接
4. 打开链接，对话框发任意问题，看流式输出

### 18.3 边缘函数里怎么调

模板核心是边缘函数。示例路径 `/functions/v1/chat/completions/index.js`：

```javascript
export async function onRequestPost({ request }) {
  const { content } = await request.json();
  try {
    const response = await AI.chatCompletions({
      model: '@tx/deepseek-ai/deepseek-v3-0324',
      messages: [{ role: 'user', content }],
      stream: true, // 启用流式输出
    });
    // 返回流式响应
  } catch (error) {
    // 错误处理
  }
}
```

> 建议：我一般把域名绑成自定义域名（如 `www.example.com`）。这个函数跑在边缘节点上，直接 `AI.chatCompletions` 调模型，**不需要你自己的 API Key**，它就成了可持久调用的 API 地址——预览链接有时效限制，正式用一定要绑域名。

### 18.4 多提供商容错

接口的调用符合 OpenAI API 标准，意味着你能轻松在不同厂商间切换、复用代码。下面这个类实现多重保障的自动容错：

```typescript
export class AIService {
  constructor(
    deepseekApiKey: string,
    siliconFlowApiKey: string,
    groqApiKey: string,
    tencentApiKey: string
  ) {
    this.serviceConfigs = [
      { name: 'edgeonemakers', baseURL: 'https://www.example.com/v1', enabled: true, priority: 1 },
      { name: 'tencent', baseURL: 'https://api.lkeap.cloud.tencent.com/v1', model: 'deepseek-v3', enabled: true, priority: 2 },
      { name: 'deepseek', baseURL: 'https://api.deepseek.com/v1', model: 'deepseek-chat', enabled: true, priority: 3 },
    ];
  }
}
```

| 优先级 | 提供商         | 说明       |
| --- | ----------- | -------- |
| 1   | 你的边缘域名      | 最快，免 Key |
| 2   | 腾讯云大模型      | 兜底备用     |
| 3   | DeepSeek 官方 | 再兜底      |

> 标叔的结论：我习惯把边缘模型当主链路、云端模型当兜底，你的对话服务就有了弹性。这也是 Makers 的思路——能力下沉到边缘，控制留在你手里。

下一章，我们深潜模型与智能体的进阶能力——从接自己的厂商 Key，到让 Agent 真正“动手”、把链路看穿。

---

## Part 6: 模型与智能体深潜

读完前面，你能跑通、能部署、能上线。这一 Part，我们往深处走。模型怎么接自己的 Key、记忆怎么精细管、Agent 怎么真正"动手"、链路怎么看穿、Skills 怎么拼装——这些都是把 demo 做成产品必须跨的坎。

## §19 模型厂商密钥：用你自己的 Key 接任意大模型

### 19.1 我踩过的"额度焦虑"

上个月我做一个要 24 小时在线的客服 Agent。内置模型免 Key，但文档写得很直白：内置模型只供技术验证，**生产环境别用**。我顿时慌了——难道要自己接厂商？

后来我才搞明白：Makers 的模型网关，分"内置"和"厂商"两路。内置免 Key 验证用，厂商模型你自备 Key，平台帮你托管转发。两条路都在同一个网关上，切换只改一个 model 字段。

### 19.2 两条路怎么选

| 维度      | 内置模型            | 厂商模型   |
| ------- | --------------- | ------ |
| 要不要 Key | 免 Key           | 自备并绑定  |
| 模型质量    | 够验证             | 厂商最新最强 |
| 适用阶段    | 原型 / Demo       | 生产     |
| 计费      | 50 万 token/月 免费 | 厂商按量计费 |
| 标叔的结论   | 早期快验证           | 上线必须切  |

> **重点看**："上线必须切"那一格。
>
> 内置模型文档明确说不保证生产质量。真要服务用户，绑一个厂商 Key 是刚需。

### 19.3 实战：绑定 DeepSeek Key

以 DeepSeek 为例。平台不替你买 Key，你得去 DeepSeek 官网开一个。

**第一步**：去 DeepSeek 开放平台拿到 API Key。

预期结果：拿到一串 `sk-...`。

**第二步**：进 Makers 控制台「模型与密钥」页，绑定这个 Key。

预期结果：DeepSeek 出现在可选厂商里。

**第三步**：代码里用厂商写法调模型。

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.AI_GATEWAY_API_KEY,        // 平台自动注入，不是你的厂商 Key
  baseURL: "https://ai-gateway.edgeone.link/v1",
});

// 厂商模型用 "厂商/模型名" 写法
const completion = await client.chat.completions.create({
  model: "deepseek/deepseek-v4-pro",
  messages: [{ role: "user", content: "你好" }],
});
```

预期结果：请求经 Makers 网关转发到 DeepSeek，你的厂商 Key 由平台加密托管，代码里不出现。

> **核心建议**：代码里永远只放 `AI_GATEWAY_API_KEY`。
>
> 你的厂商 Key 在控制台绑定，平台托管转发。这样换厂商、换 Key 都不用动代码。

### 19.4 支持哪些厂商

文档列了 8 家：OpenAI、Anthropic、Google、DeepSeek、MiniMax、混元、智谱、月之暗面。模型名统一用 `厂商/模型` 写法，比如 `deepseek/deepseek-v4-flash`、`openai/gpt-4o`、`anthropic/claude-sonnet-4`。

具体可用模型以各家文档为准。切模型还是只改 `model` 字段。

模型接好了，Key 也管住了。下一章，我们让 Agent 的"记忆"更精细，并把它锁起来。

---

## §20 会话存储与鉴权：让 Agent 记得住、管得严

### 20.1 我把对话存哪儿了

2月前我上线第一个 Agent，用户第二轮就"失忆"。§05 讲过平台零配置记忆，但那只是开胃菜。真要做产品，你得会精细管对话——按用户列、分页拉、改某条、甚至压成摘要。

Makers 的 `context.store` 就是干这个的。它零配置，Node 和 Python 两套 API 完全镜像。

### 20.2 存储怎么用

`agents/` 目录里用 `context.store`，`cloud-functions/` 里用 `context.agent.store`，指向同一份数据。

最常用的是追加和读取：

```typescript
// 追加一条用户消息
await context.store.appendMessage({
  conversationId: context.conversation_id,
  role: "user",
  content: context.request.body.message,
  userId: context.request.body.userId,   // 关联用户，便于按用户列对话
});

// 拉历史，直接拼成 OpenAI 格式喂给模型
const messages = await context.store.getMessages({
  conversationId: context.conversation_id,
  limit: 50,
});
const reply = await openai.chat.completions.create({
  model: "deepseek/deepseek-v4-flash",
  messages: context.store.toOpenAIInput(messages),
});
```

预期结果：多轮上下文自动承接，还能按 `userId` 归拢。

| 方法                   | 干什么               |
| -------------------- | ----------------- |
| `appendMessage`      | 追加一条消息，对话不存在自动建   |
| `getMessages`        | 拉消息，支持游标分页        |
| `listConversations`  | 按用户列对话，倒序         |
| `updateConversation` | 更新对话元信息（标题、标签）    |
| `deleteConversation` | 删整个对话，不可恢复        |
| 标叔的结论                | 通用 API 够接管 90% 场景 |

> **重点看**：`toOpenAIInput` 那行。
>
> Store 帮你把内部消息转成任意框架格式，Claude / OpenAI / LangGraph 都能直接吃。

### 20.3 长对话要压缩

`getMessages` 单次最多 100 条。对话长了怎么办？保留最近 N 条原文，早期压成一段摘要。

平台不替你调 LLM 生成摘要，只提供一个 `metadata` JSON 容器。约定两个 key：`summary`（摘要文本）、`summarizedUntil`（已摘要到哪条）。你用便宜模型生成摘要，写回即可。

```typescript
async function summarize(previousSummary, newMessages) {
  const prompt = previousSummary
    ? `合并已有摘要和新增对话成一段新摘要，控制在 500 字内：\n${previousSummary}\n${newMessages}`
    : `总结这段对话成摘要，控制在 500 字内：\n${newMessages}`;
  const { text } = await generateText({
    model: openai("gpt-4o-mini"),   // 便宜模型压摘要，省钱
    prompt,
  });
  return text.trim();
}
```

预期结果：上万条消息的对话，模型每次只看最近 N 条 + 一段摘要，又快又省。

### 20.4 没鉴权，任何人都能调你 Agent

上个月我一个没加登录的 Agent，半夜被刷了几万次调用。查账单我心都凉了。

Agent 接口若没登录，任何人都能直接请求 `/agents/*`，白嫖你的 LLM 和工具额度。Makers 的解法是**中间件 + Cloud Functions 签发 JWT**：

- `cloud-functions/auth/*` 负责登录注册、签发 JWT；
- `middleware.js` 在边缘节点拦未登录请求，失败直接 401；
- Agent 入口再 `requireAuth(context)` 验一次。

```js
// middleware.js：命中受保护路径先验 JWT
export const config = {
  matcher: ["/chat/:path*", "/agents/:path*"],
};
export async function middleware(context) {
  const token = readCookie(context.request.headers, "jwt_token");
  if (!token) return unauthorized("no auth cookie");
  await verifyJwt(token, context.env.JWT_SECRET);  // 失败直接 401
  return context.next();
}
```

预期结果：未登录请求在边缘就被挡掉，省下 Agent Runtime、Sandbox、LLM 的成本。

| 层               | 作用            | 标叔的结论   |
| --------------- | ------------- | ------- |
| 中间件             | 边缘早拒          | 省钱第一道   |
| Agent 侧         | 再验一次          | 安全兜底    |
| HttpOnly Cookie | token 不落前端 JS | 防 XSS 偷 |

> **核心建议**：公开 Agent 前，先加这一层。
>
> 我那次被刷，就是漏了中间件。早拒比事后查账单便宜一万倍。

记忆精细了，入口锁住了。下一章，让 Agent 真正"动手"——给它沙箱和工具。

---

## §21 沙箱与工具框架：给 Agent 装上手脚

### 21.1 只会说话的 Agent 不值钱

6月前我做一个能"改代码并预览"的 Agent。光输出文本没用，它得真能跑命令、读文件、开浏览器。我一度想自己搭执行环境，看到 Makers 内置沙箱才松口气——这活它接了。

沙箱底层是腾讯云隔离实例，专门承载 Agent 的"副作用"。LLM 不再只能聊天，能真动手。

### 21.2 两层 API，同一个实例

平台把沙箱包成两层，都挂在 `context` 上：

| 视角     | 字段                  | 给谁         | 粒度                                 |
| ------ | ------------------- | ---------- | ---------------------------------- |
| LLM 视角 | `context.tools.*`   | 传给 LLM 当工具 | 原子化，便于放开范围                         |
| 开发者视角  | `context.sandbox.*` | 你直接调       | 按模块：commands/files/browser/runCode |
| 标叔的结论  | 两层共用一实例             | 不用自己维护     | 一致才省心                              |

`context.tools` 里的内置工具，底层就是调 `context.sandbox.*`，没有两套逻辑。

### 21.3 内置工具清单（节选）

工具按能力原子化，LLM 按名字语义匹配：

| 工具                           | 干什么                |
| ---------------------------- | ------------------ |
| `commands`                   | 执行一次性 shell 命令     |
| `files_read` / `files_write` | 读 / 写文件            |
| `browser_fetch`              | 真实 Chromium 取渲染后页面 |
| `browser_screenshot`         | 截图，返回 base64       |
| `code_interpreter`           | 跑代码                |
| `web_search`                 | 轻量网页搜索             |

给 LLM 全部工具很简单：

```typescript
import { Agent } from "@openai/agents";
const agent = new Agent({
  name: "Assistant",
  instructions: "Use sandbox tools.",
  tools: context.tools.all(),   // 全部内置工具
  model,
});
```

预期结果：Agent 能自己决定调哪个工具，跑命令、读文件、开浏览器。

> **注意**：别一股脑全放开。
>
> 只给文件 + 浏览器，不开放 shell 和代码解释器，更安全：
>
> ```typescript
> const safeTools = [...context.tools.files(), ...context.tools.browser()];
> ```

### 21.4 不同框架，同一套工具

`context.tools` 的输出格式由 `edgeone.json` 里的 `framework` 决定。Claude / OpenAI / LangGraph / CrewAI / DeepAgents 各自适配。

```json
{ "agents": { "framework": "claude-agent-sdk" } }
```

预期结果：你不用自己写工具转换，平台按框架把沙箱工具包成原生形态。我第一次对接 LangGraph 时，光工具适配就耗了两天，换成 Makers 的 `toLangChainTools`，一行就完事。

| framework         | 输出形态              | 标叔的结论                   |
| ----------------- | ----------------- | ----------------------- |
| claude-agent-sdk  | MCP server bundle | 直接 `createSdkMcpServer` |
| openai-agents-sdk | function-tool     | 无需 helper               |
| langgraph         | LangChain 工具      | `toLangChainTools`      |
| crewai            | CrewAI 工具         | `toCrewAITools`         |

### 21.5 开发者也能直接用沙箱

不只 LLM，你的代码也能直接操作沙箱。比如沙箱里起个 vite，把预览地址返前端：

```typescript
await context.sandbox.commands.run("nohup npx vite --port 5173 &", { timeout: 10 });
const previewUrl = context.sandbox.getHost(5173);   // 暴露到外网
return Response.json({ previewUrl });
```

预期结果：Agent 改完代码，立刻把预览地址给用户，闭环体验。

> **标叔的经验**：沙箱实例按 `conversation_id` 一对话一实例。
>
> 我第一次跑长任务没续命，沙箱到点被回收，进度全丢。后来才学会在快到期前 `extendTimeout`。长任务用它续命，结束用 `kill()` 释放。别让它空跑烧额度。

Agent 会想、会记、会动手了。但它万一乱来怎么办？下一章，把它的每一步看穿。

---

## §22 手动插桩与可观测：把链路看穿

### 22.1 自动的还��够

§07 讲过 Metrics 和 Traces 面板。但有些事自动采集不到：你自写的业务逻辑、内部服务调用、没被支持的框架。这时得自己插桩。

上个月我一个 Agent 偶发卡顿，自动 trace 只看到"慢"，看不到慢在哪。我手动插了一段 span，十秒定位是摘要函数拖了后腿。

### 22.2 用 context.tracer 手动补

平台基于 OpenInference，在你代码加载前就注入了。自动 span 和手动 span 共享同一个 `traceId`，自然嵌套。

最常用的 `span()`：

```typescript
const intent = await context.tracer.span(
  "classify_intent",                       // span 名，别用动态值
  async (span) => {
    const res = await openai.chat.completions.create({ /* ... */ });
    span.setAttributes({ "intent.label": res.choices[0].message.content });
    return res;
  },
  { "agent.step": "intent" }
);
```

预期结果：这段逻辑在 Traces 面板里变成一颗可展开的树，耗时、入参、返回值一目了然。

| API                       | 用途              | 标叔的结论 |
| ------------------------- | --------------- | ----- |
| `span(name, fn, attrs?)`  | 包一段逻辑，自动管生命周期   | 首选    |
| `startSpan(name, attrs?)` | 手动开，须配对 `end()` | 跨异步边界 |
| `setAttributes(attrs)`    | 给当前 span 打标签    | 过滤维度  |

> **注意**：span 名别用 userId、订单号这类高基数动态值。
>
> 把它们放 `attributes` 里。否则面板聚合会炸。

### 22.3 把业务标签打上去

给 span 打业务维度，后面在面板按维度过滤：

```typescript
context.tracer.setAttributes({
  "user.tier": "premium",
  "agent.scenario": "customer_service",
});
```

预期结果：你能在 Traces 里按"付费用户""客服场景"筛出问题链路。

自动能看全貌，手动能看细节。两者配合，Agent 再也没法"暗箱操作"。下一章，我们用 Skills 把上面这些能力快速拼起来。

---

## §23 AI 原生开发：用 Skills 拼装 Agent 能力

### 23.1 我装完 Skill 包那一刻

3天前我装官方 Skill 包，一句"在 Makers 上用 Claude Agent SDK 写个对话 Agent"，它自动拉模板、写代码、本地起调试。我这才意识到：开发 Agent 这件事，本身也能被 Agent 加速。

`edgeone-makers-tools` 是一套社区开放规范，给 AI 编程工具（Claude Code、CodeBuddy、Cursor）注入 Makers 的领域知识。装好它，你用自然语言就能驱动 Agent 完成 Makers 开发。

### 23.2 它含 8 个 Skill

| Skill                    | 覆盖                |
| ------------------------ | ----------------- |
| `makers-agents`          | AI Agent 开发（五大框架） |
| `makers-edge-functions`  | 边缘函数              |
| `makers-cloud-functions` | 云函数               |
| `makers-storage`         | KV 与 Blob 存储      |
| `makers-middleware`      | 中间件（鉴权/重写/路由）     |
| `makers-deploy`          | 部署到 EdgeOne       |
| `makers-cli`             | CLI 命令参考          |
| `makers-recipes`         | 项目脚手架             |
| 标叔的结论                    | 从开发到部署全覆盖         |

### 23.3 装好怎么用

```bash
npx skills add TencentEdgeOne/edgeone-makers-tools
```

装完，直接说人话。比如"把这个 Next.js 项目部署到 EdgeOne Makers，给我预览链接"——它会自己检查环境、登录、构建、部署、回 URL。

| 场景      | 说一句                           |
| ------- | ----------------------------- |
| 部署      | 部署这个 Next.js 项目到 Makers       |
| 写 Agent | 用 Claude Agent SDK 写个对话 Agent |
| 加鉴权     | 写个中间件给 /api 加鉴权               |
| 标叔的结论   | 带"Makers""Agent"关键词更准         |

> **核心建议**：描述带上平台/框架关键词。
>
> 太宽泛的话，Agent 可能匹配不到对的 Skill。这是我和它磨合出的经验。

### 23.4 中国站还是国际站

登录时它会让你选 China 还是 Global。规则很简单：腾讯云**中国站**账号选 China，国际站（edgeone.ai）账号选 Global。两套账号体系独立，别选错。

接下来，我们进入最后一块拼图——高级功能篇。模型网关、沙箱、工具、MCP、Copilot 这几样凑齐，你才算真正把 Makers 玩透。翻到 §24，我先带你看看那个能让你只用一把钥匙调遍所有模型的统一网关。

---

## Part 7: 高级功能篇

## §24 Makers Models 统一模型网关：从任意 SDK 直接调用

### 24.1 我为什么想要一个"只带一把钥匙"的网关

2周前我帮一个做客服系统的朋友排查问题，他前端、后端、定时任务三处各自硬编码了不同厂商的 Key，换一次模型要改三个仓库。我告诉他：Makers 有个独立的模型网关服务，一把 Key 调遍所有厂商，根本不用在代码里塞厂商密钥。

这就是 **Makers Models**——部署在 EdgeOne 边缘节点的统一模型接入服务。它和你写 Agent 时平台自动注入的那套网关，是同一张网，但用法完全不同。

### 24.2 它和 Agent 里的 AI_GATEWAY 不是一回事

我在前面 §04 讲过，Agent 运行时平台会自动注入 `AI_GATEWAY_API_KEY` 和 `AI_GATEWAY_BASE_URL`，你写 Agent 时不用管密钥。而 **Makers Models 是独立对外暴露的网关**，你拿自己的 `MAKERS_MODELS_KEY`，从任何地方都能调：前端后端代理、独立脚本、甚至别的平台。

| 维度    | AI_GATEWAY（Agent 内） | Makers Models（独立网关）       |
| ----- | ------------------- | ------------------------- |
| 密钥来源  | 平台自动注入，拿不到明文        | 控制台创建 `MAKERS_MODELS_KEY` |
| 调用位置  | 仅 Agent 运行时内        | 任意能发 HTTP 的地方             |
| 典型用法  | 写 Agent 业务逻辑        | 前端流式 UI、独立服务、Demo         |
| 标叔的结论 | 写 Agent 用它最省心       | 要"带出门"调用就靠它               |

### 24.3 实战：三种 SDK 直接调用

我试过最顺手的是直接套 OpenAI 的 SDK，因为网关兼容 OpenAI 协议。换成 Anthropic 或 Vercel AI SDK 也行。

```typescript
// 方式一：Vercel AI SDK + 官方 provider
import { createAiGateway } from "@edgeone/makers-models-provider";
import { generateText } from "ai";

const aiGateway = createAiGateway({ apiKey: process.env.MAKERS_MODELS_KEY });
const { text } = await generateText({
  model: aiGateway("@makers/deepseek-v4-flash"),
  prompt: "What can you do?",
});
```

```typescript
// 方式二：OpenAI SDK（baseURL 指到网关）
import OpenAI from "openai";
const client = new OpenAI({
  apiKey: process.env.MAKERS_MODELS_KEY,
  baseURL: "https://ai-gateway.edgeone.link/v1",
});
const completion = await client.chat.completions.create({
  model: "@makers/deepseek-v4-flash",
  messages: [{ role: "user", content: "What can you do?" }],
});
```

```python
# 方式三：Python OpenAI SDK
import os
from openai import OpenAI
client = OpenAI(api_key=os.getenv("MAKERS_MODELS_KEY"), base_url="https://ai-gateway.edgeone.link/v1")
completion = client.chat.completions.create(
    model="@makers/deepseek-v4-flash",
    messages=[{"role": "user", "content": "What can you do?"}],
)
```

### 24.4 SSE 流式输出原生支持

我做对话 UI 时最在意的就是流式。网关对所有协议原生支持 SSE，前端拿 `stream: true` 就能边生成边渲染，密钥还不落前端——前端只碰 `MAKERS_MODELS_KEY` 经你后端代理转发。

```bash
curl -X POST "https://ai-gateway.edgeone.link/v1/chat/completions" \
  --header "Authorization: Bearer $MAKERS_MODELS_KEY" \
  --header "Content-Type: application/json" \
  --data '{"model":"@makers/deepseek-v4-flash","stream":true,"messages":[{"role":"user","content":"What can you do?"}]}'
```

> **注意**：`MAKERS_MODELS_KEY` 和厂商密钥一样，别提交进版本控制。

### 24.5 标叔的结论

我现在的习惯是：写 Agent 用平台注入的 `AI_GATEWAY` 省心；凡是要在 Agent 之外（前端代理、独立服务、Demo）调模型，就用 Makers Models 这把独立钥匙。两把钥匙分工，代码反而更干净。

接下来，翻到 §25，我看 Agent 是怎么在沙箱里"自己动手"封装工具的。

## §25 沙箱原子 API：自己动手封装工具

### 25.1 平台给的工具不够用时

3周前我接了个活：要让 Agent 批量把 200 个 CSV 跑成图表，还要登录某后台截图存证。平台内置工具够日常用，但这活儿要**自己控制进程、读写文件、操作浏览器、跨调用保留变量**——光靠高级封装不够。这时候就得直接用 `context.sandbox.*` 这套原子 API。

`sandbox` 是开发者直接调用的视角，你基于它自己封装工具，想怎么玩怎么玩。

### 25.2 commands：每次都是干净的新进程

我第一次用 `commands.run` 时踩了个坑：我以为连续两次调用能共享环境变量，结果第二次拿不到。后来才看懂文档——**每次调用都是独立新进程**，不保留 cwd、不保留环境变量改动。要跨调用保留状态，得用后面的 `runCode`。

```typescript
const { stdout, exitCode } = await context.sandbox.commands.run(
  'pip install requests && python -c "import requests; print(requests.__version__)"',
  { timeout: 60 },
);
```

`opts` 支持 `cwd` / `env` / `user` / `timeout`（秒），返回 `{ stdout, stderr, exitCode }`。一句话跑完即焚，干净。

### 25.3 files：读写沙箱文件系统

我在做数据预处理时，全靠 `files` 在沙箱里落盘。文本直接读写，二进制资产（比如 `.png`）建议先用 `commands` 在沙箱内下载或解码，再走别的通道读出。

```typescript
await context.sandbox.files.makeDir('/work/output');
await context.sandbox.files.write('/work/output/result.json', JSON.stringify(data));
const entries = await context.sandbox.files.list('/work/output');
```

可用方法：`read` / `write` / `list` / `makeDir`(或 `make_dir`) / `exists` / `remove`，覆盖日常文件系统操作。

### 25.4 browser：CDP 连内置 Chromium

我做过一个需要"登录后截图"的需求，内置的 `browser_screenshot` 工具做不到——它没法保持登录态。原子 API 里的 `browser` 走 CDP 连沙箱内置 Chromium（底层 Playwright），能跑多步有状态流程。

```typescript
await context.sandbox.browser.goto('https://example.com/login');
await context.sandbox.browser.type('input[name=user]', 'alice');
await context.sandbox.browser.type('input[name=pass]', 'secret');
await context.sandbox.browser.click('button[type=submit]');
await context.sandbox.browser.goto('https://example.com/dashboard');
const { base64Image } = await context.sandbox.browser.screenshot({ fullPage: true });
```

`browser` 还暴露 `cdpUrl`（外部 Playwright 直连）和 `liveUrl`（NoVNC 人工实时看页面），方法含 `goto` / `click` / `type` / `evaluate` / `getContent` / `close`。这是比"截个图"高级得多的浏览器控制力。

### 25.5 runCode：变量跨调用保留的 Jupyter kernel

我做数据批处理时最依赖 `runCode`——它在沙箱内置 Jupyter kernel 里执行代码，**变量跨调用保留**。这是它和 `commands` 最大的区别。

```python
exec = await context.sandbox.run_code(
    """
import pandas as pd
df = pd.read_csv('/work/data.csv')
df.plot().get_figure().savefig('/work/out.png')
print('done')
""",
    language='python',
)
```

`opts` 支持 `language`（默认 `python`，也支持 `javascript` / `r` / `bash`）和 `timeout`（秒），返回 `Execution { results, logs, error }`。

### 25.6 标叔的结论

我的经验：`commands` 干一次性的脏活，`files` 管落盘，`browser` 做有状态的网页操作，`runCode` 跑要保状态的数据任务。四件套一上手，你基本能给 Agent 封出任何工具，不再受平台内置清单的限制。

接下来，翻到 §26，我看怎么给 Agent 接上"联网搜索"这种即插即用的工具。

## §26 联网搜索与自定义工具

### 26.1 内置 web_search 开箱即用

2天前我给一个资讯 Agent 加搜索能力，本来以为要自己接搜索 API、处理鉴权，结果发现平台已经给了 `web_search` 这个**公网搜索工具示例**，底层调腾讯云联网搜索（WSA），开箱即用。

启用前提就一条：配置环境变量 `WSA_API_KEY`（dev 写 `.env`，线上写控制台环境变量，缺失会提示 `web_search requires the WSA_API_KEY...`）。主账号还要在腾讯云控制台开通联网搜索（WSA）服务。

### 26.2 参数与返回值

我调的时候最常改的是 `maxResults` 和 `site`，一个控数量、一个控范围。

| 参数           | 类型          | 必填 | 默认  | 说明              |
| ------------ | ----------- | -- | --- | --------------- |
| `query`      | string      | 是  | —   | 搜索关键词，不可为空      |
| `maxResults` | integer ≥ 1 | 否  | `5` | 去重后最大条数         |
| `site`       | string      | 否  | —   | 站内搜索，限单个域；省略则全网 |

返回值 `SearchResult[]`，每项含 `title` / `href` / `snippet` / `site` / `date`。注意 `href` 是 WSA 直接返回的真实可访问地址，不用再跟重定向。

```typescript
const webSearch = context.tools.get('web_search');
const results = await webSearch.execute({ query: '最近 AI 有什么新的技术' });
```

### 26.3 接第三方（Exa / Tavily）并屏蔽内置

我有次觉得 WSA 结果不够准，想换 Exa。做法是把第三方调用包成和 framework 工具形态一致的对象，挂载时把内置 `web_search` 过滤掉，避免 LLM 同时看到两个用途相同的工具。

```typescript
import Exa from 'exa-js';
import { tool } from '@openai/agents';
import { z } from 'zod';

const exa = new Exa(process.env.EXA_API_KEY!);
const exaSearch = tool({
  name: 'web_search',
  description: 'Search the public web. Returns title / url / snippet for top results.',
  parameters: z.object({
    query: z.string().describe('Search keywords'),
    maxResults: z.number().int().min(1).default(5),
  }),
  execute: async ({ query, maxResults }) => {
    const { results } = await exa.search(query, { numResults: maxResults, contents: { highlights: true } });
    return results.map((r) => ({
      title: r.title ?? '',
      href: r.url,
      snippet: r.highlights?.[0] ?? r.text?.slice(0, 200) ?? '',
      site: new URL(r.url).hostname,
      date: r.publishedDate ?? '',
    }));
  },
});

const tools = [...context.tools.all().filter((t) => t.name !== 'web_search'), exaSearch];
```

> **注意**：不想用 WSA，也能接任何第三方搜索服务，关键是工具形态和 framework 对齐、再屏蔽内置同名工具。

### 26.4 标叔的结论

我的判断：先用内置 `web_search` 跑通，验证完业务再决定是否换第三方。换的时候记得"屏蔽内置 + 形态对齐"两步走，否则 LLM 会犹豫用哪个。

接下来，翻到 §27，我看怎么用 MCP 把 Makers 的能力接到你常用的 AI 编程客户端里。

## §27 用 MCP 把能力接到外部世界

### 27.1 什么是 MCP，为什么 Agent 需要它

去年底我第一次接触 MCP（Model Context Protocol，模型上下文协议）时就觉得它顺：这是一种开放协议，让 AI 模型能安全地跟本地和远程资源交互，只需在支持 MCP 的客户端（Cline、Cursor、Claude 等）里统一配置一次。Makers 顺势给了 **Makers Deploy MCP**，把"部署到 Makers 并生成公开链接"这件事，直接变成 AI 客户端里的一个能力。

### 27.2 Makers Deploy MCP：一句话部署全栈应用

我现在的日常：在 Cursor 里跟 AI 说"把这个项目部署到 Makers"，它直接调 MCP 完成编码并持续迭代。配置只要一段：

```json
{
  "mcpServers": {
    "edgeone-pages-mcp-server": {
      "command": "npx",
      "args": ["edgeone-pages-mcp-fullstack"]
    }
  }
}
```

如果部署到腾讯云中国站，把 `args` 改成 `["edgeone-pages-mcp-fullstack", "--region", "china"]`。支持的客户端有 Cursor、VSCode、Windsurf、ChatWise、Cherry Studio 等。

### 27.3 分享 HTML：免登录秒级部署

我常用来快速分享 AI 生成的网页：不用登录，把 HTML 内容推给 MCP Server 就自动生成公开链接。配置走 URL 而非命令：

```json
{
  "mcpServers": {
    "edgeone-pages-mcp-server": {
      "url": "https://mcp-on-edge.edgeone.app/mcp-server"
    }
  }
}
```

它利用无服务器边缘计算加 KV 存储，接收 HTML 后秒级生成公共访问链接，还内置了错误处理。适合临时预览、分享 Demo。

### 27.4 自部署 MCP Server

我有次想用自己的域名跑这套能力，就用了官方模板 **Self Hosted Makers MCP**。前置两件事：配置 KV 存储（变量名必须为 `my_kv`，绑定后重新部署）、绑定自定义域名。完成后在客户端这么配：

```json
{
  "mcpServers": {
    "edgeone-pages": {
      "url": "https://你的自定义域名/mcp-server"
    }
  }
}
```

也能走 API 直接部署 HTML：

```bash
curl -X POST https://你的自定义域名/kv/set \
  -H "Content-Type: application/json" \
  -d '{"value": "<html><body><h1>Hello, World!</h1></body></html>"}'
```

### 27.5 标叔的结论

我的看法：MCP 把"部署"从控制台点击变成了 AI 工作流里的一个原子动作。你写 Agent 也好、写网页也好，都能让 AI 客户端一句话帮你发上线——这正是 Makers 想做的"AI 原生开发"。

接下来，翻到 §28，我看平台自带的 AI 编程助手 Copilot 怎么帮你改项目。

## §28 Copilot：用自然语言改项目、自动预览与故障分析

### 28.1 我第一次让 AI 改自己项目

上周我一个线上页面样式错位，懒得切环境，就在 Makers 控制台跟 Copilot 说"把首页卡片间距调大、标题改红"，它自己读懂代码、改完、还给我生成了个独立预览。我确认没问题才发布。那一刻我意识到：改项目这事儿，也能交给对话。

EdgeOne Makers Copilot 是集成在 Makers 里的 AI 编程助手，你说人话，它结合项目上下文理解代码、生成修改、协助预览与发布。

### 28.2 核心能力

我用下来最值钱的有四条：

- **自然语言驱动**：不用深开发背景，对话提示词就能开工。
- **理解项目上下文**：它结合代码和构建配置改，结果更贴项目现状。
- **独立预览环境**：每次修改都生成独立预览，确认无误再发生产，保生产安全。
- **移动端便捷**：手机上也能发修改指令，随时更新内容。

### 28.3 典型场景

我给团队安利时总举这几个例子：

- **快速修复**：样式错位、文案错误、链接失效，范围明确的活儿它最拿手。
- **内容更新**：运营、设计直接对话改文案、换图、调主题色，不用开发介入。
- **快速建页**：给老项目一句话生成落地页、活动专题页。
- **智能故障排除**：构建或部署失败时，基于失败记录让它分析定位。

### 28.4 限额与边界

我用的时候踩过边界，得说清楚：

| 模型能力          | 任务次数 / 天 |
| ------------- | -------- |
| 使用 GLM 5.1 模型 | 20-30    |

目前 Copilot 处于免费公开测试，每日额度受编程模式、任务复杂度、代码库规模、上下文长度影响，用完次日刷新。还有个硬限制：**当前仅支持 GitHub 项目**。构建失败时可在失败部署详情页点 `Why did it fail`，让它结合错误日志辅助分析。

### 28.5 标叔的结论

我的建议：Copilot 适合"改已有项目"和"救火"，不适合从零造复杂系统。把它当成你随叫随到的初级工程师，给它明确、范围清晰的任务，效率最高。

接下来，翻到附录的环境变量速查表，部署前扫一眼，能省你半小时查文档。到此，从起步、核心、实战、进阶，到模型与智能体的深潜，再到高级功能，这本书走完了。你手里现在有一套完整打法：模型网关解耦、记忆零配置、工具即沙箱、链路可观测、Skills 拼装，外加统一模型网关、原子沙箱、联网搜索、MCP 与 Copilot。去把你的 Agent 想法，做成别人能打开就用的服务吧。

---

## 附录

### A 环境变量速查表

| 变量名                 | 作用                   | 示例值                                  |
| ------------------- | -------------------- | ------------------------------------ |
| AI_GATEWAY_BASE_URL | 模型网关地址               | <https://ai-gateway.edgeone.link/v1> |
| AI_GATEWAY_API_KEY  | 平台生成的密钥              | sk-xxx                               |
| AI_GATEWAY_MODEL    | 当前模型（改它换模型）          | @makers/hy3-preview                  |
| 联网搜索 Key            | 调用腾讯云 Web Search API | sk-xxx                               |

> **注意**：API Key 界面不二次显示，丢了要重建。
>
> 复制后妥善保管。别写进代码仓库。

### B 常见错误与解决方案

| 现象      | 原因          | 解决                      |
| ------- | ----------- | ----------------------- |
| 多轮对话记不住 | 没走平台会话接口    | 用平台提供的记忆，别自接存储          |
| 切模型没生效  | 只改了代码没改环境变量 | 改 AI_GATEWAY_MODEL 后重部署 |
| 中国大陆打不开 | 没实名/没备案     | 实名+ICP 备案，或选不含中国大陆区     |
| Key 丢了  | 界面不二次显示     | 控制台重建 API Key           |
| 临时链接失效  | 超过 3 小时     | 加自定义域名长期可用              |

### 阅读指南

| 时间      | 章节      | 目标                               |
| ------- | ------- | -------------------------------- |
| Day 1   | §01-§03 | 从零到第一次跑通                         |
| Day 2-3 | §04-§07 | 掌握四大核心能力                         |
| Day 4-5 | §08-§14 | 进阶实战与边缘能力                        |
| Day 6   | §15-§18 | 最佳实践篇                            |
| Day 7   | §19-§23 | 模型与智能体深潜                         |
| Day 8   | §24-§28 | 高级功能篇：统一网关、原子沙箱、联网搜索、MCP、Copilot |
| 随时      | 附录      | 查表排错                             |

> **行动清单**：
>
> - [ ] 用控制台模板跑通第一个 Agent
> - [ ] 装好 edgeone-makers-tools 全局 Skill
> - [ ] 改一次 AI_GATEWAY_MODEL，体验零代码换模型
> - [ ] 部署一个属于你自己的业务逻辑


### 阅读参考

https://ai.codefather.cn/post/2071512495712894978#heading-5