#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2EX 热帖获取工具
"""

import requests
from datetime import datetime


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}


def get_latest_articles():
    """获取V2EX热帖"""
    feeds = ["create", "ideas", "programmer", "share"]
    all_news = []
    
    try:
        for feed in feeds:
            url = f"https://www.v2ex.com/feed/{feed}.json"
            try:
                response = requests.get(url, headers=HEADERS, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                for item in data.get("items", []):
                    news = {
                        "id": item.get("id"),
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "date": item.get("date_modified") or item.get("date_published", ""),
                        "feed": feed
                    }
                    if news["title"]:
                        all_news.append(news)
            except:
                continue
        
        # 按日期排序
        all_news.sort(key=lambda x: x["date"], reverse=True)
        return all_news
    except Exception as e:
        print(f"获取V2EX热帖失败: {e}")
        return []


def main():
    """主函数"""
    print("=" * 80)
    print("V2EX 热帖")
    print("=" * 80)
    
    articles = get_latest_articles()
    
    if articles:
        for i, article in enumerate(articles[:30], 1):  # 显示前30条
            print(f"\n{i}. [{article['feed']}] {article['title']}")
            print(f"   链接: {article['url']}")
            if article['date']:
                print(f"   时间: {article['date']}")
        print(f"\n共获取 {len(articles)} 条帖子")
    else:
        print("未能获取到数据")


if __name__ == "__main__":
    main()
