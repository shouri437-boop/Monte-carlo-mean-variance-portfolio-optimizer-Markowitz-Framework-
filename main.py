

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
'''get the data from yfinance'''

sym = ['AMZN','NVDA','AAPL','JPM']
start_date = "2019-01-01"
end_date   = "2024-01-01"
data = yf.download(sym,start = start_date,end = end_date,auto_adjust = True)

prices = data["Close"]
prices = prices[sym]


'''calculate returns'''
returns = prices.pct_change()
returns = returns.dropna()


trading_days = 252

mean_returns = returns.mean() * trading_days
cov_matrix = returns.cov() * trading_days
'''make covariance matrix and simulations starts now'''
'''phase 2'''
num_portfolio = 10000
portfolio_risks = []
portfolio_returns = []
portfolio_sharpes = []
portfolio_weights = []
for _ in range(num_portfolio):
    weights = np.random.random(len(sym))

    weights = weights/np.sum(weights)

    port_return = np.dot(weights,mean_returns)

    port_variance = weights.T @ cov_matrix @ weights

    port_risk = np.sqrt(port_variance)

    sharpe = port_return / port_risk

    portfolio_risks.append(port_risk)
    portfolio_returns.append(port_return)
    portfolio_sharpes.append(sharpe)
    portfolio_weights.append(weights)
portfolio_returns = np.array(portfolio_returns)
portfolio_risks = np.array(portfolio_risks)
portfolio_sharpes = np.array(portfolio_sharpes)


max_sharpe_index = np.argmax(portfolio_sharpes)
min_risk_index = np.argmin(portfolio_risks)


optimal_return = portfolio_returns[max_sharpe_index]
optimal_risk = portfolio_risks[max_sharpe_index]
optimal_weights = portfolio_weights[max_sharpe_index]

max_sharpe_return = portfolio_returns[max_sharpe_index]
max_sharpe_risk = portfolio_risks[max_sharpe_index]
min_risk_return = portfolio_returns[min_risk_index]
min_risk_risk = portfolio_risks[min_risk_index]

plt.figure(figsize=(10,6))

plt.scatter(
    portfolio_risks,
    portfolio_returns,
    c = portfolio_sharpes,
    cmap="viridis",
    alpha=0.6
)
#max sharpe
plt.scatter(
    max_sharpe_risk,
    max_sharpe_return,
    color = "red",
    marker="*",
    s = 200,
    label = "max sharpe"
)
# min risk
plt.scatter(
    min_risk_risk,
    min_risk_return,
    color="blue",
    marker="o",
    s=150,
    label="Min Risk"
)

plt.xlabel("Risk (Standard Deviation)")
plt.ylabel("Expected Return")
plt.title("Efficient Frontier")
plt.colorbar(label="Sharpe Ratio")
plt.legend()
plt.show()

print("Maximum Sharpe Portfolio Weights:")
for i,ticker in enumerate(sym):
    print(f"{ticker}:{optimal_weights[i]:.4f}")

print("\nExpected Return:", max_sharpe_return)
print("Expected Risk:", max_sharpe_risk)
print("Sharpe Ratio:", portfolio_sharpes[max_sharpe_index])
print(prices.columns)
print("Annual mean returns:")
print(mean_returns)

