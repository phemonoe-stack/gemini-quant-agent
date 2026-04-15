import os
import json
from google import genai


class DataAnalysisAgent:
    def __init__(self, config_path):
        """Initializes the agent with a config file and the Gemini client."""
        
        # Load configuration from JSON
        try:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {}
            print(f"Warning: {config_path} not found. Using default settings.")

        # Initialize the Google GenAI Client using the API Key from environment variables
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")

        self.client = genai.Client(api_key=api_key)

        # Target model
        self.model_id = "gemini-3.1-flash-lite-preview"

    def analyze_portfolio(self, open_positions_path, closed_positions_path):
        """Analyze open and closed positions using Gemini as the quant engine."""
        print(f"Analyzing: {open_positions_path} and {closed_positions_path}\n")

        # Read open positions CSV
        try:
            with open(open_positions_path, 'r') as f:
                open_csv = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Open positions CSV not found: {open_positions_path}")

        # Read closed positions CSV
        try:
            with open(closed_positions_path, 'r') as f:
                closed_csv = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Closed positions CSV not found: {closed_positions_path}")

        prompt = f"""
You are a quantitative trading and risk analysis agent.

You are given two CSV datasets as raw text. 
Do NOT assume fixed column names; instead, infer the meaning of each column from its header and values.

OPEN POSITIONS CSV (current holdings):
[OPEN_CSV_START]
{open_csv}
[OPEN_CSV_END]

CLOSED POSITIONS CSV (historical trades):
[CLOSED_CSV_START]
{closed_csv}
[CLOSED_CSV_END]

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

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )

        print(response.text)
        return response.text


def main():
    """Main execution function."""
    print("\nGEMINI PORTFOLIO QUANT AGENT\n")

    if not os.getenv('GEMINI_API_KEY'):
        print("ERROR: GEMINI_API_KEY environment variable not set.\n")
        print("To fix this:")
        print("Windows (CMD):   set GEMINI_API_KEY=your-api-key-here")
        print("Linux/Mac:       export GEMINI_API_KEY='your-api-key-here'")
        return

    try:
        agent = DataAnalysisAgent('agent_config.json')
        agent.analyze_portfolio('Positions.csv', 'closed2026.csv')

    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        print("Ensure 'Positions.csv', 'ClosedPositions.csv', and 'agent_config.json' are in this folder.")

    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Run: pip install google-genai")
        print("2. Verify your API key is valid.")


if __name__ == "__main__":
    main()
