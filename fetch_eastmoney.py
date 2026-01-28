#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
东方财富新闻获取工具
独立脚本，可以放在任何文件夹运行
只需要安装 requests 库: pip install requests
"""

import requests
import json
import re
from datetime import datetime


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.eastmoney.com/',
}


def get_live_news():
    """获取东方财富7x24小时快讯"""
    url = "https://np-anotice-stock.eastmoney.com/api/security/ann"
    params = {
        "cb": "jQuery_callback",
        "sr": -1,
        "page_size": 30,
        "page_index": 1,
        "ann_type": "SHA,SZA,BJA",
        "client_source": "web",
        "f_node": 0,
        "s_node": 0
    }
    
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        # 解析JSONP响应
        text = response.text
        match = re.search(r'jQuery_callback\((.*)\)', text, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
        else:
            # 尝试直接解析JSON
            data = response.json() if response.text.startswith('{') else {}
        
        news_list = []
        for item in data.get("data", {}).get("list", []):
            codes = item.get("codes", [{}])
            stock_name = codes[0].get("short_name", "") if codes else ""
            news = {
                "id": item.get("art_code"),
                "title": f"[{stock_name}] {item.get('title', '')}" if stock_name else item.get('title', ''),
                "url": f"https://data.eastmoney.com/notices/detail/{codes[0].get('stock_code', '') if codes else ''}/{item.get('art_code', '')}.html",
                "time": item.get("notice_date", ""),
                "source": stock_name
            }
            news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取快讯失败: {e}")
        return []


def get_stock_news():
    """获取东方财富股票资讯"""
    url = "https://np-anotice-stock.eastmoney.com/api/security/ann"
    params = {
        "cb": "callback",
        "sr": -1,
        "page_size": 30,
        "page_index": 1,
        "ann_type": "A",
        "f_node": 0,
        "s_node": 0
    }
    
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        # 解析JSONP响应
        text = response.text
        match = re.search(r'callback\((.*)\)', text, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
        else:
            data = {}
        
        news_list = []
        for item in data.get("data", {}).get("list", []):
            news = {
                "id": item.get("art_code"),
                "title": f"[{item.get('codes', [{}])[0].get('short_name', '')}] {item.get('title', '')}",
                "url": f"https://data.eastmoney.com/notices/detail/{item.get('codes', [{}])[0].get('ann_code', '')}/{item.get('art_code', '')}.html",
                "time": item.get("notice_date", "")
            }
            news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取股票资讯失败: {e}")
        return []


def get_finance_news():
    """获取东方财富财经要闻"""
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "cb": "jQuery_callback",
        "fid": "f62",
        "po": 1,
        "pz": 30,
        "pn": 1,
        "np": 1,
        "fltt": 2,
        "invt": 2,
        "fs": "m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2",
        "fields": "f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124"
    }
    
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        # 解析JSONP响应
        text = response.text
        match = re.search(r'jQuery_callback\((.*)\)', text, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
        else:
            data = {}
        
        news_list = []
        for item in data.get("data", {}).get("diff", []):
            news = {
                "id": item.get("f12"),
                "title": f"[{item.get('f14', '')}] 涨跌幅: {item.get('f3', '')}%",
                "url": f"https://quote.eastmoney.com/{item.get('f12', '')}.html",
                "time": "",
                "info": f"现价: {item.get('f2', '')} 主力净流入: {item.get('f62', '')}"
            }
            news_list.append(news)
        
        return news_list
    except Exception as e:
        print(f"获取财经要闻失败: {e}")
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
        if news.get('time'):
            print(f"   🕐 {news['time']}")
        if news.get('url'):
            print(f"   🔗 {news['url']}")
        if news.get('source'):
            print(f"   📍 来源: {news['source']}")


def main():
    print("\n🌐 东方财富新闻获取工具")
    print("正在获取最新数据...\n")
    
    # 1. 获取7x24快讯
    live = get_live_news()
    print_news(live[:10], "7x24小时快讯 (最新10条)")
    
    # 2. 获取财经要闻
    finance = get_finance_news()
    print_news(finance[:10], "财经要闻 (最新10条)")
    
    print("\n" + "=" * 60)
    print("✅ 获取完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
