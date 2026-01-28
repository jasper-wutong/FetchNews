# Daily Brief 更新说明

## 📈 更新内容（2026-01-28）

已将13个新增的新闻源集成到 `daily_brief_copilot.py` 和 `daily_brief_gemini.py` 中！

---

## 🎯 新增新闻源列表

### Copilot 版本新增：
- ✅ **fetch_baidu** - 百度热搜榜
- ✅ **fetch_zhihu** - 知乎热榜
- ✅ **fetch_jin10** - 金十数据快讯
- ✅ **fetch_wallstreetcn** - 华尔街见闻快讯
- ✅ **fetch_36kr** - 36氪快讯
- ✅ **fetch_toutiao** - 今日头条热榜
- ✅ **fetch_github** - GitHub Trending
- ✅ **fetch_juejin** - 掘金热榜

**Copilot 版总计**：10个新闻源（2个原有 + 8个新增）

### Gemini 版本新增：
- ✅ **fetch_baidu** - 百度热搜榜
- ✅ **fetch_zhihu** - 知乎热榜
- ✅ **fetch_jin10** - 金十数据快讯
- ✅ **fetch_wallstreetcn** - 华尔街见闻快讯
- ✅ **fetch_36kr** - 36氪快讯
- ✅ **fetch_bilibili** - B站热搜
- ✅ **fetch_toutiao** - 今日头条热榜
- ✅ **fetch_thepaper** - 澎湃新闻热榜
- ✅ **fetch_ithome** - IT之家新闻
- ✅ **fetch_github** - GitHub Trending
- ✅ **fetch_juejin** - 掘金热榜
- ✅ **fetch_v2ex** - V2EX 热帖

**Gemini 版总计**：15个新闻源（3个原有 + 12个新增）

---

## 📊 新闻源分类

### 📈 财经快讯类（深度分析）
- 同花顺快讯（10条）
- 财新网（10条）- *仅Gemini*
- 华尔街日报（10条）
- 金十数据（10条，带重要标记⭐）
- 华尔街见闻（10条）
- 36氪快讯（5-8条）

### 🔥 热搜热榜类（舆情热点）
- 百度热搜（5-8条）
- 知乎热榜（5-8条）
- 今日头条（5-6条）
- 澎湃新闻（6条）- *仅Gemini*
- B站热搜（5条）- *仅Gemini*

### 💻 技术科技类（科技趋势）
- IT之家（5条）- *仅Gemini*
- GitHub Trending（3-5条）
- 掘金热榜（3-5条）
- V2EX（5条）- *仅Gemini*

---

## 🚀 使用方法

### Gemini 版本（推荐，新闻源最多）

```bash
cd ~/Desktop/VSCodePyScripts/NEWS

# 确保已配置 GEMINI_API_KEY
# 在 .env 文件中添加：GEMINI_API_KEY=your_key_here

python3 daily_brief_gemini.py
```

### Copilot 版本

```bash
cd ~/Desktop/VSCodePyScripts/NEWS

# 确保已安装 copilot-sdk
python3 daily_brief_copilot.py
```

---

## 📋 数据采集统计

### Gemini 版本采集量（预估）：
- 财经快讯：~60条
- 热搜热榜：~30条
- 技术科技：~18条
- **总计：约108条新闻**

### Copilot 版本采集量（预估）：
- 财经快讯：~40条
- 热搜热榜：~15条
- 技术科技：~8条
- **总计：约63条新闻**

---

## 🛡️ 错误处理

所有新闻源都添加了 try-except 错误处理：
- ✅ 单个新闻源失败不影响整体运行
- ✅ 失败时会显示警告信息 `⚠️  [来源]抓取失败`
- ✅ 继续执行其他新闻源的抓取

---

## 🎨 输出格式

新闻标题格式统一为：
```
[来源] 标题: 摘要/详情
[金十数据⭐] 重要快讯: 详情  # 重要新闻带星标
[GitHub] 项目名 ✰stars数
```

---

## 📱 推送通知

两个版本都会自动推送到 Bark：
- 标题：`智能 Market Color [HH:MM]`
- 分组：`MarketBrief`
- 图标：金融市场图标

---

## ⚙️ 性能优化建议

1. **调整新闻数量**
   - 如果采集时间过长，可以减少每个源的条数
   - 修改代码中的 `[:10]` 为 `[:5]` 等

2. **禁用某些新闻源**
   - 注释掉不需要的 try-except 块
   - 例如：不需要技术类新闻可以注释掉相关部分

3. **添加超时控制**
   - 所有 fetch 函数默认有 10 秒超时
   - 可以在各 fetch_*.py 中调整

---

## 🔍 测试结果

✅ **Gemini 版本测试通过**
- 成功抓取 15 个新闻源
- AI 分析生成完整的 Market Color
- Bark 推送成功

⏳ **Copilot 版本**
- 待测试（需要 copilot-sdk 环境）

---

## 🐛 已知问题

1. **微博热搜需要 Cookie**
   - fetch_weibo.py 中的 Cookie 可能过期
   - 需要定期更新

2. **部分 API 可能限流**
   - 如果请求过快可能被限制
   - 建议不要频繁运行（建议间隔 > 5 分钟）

3. **网络超时**
   - 某些海外网站可能访问较慢
   - 已设置 10 秒超时自动跳过

---

## 📝 后续优化方向

1. **添加缓存机制**
   - 避免短时间内重复抓取相同新闻
   - 可以使用 SQLite 或文件缓存

2. **智能去重**
   - 不同来源可能有相同新闻
   - 可以添加标题相似度检测

3. **新闻分级**
   - 给不同重要性的新闻打分
   - 优先处理高价值信息

4. **定时任务**
   - 使用 cron 或 schedule 库
   - 每天固定时间自动运行

---

## 📊 对比原版改进

### Before（旧版）：
- Copilot: 2个新闻源（同花顺、华尔街日报）
- Gemini: 3个新闻源（同花顺、财新、华尔街日报）
- 总计约 30 条新闻

### After（新版）：
- Copilot: 10个新闻源
- Gemini: 15个新闻源  
- 总计约 **63-108 条新闻**

**信息量提升 2-3 倍！** 🎉

---

## 🎯 使用场景建议

### 适合 Gemini 版本的场景：
- ✅ 需要全面的市场信息
- ✅ 关注社会热点和技术趋势
- ✅ 有 Gemini API 配额

### 适合 Copilot 版本的场景：
- ✅ 主要关注财经市场
- ✅ 需要快速简洁的分析
- ✅ 有 Copilot SDK 访问权限

---

**更新时间**：2026-01-28  
**版本**：v2.0  
**状态**：✅ 已测试通过（Gemini）
