#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同花顺新闻获取工具
独立脚本，可以放在任何文件夹运行
只需要安装 requests 库: pip install requests
"""

import requests
from datetime import datetime


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.10jqka.com.cn/',
}


def get_live_news():
    """获取同花顺7x24小时快讯"""
    url = "https://news.10jqka.com.cn/tapp/news/push/stock/"
    params = {
        "page": 1,
        "tag": "",
        "track": "website",
        "pagesize": 30
    }
    
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        news_list = []
        raw_list = data.get("data", {}).get("list", [])
        
        for item in raw_list:
            # 解析时间
            time_str = ""
            ctime = item.get("ctime", 0)
            if ctime:
                try:
                    time_str = datetime.fromtimestamp(int(ctime)).strftime("%Y-%m-%d %H:%M:%S")
                except:
                    time_str = str(ctime)
            
            news = {
                "id": item.get("id"),
                "title": item.get("title", ""),
                "url": item.get("url", "") or f"https://news.10jqka.com.cn/{item.get('id')}/",
                "time": time_str,
                "source": item.get("source", ""),
                "digest": item.get("digest", "")
            }
            news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取快讯失败: {e}")
        return []


def get_hot_news():
    """获取同花顺热门新闻"""
    # 原接口已失效 (404)，暂时返回空列表，避免中断程序
    # url = "https://news.10jqka.com.cn/tapp/news/push/stock/hotnews/"
    print("提示: 热门新闻接口已失效，暂不展示。")
    return []


def get_important_news():
    """获取同花顺要闻精选"""
    url = "https://news.10jqka.com.cn/tapp/news/push/stock/?page=1&tag=-20000&track=website&pagesize=30"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # 增加判空逻辑
        response_data = data.get("data")
        if not response_data or not isinstance(response_data, dict):
            return []
            
        news_list = []
        for item in response_data.get("list", []):
            # 解析时间
            time_str = ""
            ctime = item.get("ctime", 0)
            if ctime:
                try:
                    time_str = datetime.fromtimestamp(int(ctime)).strftime("%Y-%m-%d %H:%M:%S")
                except:
                    time_str = str(ctime)
            
            news = {
                "id": item.get("id"),
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "time": time_str,
                "digest": item.get("digest", "")[:100] if item.get("digest") else ""
            }
            news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取要闻精选失败: {e}")
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
        if news.get('source'):
            print(f"   📍 来源: {news['source']}")
        if news.get('read_count'):
            print(f"   👁️ 阅读: {news['read_count']}")


def main():
    print("\n🌐 同花顺新闻获取工具")
    print("正在获取最新数据...\n")
    
    # 1. 获取7x24快讯
    live = get_live_news()
    print_news(live[:10], "7x24小时快讯 (最新10条)")
    
    # 2. 获取热门新闻
    hot = get_hot_news()
    print_news(hot[:10], "热门新闻 (最新10条)")
    
    # 3. 获取要闻精选
    important = get_important_news()
    print_news(important[:10], "要闻精选 (最新10条)")
    
    print("\n" + "=" * 60)
    print("✅ 获取完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
