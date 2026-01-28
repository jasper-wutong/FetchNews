import requests
import pandas as pd
from datetime import datetime
import json
from typing import Optional, List, Dict

def get_event_info(url_or_slug: str) -> Optional[Dict]:
    """
    从 Polymarket 事件 URL 或 slug 获取事件信息
    
    参数:
        url_or_slug: 完整的 URL (如 https://polymarket.com/event/xxx) 或直接是 slug
    
    返回:
        包含事件信息的字典，包括 token IDs
    """
    # 提取 slug
    if url_or_slug.startswith('http'):
        slug = url_or_slug.split('/event/')[-1].strip('/')
    else:
        slug = url_or_slug
    
    print(f"正在获取事件信息: {slug}")
    
    api_url = f"https://gamma-api.polymarket.com/events?slug={slug}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"获取事件信息失败，状态码: {response.status_code}")
            return None
        
        data = response.json()
        
        if not isinstance(data, list) or len(data) == 0:
            print("未找到该事件")
            return None
        
        event = data[0]
        markets = event.get('markets', [])
        
        if not markets:
            print("该事件没有市场数据")
            return None
        
        market = markets[0]
        
        # 解析 token IDs 和结果选项
        clob_token_ids = json.loads(market.get('clobTokenIds', '[]'))
        outcomes = json.loads(market.get('outcomes', '[]'))
        
        result = {
            'title': event.get('title'),
            'question': market.get('question'),
            'description': market.get('description', ''),
            'market_id': market.get('id'),
            'outcomes': outcomes,
            'token_ids': clob_token_ids,
            'current_prices': json.loads(market.get('outcomePrices', '[]')),
            'volume': market.get('volume'),
            'liquidity': market.get('liquidity'),
        }
        
        print(f"\n事件: {result['title']}")
        print(f"问题: {result['question']}")
        print(f"\n可选结果:")
        for i, (outcome, price) in enumerate(zip(outcomes, result['current_prices'])):
            print(f"  {outcome}: {float(price)*100:.2f}% (Token ID: {clob_token_ids[i]})")
        
        return result
        
    except Exception as e:
        print(f"获取事件信息时发生错误: {e}")
        return None

def fetch_polymarket_data(token_id: str, fidelity: int = 1, output_file: str = None):
    """
    根据 token_id 获取历史价格数据
    
    参数:
        token_id: Token ID (从 get_event_info 获取)
        fidelity: 粒度（分钟），1 表示每分钟一个数据点，60 表示每小时
        output_file: 输出文件名
    """
    # 使用正确的 CLOB 历史数据接口
    url = "https://clob.polymarket.com/prices-history"
    
    # 构造请求参数
    params = {
        "market": token_id,
        "interval": "max", # 使用 max 确保拿到该市场自创建以来的所有记录
        "fidelity": fidelity # 数据点的频率（分钟）
    }
    
    # 必须加上浏览器伪装，否则很容易被 Cloudflare 报 400/403
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    print(f"\n正在调取历史数据...")
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"错误详情: {response.text}") # 打印出服务器返回的报错信息，方便排查
            return None
        
        data = response.json().get('history', [])
        
        if not data:
            print("未获取到数据，可能是该市场目前成交量极低或该粒度下无成交。")
            return None
        
        # 数据清洗
        df = pd.DataFrame(data)
        # 将 Unix 时间戳转换为北京时间
        df['t'] = pd.to_datetime(df['t'], unit='s') + pd.Timedelta(hours=8)
        df.columns = ['时间', '价格 (胜率)']
        
        # 保存为 Excel
        if output_file is None:
            output_file = f"polymarket_{token_id[:8]}.xlsx"
        
        df.to_excel(output_file, index=False)
        print(f"成功！数据已保存至 {output_file}，共 {len(df)} 条。")
        return df

    except Exception as e:
        print(f"发生错误: {e}")
        return None

