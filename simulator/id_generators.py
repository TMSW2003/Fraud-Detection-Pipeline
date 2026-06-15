from itertools import count

transaction_counter = count(1)
burst_counter = count(1)

def generate_transaction_id()-> str:
    '''Generates a unique transaction ID using a simple counter.'''
    
    txn_number = next(transaction_counter)
    return f"txn_{txn_number:08d}"

def generate_burst_id() -> str:
    '''Generates unique burst ID using simple counter.'''
    return f"burst_{next(burst_counter):03d}"