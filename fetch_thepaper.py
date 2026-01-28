#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
澎湃新闻热榜获取工具
"""

import requests
from datetime import datetime


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}


def get_latest_articles():
    """获取澎湃新闻热榜"""
    url = "https://cache.thepaper.cn/contentapi/wwwIndex/rightSidebar"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        news_list = []
        for item in data.get("data", {}).get("hotNews", []):
            cont_id = item.get("contId", "")
            news = {
                "id": cont_id,
                "title": item.get("name", ""),
                "url": f"https://www.thepaper.cn/newsDetail_forward_{cont_id}",
                "mobile_url": f"https://m.thepaper.cn/newsDetail_forward_{cont_id}",
                "time": item.get("pubTimeLong", "")
            }
            if news["title"]:
                news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取澎湃新闻失败: {e}")
        return []


def main():
    """主函数"""
    print("=" * 80)
    print("澎湃新闻热榜")
    print("=" * 80)
    
    articles = get_latest_articles()
    
    if articles:
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article['title']}")
            print(f"   链接: {article['url']}")
        print(f"\n共获取 {len(articles)} 条新闻")
    else:
        print("未能获取到数据")


if __name__ == "__main__":
    main()