def fetch_from_url(url: str, outcome: str = "Yes", fidelity: int = 60, output_file: str = None):
    """
    直接从 Polymarket URL 获取数据（推荐使用）
    
    参数:
        url: Polymarket 事件页面 URL
        outcome: 要获取数据的选项，如 "Yes"、"No" 等
        fidelity: 数据粒度（分钟），默认60分钟
        output_file: 输出文件名，如果不指定则自动生成
    """
    # 获取事件信息
    event_info = get_event_info(url)
    
    if not event_info:
        return None
    
    # 找到对应的 token ID
    try:
        outcome_index = event_info['outcomes'].index(outcome)
        token_id = event_info['token_ids'][outcome_index]
    except (ValueError, IndexError):
        print(f"\n错误: 找不到选项 '{outcome}'")
        print(f"可用选项: {', '.join(event_info['outcomes'])}")
        return None
    
    # 生成输出文件名
    if output_file is None:
        # 从 URL 生成简短的文件名
        slug = url.split('/event/')[-1].strip('/')
        output_file = f"{slug}_{outcome}.xlsx"
    
    # 获取历史数据
    return fetch_polymarket_data(token_id, fidelity, output_file)

def fetch_orderbook(token_id: str) -> Optional[Dict]:
    """
    获取指定 token 的当前 order book (买卖盘口)
    
    参数:
        token_id: Token ID
    
    返回:
        包含 bids (买单) 和 asks (卖单) 的字典
    """
    url = f"https://clob.polymarket.com/book?token_id={token_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"获取 Order Book 失败，状态码: {response.status_code}")
            return None
        
        data = response.json()
        
        print(f"\n📊 Order Book 数据:")
        print(f"Market: {data.get('market')}")
        print(f"时间戳: {datetime.fromtimestamp(int(data.get('timestamp', 0))/1000).strftime('%Y-%m-%d %H:%M:%S')}")
        
        bids = data.get('bids', [])
        asks = data.get('asks', [])
        
        # 注意：API 返回的数据结构：
        # bids: 按价格从低到高排序，最后一个是最高买价（愿意买入的最高价）
        # asks: 按价格从高到低排序（实际上也是从低到高），最后一个才是最低卖价（愿意卖出的最低价）
        # 
        # 对于 Yes 选项:
        # - Bids[-1] = 最高买价 (例如 2.5%)
        # - Asks[-1] = 最低卖价 (例如 2.6%)
        # - Asks[0] 显示的是补数 (1 - Yes) = No 的价格 (99.9%)
        
        # 反转数组以便从高到低显示
        bids_sorted = sorted(bids, key=lambda x: float(x['price']), reverse=True)
        asks_sorted = sorted(asks, key=lambda x: float(x['price']), reverse=True)
        
        print(f"\n买单 (Bids) 数量: {len(bids)}")
        if bids_sorted:
            print("前10个买单 (价格从高到低):")
            for bid in bids_sorted[:10]:
                print(f"  价格: {float(bid['price']):.4f} ({float(bid['price'])*100:.2f}%), 数量: {bid['size']}")
        
        print(f"\n卖单 (Asks) 数量: {len(asks)}")
        if asks_sorted:
            print("前10个卖单 (价格从高到低，实际成交应看最低的):")
            for ask in asks_sorted[:10]:
                print(f"  价格: {float(ask['price']):.4f} ({float(ask['price'])*100:.2f}%), 数量: {ask['size']}")
        
        # 计算最佳买卖价和价差
        if bids and asks:
            # 最佳买价 = bids 中最高的价格
            best_bid = max(float(b['price']) for b in bids)
            # 最佳卖价 = asks 中最低的价格（注意：不是 asks[0]）
            best_ask = min(float(a['price']) for a in asks)
            spread = best_ask - best_bid
            mid_price = (best_bid + best_ask) / 2
            
            print(f"\n📈 市场深度:")
            print(f"最佳买价 (Best Bid): {best_bid:.4f} ({best_bid*100:.2f}%)")
            print(f"最佳卖价 (Best Ask): {best_ask:.4f} ({best_ask*100:.2f}%)")
            print(f"中间价 (Mid Price): {mid_price:.4f} ({mid_price*100:.2f}%)")
            print(f"价差 (Spread): {spread:.4f} ({spread*100:.2f}% 或占中间价的 {spread/mid_price*100:.2f}%)")
        
        return data
        
    except Exception as e:
        print(f"获取 Order Book 时发生错误: {e}")
        return None

