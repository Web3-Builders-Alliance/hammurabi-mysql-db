import os
from flipside import Flipside

def get_transaction_hash(api_key=None, sql_query=""):
  if api_key is None:
    api_key = os.environ('FLIPSIDE_API')
  
  flipside = Flipside(api_key, "https://api-v2.flipsidecrypto.xyz")
  
  ## Run the query and await results
  query_result_set = flipside.query(sql)
  return query_result_set

sql = """
  SELECT 
    tx_id
  FROM 
    solana.defi.fact_swaps
  WHERE 
    block_timestamp :: date >= CURRENT_DATE - 1
    AND swap_program ilike '%orca%'
    AND succeeded = true
    AND swap_to_mint = 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'
    AND swap_from_mint = 'So11111111111111111111111111111111111111112'

  UNION
  
  SELECT 
    tx_id
  FROM 
    solana.defi.fact_swaps
  WHERE 
    block_timestamp :: date >= CURRENT_DATE - 1
    AND swap_program ilike '%orca%'
    AND succeeded = true
    AND swap_from_mint = 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'
    AND swap_to_mint = 'So11111111111111111111111111111111111111112'
"""
