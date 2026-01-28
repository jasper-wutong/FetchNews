#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知乎热榜新闻获取工具
"""

import requests
from datetime import datetime


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}


def get_latest_articles():
    """获取知乎热榜"""
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot-list-web?limit=20&desktop=true"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        news_list = []
        for item in data.get("data", []):
            target = item.get("target", {})
            title_area = target.get("title_area", {})
            excerpt_area = target.get("excerpt_area", {})
            metrics_area = target.get("metrics_area", {})
            link = target.get("link", {})
            
            news = {
                "id": link.get("url", "").split('/')[-1] if link.get("url") else "",
                "title": title_area.get("text", ""),
                "url": link.get("url", ""),
                "summary": excerpt_area.get("text", ""),
                "metrics": metrics_area.get("text", "")  # 热度指标
            }
            if news["title"]:
                news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取知乎热榜失败: {e}")
        return []


def main():
    """主函数"""
    print("=" * 80)
    print("知乎热榜")
    print("=" * 80)
    
    articles = get_latest_articles()
    
    if articles:
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article['title']}")
            print(f"   链接: {article['url']}")
            if article['metrics']:
                print(f"   热度: {article['metrics']}")
            if article['summary']:
                print(f"   摘要: {article['summary'][:80]}...")
        print(f"\n共获取 {len(articles)} 条热榜")
    else:
        print("未能获取到数据")


if __name__ == "__main__":
    main()