def save_orderbook_to_excel(orderbook_data: Dict, output_file: str = None):
    """
    将 order book 数据保存为 Excel 文件
    
    参数:
        orderbook_data: order book 数据字典
        output_file: 输出文件名
    """
    if not orderbook_data:
        print("没有 order book 数据可保存")
        return
    
    try:
        # 创建 Excel writer
        if output_file is None:
            output_file = f"orderbook_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        bids = orderbook_data.get('bids', [])
        asks = orderbook_data.get('asks', [])
        
        # 准备数据框列表
        sheets_to_save = {}
        
        # 保存买单 (按价格从高到低排序)
        if bids:
            df_bids = pd.DataFrame(bids)
            df_bids['price'] = df_bids['price'].astype(float)
            df_bids['size'] = pd.to_numeric(df_bids['size'], errors='coerce')
            df_bids['probability'] = df_bids['price'] * 100
            df_bids = df_bids.sort_values('price', ascending=False)  # 从高到低
            df_bids = df_bids[['price', 'probability', 'size']]
            df_bids.columns = ['价格', '概率 (%)', '数量']
            sheets_to_save['买单 (Bids)'] = df_bids
        
        # 保存卖单
        if asks:
            df_asks = pd.DataFrame(asks)
            df_asks['price'] = df_asks['price'].astype(float)
            df_asks['size'] = pd.to_numeric(df_asks['size'], errors='coerce')
            df_asks['probability'] = df_asks['price'] * 100
            df_asks = df_asks[['price', 'probability', 'size']]
            df_asks.columns = ['价格', '概率 (%)', '数量']
            sheets_to_save['卖单 (Asks)'] = df_asks
        
        # 保存摘要信息
        if bids and asks:
            # 最佳买价 = 最高的 bid
            best_bid = max(float(b['price']) for b in bids)
            # 最佳卖价 = 最低的 ask
            best_ask = min(float(a['price']) for a in asks)
            spread = best_ask - best_bid
            mid_price = (best_bid + best_ask) / 2
            
            summary = {
                '指标': ['最佳买价', '最佳卖价', '中间价', '价差（绝对值）', '价差（相对于中间价%）'],
                '数值': [best_bid, best_ask, mid_price, spread, spread/mid_price*100]
            }
            df_summary = pd.DataFrame(summary)
            sheets_to_save['市场摘要'] = df_summary
        
        # 写入 Excel
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            for sheet_name, df in sheets_to_save.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"\n✅ Order Book 数据已保存至 {output_file}")
        
    except Exception as e:
        print(f"保存 Order Book 时发生错误: {e}")

def fetch_orderbook_from_url(url: str, outcome: str = "Yes", save_to_file: bool = True, output_file: str = None):
    """
    从 URL 获取 order book 数据（推荐使用）
    
    参数:
        url: Polymarket 事件页面 URL
        outcome: 要获取的选项，如 "Yes"、"No" 等
        save_to_file: 是否保存到 Excel 文件
        output_file: 输出文件名
    """
    # 获取事件信息
    event_info = get_event_info(url)
    
    if not event_info:
        return None
    
    # 找到对应的 token ID
    try:
        outcome_index = event_info['outcomes'].index(outcome)
        token_id = event_info['token_ids'][outcome_index]
    except (ValueError, IndexError):
        print(f"\n错误: 找不到选项 '{outcome}'")
        print(f"可用选项: {', '.join(event_info['outcomes'])}")
        return None
    
    print(f"\n正在获取 '{outcome}' 选项的 Order Book...")
    
    # 获取 order book
    orderbook_data = fetch_orderbook(token_id)
    
    # 保存到文件
    if save_to_file and orderbook_data:
        if output_file is None:
            slug = url.split('/event/')[-1].strip('/')
            output_file = f"orderbook_{slug}_{outcome}.xlsx"
        save_orderbook_to_excel(orderbook_data, output_file)
    
    return orderbook_data

def main():
    # 示例 1: 获取历史价格数据
    url = "https://polymarket.com/event/will-jesus-christ-return-before-2027"
    
    # fetch_from_url(
    #     url=url,
    #     outcome="Yes",
    #     fidelity=60,
    #     output_file="jesus_return_yes.xlsx"
    # )
    
    # 示例 2: 获取 Order Book (买卖盘口)
    fetch_orderbook_from_url(
        url=url,
        outcome="Yes",
        save_to_file=True,
        output_file="orderbook_jesus_yes.xlsx"
    )
    
    # 示例 3: 如果已知 token_id，也可以直接使用
    # token_id = "69324317355037271422943965141382095011871956039434394956830818206664869608517"
    # orderbook = fetch_orderbook(token_id)
    # save_orderbook_to_excel(orderbook, "my_orderbook.xlsx")

if __name__ == "__main__":
    main()