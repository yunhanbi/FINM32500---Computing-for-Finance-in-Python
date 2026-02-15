from baseline import baseline
from optimization import optimization
import func_timeout
import numpy as np
import pandas as pd
import time

def generate_input(len):
    input_df = pd.DataFrame(None)
    input_df['price'] = np.random.uniform(low=1.0, high=200.0, size=len)
    input_df['quantity'] = np.random.default_rng().integers(low=1.0, high=200.0, size=len)
    sides = ['bid', 'ask']
    input_df['side'] = np.random.choice(sides, size=len)
    input_df = input_df.reset_index(names=['order_id'])
    return input_df

def timer(ops, orders, model, result, action, model_name):

    if model_name == 'base':
        start_time = time.perf_counter()
        for idx in orders.index:
            if action == 'add':
                model.add_order(orders.loc[idx, :].to_dict())
            elif action == 'amend':
                model.amend_order(orders.loc[idx, 'order_id'].squeeze(), 1)
            else:
                model.delete_order(orders.loc[idx, 'order_id'].squeeze())
        end_time = time.perf_counter()
        total_time = end_time - start_time

    elif model_name == 'opt':
        start_time = time.perf_counter()
        if action == 'add':
            model.add_order(orders)
        elif action == 'amend':
            model.amend_order(orders['order_id'], [1]*len(orders))
        else:
            model.delete_order(orders['order_id'])
        end_time = time.perf_counter()
        total_time = end_time - start_time

    result.loc[result['operations']==ops, '{}_{}_total_time'.format(model_name, action)] = total_time
    result.loc[result['operations']==ops, '{}_{}_avg_time'.format(model_name, action)] = (total_time) / ops
    result.loc[result['operations']==ops, '{}_{}_scaling_behavior'.format(model_name, action)] = np.log2(total_time + 1)

    return result

def timeout_timer(ops, orders, model, result, action, model_name, timer, timeout_seconds):
    try:
        result = func_timeout.func_timeout(timeout=timeout_seconds, func=timer, args=(ops, orders, model, result, action, model_name))
        return result

    except func_timeout.FunctionTimedOut:
        total_time = timeout_seconds
        result.loc[result['operations'] == ops, '{}_{}_total_time'.format(model_name, action)] = total_time
        result.loc[result['operations'] == ops, '{}_{}_avg_time'.format(model_name, action)] = (total_time) / ops
        result.loc[result['operations'] == ops, '{}_{}_scaling_behavior'.format(model_name, action)] = np.log2(total_time + 1)
        return result

def main():
    input_df = generate_input(1000000)
    operations = [10, 100, 1000, 10000, 100000, 1000000]
    result_df = pd.DataFrame({'operations': operations})
    base = baseline()
    opt = optimization()
    for i in operations:
        input = input_df.iloc[:i, :]
        result_df = timeout_timer(i, input, base, result_df, 'add', 'base', timer, 900)
        result_df = timeout_timer(i, input, base, result_df, 'amend', 'base', timer, 900)
        result_df = timeout_timer(i, input, base, result_df, 'delete', 'base', timer, 900)
        result_df = timeout_timer(i, input, opt, result_df, 'add', 'opt', timer, 900)
        result_df = timeout_timer(i, input, opt, result_df, 'amend', 'opt', timer, 900)
        result_df = timeout_timer(i, input, opt, result_df, 'delete', 'opt', timer, 900)
    result_df.to_csv('result.csv', index=False)

    return result_df

if __name__ == '__main__':
    main()
