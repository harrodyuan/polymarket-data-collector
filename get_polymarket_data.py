import os
import requests
import pandas as pd
from dotenv import load_dotenv
from py_clob_client.constants import POLYGON
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs
from py_clob_client.order_builder.constants import BUY
from datetime import datetime

def fetch_polymarket_data():
    """
    Fetches market data from Polymarket API with pagination support
    Returns a list of all markets
    """
    # Set up environment variables and constants
    host = "https://clob.polymarket.com"

    load_dotenv()
    private_key = os.getenv("PK")
    chain_id = POLYGON
    
    # Initialize lists to store all markets
    all_markets = []
    page = 1
    next_cursor = None
    client = ClobClient(host, key=private_key, chain_id=chain_id)
    
    try:
        # Initialize the client
        
        start_time = datetime.now()
        
        while True:
            try:
                if page == 1:
                    response = client.get_markets()
                else:
                    response = client.get_markets(next_cursor=next_cursor)
                
                if not response or not response.get('data'):
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds()
                    print(f"\nFetch completed successfully!")
                    print(f"Total markets fetched: {len(all_markets)}")
                    print(f"Time taken: {duration:.2f} seconds")
                    print(f"Average rate: {len(all_markets)/duration:.1f} markets/second")
                    break
                
                markets = response.get('data', [])
                
                if not markets:
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds()
                    print(f"\nFetch completed successfully!")
                    print(f"Total markets fetched: {len(all_markets)}")
                    print(f"Time taken: {duration:.2f} seconds")
                    print(f"Average rate: {len(all_markets)/duration:.1f} markets/second")
                    break
                    
                all_markets.extend(markets)
                print(f"Page {page}: Fetched {len(markets)} markets. Total: {len(all_markets)}")
                
                # Increment offset for next page
                next_cursor = response.get('next_cursor')
                page += 1
                
            except Exception as e:
                if "next item should be greater than or equal to 0" in str(e):
                    # This is actually a successful completion
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds()
                    print(f"\nFetch completed successfully!")
                    print(f"Total markets fetched: {len(all_markets)}")
                    print(f"Time taken: {duration:.2f} seconds")
                    print(f"Average rate: {len(all_markets)/duration:.1f} markets/second")
                    break
                else:
                    print(f"Error fetching page {page}: {str(e)}")
                    break

        return all_markets

    except Exception as e:
        print(f"Error initializing client: {str(e)}")
        return None

def clean_text(text):
    """Clean text fields for CSV output"""
    if not text:
        return ""
    # Replace newlines and multiple spaces with single space
    text = ' '.join(text.split())
    # Remove any problematic characters
    text = text.replace('"', '""')  # Escape quotes
    return text

def save_markets_to_csv(markets, filename):
    """Save markets data to CSV file with all available fields"""
    data = []
    for market in markets:
        # Handle tags - ensure we have a list even if tags is None
        tags = market.get('tags', [])
        tags = tags if isinstance(tags, list) else []
        
        row = {
            # Market identification
            'condition_id': market.get('condition_id', ''),
            'question_id': market.get('question_id', ''),
            'question': clean_text(market.get('question', '')),
            'description': clean_text(market.get('description', '')),
            'market_slug': market.get('market_slug', ''),
            'category': clean_text(market.get('category', '')),
            
            # Status flags
            'active': market.get('active', ''),
            'closed': market.get('closed', ''),
            'archived': market.get('archived', ''),
            'accepting_orders': market.get('accepting_orders', ''),
            'accepting_order_timestamp': market.get('accepting_order_timestamp', ''),
            'enable_order_book': market.get('enable_order_book', ''),
            
            # Market parameters
            'minimum_order_size': market.get('minimum_order_size', ''),
            'minimum_tick_size': market.get('minimum_tick_size', ''),
            'min_incentive_size': market.get('min_incentive_size', ''),
            'max_incentive_spread': market.get('max_incentive_spread', ''),
            'maker_base_fee': market.get('maker_base_fee', ''),
            'taker_base_fee': market.get('taker_base_fee', ''),
            
            # Timing information
            'end_date_iso': market.get('end_date_iso', ''),
            'game_start_time': market.get('game_start_time', ''),
            'seconds_delay': market.get('seconds_delay', ''),
            
            # Contract information
            'fpmm': market.get('fpmm', ''),
            'icon': market.get('icon', ''),
            'image': market.get('image', ''),
            
            # Risk parameters
            'neg_risk': market.get('neg_risk', ''),
            'neg_risk_market_id': market.get('neg_risk_market_id', ''),
            'neg_risk_request_id': market.get('neg_risk_request_id', ''),
            'is_50_50_outcome': market.get('is_50_50_outcome', ''),
            
            # Token 0 information
            'token_0_id': market['tokens'][0].get('token_id', '') if market.get('tokens') else '',
            'token_0_outcome': clean_text(market['tokens'][0].get('outcome', '')) if market.get('tokens') else '',
            'token_0_price': market['tokens'][0].get('price', '') if market.get('tokens') else '',
            'token_0_winner': market['tokens'][0].get('winner', '') if market.get('tokens') else '',
            
            # Token 1 information
            'token_1_id': market['tokens'][1].get('token_id', '') if len(market.get('tokens', [])) > 1 else '',
            'token_1_outcome': clean_text(market['tokens'][1].get('outcome', '')) if len(market.get('tokens', [])) > 1 else '',
            'token_1_price': market['tokens'][1].get('price', '') if len(market.get('tokens', [])) > 1 else '',
            'token_1_winner': market['tokens'][1].get('winner', '') if len(market.get('tokens', [])) > 1 else '',
            
            # Rewards information
            'rewards_rates': str(market.get('rewards', {}).get('rates', '')) if market.get('rewards') else '',
            'rewards_min_size': str(market.get('rewards', {}).get('min_size', '')) if market.get('rewards') else '',
            'rewards_max_spread': str(market.get('rewards', {}).get('max_spread', '')) if market.get('rewards') else '',
            
            # Notifications and tags - updated tags handling
            'notifications_enabled': market.get('notifications_enabled', ''),
            'tags': ','.join(tags)  # Now tags is guaranteed to be a list
        }
        data.append(row)
    
    # Convert to DataFrame and save to CSV with specific formatting
    df = pd.DataFrame(data)
    df.to_csv(filename, 
              index=False, 
              encoding='utf-8',
              quoting=1,  # Quote all fields
              escapechar='\\',  # Use backslash as escape character
              doublequote=True  # Double up quotes for escaping
    )
    print(f"Data saved to {filename}")

def main():
    markets = fetch_polymarket_data()
    if markets:
        # Get current date for filename
        current_date = datetime.now().strftime('%Y%m%d')
        # Create filename with date
        csv_file = os.path.join(
            os.path.dirname(__file__), 
            'historical_data',
            'raw_data',
            f'polymarket_data_{current_date}.csv'
        )
        save_markets_to_csv(markets, csv_file)
        
                
if __name__ == "__main__":
    main()
