import os
import json
import pandas as pd
from dotenv import load_dotenv
from solana.rpc.api import Client
from solders.signature import Signature
from solders.transaction_status import EncodedConfirmedTransactionWithStatusMeta, EncodedTransactionWithStatusMeta
from .query import get_transaction_hash

def fetch_transactions_in_batches(sql_query, quicknode_client_url):
    # Load environment variables
    load_dotenv()

    # Get transaction IDs
    tx_ids = get_transaction_hash(sql_query=sql_query)
    tx_df = pd.DataFrame(tx_ids.records)
    tx_id_list = tx_df['tx_id'].tolist()

    # Initialize Solana client
    solana_client = Client(quicknode_client_url)

    # Console status counters
    total_transactions = len(tx_id_list)
    processed_transactions = 0

    # Process transactions in batches
    all_batch_results = []
    failed_tx_ids = []
    for chunk in chunk_list(tx_id_list, 1000): 
        batch_results = []
        for tx_id in chunk: 
            try: 
                sig = Signature.from_string(tx_id)
                response = solana_client.get_transaction(sig, "jsonParsed", max_supported_transaction_version=0).value
                # Convert response to dict
                response_dict = response_to_dict(response)
                if response_dict:
                    batch_results.append(response_dict)
                else:
                    print(f"No valid response for transaction ID {tx_id}")
            except Exception as e: 
                print(f"Error processing transaction ID: {tx_id}, {e}")
                failed_tx_ids.append(tx_id)
            finally: 
                processed_transactions += 1
                remaining = total_transactions - processed_transactions
                print(f"Processed: {processed_transactions}/{total_transactions}, Remaining: {remaining}")
        all_batch_results.extend(batch_results)

    ## Retry failed transaction IDs 
    if failed_tx_ids: 
        print("Retrying unsuccessful transaction calls")
        for tx_id in failed_tx_ids: 
            try: 
                sig = Signature.from_string(tx_id)
                response = solana_client.get_transaction(sig, "jsonParsed", max_supported_transaction_version=0).value
                response_dict = response_to_dict(response)
                if response_dict:
                    batch_results.append(response_dict)
                else: 
                    print(f"No valid response for transactions ID: {tx_id}")
            except Exception as e: 
                print(f"Failed again to process transaction ID: {tx_id}")

    ## Save to data-seed folder in case database upload fails 
    try: 
        os.makedirs('data-seed', exist_ok=True)
        with open('data-seed/all_batch_results.json', 'w') as f:
            json.dump(all_batch_results, f)
    except Exception as e: 
        print(f"Error saving data to file: {e}")
    return all_batch_results

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def parse_ui_transaction(ui_transaction):
    return {
        "signatures": [str(signature) for signature in ui_transaction.signatures],
        "message": parse_ui_parsed_message(ui_transaction.message) if ui_transaction.message else None,
    }

def parse_ui_parsed_message(ui_parsed_message):
    return {
        "account_keys": [parse_parsed_account(account) for account in ui_parsed_message.account_keys],
        "recent_blockhash": str(ui_parsed_message.recent_blockhash),
        "instructions": [parse_ui_instruction(instruction) for instruction in ui_parsed_message.instructions],
    }

def parse_parsed_account(parsed_account):
    return {
        "pubkey": str(parsed_account.pubkey),
        "writable": parsed_account.writable,
        "signer": parsed_account.signer,
    }

def parse_ui_instruction(instruction):
    # Implement the parsing logic for UiPartiallyDecodedInstruction
    return {
        # Example fields
        "program_id": str(instruction.program_id),
        "data": instruction.data,
    }

def parse_ui_meta(ui_meta): 
    return {
        "err": str(ui_meta.err),
        "fee": int(ui_meta.fee),
        "pre_balances": ui_meta.pre_balances, 
        "post_balances": ui_meta.post_balances, 
        "inner_instructions": [parse_ui_inner_instruction(inner_instr) for inner_instr in ui_meta.inner_instructions] if ui_meta.inner_instructions else None,
        "log_messages": ui_meta.log_messages,
        "pre_token_balances": [parse_token_balance(tb) for tb in ui_meta.pre_token_balances] if ui_meta.pre_token_balances else None, 
        "post_token_balances": [parse_token_balance(tb) for tb in ui_meta.post_token_balances] if ui_meta.post_token_balances else None, 
        "compute_units_consumed": int(ui_meta.compute_units_consumed)
    }

def parse_token_balance(token_balance): 
    return {
       "account_index": int(token_balance.account_index), 
       "mint": str(token_balance.mint), 
       "ui_token_amount": parse_ui_token_amount(token_balance.ui_token_amount) if token_balance.ui_token_amount else None, 
       "owner": str(token_balance.owner), 
       "program_id": str(token_balance.program_id) 
    }

def parse_ui_token_amount(ui_token_amount):
    return {
        "ui_amount": ui_token_amount.ui_amount,
        "decimals": int(ui_token_amount.decimals),
        "amount": ui_token_amount.amount,
        "ui_amount_string": ui_token_amount.ui_amount_string
    }

def parse_ui_inner_instruction(ui_inner_instruction):
    return {
        "index": ui_inner_instruction.index,
        "instructions": [parse_parsed_instruction(instr) for instr in ui_inner_instruction.instructions]
    }

def parse_parsed_instruction(parsed_instruction):
    return {
        "program": parsed_instruction.program,
        "program_id": str(parsed_instruction.program_id),
        "parsed": parse_parsed_info(parsed_instruction.parsed) if parsed_instruction.parsed else None,
        "stack_height": parsed_instruction.stack_height
    }

def parse_parsed_info(parsed_info):
    # Assuming parsed_info is a dictionary-like object
    return {
        "amount": parsed_info.get("amount"),
        "authority": parsed_info.get("authority"),
        "destination": parsed_info.get("destination"),
        "source": parsed_info.get("source"),
        "type": parsed_info.get("type")
    }

def response_to_dict(obj):
    if isinstance(obj, EncodedConfirmedTransactionWithStatusMeta):
        transaction_data = obj.transaction
        if isinstance(transaction_data, EncodedTransactionWithStatusMeta):
            ui_transaction = transaction_data.transaction
            ui_meta = transaction_data.meta
            return {
                "slot": obj.slot,
                "transaction": parse_ui_transaction(ui_transaction) if ui_transaction else None,
                "meta": parse_ui_meta(ui_meta) if ui_meta else None,
                "block_time": obj.block_time,
            }
    else:
        return obj

       
