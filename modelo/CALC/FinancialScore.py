import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import json
from Score import get_all_metrics

class FinancialScoring:
    def __init__(self):
        """Initialize scoring weights and feature configurations"""
        # Dimension weights (must sum to 1.0)
        self.weights = {
            'liquidity': 0.25,
            'stability': 0.20,
            'credit_usage': 0.25,
            'spending_behavior': 0.20,
            'rewards': 0.10
        }
        
        # Feature weights within dimensions
        self.feature_weights = {
            'liquidity': {
                'cash_withdraw_pct': -1.0  # Negative because higher is worse
            },
            'stability': {
                'spend_trend': -1.0  # Negative because rapid increase is worse
            },
            'credit_usage': {
                'credit_risk': -1.0  # Negative because higher risk is worse
            },
            'spending_behavior': {
                'purchase_freq': 0.20,
                'avg_purchase': 0.30,
                'merchant_diversity': 0.50
            },
            'rewards': {
                'rewards_utilization': 1.0
            }
        }

    def normalize_feature(self, values, reverse=False):
        """Normalize values to 0-100 range using min-max scaling"""
        if not values:
            return np.array([])
            
        values_array = np.array(list(values.values())).reshape(-1, 1)
        
        if len(np.unique(values_array)) <= 1:
            return np.full(len(values_array), 0 if reverse else 100)
        
        try:
            scaler = MinMaxScaler(feature_range=(0, 100))
            normalized = scaler.fit_transform(values_array).flatten()
            
            if reverse:
                normalized = 100 - normalized
                
            return normalized
        except ValueError:
            return np.full(len(values_array), 50)

    def calculate_dimension_score(self, metrics, dimension):
        """Calculate score for a single dimension"""
        dimension_score = 0
        total_weight = 0
        weights = self.feature_weights[dimension]
        
        for feature, weight in weights.items():
            if feature in metrics and metrics[feature]:
                values = metrics[feature]
                if values:
                    normalized = self.normalize_feature(values, reverse=weight < 0)
                    if len(normalized) > 0:
                        dimension_score += abs(weight) * np.mean(normalized)
                        total_weight += abs(weight)
        
        return dimension_score / total_weight if total_weight > 0 else 50

    def convert_to_credit_score(self, base_score):
        """
        Convert 0-100 score to 300-850 range using formula:
        credit_score = 300 + (base_score/100 × 550)
        """
        return 300 + ((base_score/100) * 550)  

    def calculate_final_score(self, metrics):
        """Calculate final weighted score and convert to credit score range"""
        dimension_scores = {}
        base_scores = {}
        credit_scores = {}
        
        account_ids = set()
        for feature_values in metrics.values():
            if feature_values:
                account_ids.update(feature_values.keys())
        
        if not account_ids:
            return {}, {}, {}
            
        for account_id in account_ids:
            account_dimension_scores = {}
            total_weight = 0
            weighted_score = 0
            
            for dimension, weight in self.weights.items():
                account_metrics = {
                    k: {account_id: v[account_id]} if account_id in v else {}
                    for k, v in metrics.items()
                }
                
                score = self.calculate_dimension_score(account_metrics, dimension)
                account_dimension_scores[dimension] = score
                
                if score is not None:
                    weighted_score += score * weight
                    total_weight += weight
            
            dimension_scores[account_id] = account_dimension_scores
            base_score = weighted_score / total_weight if total_weight > 0 else 50
            base_scores[account_id] = base_score
            credit_scores[account_id] = self.convert_to_credit_score(base_score)
        
        return dimension_scores, base_scores, credit_scores

def main():
    try:
        # Load accounts data
        with open('./RESPONSE/CreatedAccounts.json') as f:
            accounts_data = json.load(f)
        
        # Create account ID to account number mapping
        account_mapping = {
            account['objectCreated']['_id']: account['objectCreated']['account_number'] 
            for account in accounts_data
        }
        
        # Get metrics and calculate scores
        metrics = get_all_metrics()
        
        if not metrics:
            print("No metrics data available")
            return
        
        scorer = FinancialScoring()
        dimension_scores, base_scores, credit_scores = scorer.calculate_final_score(metrics)
        
        if not base_scores:
            print("No scores could be calculated")
            return
        
        # Create results DataFrame
        results = []
        for account_id in base_scores.keys():
            account_number = account_mapping.get(account_id, "Unknown")
            result = {
                'account_id': account_id,
                'account_number': account_number,
                'base_score': base_scores[account_id],
                'credit_score': credit_scores[account_id]
            }
            
            # Add dimension scores
            for dimension, score in dimension_scores[account_id].items():
                result[f'{dimension}_score'] = score
                
            results.append(result)
        
        # Convert to DataFrame and save to CSV
        df_results = pd.DataFrame(results)
        csv_path = './CSVReports/health_scores.csv'
        df_results.to_csv(csv_path, index=False)
        
        print(f"\n## Score Results saved to {csv_path}")
        print(f"Total accounts processed: {len(results)}")
        
        # Display sample of results
        print("\n## Sample Results (first 5 accounts):")
        print(df_results.head().to_string())
            
    except Exception as e:
        print(f"Error calculating scores: {str(e)}")

if __name__ == "__main__":
    main()