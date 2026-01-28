#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华尔街见闻新闻获取工具
独立脚本，可以放在任何文件夹运行
只需要安装 requests 库: pip install requests
"""

import requests
from datetime import datetime


def get_live_news():
    """获取华尔街见闻快讯（实时资讯）"""
    url = "https://api-one.wallstcn.com/apiv1/content/lives?channel=global-channel&limit=30"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        news_list = []
        for item in data.get("data", {}).get("items", []):
            news = {
                "id": item.get("id"),
                "title": item.get("title") or item.get("content_text", ""),
                "url": item.get("uri", ""),
                "time": datetime.fromtimestamp(item.get("display_time", 0)).strftime("%Y-%m-%d %H:%M:%S"),
                "digest": item.get("content_text", "")  # 提取快讯内容作为摘要
            }
            # 如果标题和摘要一样（有些快讯没标题），则清空摘要，避免重复
            if news["title"] == news["digest"]:
                news["digest"] = ""
            news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取快讯失败: {e}")
        return []


def get_articles():
    """获取华尔街见闻文章（深度报道）"""
    url = "https://api-one.wallstcn.com/apiv1/content/information-flow?channel=global-channel&accept=article&limit=30"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        news_list = []
        for item in data.get("data", {}).get("items", []):
            resource_type = item.get("resource_type", "")
            resource = item.get("resource", {})
            
            # 过滤广告和主题
            if resource_type in ["theme", "ad"]:
                continue
            if resource.get("type") == "live":
                continue
            if not resource.get("uri"):
                continue
            
            news = {
                "id": resource.get("id"),
                "title": resource.get("title") or resource.get("content_short", ""),
                "url": resource.get("uri", ""),
                "time": datetime.fromtimestamp(resource.get("display_time", 0)).strftime("%Y-%m-%d %H:%M:%S"),
                "digest": resource.get("content_short", "")  # 提取文章摘要
            }
            news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取文章失败: {e}")
        return []


def get_hot_news():
    """获取华尔街见闻热门文章"""
    url = "https://api-one.wallstcn.com/apiv1/content/articles/hot?period=all"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        news_list = []
        for item in data.get("data", {}).get("day_items", []):
            news = {
                "id": item.get("id"),
                "title": item.get("title", ""),
                "url": item.get("uri", ""),
                "digest": item.get("content_short", "")
            }
            news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取热门文章失败: {e}")
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
        if news.get('digest'):
            print(f"   📝 摘要: {news['digest']}")
        if news.get('time'):
            print(f"   🕐 {news['time']}")
        if news.get('url'):
            print(f"   🔗 {news['url']}")


def main():
    print("\n🌐 华尔街见闻新闻获取工具")
    print("正在获取最新数据...\n")
    
    # 1. 获取实时快讯
    live_news = get_live_news()
    print_news(live_news[:10], "实时快讯 (最新10条)")
    
    # 2. 获取深度文章
    articles = get_articles()
    print_news(articles[:10], "深度文章 (最新10条)")
    
    # 3. 获取热门文章
    hot_news = get_hot_news()
    print_news(hot_news[:10], "热门文章 (最新10条)")
    
    print("\n" + "=" * 60)
    print("✅ 获取完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
