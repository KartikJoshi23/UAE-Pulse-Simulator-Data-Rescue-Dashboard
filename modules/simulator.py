"""
Simulator Module for UAE Pulse Dashboard
Campaign simulation and KPI calculations
"""

import pandas as pd
import numpy as np

class Simulator:
    """Campaign simulator with KPI calculations."""
    
    def __init__(self):
        """Initialize simulator with default elasticity values."""
        self.category_elasticity = {
            'Electronics': 1.8,
            'Fashion': 2.0,
            'Grocery': 1.2,
            'Beauty': 1.6,
            'Home': 1.4,
            'Sports': 1.7
        }
        self.default_elasticity = 1.5
    
    def calculate_overall_kpis(self, sales_df, products_df):
        """Calculate overall KPIs from sales data."""
        kpis = {}
        
        try:
            # Merge with products for cost data
            merged = sales_df.merge(products_df[['sku', 'cost_aed']], on='sku', how='left')
            merged['cost_aed'] = merged['cost_aed'].fillna(0)
            
            # Ensure numeric columns
            merged['qty'] = pd.to_numeric(merged['qty'], errors='coerce').fillna(0)
            merged['selling_price_aed'] = pd.to_numeric(merged['selling_price_aed'], errors='coerce').fillna(0)
            merged['cost_aed'] = pd.to_numeric(merged['cost_aed'], errors='coerce').fillna(0)
            
            # Calculate revenue and profit
            merged['revenue'] = merged['qty'] * merged['selling_price_aed']
            merged['profit'] = merged['qty'] * (merged['selling_price_aed'] - merged['cost_aed'])
            
            kpis['total_revenue'] = float(merged['revenue'].sum())
            kpis['total_profit'] = float(merged['profit'].sum())
            kpis['total_orders'] = int(merged['order_id'].nunique()) if 'order_id' in merged.columns else len(merged)
            kpis['total_units'] = float(merged['qty'].sum())
            kpis['avg_order_value'] = kpis['total_revenue'] / kpis['total_orders'] if kpis['total_orders'] > 0 else 0
            kpis['profit_margin_pct'] = (kpis['total_profit'] / kpis['total_revenue'] * 100) if kpis['total_revenue'] > 0 else 0
            
            # Return rate
            if 'is_returned' in sales_df.columns:
                try:
                    returned = pd.to_numeric(sales_df['is_returned'], errors='coerce').fillna(0)
                    kpis['return_rate_pct'] = float(returned.mean() * 100)
                except:
                    kpis['return_rate_pct'] = 0
            else:
                kpis['return_rate_pct'] = 0
            
            # Discount
            if 'discount_pct' in sales_df.columns:
                try:
                    discount = pd.to_numeric(sales_df['discount_pct'], errors='coerce').fillna(0)
                    kpis['avg_discount_pct'] = float(discount.mean())
                except:
                    kpis['avg_discount_pct'] = 0
            else:
                kpis['avg_discount_pct'] = 0
                
        except Exception as e:
            kpis = {
                'total_revenue': 0,
                'total_profit': 0,
                'total_orders': 0,
                'total_units': 0,
                'avg_order_value': 0,
                'profit_margin_pct': 0,
                'return_rate_pct': 0,
                'avg_discount_pct': 0
            }
        
        return kpis
    
    def calculate_kpis_by_dimension(self, sales_df, stores_df, products_df, dimension):
        """Calculate KPIs grouped by a dimension (city, channel, category)."""
        try:
            # Merge data
            merged = sales_df.merge(stores_df[['store_id', 'city', 'channel']], on='store_id', how='left')
            merged = merged.merge(products_df[['sku', 'cost_aed', 'category']], on='sku', how='left')
            
            # Ensure numeric
            merged['qty'] = pd.to_numeric(merged['qty'], errors='coerce').fillna(0)
            merged['selling_price_aed'] = pd.to_numeric(merged['selling_price_aed'], errors='coerce').fillna(0)
            merged['cost_aed'] = pd.to_numeric(merged['cost_aed'], errors='coerce').fillna(0)
            
            merged['revenue'] = merged['qty'] * merged['selling_price_aed']
            merged['profit'] = merged['qty'] * (merged['selling_price_aed'] - merged['cost_aed'])
            
            # Group by dimension
            grouped = merged.groupby(dimension).agg({
                'revenue': 'sum',
                'profit': 'sum',
                'order_id': 'nunique',
                'qty': 'sum'
            }).reset_index()
            
            grouped.columns = [dimension, 'revenue', 'profit', 'orders', 'units']
            grouped['avg_order_value'] = grouped['revenue'] / grouped['orders']
            grouped['profit_margin_pct'] = (grouped['profit'] / grouped['revenue'] * 100).fillna(0)
            grouped = grouped.sort_values('revenue', ascending=False)
            
            return grouped
            
        except Exception as e:
            return pd.DataFrame()
    
   def calculate_daily_trends(self, sales_df, products_df):
    """Calculate daily performance trends."""
    try:
        merged = sales_df.copy()
        merged = merged.merge(products_df[['sku', 'cost_aed']], on='sku', how='left')
        merged['cost_aed'] = pd.to_numeric(merged['cost_aed'], errors='coerce').fillna(0)
        
        # Ensure numeric
        merged['qty'] = pd.to_numeric(merged['qty'], errors='coerce').fillna(0)
        merged['selling_price_aed'] = pd.to_numeric(merged['selling_price_aed'], errors='coerce').fillna(0)
        
        merged['revenue'] = merged['qty'] * merged['selling_price_aed']
        merged['profit'] = merged['qty'] * (merged['selling_price_aed'] - merged['cost_aed'])
        
        # Parse date - try multiple columns
        date_col = None
        if 'order_ts' in merged.columns:
            date_col = 'order_ts'
        elif 'order_date' in merged.columns:
            date_col = 'order_date'
        elif 'date' in merged.columns:
            date_col = 'date'
        elif 'timestamp' in merged.columns:
            date_col = 'timestamp'
        
        if date_col is None:
            # Create dummy dates if no date column exists
            merged['date'] = pd.date_range(end=pd.Timestamp.today(), periods=len(merged), freq='H').date
        else:
            merged['date'] = pd.to_datetime(merged[date_col], errors='coerce').dt.date
        
        # Remove rows with invalid dates
        merged = merged.dropna(subset=['date'])
        
        if len(merged) == 0:
            return pd.DataFrame(columns=['date', 'revenue', 'profit', 'orders', 'units'])
        
        # Group by date
        daily = merged.groupby('date').agg({
            'revenue': 'sum',
            'profit': 'sum',
            'qty': 'sum'
        }).reset_index()
        
        # Count orders
        if 'order_id' in merged.columns:
            orders_per_day = merged.groupby('date')['order_id'].nunique().reset_index()
            orders_per_day.columns = ['date', 'orders']
            daily = daily.merge(orders_per_day, on='date', how='left')
        else:
            daily['orders'] = daily['qty']
        
        daily.columns = ['date', 'revenue', 'profit', 'units', 'orders']
        daily = daily.sort_values('date')
        
        return daily
        
    except Exception as e:
        print(f"Error in calculate_daily_trends: {e}")
        return pd.DataFrame(columns=['date', 'revenue', 'profit', 'orders', 'units'])
    
    def calculate_stockout_risk(self, inventory_df):
        """Calculate stockout risk metrics."""
        try:
            inventory_df['stock_on_hand'] = pd.to_numeric(inventory_df['stock_on_hand'], errors='coerce').fillna(0)
            
            if 'reorder_point' in inventory_df.columns:
                inventory_df['reorder_point'] = pd.to_numeric(inventory_df['reorder_point'], errors='coerce').fillna(10)
            else:
                inventory_df['reorder_point'] = 10
            
            total_items = len(inventory_df)
            zero_stock = len(inventory_df[inventory_df['stock_on_hand'] == 0])
            low_stock = len(inventory_df[inventory_df['stock_on_hand'] <= inventory_df['reorder_point']])
            
            return {
                'total_items': total_items,
                'zero_stock': zero_stock,
                'low_stock': low_stock,
                'stockout_risk_pct': (low_stock / total_items * 100) if total_items > 0 else 0
            }
        except:
            return {
                'total_items': 0,
                'zero_stock': 0,
                'low_stock': 0,
                'stockout_risk_pct': 0
            }
    
    def simulate_campaign(self, sales_df, stores_df, products_df, 
                          discount_pct=10, promo_budget=10000, margin_floor=15,
                          city='All', channel='All', category='All', campaign_days=7):
        """Simulate a promotional campaign."""
        try:
            # Merge data
            merged = sales_df.merge(stores_df[['store_id', 'city', 'channel']], on='store_id', how='left')
            merged = merged.merge(products_df[['sku', 'cost_aed', 'category']], on='sku', how='left')
            
            # Ensure numeric
            merged['qty'] = pd.to_numeric(merged['qty'], errors='coerce').fillna(0)
            merged['selling_price_aed'] = pd.to_numeric(merged['selling_price_aed'], errors='coerce').fillna(0)
            merged['cost_aed'] = pd.to_numeric(merged['cost_aed'], errors='coerce').fillna(0)
            
            # Filter by targeting
            if city != 'All':
                merged = merged[merged['city'] == city]
            if channel != 'All':
                merged = merged[merged['channel'] == channel]
            if category != 'All':
                merged = merged[merged['category'] == category]
            
            if len(merged) == 0:
                return {'outputs': None, 'comparison': None, 'warnings': ['No data matches the selected filters']}
            
            # Baseline metrics
            merged['revenue'] = merged['qty'] * merged['selling_price_aed']
            merged['profit'] = merged['qty'] * (merged['selling_price_aed'] - merged['cost_aed'])
            
            # Calculate baseline per day (assume data spans 30 days)
            data_days = 30
            baseline_revenue = merged['revenue'].sum() / data_days * campaign_days
            baseline_profit = merged['profit'].sum() / data_days * campaign_days
            baseline_orders = merged['order_id'].nunique() / data_days * campaign_days
            baseline_units = merged['qty'].sum() / data_days * campaign_days
            
            # Get elasticity for category
            if category != 'All':
                elasticity = self.category_elasticity.get(category, self.default_elasticity)
            else:
                elasticity = self.default_elasticity
            
            # Calculate demand lift
            demand_lift_pct = discount_pct * elasticity
            
            # Campaign projections
            expected_units = baseline_units * (1 + demand_lift_pct / 100)
            avg_price = merged['selling_price_aed'].mean()
            avg_cost = merged['cost_aed'].mean()
            
            discounted_price = avg_price * (1 - discount_pct / 100)
            expected_revenue = expected_units * discounted_price
            
            # Costs
            promo_cost = min(promo_budget, expected_revenue * 0.1)  # Cap at 10% of revenue
            fulfillment_cost = expected_units * 2  # AED 2 per unit
            cogs = expected_units * avg_cost
            
            # Profit calculation
            expected_gross_profit = expected_revenue - cogs
            expected_net_profit = expected_gross_profit - promo_cost - fulfillment_cost
            expected_margin_pct = (expected_net_profit / expected_revenue * 100) if expected_revenue > 0 else 0
            
            # ROI
            total_investment = promo_cost + fulfillment_cost
            roi_pct = ((expected_net_profit - baseline_profit) / total_investment * 100) if total_investment > 0 else 0
            
            # Warnings
            warnings = []
            if expected_margin_pct < margin_floor:
                warnings.append(f"Margin ({expected_margin_pct:.1f}%) is below floor ({margin_floor}%)")
            if roi_pct < 0:
                warnings.append(f"Negative ROI expected ({roi_pct:.1f}%)")
            if discount_pct > 30:
                warnings.append("High discount may erode brand value")
            
            outputs = {
                'expected_revenue': expected_revenue,
                'expected_orders': int(baseline_orders * (1 + demand_lift_pct / 100)),
                'expected_units': expected_units,
                'expected_net_profit': expected_net_profit,
                'expected_margin_pct': expected_margin_pct,
                'demand_lift_pct': demand_lift_pct,
                'roi_pct': roi_pct,
                'promo_cost': promo_cost,
                'fulfillment_cost': fulfillment_cost
            }
            
            comparison = {
                'baseline_revenue': baseline_revenue,
                'baseline_profit': baseline_profit,
                'baseline_orders': int(baseline_orders),
                'revenue_change_pct': ((expected_revenue - baseline_revenue) / baseline_revenue * 100) if baseline_revenue > 0 else 0,
                'profit_change_pct': ((expected_net_profit - baseline_profit) / baseline_profit * 100) if baseline_profit > 0 else 0,
                'order_change_pct': demand_lift_pct
            }
            
            return {
                'outputs': outputs,
                'comparison': comparison,
                'warnings': warnings
            }
            
        except Exception as e:
            return {
                'outputs': None,
                'comparison': None,
                'warnings': [f'Simulation error: {str(e)}']
            }
