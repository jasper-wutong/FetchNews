#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路透社新闻获取工具
独立脚本，可以放在任何文件夹运行
只需要安装 requests 库: pip install requests

注意：Reuters API 可能需要科学上网才能访问
"""

import requests
from datetime import datetime
import json


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
}


def get_wire_news():
    """获取Reuters Wire新闻"""
    url = "https://www.reuters.com/pf/api/v3/content/fetch/articles-by-section-alias-or-id-v1"
    query = {
        "arc-site": "reuters",
        "called_from_a_]component": True,
        "fetch_type": "section",
        "offset": 0,
        "section_id": "/wire/",
        "size": 30,
        "website": "reuters"
    }
    params = {
        "query": json.dumps(query),
        "_website": "reuters"
    }
    
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        news_list = []
        for item in data.get("result", {}).get("articles", []):
            # 解析时间
            time_str = ""
            published = item.get("published_time", "")
            if published:
                try:
                    dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
                    time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    time_str = published
            
            news = {
                "id": item.get("id"),
                "title": item.get("title", ""),
                "url": f"https://www.reuters.com{item.get('canonical_url', '')}",
                "time": time_str,
                "summary": item.get("description", "")[:150] if item.get("description") else ""
            }
            news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取Wire新闻失败: {e}")
        return []


def get_business_news():
    """获取Reuters商业新闻"""
    url = "https://www.reuters.com/pf/api/v3/content/fetch/articles-by-section-alias-or-id-v1"
    query = {
        "arc-site": "reuters",
        "called_from_a_component": True,
        "fetch_type": "section",
        "offset": 0,
        "section_id": "/business/",
        "size": 30,
        "website": "reuters"
    }
    params = {
        "query": json.dumps(query),
        "_website": "reuters"
    }
    
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        news_list = []
        for item in data.get("result", {}).get("articles", []):
            # 解析时间
            time_str = ""
            published = item.get("published_time", "")
            if published:
                try:
                    dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
                    time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    time_str = published
            
            news = {
                "id": item.get("id"),
                "title": item.get("title", ""),
                "url": f"https://www.reuters.com{item.get('canonical_url', '')}",
                "time": time_str,
                "summary": item.get("description", "")[:150] if item.get("description") else ""
            }
            news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取商业新闻失败: {e}")
        return []


def get_markets_news():
    """获取Reuters市场新闻"""
    url = "https://www.reuters.com/pf/api/v3/content/fetch/articles-by-section-alias-or-id-v1"
    query = {
        "arc-site": "reuters",
        "called_from_a_component": True,
        "fetch_type": "section",
        "offset": 0,
        "section_id": "/markets/",
        "size": 30,
        "website": "reuters"
    }
    params = {
        "query": json.dumps(query),
        "_website": "reuters"
    }
    
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        news_list = []
        for item in data.get("result", {}).get("articles", []):
            # 解析时间
            time_str = ""
            published = item.get("published_time", "")
            if published:
                try:
                    dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
                    time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    time_str = published
            
            news = {
                "id": item.get("id"),
                "title": item.get("title", ""),
                "url": f"https://www.reuters.com{item.get('canonical_url', '')}",
                "time": time_str,
                "summary": item.get("description", "")[:150] if item.get("description") else ""
            }
            news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取市场新闻失败: {e}")
        return []


def get_reuters_rss():
    """通过RSS获取Reuters新闻（备用方案）"""
    # Reuters RSS feeds
    feeds = [
        ("商业新闻", "https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best"),
        ("世界新闻", "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best"),
    ]
    
    all_news = []
    
    for feed_name, url in feeds:
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            
            # 简单解析RSS XML
            import re
            items = re.findall(r'<item>(.*?)</item>', response.text, re.DOTALL)
            
            for item in items[:10]:
                title = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item) or re.search(r'<title>(.*?)</title>', item)
                link = re.search(r'<link>(.*?)</link>', item)
                pubDate = re.search(r'<pubDate>(.*?)</pubDate>', item)
                description = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', item, re.DOTALL) or \
                              re.search(r'<description>(.*?)</description>', item, re.DOTALL)
                
                news = {
                    "title": title.group(1) if title else "",
                    "url": link.group(1) if link else "",
                    "time": pubDate.group(1) if pubDate else "",
                    "summary": description.group(1)[:150] if description else "",
                    "category": feed_name
                }
                if news["title"]:
                    all_news.append(news)
        except Exception as e:
            print(f"获取{feed_name} RSS失败: {e}")
    
    return all_news


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
            # 清理HTML标签
            import re
            summary = re.sub(r'<[^>]+>', '', news['summary'])
            print(f"   📝 {summary}...")


def main():
    print("\n🌐 Reuters（路透社）新闻获取工具")
    print("⚠️  注意：可能需要科学上网才能正常访问")
    print("正在获取最新数据...\n")
    
    # 1. 尝试获取RSS新闻（更稳定）
    rss_news = get_reuters_rss()
    print_news(rss_news[:10], "Reuters RSS新闻 (最新10条)")
    
    # 2. 获取Wire新闻
    wire = get_wire_news()
    print_news(wire[:10], "实时新闻 (最新10条)")
    
    # 3. 获取商业新闻
    business = get_business_news()
    print_news(business[:10], "商业新闻 (最新10条)")
    
    # 4. 获取市场新闻
    markets = get_markets_news()
    print_news(markets[:10], "市场新闻 (最新10条)")
    
    print("\n" + "=" * 60)
    print("✅ 获取完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
