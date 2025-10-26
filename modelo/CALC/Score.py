import pandas as pd
import numpy as np
from datetime import datetime
import json
from sklearn.linear_model import LinearRegression

def calculate_cash_withdraw_pct():
    """
    CashWithdrawPct = sum(amount_withdrawals) / sum(amount_total_outflows)
    """
    # Load withdrawals
    with open('./RESPONSE/CreatedWithdrawals.json') as f:
        withdrawals = json.load(f)
    
    # Load purchases (other outflows)
    with open('./RESPONSE/CreatedPurchases.json') as f:
        purchases = json.load(f)

    # Process withdrawals
    df_withdrawals = pd.json_normalize(withdrawals)
    total_withdrawals = df_withdrawals.groupby('account_id')['withdrawal.objectCreated.amount'].sum()

    # Process purchases
    df_purchases = pd.json_normalize(purchases)
    total_purchases = df_purchases.groupby('objectCreated.payer_id')['objectCreated.amount'].sum()

    # Calculate ratio
    cash_withdraw_pct = {}
    for account in total_withdrawals.index:
        total_outflows = total_withdrawals[account]
        if account in total_purchases.index:
            total_outflows += total_purchases[account]
        cash_withdraw_pct[account] = total_withdrawals[account] / total_outflows

    return cash_withdraw_pct

def calculate_purchase_metrics():
    """
    PurchaseFreq = mean(number_of_purchases_per_month)
    AvgPurchase = mean(amount_per_purchase)
    """
    with open('./RESPONSE/CreatedPurchases.json') as f:
        purchases = json.load(f)
    
    df = pd.json_normalize(purchases)
    df['purchase_date'] = pd.to_datetime(df['objectCreated.purchase_date'])
    df['month'] = df['purchase_date'].dt.to_period('M')
    
    # Calculate frequency
    purchase_freq = df.groupby(['objectCreated.payer_id', 'month']).size().groupby('objectCreated.payer_id').mean()
    
    # Calculate average purchase amount
    avg_purchase = df.groupby('objectCreated.payer_id')['objectCreated.amount'].mean()
    
    return purchase_freq.to_dict(), avg_purchase.to_dict()

def calculate_merchant_diversity():
    """
    MerchantDiversity = unique categories / total transactions
    """
    with open('./RESPONSE/CreatedPurchases.json') as f:
        purchases = json.load(f)
    
    with open('./RESPONSE/CreatedMerchants.json') as f:
        merchants = json.load(f)

    df_purchases = pd.json_normalize(purchases)
    df_merchants = pd.json_normalize(merchants)
    
    # Create merchant category mapping
    merchant_categories = {m['objectCreated']['_id']: m['objectCreated']['category'] for m in merchants}
    
    # Add category to purchases
    df_purchases['category'] = df_purchases['objectCreated.merchant_id'].map(merchant_categories)
    
    # Calculate diversity
    diversity = {}
    for payer_id in df_purchases['objectCreated.payer_id'].unique():
        payer_purchases = df_purchases[df_purchases['objectCreated.payer_id'] == payer_id]
        unique_categories = len(payer_purchases['category'].unique())
        total_transactions = len(payer_purchases)
        diversity[payer_id] = unique_categories / total_transactions if total_transactions > 0 else 0
    
    return diversity

def calculate_rewards_utilization():
    """
    RewardsUtilization based on account rewards as proxy
    """
    with open('./RESPONSE/CreatedAccounts.json') as f:
        accounts = json.load(f)
    
    df = pd.json_normalize(accounts)
    rewards_util = df[df['objectCreated.type'] == 'Credit Card'].set_index('objectCreated._id')['objectCreated.rewards'].to_dict()
    
    return rewards_util

def calculate_credit_risk():
    """
    CreditRiskProxy using balance/avg monthly spending
    """
    with open('./RESPONSE/CreatedAccounts.json') as f:
        accounts = json.load(f)
    
    with open('./RESPONSE/CreatedPurchases.json') as f:
        purchases = json.load(f)
        
    df_accounts = pd.json_normalize(accounts)
    df_purchases = pd.json_normalize(purchases)
    
    # Calculate average monthly spending
    df_purchases['month'] = pd.to_datetime(df_purchases['objectCreated.purchase_date']).dt.to_period('M')
    monthly_spending = df_purchases.groupby(['objectCreated.payer_id', 'month'])['objectCreated.amount'].sum().groupby('objectCreated.payer_id').mean()
    
    # Calculate risk proxy
    credit_risk = {}
    credit_accounts = df_accounts[df_accounts['objectCreated.type'] == 'Credit Card']
    
    for _, account in credit_accounts.iterrows():
        account_id = account['objectCreated._id']
        balance = account['objectCreated.balance']
        if account_id in monthly_spending.index:
            avg_spending = monthly_spending[account_id]
            credit_risk[account_id] = balance / avg_spending if avg_spending > 0 else float('inf')
            
    return credit_risk

def calculate_spend_trend():
    """
    SpendTrend using linear regression on monthly spending
    """
    with open('./RESPONSE/CreatedPurchases.json') as f:
        purchases = json.load(f)
    
    df = pd.json_normalize(purchases)
    df['month'] = pd.to_datetime(df['objectCreated.purchase_date']).dt.to_period('M')
    monthly_spend = df.groupby(['objectCreated.payer_id', 'month'])['objectCreated.amount'].sum().reset_index()
    
    trends = {}
    for payer_id in monthly_spend['objectCreated.payer_id'].unique():
        payer_data = monthly_spend[monthly_spend['objectCreated.payer_id'] == payer_id]
        if len(payer_data) > 1:
            X = np.arange(len(payer_data)).reshape(-1, 1)
            y = payer_data['objectCreated.amount'].values
            reg = LinearRegression().fit(X, y)
            trends[payer_id] = reg.coef_[0]
        else:
            trends[payer_id] = 0
            
    return trends

def get_all_metrics():
    """
    Calculate and return all metrics in a single dictionary
    """
    metrics = {
        'cash_withdraw_pct': calculate_cash_withdraw_pct(),
        'purchase_freq': calculate_purchase_metrics()[0],
        'avg_purchase': calculate_purchase_metrics()[1],
        'merchant_diversity': calculate_merchant_diversity(),
        'rewards_utilization': calculate_rewards_utilization(),
        'credit_risk': calculate_credit_risk(),
        'spend_trend': calculate_spend_trend()
    }
    
    return metrics

if __name__ == "__main__":
    metrics = get_all_metrics()
    print(json.dumps(metrics, indent=2))