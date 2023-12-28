import os 
from flipside import Flipside 

def get_token_metadata(api_key=None):
    if api_key is None: 
        api_key = os.getenv('FLIPSIDE_API')
    
    flipside = Flipside(api_key, "https://api-v2.flipsidecrypto.xyz")

    # Grabs all available token metadata for solana tokens
    sql = """
    SELECT 
        decimals, 
        symbol, 
        token_address, 
        token_name, 
        coin_gecko_id, 
        coin_market_cap_id  
    FROM solana.core.dim_tokens
    """

    ## Run query and await results 
    query_result_set = flipside.query(sql)
    records = getattr(query_result_set, 'records', [])
    return records