#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
36氪新闻获取工具
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}


def parse_relative_time(time_str):
    """解析相对时间，如'2小时前'"""
    now = datetime.now()
    
    if '分钟前' in time_str or '分钟' in time_str:
        minutes = int(re.search(r'(\d+)', time_str).group(1))
        return (now - timedelta(minutes=minutes)).strftime('%Y-%m-%d %H:%M')
    elif '小时前' in time_str or '小时' in time_str:
        hours = int(re.search(r'(\d+)', time_str).group(1))
        return (now - timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M')
    elif '天前' in time_str or '天' in time_str:
        days = int(re.search(r'(\d+)', time_str).group(1))
        return (now - timedelta(days=days)).strftime('%Y-%m-%d')
    else:
        return time_str


def get_latest_articles():
    """获取36氪快讯"""
    url = "https://www.36kr.com/newsflashes"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = []
        
        items = soup.select('.newsflash-item')
        for item in items:
            link = item.select_one('a.item-title')
            time_elem = item.select_one('.time')
            
            if link:
                title = link.text.strip()
                href = link.get('href', '')
                relative_time = time_elem.text.strip() if time_elem else ""
                
                news = {
                    "id": href,
                    "title": title,
                    "url": f"https://www.36kr.com{href}",
                    "time": parse_relative_time(relative_time) if relative_time else ""
                }
                if news["title"]:
                    news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取36氪快讯失败: {e}")
        return []


def main():
    """主函数"""
    print("=" * 80)
    print("36氪快讯")
    print("=" * 80)
    
    articles = get_latest_articles()
    
    if articles:
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article['title']}")
            print(f"   链接: {article['url']}")
            if article['time']:
                print(f"   时间: {article['time']}")
        print(f"\n共获取 {len(articles)} 条快讯")
    else:
        print("未能获取到数据")


if __name__ == "__main__":
    main()
