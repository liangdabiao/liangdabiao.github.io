# 标叔的 AI 教学站

> 多个 AI 技术框架的「从入门到精通」教程合集 — 讲人话、能跑通、能上线。

## 这是什么

这是一个托管在 GitHub Pages 上的 AI 教学站。每个子目录对应一门课程，根目录的 [`index.html`](./index.html) 是整体入口与课程导航。

所有教程由 **标叔**（AI Native Coder · 独立开发者）整理，资料截至 **2026 年 7 月**。

## 课程目录

| 类别 | 课程 | 入口 |
| --- | --- | --- |
| 入门先行 | 真·AI Agent 小蓝书 | [`agent-action/index.html`](./agent-action/index.html) |
| 入门先行 | 阿里云百炼 从入门到精通 | [`bailian/index.html`](./bailian/index.html) |
| 入门先行 | LangGraph 从入门到精通 | [`langgraph/index.html`](./langgraph/index.html) |
| 入门先行 | Agent Skills 从入门到精通 | [`skills-site/index.html`](./skills-site/index.html) |
| Agent 框架 | Claude Agent SDK 从入门到精通 | [`Claude-Agent-SDK/index.html`](./Claude-Agent-SDK/index.html) |
| Agent 框架 | DeepAgents 从入门到精通 | [`deepagents/index.html`](./deepagents/index.html) |
| Agent 框架 | DeerFlow 2.0 从入门到精通 | [`deerflow/index.html`](./deerflow/index.html) |
| Agent 框架 | Flue 框架从入门到精通 | [`flue/index.html`](./flue/index.html) |
| Agent 框架 | OpenAI Agents SDK 从入门到精通 | [`openai-agent/index.html`](./openai-agent/index.html) |
| Agent 框架 | Vercel Eve 从入门到精通 | [`Vercel-Eve/index.html`](./Vercel-Eve/index.html) |
| Agent 部署 | Cloudflare Agents 从入门到精通 | [`Cloudflare-Agents/index.html`](./Cloudflare-Agents/index.html) |
| Agent 部署 | EdgeOne Makers 从入门到精通 | [`edgeone/index.html`](./edgeone/index.html) |

## 怎么读

1. **入门先行** 从四本里挑：想懂概念看《真·AI Agent 小蓝书》；想零代码出活看阿里云百炼；想从代码开始看 LangGraph；想把经验沉淀成可复用技能看 Agent Skills。
2. **进阶** 挑一个 Agent 框架深入（Claude Agent SDK / OpenAI Agents SDK / Flue / Vercel Eve / DeepAgents / DeerFlow）。
3. **想托管上线** 看 Cloudflare Agents / EdgeOne Makers — 把 Agent 部署到边缘 / 云平台，不用管运维。

## 写作约定

- **先说结论，再给证据，最后上代码。** 短句为主，能断言就不含糊。
- 每章末尾有「向前桥接」点出下一章看点。
- 每本书都附 **6 天 / 7 天阅读计划** 与 **附录速查表**。

## 部署

本站为纯静态站：每个课程是独立的 HTML 集合，无构建工具。可直接托管在 GitHub Pages、Netlify、Vercel、Cloudflare Pages 任何静态服务上。

```bash
# 本地预览
npx serve .
# 或
python -m http.server 8000
```

## 反馈

- GitHub: [@liangdabiao](https://github.com/liangdabiao)
- 公众号：标叔
- 官方站：Liangdabiao.com

## 许可

教程内容仅供学习使用。涉及到的第三方平台、框架与商标归各自所有者所有。

## 感谢

https://linux.do
