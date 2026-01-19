# reporting.py

import datetime
from typing import Dict, List
import math


def generate_markdown_report(results: Dict, output_filename: str = "performance.md") -> None:
    """
    Generate a comprehensive Markdown performance report.
    
    Args:
        results: Dictionary containing backtest results
        output_filename: Name of the output Markdown file
    """
    
    report_lines = []
    
    # Header
    report_lines.append("# Algorithmic Trading Backtest Performance Report")
    report_lines.append("")
    report_lines.append(f"**Report Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    # Executive Summary
    report_lines.append("## Executive Summary")
    report_lines.append("")
    
    total_return_pct = results['total_return'] * 100
    sharpe_ratio = results['sharpe_ratio']
    max_drawdown_pct = results['max_drawdown'] * 100
    
    if total_return_pct > 0:
        performance_summary = "The strategy generated positive returns"
    elif total_return_pct == 0:
        performance_summary = "The strategy broke even"
    else:
        performance_summary = "The strategy generated negative returns"
    
    risk_assessment = ""
    if sharpe_ratio > 1:
        risk_assessment = "excellent risk-adjusted returns"
    elif sharpe_ratio > 0.5:
        risk_assessment = "good risk-adjusted returns"
    elif sharpe_ratio > 0:
        risk_assessment = "moderate risk-adjusted returns"
    else:
        risk_assessment = "poor risk-adjusted returns"
    
    report_lines.append(f"{performance_summary} of **{total_return_pct:.2f}%** over the backtest period. ")
    report_lines.append(f"The strategy achieved a Sharpe ratio of **{sharpe_ratio:.3f}**, indicating {risk_assessment}. ")
    report_lines.append(f"Maximum drawdown was **{max_drawdown_pct:.2f}%**, representing the largest peak-to-trough decline.")
    report_lines.append("")
    
    # Key Performance Metrics
    report_lines.append("## Key Performance Metrics")
    report_lines.append("")
    
    metrics_table = [
        "| Metric | Value |",
        "|--------|-------|",
        f"| Initial Portfolio Value | ${results['initial_value']:,.2f} |",
        f"| Final Portfolio Value | ${results['final_value']:,.2f} |",
        f"| Total Return | {total_return_pct:.2f}% |",
        f"| Sharpe Ratio | {sharpe_ratio:.3f} |",
        f"| Maximum Drawdown | {max_drawdown_pct:.2f}% |",
        f"| Total Trades | {results['total_trades']:,} |",
        f"| Successful Trades | {results['successful_trades']:,} |",
        f"| Failed Trades | {results['failed_trades']:,} |",
        f"| Trade Success Rate | {(results['successful_trades'] / max(results['total_trades'], 1) * 100):.1f}% |"
    ]
    
    report_lines.extend(metrics_table)
    report_lines.append("")
    
    # Portfolio Evolution
    report_lines.append("## Portfolio Evolution")
    report_lines.append("")
    
    if results['portfolio_values'] and results['timestamps']:
        # Create ASCII art equity curve
        report_lines.append("### Equity Curve (ASCII Visualization)")
        report_lines.append("")
        report_lines.append("```")
        
        values = results['portfolio_values']
        width = 60
        height = 15
        
        min_val = min(values)
        max_val = max(values)
        
        if max_val > min_val:
            # Normalize values to fit chart
            normalized = [(val - min_val) / (max_val - min_val) * (height - 1) for val in values]
            
            # Create chart
            chart = [[' ' for _ in range(width)] for _ in range(height)]
            
            for i, norm_val in enumerate(normalized):
                if i < width:
                    y = int(height - 1 - norm_val)
                    chart[y][i] = '*'
            
            # Add chart to report
            for row in chart:
                report_lines.append(''.join(row))
                
            report_lines.append("")
            report_lines.append(f"Min: ${min_val:,.2f} | Max: ${max_val:,.2f}")
        else:
            report_lines.append("Portfolio value remained constant throughout the backtest period.")
        
        report_lines.append("```")
        report_lines.append("")
    
    # Trading Activity Summary
    report_lines.append("## Trading Activity Summary")
    report_lines.append("")
    
    if results['trades']:
        # Analyze trades
        buy_trades = [t for t in results['trades'] if t['action'] == 'buy']
        sell_trades = [t for t in results['trades'] if t['action'] == 'sell']
        
        avg_buy_price = sum(t['price'] for t in buy_trades) / len(buy_trades) if buy_trades else 0
        avg_sell_price = sum(t['price'] for t in sell_trades) / len(sell_trades) if sell_trades else 0
        
        total_volume = sum(t['quantity'] for t in results['trades'])
        
        trading_table = [
            "| Trading Metric | Value |",
            "|----------------|-------|",
            f"| Total Trades | {len(results['trades'])} |",
            f"| Buy Trades | {len(buy_trades)} |",
            f"| Sell Trades | {len(sell_trades)} |",
            f"| Average Buy Price | ${avg_buy_price:.2f} |",
            f"| Average Sell Price | ${avg_sell_price:.2f} |",
            f"| Total Volume | {total_volume:,} shares |"
        ]
        
        report_lines.extend(trading_table)
        report_lines.append("")
        
        # Recent trades (last 10)
        report_lines.append("### Recent Trades (Last 10)")
        report_lines.append("")
        
        recent_trades_table = [
            "| Timestamp | Symbol | Action | Quantity | Price |",
            "|-----------|---------|---------|----------|-------|"
        ]
        
        for trade in results['trades'][-10:]:
            timestamp_str = trade['timestamp'].strftime('%Y-%m-%d %H:%M')
            recent_trades_table.append(
                f"| {timestamp_str} | {trade['symbol']} | {trade['action'].title()} | "
                f"{trade['quantity']} | ${trade['price']:.2f} |"
            )
        
        report_lines.extend(recent_trades_table)
        report_lines.append("")
    
    # Position Summary
    report_lines.append("## Final Position Summary")
    report_lines.append("")
    
    if results['positions']:
        position_table = [
            "| Symbol | Quantity | Avg Price | Unrealized P&L |",
            "|---------|----------|-----------|----------------|"
        ]
        
        for symbol, position in results['positions'].items():
            if position.quantity != 0:
                position_table.append(
                    f"| {symbol} | {position.quantity} | ${position.avg_price:.2f} | "
                    f"${position.unrealized_pnl:.2f} |"
                )
        
        if len(position_table) > 2:
            report_lines.extend(position_table)
        else:
            report_lines.append("No open positions at the end of the backtest period.")
    else:
        report_lines.append("No positions were established during the backtest period.")
    
    report_lines.append("")
    
    # Risk Analysis
    report_lines.append("## Risk Analysis")
    report_lines.append("")
    
    if results['returns']:
        returns = results['returns']
        
        # Calculate additional risk metrics
        positive_returns = [r for r in returns if r > 0]
        negative_returns = [r for r in returns if r < 0]
        
        win_rate = len(positive_returns) / len(returns) * 100 if returns else 0
        avg_positive_return = sum(positive_returns) / len(positive_returns) if positive_returns else 0
        avg_negative_return = sum(negative_returns) / len(negative_returns) if negative_returns else 0
        
        # Volatility
        if len(returns) > 1:
            mean_return = sum(returns) / len(returns)
            variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
            volatility = math.sqrt(variance) * math.sqrt(252) * 100  # Annualized
        else:
            volatility = 0
        
        risk_table = [
            "| Risk Metric | Value |",
            "|-------------|-------|",
            f"| Annualized Volatility | {volatility:.2f}% |",
            f"| Win Rate | {win_rate:.1f}% |",
            f"| Average Positive Return | {avg_positive_return * 100:.3f}% |",
            f"| Average Negative Return | {avg_negative_return * 100:.3f}% |",
            f"| Best Single Period Return | {max(returns) * 100:.3f}% |",
            f"| Worst Single Period Return | {min(returns) * 100:.3f}% |"
        ]
        
        report_lines.extend(risk_table)
        report_lines.append("")
    
    # Error Summary
    if results['errors']:
        report_lines.append("## Error Summary")
        report_lines.append("")
        
        report_lines.append(f"During the backtest, **{len(results['errors'])}** errors were encountered:")
        report_lines.append("")
        
        # Group errors by type
        error_types = {}
        for error in results['errors']:
            error_msg = error['error']
            error_type = error_msg.split(':')[0] if ':' in error_msg else 'Unknown'
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        error_table = [
            "| Error Type | Count |",
            "|------------|-------|"
        ]
        
        for error_type, count in error_types.items():
            error_table.append(f"| {error_type} | {count} |")
        
        report_lines.extend(error_table)
        report_lines.append("")
        
        report_lines.append("The backtesting engine continued processing despite these errors, ")
        report_lines.append("demonstrating robust exception handling capabilities.")
        report_lines.append("")
    
    # Strategic Insights
    report_lines.append("## Strategic Insights and Recommendations")
    report_lines.append("")
    
    # Generate insights based on performance
    insights = []
    
    if total_return_pct > 10:
        insights.append("**Strong Performance**: The strategy delivered significant positive returns.")
    elif total_return_pct > 0:
        insights.append("**Positive Returns**: The strategy generated modest positive returns.")
    else:
        insights.append("**Negative Returns**: The strategy underperformed; consider parameter optimization.")
    
    if sharpe_ratio > 1:
        insights.append("**Excellent Risk-Adjusted Returns**: High Sharpe ratio indicates strong risk management.")
    elif sharpe_ratio > 0.5:
        insights.append("**Good Risk-Adjusted Returns**: Moderate Sharpe ratio shows decent risk management.")
    else:
        insights.append("**Poor Risk-Adjusted Returns**: Consider reducing volatility or improving signal quality.")
    
    if max_drawdown_pct < 10:
        insights.append("**Low Drawdown**: Maximum drawdown is within acceptable limits.")
    elif max_drawdown_pct < 20:
        insights.append("**Moderate Drawdown**: Consider implementing better risk management.")
    else:
        insights.append("**High Drawdown**: Significant capital at risk; review position sizing and stop losses.")
    
    trade_success_rate = results['successful_trades'] / max(results['total_trades'], 1) * 100
    if trade_success_rate > 95:
        insights.append("**High Execution Success**: Most orders were executed successfully.")
    elif trade_success_rate > 90:
        insights.append("**Good Execution Success**: Minimal execution issues encountered.")
    else:
        insights.append("**Execution Issues**: Consider reviewing order validation and market conditions.")
    
    for insight in insights:
        report_lines.append(insight)
        report_lines.append("")
    
    # Recommendations
    recommendations = [
        "### Recommendations for Future Development:",
        "",
        "1. **Parameter Optimization**: Conduct systematic parameter sweeps to find optimal strategy settings.",
        "2. **Risk Management**: Implement position sizing rules and stop-loss mechanisms.",
        "3. **Transaction Costs**: Include more realistic transaction costs and market impact models.",
        "4. **Multiple Assets**: Extend the framework to support multi-asset portfolios.",
        "5. **Walk-Forward Analysis**: Implement out-of-sample testing to validate strategy robustness.",
        "6. **Alternative Strategies**: Explore mean reversion, arbitrage, and machine learning-based approaches."
    ]
    
    report_lines.extend(recommendations)
    report_lines.append("")
    
    # Footer
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("*This report was generated by the CSV-Based Algorithmic Trading Backtester.*")
    report_lines.append(f"*Analysis completed on {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}.*")
    
    # Write report to file
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"Performance report generated: {output_filename}")


def print_summary_stats(results: Dict) -> None:
    """Print a quick summary of backtest results to console."""
    print("\n" + "="*60)
    print("BACKTEST SUMMARY")
    print("="*60)
    
    print(f"Initial Value:    ${results['initial_value']:>15,.2f}")
    print(f"Final Value:      ${results['final_value']:>15,.2f}")
    print(f"Total Return:     {results['total_return']*100:>14.2f}%")
    print(f"Sharpe Ratio:     {results['sharpe_ratio']:>15.3f}")
    print(f"Max Drawdown:     {results['max_drawdown']*100:>14.2f}%")
    print(f"Total Trades:     {results['total_trades']:>15,}")
    print(f"Success Rate:     {(results['successful_trades']/max(results['total_trades'],1)*100):>14.1f}%")
    
    if results['errors']:
        print(f"Errors:           {len(results['errors']):>15,}")
    
    print("="*60)