# gemini-quant-agent
Gemini Quantitative Analysis Agent v0.15

Set your Gemini API key first. Depending on your system.

$env:GEMINI_API_KEY='your-api-key-here' 
export GEMINI_API_KEY='your-api-key-here' 
set GEMINI_API_KEY='your-api-key-here'

The original code came from https://www.codecademy.com/article/how-to-build-ai-agents-with-gemini-3
Alot of this is depreciated and what not, but I had Copilot clean it up. :D

Make sure all your files are in the same directory. The code can be tweaked to anything really, the original code was for sales data, I just jammed in my Fidelity .csv and it started working. Then manipulated the code a little bit to include more quant metrics and closed positions.

Gemini's instructions:
Your tasks:

1. **Infer Schema**
   - Identify what each column likely represents (e.g., symbol, quantity, entry price, exit price, side, dates, realized PnL, etc.).
   - If explicit PnL or return columns are missing, compute them using whatever fields are available
     (for example: PnL ≈ (exit - entry) * quantity, return ≈ (exit - entry) / entry).

2. **Risk & Performance Metrics (Closed Positions)**
   - Total number of trades
   - Win rate
   - Average win and average loss
   - Profit factor
   - Expectancy (average PnL per trade)
   - Equity curve over time (based on cumulative PnL)
   - Maximum drawdown (absolute and percentage)
   - Volatility of returns (annualized if possible)
   - Sharpe ratio
   - Sortino ratio
   - Any notable streaks (winning or losing)

3. **Open Positions Analysis**
   - Current exposure by symbol, sector, or asset type (if inferable)
   - Concentration risk (e.g., overexposed to a single name or theme)
   - Unrealized PnL and key risk points (e.g., large losers, outsized positions)

4. **Combined Portfolio View**
   - Realized vs unrealized PnL
   - Overall performance profile
   - Risk/return tradeoff
   - Any obvious structural issues (e.g., oversized bets, poor reward-to-risk, skewed distribution)

5. **Classic Quant Commentary**
   - Provide a concise, professional-style quant summary:
     - What kind of strategy this looks like (trend, mean reversion, discretionary, etc., if inferable)
     - Strengths and weaknesses
     - How robust the edge appears (based on metrics)
     - How painful the drawdowns are relative to returns

6. **Actionable Recommendations**
   - Numbered list of concrete improvements:
     - Risk management
     - Position sizing
     - Trade selection
     - Possible filters or rules to test

Important:
- You may internally imagine using Python, pandas, and numpy to compute metrics, but DO NOT show any code.
- Only output human-readable tables, metrics, and commentary.
- If something cannot be computed reliably due to missing data, say so explicitly and explain what would be needed.
"""

