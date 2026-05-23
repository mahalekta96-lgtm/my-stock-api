from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
import os

app = Flask(__name__)
CORS(app)

def get_market_cap_category(market_cap_cr):
    if market_cap_cr >= 1000000:
        return "Large Cap"
    elif market_cap_cr >= 20000:
        return "Mid Cap"
    else:
        return "Small Cap"

@app.route("/stock", methods=["GET"])
def stock():
    symbol = request.args.get("symbol", "").strip()
    if not symbol:
        return jsonify({"success": False, "error": "Please provide a stock symbol"}), 400
    if not symbol.endswith(".NS") and not symbol.endswith(".BO"):
        symbol = symbol.upper() + ".NS"
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        data = {
            "symbol": symbol,
            "name": info.get("longName") or info.get("shortName") or symbol,
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap_cr": round((info.get("marketCap") or 0) / 1e7, 2),
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice") or 0,
            "face_value": info.get("faceValue") or 1,
            "pe_ratio": round(info.get("trailingPE") or 0, 2),
            "forward_pe": round(info.get("forwardPE") or 0, 2),
            "pb_ratio": round(info.get("priceToBook") or 0, 2),
            "eps": round(info.get("trailingEps") or 0, 2),
            "book_value": round(info.get("bookValue") or 0, 2),
            "roe": round((info.get("returnOnEquity") or 0) * 100, 2),
            "roce": round((info.get("returnOnAssets") or 0) * 100, 2),
            "profit_margin": round((info.get("profitMargins") or 0) * 100, 2),
            "operating_margin": round((info.get("operatingMargins") or 0) * 100, 2),
            "debt_to_equity": round((info.get("debtToEquity") or 0) / 100, 2),
            "current_ratio": round(info.get("currentRatio") or 0, 2),
            "total_cash_cr": round((info.get("totalCash") or 0) / 1e7, 2),
            "total_debt_cr": round((info.get("totalDebt") or 0) / 1e7, 2),
            "net_profit_cr": round((info.get("netIncomeToCommon") or 0) / 1e7, 2),
            "revenue_cr": round((info.get("totalRevenue") or 0) / 1e7, 2),
            "free_cashflow_cr": round((info.get("freeCashflow") or 0) / 1e7, 2),
            "promoter_holding": round((info.get("heldPercentInsiders") or 0) * 100, 2),
            "institution_holding": round((info.get("heldPercentInstitutions") or 0) * 100, 2),
            "week_52_high": info.get("fiftyTwoWeekHigh") or 0,
            "week_52_low": info.get("fiftyTwoWeekLow") or 0,
            "dividend_yield": round((info.get("dividendYield") or 0) * 100, 2),
            "beta": round(info.get("beta") or 0, 2),
            "market_cap_category": get_market_cap_category((info.get("marketCap") or 0) / 1e7),
        }
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running", "message": "Stock API is live!"})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Your Personal Stock Analysis API"})

