#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能 Market Color 早报推送 (Google Gemini版)
功能：抓取多源新闻 -> Gemini AI 总结 Market Color -> Bark 推送
"""

import warnings
warnings.filterwarnings("ignore")

import os
import sys
import requests
from datetime import datetime

# 导入采集模块
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# 尝试导入
try:
    from google import genai
    from dotenv import load_dotenv
    import fetch_10jqka
    import fetch_caixin
    import fetch_WSJ
    import fetch_baidu
    import fetch_zhihu
    import fetch_weibo
    import fetch_jin10
    import fetch_wallstreetcn
    import fetch_36kr
    import fetch_bilibili
    import fetch_toutiao
    import fetch_thepaper
    import fetch_ithome
    import fetch_github
    import fetch_juejin
    import fetch_v2ex
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请安装依赖: pip install google-genai python-dotenv requests")
    sys.exit(1)

# 加载环境变量 (优先读取当前目录的 .env)
load_dotenv(os.path.join(BASE_DIR, ".env"))

# 配置
BARK_KEY = "n7ga9gQ9xmUaogdtqXdpe9"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_gemini_analysis(raw_news_text):
    """调用 Google Gemini API 生成 Market Color"""
    if not GEMINI_API_KEY:
        return "错误: 请设置 GEMINI_API_KEY 环境变量"
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""你是一个专业的全球宏观策略分析师。请根据以下抓取到的即时新闻，撰写一篇名为 'Market Color' 的深度市场评论。重点是洞察，不是复述新闻表面。

要求：
1. 结构：【今日大势】、【核心逻辑】、【交易员备忘】。
2. 每一部分尽量给出 3-5 条要点，强调因果链条、二阶影响、跨资产/跨行业的传导。
3. 明确区分“已被市场定价”与“潜在超预期”的内容，给出至少 1 个反身性/情绪面的观察。
4. 给出 1-2 个风险情景或反向假设，并提示关键观察指标。
5. 长度控制在 800 字以内，始终用中文回答，风格专业精炼。
6. 避免简单罗列新闻标题或原文摘要。

新闻内容：
{raw_news_text}"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Gemini 分析失败: {e}"

def send_bark(title, content):
    """发送 Bark 通知"""
    url = "https://api.day.app/push"
    payload = {
        "body": content,
        "title": f"{title} [{datetime.now().strftime('%H:%M')}]",
        "group": "MarketBrief",
        "icon": "https://cdn-icons-png.flaticon.com/512/2503/2503903.png",
        "device_key": BARK_KEY,
        "level": "active"
    }
    try:
        requests.post(url, json=payload, timeout=10)
        print("✅ 推送成功")
    except Exception as e:
        print(f"❌ 推送失败: {e}")

def main():
    print("🚀 正在启动智能早报采集 (Gemini)...")
    
    # 1. 抓取多源新闻
    raw_text_parts = []
    
    # ===== 财经快讯类 =====
    try:
        print("📡 抓取同花顺快讯...")
        ths = fetch_10jqka.get_live_news()
        for n in ths[:10]: 
            raw_text_parts.append(f"[同花顺] {n['title']}: {n.get('digest', '')}")
    except Exception as e:
        print(f"⚠️  同花顺抓取失败: {e}")
    
    try:
        print("📡 抓取财新...")
        caixin_latest = fetch_caixin.get_latest_articles()
        for n in caixin_latest[:10]:
            raw_text_parts.append(f"[财新] {n.get('title', '')}: {n.get('summary', '') or n.get('digest', '')}")
    except Exception as e:
        print(f"⚠️  财新抓取失败: {e}")
    
    try:
        print("📡 抓取华尔街日报...")
        wsj_live = fetch_WSJ.get_live_news()
        for n in wsj_live[:10]: 
            raw_text_parts.append(f"[华尔街日报] {n['title']}: {n.get('digest', '')}")
    except Exception as e:
        print(f"⚠️  华尔街日报抓取失败: {e}")
    
    try:
        print("📡 抓取金十数据...")
        jin10 = fetch_jin10.get_latest_articles()
        for n in jin10[:10]:
            important = "⭐" if n.get('important') else ""
            summary = n.get('summary', '')
            raw_text_parts.append(f"[金十数据{important}] {n['title']}: {summary}")
    except Exception as e:
        print(f"⚠️  金十数据抓取失败: {e}")
    
    try:
        print("📡 抓取华尔街见闻...")
        wallst = fetch_wallstreetcn.get_latest_articles()
        for n in wallst[:10]:
            raw_text_parts.append(f"[华尔街见闻] {n['title']}")
    except Exception as e:
        print(f"⚠️  华尔街见闻抓取失败: {e}")
    
    try:
        print("📡 抓取36氪快讯...")
        kr36 = fetch_36kr.get_latest_articles()
        for n in kr36[:8]:
            raw_text_parts.append(f"[36氪] {n['title']}")
    except Exception as e:
        print(f"⚠️  36氪抓取失败: {e}")
    
    # ===== 热搜热榜类 =====
    try:
        print("📡 抓取百度热搜...")
        baidu = fetch_baidu.get_latest_articles()
        for n in baidu[:8]:
            summary = n.get('summary', '')
            if summary:
                raw_text_parts.append(f"[百度热搜] {n['title']}: {summary[:80]}...")
            else:
                raw_text_parts.append(f"[百度热搜] {n['title']}")
    except Exception as e:
        print(f"⚠️  百度热搜抓取失败: {e}")
    
    try:
        print("📡 抓取知乎热榜...")
        zhihu = fetch_zhihu.get_latest_articles()
        for n in zhihu[:8]:
            summary = n.get('summary', '')
            if summary:
                raw_text_parts.append(f"[知乎] {n['title']}: {summary[:60]}...")
            else:
                raw_text_parts.append(f"[知乎] {n['title']}")
    except Exception as e:
        print(f"⚠️  知乎热榜抓取失败: {e}")
    
    try:
        print("📡 抓取今日头条...")
        toutiao = fetch_toutiao.get_latest_articles()
        for n in toutiao[:6]:
            raw_text_parts.append(f"[头条] {n['title']}")
    except Exception as e:
        print(f"⚠️  今日头条抓取失败: {e}")
    
    try:
        print("📡 抓取澎湃新闻...")
        thepaper = fetch_thepaper.get_latest_articles()
        for n in thepaper[:6]:
            raw_text_parts.append(f"[澎湃] {n['title']}")
    except Exception as e:
        print(f"⚠️  澎湃新闻抓取失败: {e}")
    
    try:
        print("📡 抓取B站热搜...")
        bilibili = fetch_bilibili.get_hot_search()
        for n in bilibili[:5]:
            raw_text_parts.append(f"[B站] {n['title']}")
    except Exception as e:
        print(f"⚠️  B站抓取失败: {e}")
    
    # ===== 技术科技类 =====
    try:
        print("📡 抓取IT之家...")
        ithome = fetch_ithome.get_latest_articles()
        for n in ithome[:5]:
            raw_text_parts.append(f"[IT之家] {n['title']}")
    except Exception as e:
        print(f"⚠️  IT之家抓取失败: {e}")
    
    try:
        print("📡 抓取GitHub Trending...")
        github = fetch_github.get_latest_articles()
        for n in github[:5]:
            raw_text_parts.append(f"[GitHub] {n['title']} ✰{n.get('stars', '')}")
    except Exception as e:
        print(f"⚠️  GitHub抓取失败: {e}")
    
    try:
        print("📡 抓取掘金热榜...")
        juejin = fetch_juejin.get_latest_articles()
        for n in juejin[:5]:
            raw_text_parts.append(f"[掘金] {n['title']}")
    except Exception as e:
        print(f"⚠️  掘金抓取失败: {e}")
    
    try:
        print("📡 抓取V2EX...")
        v2ex = fetch_v2ex.get_latest_articles()
        for n in v2ex[:5]:
            raw_text_parts.append(f"[V2EX] {n['title']}")
    except Exception as e:
        print(f"⚠️  V2EX抓取失败: {e}")
    
    # 2. 汇总
    full_raw_text = "\n".join(raw_text_parts)
    
    if not full_raw_text.strip():
        print("❌ 未抓取到任何新闻")
        return
    
    # 3. 分析
    print("🧠 Gemini 正在分析市场脉络...")
    market_color = get_gemini_analysis(full_raw_text)
    
    # 4. 打印并推送
    print("\n" + "="*30)
    print(market_color)
    print("="*30 + "\n")
    
    send_bark("智能 Market Color", market_color)

if __name__ == "__main__":
    main()
