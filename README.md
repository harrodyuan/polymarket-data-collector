# Polymarket Data Collection Pipeline

A Python pipeline for collecting and analyzing market data from [Polymarket](https://polymarket.com).

## Setup

### Prerequisites
- Python 3.8+
- Required packages: pandas, python-dotenv
- Polymarket API credentials

### Environment Setup
1. Create a `.env` file in the project root
2. Add your Polymarket private key:
```
PK=your_private_key_here
```

## Directory Structure
```
polymarket_data_collector/
├── historical_data/
│   ├── raw_data/              # All market data
│   └── open_markets/          # Only open markets
├── get_polymarket_data.py     # Fetches all markets
├── get_open_markets.py        # Filters for open markets
└── pipeline_all_poly.py       # Main pipeline script
```

## Usage

### Run Complete Pipeline
```bash
python pipeline_all_poly.py
```

This will:
1. Create necessary directories if they don't exist
2. Fetch all Polymarket data (~30k+ markets)
3. Filter for currently open markets
4. Save results in CSV format with date stamps

### Output Files
- Raw data: `historical_data/raw_data/polymarket_data_YYYYMMDD.csv`
- Open markets: `historical_data/open_markets/open_markets_YYYYMMDD.csv`

## Performance
- Typical runtime: ~45 seconds
- Handles pagination automatically
- Processes 30,000+ markets efficiently

## Author
BD_Harold