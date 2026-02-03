# NEWS - 智能财经新闻聚合与 Market Color 推送

一个完整的财经新闻抓取、AI 分析、自动推送工具集。

## 📋 系统要求

- **Python 版本**: Python 3.9 或更高版本
- **操作系统**: macOS, Linux, Windows

---

## 📁 项目结构

```
NEWS/
├── .venv/                      # Python 虚拟环境 (已配置所有依赖)
├── .env                        # 环境变量 (GEMINI_API_KEY, BARK_KEY)
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

### 1. 安装依赖

```bash
# 克隆仓库
git clone https://github.com/jasper-wutong/FetchNews.git
cd FetchNews

# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# (可选) 安装 GitHub Copilot SDK (仅 daily_brief_copilot.py 需要)
# cd ~/Desktop/VSCodePyScripts/TESTAI/copilot-sdk/python && pip install -e .
```

### 2. 配置环境变量

创建 `.env` 文件（可参考 `.env.example`）：

```bash
GEMINI_API_KEY=你的_Gemini_API_Key
BARK_KEY=你的_Bark_Key
```

### 3. 运行 Market Color 早报推送

```bash
cd ~/Desktop/VSCodePyScripts/NEWS

# 激活虚拟环境
source .venv/bin/activate

# Gemini 版本 (推荐，速度快)
python daily_brief_gemini.py
# 或
./run_gemini.sh

# Copilot SDK 版本
python daily_brief_copilot.py
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
BARK_KEY=你的_Bark_Key
```

### 获取 API Key

- **Gemini API**: 访问 [Google AI Studio](https://aistudio.google.com/app/apikey) 获取免费 API Key
- **Bark**: 在 iOS App Store 下载 Bark 应用获取推送 Key

---

## 📡 新闻源 API

| 模块 | 数据源 | 说明 |
|------|--------|------|
| `fetch_10jqka.py` | 同花顺 | 7x24 快讯、要闻精选 |
| `fetch_36kr.py` | 36氪 | 科技创投资讯 |
| `fetch_WSJ.py` | 华尔街见闻 | 实时快讯、深度文章 |
| `fetch_wallstreetcn.py` | 华尔街见闻 | 实时快讯 |
| `fetch_baidu.py` | 百度热搜 | 热点新闻 |
| `fetch_bilibili.py` | 哔哩哔哩 | 热门视频 |
| `fetch_bloomberg.py` | Bloomberg | 国际财经 |
| `fetch_caixin.py` | 财新网 | 财经新闻 |
| `fetch_eastmoney.py` | 东方财富 | A股资讯 |
| `fetch_github.py` | GitHub Trending | 开源项目动态 |
| `fetch_ithome.py` | IT之家 | 科技新闻 |
| `fetch_jin10.py` | 金十数据 | 财经快讯 |
| `fetch_juejin.py` | 掘金 | 技术文章 |
| `fetch_polymarket.py` | Polymarket | 预测市场数据 |
| `fetch_reuters.py` | 路透社 | 国际新闻 |
| `fetch_thepaper.py` | 澎湃新闻 | 时政新闻 |
| `fetch_toutiao.py` | 今日头条 | 综合资讯 |
| `fetch_v2ex.py` | V2EX | 技术社区热帖 |
| `fetch_weibo.py` | 微博热搜 | 社交媒体热点 |
| `fetch_zhihu.py` | 知乎热榜 | 问答社区热门 |

---

## 🔧 依赖说明

本项目的依赖已在 `requirements.txt` 中定义，主要包括：

- **requests**: HTTP 请求库
- **beautifulsoup4**: HTML 解析
- **pandas**: 数据处理
- **python-dotenv**: 环境变量管理
- **google-genai**: Google Gemini AI SDK
- **pydantic**: 数据验证
- **httpx**: 异步 HTTP 客户端

完整依赖列表请查看 `requirements.txt`。

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
