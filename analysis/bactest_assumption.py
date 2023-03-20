import pandas as pd
import sys
sys.path.append('../')

from backtest.backtester import simulate_pair

def get_backtest_return(pair, signal_object, sig1, sig2, trading_price, trading_sizes, betas, exit_lower= 0.2, trading_cost = 0, series = True, K = 50_000):
    exit_upper= 1 - exit_lower
    signals = signal_object.generate_signals(sig1 = sig1[pair], sig2 = sig2[pair], exit_lower = exit_lower, exit_upper = exit_upper)
    signals = pd.DataFrame(data=signals['Signal'].values, index=trading_price.index, columns=['Signal'])
    pair_leg_1 = pair[0]
    pair_leg_2 = pair[1]

    execution_delay = 1
    prepped = pd.DataFrame(
        data={
            f'Leg 1 VWAP {execution_delay}': trading_price[pair_leg_1],
            f'Leg 2 VWAP {execution_delay}': trading_price[pair_leg_2],
            f'Volume 1': trading_sizes[pair_leg_1],
            f'Volume 2': trading_sizes[pair_leg_2],
            f'Leg 1 VWAP Volume {execution_delay}': trading_sizes[pair_leg_1],
            f'Leg 2 VWAP Volume {execution_delay}': trading_sizes[pair_leg_2],
            f'Signal {execution_delay}': signals['Signal'].shift(1).fillna(0),
            'Betas': betas[pair],
            'FFR': 0.01
        }
    )
    backtest_res = simulate_pair(prepped, K=K, delay_time=execution_delay, trading_cost=trading_cost)
    if series:
        ret_series = backtest_res.Portfolio.pct_change() * 252
        return ret_series
    else:
        return backtest_res.Portfolio.iloc[-1]/K - 1