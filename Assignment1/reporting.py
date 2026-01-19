def analyze(portfolio, initial_cash=100000):
    final_value = portfolio.cash
    for symbol, qty in portfolio.positions.items():
        final_value += qty * 0  # Simplified - no final price lookup
    
    total_return = (final_value - initial_cash) / initial_cash * 100
    
    report = f"""
# Performance Report

**Initial Capital:** ${initial_cash:,.2f}
**Final Value:** ${final_value:,.2f}
**Total Return:** {total_return:.2f}%
**Total Trades:** {len(portfolio.history)}
**Errors:** {len(portfolio.history)}
"""
    return report

def save_report(portfolio, filename='performance.md'):
    with open(filename, 'w') as f:
        f.write(analyze(portfolio))
