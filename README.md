# NEWS - 智能财经新闻聚合与 Market Color 推送

一个完整的财经新闻抓取、AI 分析、自动推送工具集。

---

## 📁 项目结构

```
NEWS/
├── .venv/                      # Python 虚拟环境 (已配置所有依赖)
├── .env                        # 环境变量 (GEMINI_API_KEY)
│
├── 📊 Market Color 早报推送
│   ├── daily_brief_gemini.py   # Gemini AI 版本
│   ├── daily_brief_copilot.py  # GitHub Copilot SDK 版本
│   ├── run_gemini.sh           # 快捷运行脚本
│   └── run_copilot.sh          # 快捷运行脚本
│
├── 📡 新闻数据源采集模块
│   ├── fetch_10jqka.py         # 同花顺 7x24 快讯
│   ├── fetch_WSJ.py            # 华尔街见闻 (wallstcn)
│   ├── fetch_caixin.py         # 财新网
│   ├── fetch_eastmoney.py      # 东方财富
│   ├── fetch_bloomberg.py      # Bloomberg
│   ├── fetch_reuters.py        # 路透社
│   └── fetch_polymarket.py     # Polymarket 预测市场
│
├── 📈 数据文件
│   ├── jesus_return_yes.xlsx
│   ├── jesus_return_no.xlsx
│   ├── orderbook_jesus_yes.xlsx
│   └── trump_press_conf_history.xlsx
│
├── newsnow/                    # NewsNow 全栈新闻聚合平台 (可选)
└── test_WSJ.py                 # 华尔街见闻测试脚本
```

---

## 🚀 快速开始

### 运行 Market Color 早报推送

```bash
cd ~/Desktop/VSCodePyScripts/NEWS

# Gemini 版本 (推荐，速度快)
.venv/bin/python daily_brief_gemini.py
# 或
./run_gemini.sh

# Copilot SDK 版本
.venv/bin/python daily_brief_copilot.py
# 或
./run_copilot.sh
```

### 功能流程

```
1. 📡 抓取新闻 (同花顺 + 华尔街见闻)
       ↓
2. 🧠 AI 分析生成 Market Color
       ↓
3. 📱 Bark 推送到手机
```

---

## 📊 Market Color 输出格式

AI 会生成包含以下结构的专业市场评论：

- **【今日大势】** - 市场整体走势概述
- **【核心逻辑】** - 驱动市场的关键因素
- **【交易员备忘】** - 重点关注事项和风险提示

---

## ⚙️ 配置说明

### 环境变量 (.env)

```bash
GEMINI_API_KEY=你的_Gemini_API_Key
```

### Bark 推送配置

在 `daily_brief_*.py` 中修改：

```python
BARK_KEY = "你的_Bark_Key"
```

---

## 📡 新闻源 API

| 模块 | 数据源 | 说明 |
|------|--------|------|
| `fetch_10jqka.py` | 同花顺 | 7x24 快讯、要闻精选 |
| `fetch_WSJ.py` | 华尔街见闻 | 实时快讯、深度文章 |
| `fetch_caixin.py` | 财新网 | 财经新闻 |
| `fetch_eastmoney.py` | 东方财富 | A股资讯 |
| `fetch_bloomberg.py` | Bloomberg | 国际财经 |
| `fetch_reuters.py` | 路透社 | 国际新闻 |
| `fetch_polymarket.py` | Polymarket | 预测市场数据 |

---

## 🔧 依赖安装 (已预装在 .venv)

如需重新安装：

```bash
cd ~/Desktop/VSCodePyScripts/NEWS
python3 -m venv .venv
.venv/bin/pip install requests python-dotenv google-genai pydantic httpx[socks]
.venv/bin/pip install -e ~/Desktop/VSCodePyScripts/TESTAI/copilot-sdk/python
```

---

## ⏰ 定时任务 (可选)

使用 crontab 设置每日自动推送：

```bash
# 编辑 crontab
crontab -e

# 每天早上 7:30 运行 Gemini 版本
30 7 * * * cd ~/Desktop/VSCodePyScripts/NEWS && .venv/bin/python daily_brief_gemini.py
```

⚠️ **注意**：Mac 休眠时定时任务不会运行。建议使用 Mac Mini 并设置永不休眠，或部署到云服务器。

---

## 📝 版本对比

| 特性 | Gemini 版本 | Copilot SDK 版本 |
|------|-------------|------------------|
| 速度 | ⚡ 快 | 中等 |
| API Key | 需要 GEMINI_API_KEY | 使用 Copilot CLI 认证 |
| 离线使用 | ❌ | ❌ |
| 模型 | gemini-2.0-flash | gemini-3-flash (via Copilot) |

---

## 作者

Jasper Wu

## 许可证

MIT
