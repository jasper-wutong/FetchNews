# FetchNews - 新闻获取工具

一个简单易用的新闻抓取工具集合，支持获取华尔街见闻等多个新闻源的最新资讯。

## 项目结构

```
News/
├── test_WSJ.py          # 华尔街见闻新闻获取脚本（独立运行）
└── newsnow/             # NewsNow 全栈新闻聚合平台（可选）
```

## 快速开始

### 方法一：使用 test_WSJ.py（推荐，简单快速）

这是一个独立的Python脚本，无需复杂配置即可运行。

#### 安装依赖

```bash
pip install requests
```

#### 运行脚本

```bash
python test_WSJ.py
```

#### 功能特性

- ✅ **实时快讯** - 获取华尔街见闻最新财经资讯
- ✅ **深度文章** - 获取详细的财经报道
- ✅ **热门文章** - 获取当日热门新闻
- ✅ **无需登录** - 直接调用公开API
- ✅ **独立运行** - 可复制到任何文件夹使用

### 方法二：使用 NewsNow 平台（功能更丰富）

NewsNow 是一个功能完整的全栈新闻聚合平台，支持多个新闻源。

#### 前置要求

- Node.js 16+
- pnpm

#### 安装运行

```bash
cd newsnow

# 安装pnpm（如果未安装）
npm install -g pnpm

# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev
```

访问 http://localhost:5173/ 查看应用

## API 说明

### 华尔街见闻 API

test_WSJ.py 使用的公开API接口：

- **实时快讯**: `https://api-one.wallstcn.com/apiv1/content/lives`
- **新闻文章**: `https://api-one.wallstcn.com/apiv1/content/information-flow`
- **热门文章**: `https://api-one.wallstcn.com/apiv1/content/articles/hot`

这些接口是华尔街见闻官方使用的公开接口，无需身份验证。

## 技术栈

### test_WSJ.py
- Python 3.x
- requests

### NewsNow
- TypeScript
- React
- Vite
- Nitro
- UnoCSS

## 许可证

MIT

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

Jasper Wu
