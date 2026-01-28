#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IT之家新闻获取工具
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}


def parse_relative_time(time_str):
    """解析相对时间"""
    now = datetime.now()
    
    if '分钟前' in time_str:
        minutes = int(re.search(r'(\d+)', time_str).group(1))
        return (now - timedelta(minutes=minutes)).strftime('%Y-%m-%d %H:%M')
    elif '小时前' in time_str:
        hours = int(re.search(r'(\d+)', time_str).group(1))
        return (now - timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M')
    else:
        return time_str


def get_latest_articles():
    """获取IT之家最新新闻"""
    url = "https://www.ithome.com/list/"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = []
        
        items = soup.select('#list > div.fl > ul > li')
        for item in items:
            link = item.select_one('a.t')
            date_elem = item.select_one('i')
            
            if link:
                title = link.text.strip()
                href = link.get('href', '')
                date_text = date_elem.text.strip() if date_elem else ""
                
                # 过滤广告
                ad_keywords = ['神券', '优惠', '补贴', '京东', 'lapin']
                is_ad = any(kw in title for kw in ad_keywords) or 'lapin' in href
                
                if not is_ad and title:
                    news = {
                        "id": href,
                        "title": title,
                        "url": href,
                        "time": parse_relative_time(date_text) if date_text else ""
                    }
                    news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取IT之家新闻失败: {e}")
        return []


def main():
    """主函数"""
    print("=" * 80)
    print("IT之家最新新闻")
    print("=" * 80)
    
    articles = get_latest_articles()
    
    if articles:
        for i, article in enumerate(articles[:30], 1):  # 只显示前30条
            print(f"\n{i}. {article['title']}")
            print(f"   链接: {article['url']}")
            if article['time']:
                print(f"   时间: {article['time']}")
        print(f"\n共获取 {len(articles)} 条新闻")
    else:
        print("未能获取到数据")


if __name__ == "__main__":
    main()
