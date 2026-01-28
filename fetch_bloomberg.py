#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
彭博社新闻获取工具
独立脚本，可以放在任何文件夹运行
只需要安装 requests 库: pip install requests

注意：Bloomberg API 可能需要科学上网才能访问
"""

import requests
from datetime import datetime
import json


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
}


def get_markets_news():
    """获取Bloomberg市场新闻"""
    url = "https://www.bloomberg.com/lineup/api/lazy_load_paginated_module"
    params = {
        "id": "markets_news",
        "page": 1
    }
    
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        news_list = []
        for item in data.get("stories", []):
            # 解析时间
            time_str = ""
            published = item.get("publishedAt", "")
            if published:
                try:
                    dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
                    time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    time_str = published
            
            news = {
                "id": item.get("id"),
                "title": item.get("headline", ""),
                "url": f"https://www.bloomberg.com{item.get('url', '')}",
                "time": time_str,
                "summary": item.get("summary", "")[:150] if item.get("summary") else ""
            }
            news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取市场新闻失败: {e}")
        return []


def get_top_news():
    """获取Bloomberg头条新闻"""
    url = "https://www.bloomberg.com/lineup/api/paginated_stories"
    params = {
        "type": "top_news",
        "page": 1
    }
    
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        news_list = []
        for item in data.get("stories", []):
            # 解析时间
            time_str = ""
            published = item.get("publishedAt", "")
            if published:
                try:
                    dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
                    time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    time_str = published
            
            news = {
                "id": item.get("id"),
                "title": item.get("headline", ""),
                "url": f"https://www.bloomberg.com{item.get('url', '')}",
                "time": time_str,
                "summary": item.get("summary", "")[:150] if item.get("summary") else ""
            }
            news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取头条新闻失败: {e}")
        return []


def get_technology_news():
    """获取Bloomberg科技新闻"""
    url = "https://www.bloomberg.com/lineup/api/lazy_load_paginated_module"
    params = {
        "id": "technology",
        "page": 1
    }
    
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        news_list = []
        for item in data.get("stories", []):
            news = {
                "id": item.get("id"),
                "title": item.get("headline", ""),
                "url": f"https://www.bloomberg.com{item.get('url', '')}",
                "time": item.get("publishedAt", ""),
                "summary": item.get("summary", "")[:150] if item.get("summary") else ""
            }
            news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取科技新闻失败: {e}")
        return []


def get_bloomberg_rss():
    """通过RSS获取Bloomberg新闻（备用方案）"""
    url = "https://feeds.bloomberg.com/markets/news.rss"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        # 简单解析RSS XML
        import re
        items = re.findall(r'<item>(.*?)</item>', response.text, re.DOTALL)
        
        news_list = []
        for item in items[:20]:
            title = re.search(r'<title>(.*?)</title>', item)
            link = re.search(r'<link>(.*?)</link>', item)
            pubDate = re.search(r'<pubDate>(.*?)</pubDate>', item)
            description = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
            
            news = {
                "title": title.group(1) if title else "",
                "url": link.group(1) if link else "",
                "time": pubDate.group(1) if pubDate else "",
                "summary": description.group(1)[:150] if description else ""
            }
            if news["title"]:
                news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取RSS新闻失败: {e}")
        return []


def print_news(news_list, title):
    """格式化打印新闻列表"""
    print("\n" + "=" * 60)
    print(f"📰 {title}")
    print("=" * 60)
    
    if not news_list:
        print("暂无数据 (可能需要科学上网)")
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
    print("\n🌐 Bloomberg（彭博社）新闻获取工具")
    print("⚠️  注意：可能需要科学上网才能正常访问")
    print("正在获取最新数据...\n")
    
    # 尝试获取RSS新闻（更稳定）
    rss_news = get_bloomberg_rss()
    print_news(rss_news[:10], "Bloomberg RSS新闻 (最新10条)")
    
    # 尝试获取市场新闻
    markets = get_markets_news()
    print_news(markets[:10], "市场新闻 (最新10条)")
    
    # 尝试获取头条新闻
    top = get_top_news()
    print_news(top[:10], "头条新闻 (最新10条)")
    
    print("\n" + "=" * 60)
    print("✅ 获取完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
