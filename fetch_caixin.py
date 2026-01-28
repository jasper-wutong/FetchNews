#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财新网新闻获取工具
独立脚本，可以放在任何文件夹运行
只需要安装 requests 库: pip install requests
"""

import requests
from datetime import datetime


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.caixin.com/',
}


def get_latest_articles():
    """获取财新网最新文章"""
    url = "https://api.caixin.com/article/hotspot"
    params = {
        "channel": "finance",
        "limit": 30
    }
    
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        news_list = []
        for item in data.get("data", []):
            news = {
                "id": item.get("id"),
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "time": item.get("time", ""),
                "summary": item.get("summary", "")[:100] if item.get("summary") else ""
            }
            if news["title"]:
                news_list.append(news)
        
        return news_list
    except Exception as e:
        # 备用方案：从首页HTML抓取
        try:
            html_response = requests.get("https://www.caixin.com/", headers=HEADERS, timeout=10)
            html_response.raise_for_status()
            
            import re
            # 从HTML中提取新闻链接和标题
            pattern = r'<a[^>]+href="(https?://[^"]*caixin\.com/[^"]*)"[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, html_response.text)
            
            news_list = []
            seen_titles = set()
            for url, title in matches:
                title = title.strip()
                if title and len(title) > 5 and title not in seen_titles:
                    seen_titles.add(title)
                    news_list.append({
                        "title": title,
                        "url": url,
                        "time": "",
                        "summary": ""
                    })
            
            return news_list[:30]
        except Exception as e2:
            print(f"获取最新文章失败: {e}, 备用方案也失败: {e2}")
            return []


def get_breaking_news():
    """获取财新网金融新闻"""
    url = "https://finance.caixin.com/"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        import re
        # 从HTML中提取新闻链接和标题
        pattern = r'<a[^>]+href="(https?://[^"]*caixin\.com/[^"]*\.html)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, response.text)
        
        news_list = []
        seen_titles = set()
        for url, title in matches:
            title = title.strip()
            if title and len(title) > 5 and title not in seen_titles:
                seen_titles.add(title)
                news_list.append({
                    "title": title,
                    "url": url,
                    "time": "",
                    "source": "财新金融"
                })
        
        return news_list[:30]
    except Exception as e:
        print(f"获取金融新闻失败: {e}")
        return []


def get_hot_articles():
    """获取财新网国际新闻"""
    url = "https://international.caixin.com/"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        import re
        # 从HTML中提取新闻链接和标题
        pattern = r'<a[^>]+href="(https?://[^"]*caixin\.com/[^"]*\.html)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, response.text)
        
        news_list = []
        seen_titles = set()
        for url, title in matches:
            title = title.strip()
            if title and len(title) > 5 and title not in seen_titles:
                seen_titles.add(title)
                news_list.append({
                    "title": title,
                    "url": url,
                    "time": ""
                })
        
        return news_list[:20]
    except Exception as e:
        print(f"获取国际新闻失败: {e}")
        return []


def print_news(news_list, title):
    """格式化打印新闻列表"""
    print("\n" + "=" * 60)
    print(f"📰 {title}")
    print("=" * 60)
    
    if not news_list:
        print("暂无数据")
        return
    
    for i, news in enumerate(news_list, 1):
        print(f"\n{i}. {news['title']}")
        if news.get('time'):
            print(f"   🕐 {news['time']}")
        if news.get('url'):
            print(f"   🔗 {news['url']}")
        if news.get('summary'):
            print(f"   📝 {news['summary']}...")


def main():
    print("\n🌐 财新网新闻获取工具")
    print("正在获取最新数据...\n")
    
    # 1. 获取经济新闻
    latest = get_latest_articles()
    print_news(latest[:10], "经济新闻 (最新10条)")
    
    # 2. 获取金融新闻
    breaking = get_breaking_news()
    print_news(breaking[:10], "金融新闻 (最新10条)")
    
    # 3. 获取国际新闻
    hot = get_hot_articles()
    print_news(hot[:10], "国际新闻 (最新10条)")
    
    print("\n" + "=" * 60)
    print("✅ 获取完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
