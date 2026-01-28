#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度热搜榜新闻获取工具
"""

import requests
import json
import re
from datetime import datetime


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}


def get_latest_articles():
    """获取百度热搜榜"""
    url = "https://top.baidu.com/board?tab=realtime"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        # 从HTML中提取JSON数据
        html = response.text
        match = re.search(r'<!--s-data:(.*?)-->', html, re.DOTALL)
        if not match:
            return []
        
        data = json.loads(match.group(1))
        news_list = []
        
        # 提取热搜内容
        cards = data.get("data", {}).get("cards", [])
        if cards and len(cards) > 0:
            content_list = cards[0].get("content", [])
            for item in content_list:
                if item.get("isTop"):  # 跳过置顶
                    continue
                    
                news = {
                    "id": item.get("rawUrl", ""),
                    "title": item.get("word", ""),
                    "url": item.get("rawUrl", ""),
                    "summary": item.get("desc", "")
                }
                if news["title"]:
                    news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取百度热搜失败: {e}")
        return []


def main():
    """主函数"""
    print("=" * 80)
    print("百度热搜榜")
    print("=" * 80)
    
    articles = get_latest_articles()
    
    if articles:
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article['title']}")
            print(f"   链接: {article['url']}")
            if article['summary']:
                print(f"   简介: {article['summary']}")
        print(f"\n共获取 {len(articles)} 条热搜")
    else:
        print("未能获取到数据")


if __name__ == "__main__":
    main()
