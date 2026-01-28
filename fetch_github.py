#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Trending 获取工具
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}


def get_latest_articles():
    """获取GitHub Trending"""
    url = "https://github.com/trending?spoken_language_code="
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = []
        
        articles = soup.select('main .Box div[data-hpc] > article')
        for article in articles:
            link = article.select_one('h2 a')
            star_elem = article.select_one('[href$=stargazers]')
            desc_elem = article.select_one('p')
            
            if link:
                title = link.text.replace('\n', '').strip()
                href = link.get('href', '')
                stars = star_elem.text.replace('\n', '').strip() if star_elem else ""
                desc = desc_elem.text.replace('\n', '').strip() if desc_elem else ""
                
                news = {
                    "id": href,
                    "title": title,
                    "url": f"https://github.com{href}",
                    "stars": stars,
                    "summary": desc
                }
                if news["title"]:
                    news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取GitHub Trending失败: {e}")
        return []


def main():
    """主函数"""
    print("=" * 80)
    print("GitHub Trending")
    print("=" * 80)
    
    articles = get_latest_articles()
    
    if articles:
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article['title']}")
            print(f"   ✰ {article['stars']}")
            print(f"   链接: {article['url']}")
            if article['summary']:
                print(f"   简介: {article['summary'][:80]}...")
        print(f"\n共获取 {len(articles)} 个项目")
    else:
        print("未能获取到数据")


if __name__ == "__main__":
    main()
