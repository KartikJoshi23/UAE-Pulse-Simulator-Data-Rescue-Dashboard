# ============================================================================
# UAE Pulse Simulator + Data Rescue Dashboard
# Simulator Module - KPI Calculator & What-If Engine
# ============================================================================

import pandas as pd
import numpy as np
from .utils import SIMULATOR_CONFIG

# ============================================================================
# SIMULATOR CLASS
# ============================================================================

class Simulator:
    """
    KPI Calculator and What-If Campaign Simulation Engine.
    """
    
    def __init__(self):
        """Initialize the simulator with configuration."""
        self.config = SIMULATOR_CONFIG
    
    # ========================================================================
    # KPI CALCULATOR FUNCTIONS
    # ========================================================================
    
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
        """
        Calculate KPIs grouped by a dimension (city, channel, category).
        
        Args:
            sales_df: Sales DataFrame
            stores_df: Stores DataFrame
            products_df: Products DataFrame
            dimension: Column name to group by ('city', 'channel', 'category')
        
        Returns: DataFrame with KPIs per dimension value
        """
        # Merge data
        merged = sales_df.copy()
        
        if dimension in ['city', 'channel'] and stores_df is not None:
            merged = merged.merge(stores_df[['store_id', 'city', 'channel']], on='store_id', how='left')
        
        if dimension == 'category' and products_df is not None:
            merged = merged.merge(products_df[['product_id', 'category']], on='product_id', how='left')
        
        if products_df is not None:
            merged = merged.merge(products_df[['product_id', 'unit_cost_aed']], on='product_id', how='left')
            merged['line_revenue'] = merged['qty'] * merged['selling_price_aed']
            merged['line_cost'] = merged['qty'] * merged['unit_cost_aed']
            merged['line_profit'] = merged['line_revenue'] - merged['line_cost']
        else:
            merged['line_revenue'] = merged['qty'] * merged['selling_price_aed']
            merged['line_cost'] = 0
            merged['line_profit'] = merged['line_revenue']
        
        if dimension not in merged.columns:
            return pd.DataFrame()
        
        # Group by dimension
        grouped = merged.groupby(dimension).agg({
            'line_revenue': 'sum',
            'line_cost': 'sum',
            'line_profit': 'sum',
            'order_id': 'nunique',
            'qty': 'sum'
        }).reset_index()
        
        grouped.columns = [dimension, 'revenue', 'cost', 'profit', 'orders', 'units']
        
        # Calculate derived metrics
        grouped['profit_margin_pct'] = (grouped['profit'] / grouped['revenue'] * 100).round(2)
        grouped['avg_order_value'] = (grouped['revenue'] / grouped['orders']).round(2)
        
        # Sort by revenue descending
        grouped = grouped.sort_values('revenue', ascending=False)
        
        return grouped
    
    def calculate_stockout_risk(self, inventory_df):
        """
        Calculate stockout risk from inventory data.
        
        Returns: Dictionary with stockout metrics
        """
        if inventory_df is None or len(inventory_df) == 0:
            return {
                'total_items': 0,
                'below_reorder_point': 0,
                'zero_stock': 0,
                'stockout_risk_pct': 0,
                'critical_stockout_pct': 0
            }
        
        # Items below reorder point
        if 'stock_on_hand' in inventory_df.columns and 'reorder_point' in inventory_df.columns:
            below_reorder = inventory_df[inventory_df['stock_on_hand'] <= inventory_df['reorder_point']]
            zero_stock = inventory_df[inventory_df['stock_on_hand'] == 0]
        else:
            below_reorder = pd.DataFrame()
            zero_stock = pd.DataFrame()
        
        metrics = {
            'total_items': len(inventory_df),
            'below_reorder_point': len(below_reorder),
            'zero_stock': len(zero_stock),
            'stockout_risk_pct': (len(below_reorder) / len(inventory_df) * 100) if len(inventory_df) > 0 else 0,
            'critical_stockout_pct': (len(zero_stock) / len(inventory_df) * 100) if len(inventory_df) > 0 else 0
        }
        
        return metrics
    
    def calculate_daily_trends(self, sales_df, products_df=None):
        """
        Calculate daily revenue and order trends.
        
        Returns: DataFrame with daily metrics
        """
        data = sales_df.copy()
        
        # Extract date from order_time
        data['order_date'] = pd.to_datetime(data['order_time'], errors='coerce').dt.date
        
        # Calculate revenue
        if products_df is not None:
            data = data.merge(products_df[['product_id', 'unit_cost_aed']], on='product_id', how='left')
            data['line_revenue'] = data['qty'] * data['selling_price_aed']
            data['line_profit'] = data['line_revenue'] - (data['qty'] * data['unit_cost_aed'])
        else:
            data['line_revenue'] = data['qty'] * data['selling_price_aed']
            data['line_profit'] = data['line_revenue']
        
        daily = data.groupby('order_date').agg({
            'line_revenue': 'sum',
            'line_profit': 'sum',
            'order_id': 'nunique',
            'qty': 'sum'
        }).reset_index()
        
        daily.columns = ['date', 'revenue', 'profit', 'orders', 'units']
        daily['date'] = pd.to_datetime(daily['date'])
        daily = daily.sort_values('date')
        
        return daily
    
    # ========================================================================
    # WHAT-IF SIMULATION FUNCTIONS
    # ========================================================================
    
    def calculate_demand_lift(self, discount_pct, category='All', channel='All', city='All'):
        """
        Calculate expected demand lift based on campaign parameters.
        
        Returns: Demand lift multiplier (e.g., 1.15 = 15% increase)
        """
        config = self.config
        
        # Base lift from discount
        base_lift = discount_pct * config['discount_impact']['base_lift_per_percent']
        
        # Apply diminishing returns
        diminishing = config['discount_impact']['diminishing_factor'] ** (discount_pct / 10)
        adjusted_lift = base_lift * diminishing
        
        # Cap at maximum lift
        adjusted_lift = min(adjusted_lift, config['discount_impact']['max_lift'])
        
        # Apply category elasticity
        if category != 'All' and category in config['category_elasticity']:
            adjusted_lift *= config['category_elasticity'][category]
        
        # Apply channel multiplier
        if channel != 'All' and channel in config['channel_multipliers']:
            adjusted_lift *= config['channel_multipliers'][channel]
        
        return 1 + adjusted_lift
    
    def filter_campaign_data(self, sales_df, stores_df, products_df, 
                              city='All', channel='All', category='All'):
        """
        Filter and merge data based on campaign targeting.
        
        Returns: Filtered DataFrame with all necessary columns
        """
        # Start with sales
        filtered = sales_df.copy()
        
        # Merge with stores
        if stores_df is not None:
            filtered = filtered.merge(
                stores_df[['store_id', 'city', 'channel']], 
                on='store_id', 
                how='left'
            )
        
        # Merge with products
        if products_df is not None:
            filtered = filtered.merge(
                products_df[['product_id', 'category', 'unit_cost_aed']], 
                on='product_id', 
                how='left'
            )
        
        # Apply filters
        if city != 'All' and 'city' in filtered.columns:
            filtered = filtered[filtered['city'] == city]
        
        if channel != 'All' and 'channel' in filtered.columns:
            filtered = filtered[filtered['channel'] == channel]
        
        if category != 'All' and 'category' in filtered.columns:
            filtered = filtered[filtered['category'] == category]
        
        return filtered
    
    def simulate_campaign(self, sales_df, stores_df, products_df,
                          discount_pct, promo_budget, margin_floor,
                          city='All', channel='All', category='All',
                          campaign_days=7):
        """
        Simulate a promotional campaign and calculate expected outcomes.
        
        Returns: Dictionary with simulation results
        """
        results = {
            'inputs': {
                'discount_pct': discount_pct,
                'promo_budget': promo_budget,
                'margin_floor': margin_floor,
                'city': city,
                'channel': channel,
                'category': category,
                'campaign_days': campaign_days
            },
            'outputs': {},
            'comparison': {},
            'warnings': []
        }
        
        # Filter data for campaign scope
        campaign_data = self.filter_campaign_data(
            sales_df, stores_df, products_df,
            city, channel, category
        )
        
        if len(campaign_data) == 0:
            results['warnings'].append("No data matches the selected filters!")
            return results
        
        # Calculate baseline metrics (daily average)
        campaign_data['order_date'] = pd.to_datetime(campaign_data['order_time'], errors='coerce').dt.date
        valid_data = campaign_data.dropna(subset=['order_date'])
        
        if len(valid_data) == 0:
            results['warnings'].append("No valid dates in filtered data!")
            return results
        
        total_days = valid_data['order_date'].nunique()
        
        if total_days == 0:
            results['warnings'].append("Cannot calculate daily averages!")
            return results
        
        # Calculate line-level metrics
        valid_data = valid_data.copy()
        valid_data['line_revenue'] = valid_data['qty'] * valid_data['selling_price_aed']
        if 'unit_cost_aed' in valid_data.columns:
            valid_data['line_cost'] = valid_data['qty'] * valid_data['unit_cost_aed']
            valid_data['line_profit'] = valid_data['line_revenue'] - valid_data['line_cost']
        else:
            valid_data['line_cost'] = 0
            valid_data['line_profit'] = valid_data['line_revenue']
        
        daily_avg_revenue = valid_data['line_revenue'].sum() / total_days
        daily_avg_orders = valid_data['order_id'].nunique() / total_days
        daily_avg_profit = valid_data['line_profit'].sum() / total_days
        
        # Calculate demand lift
        demand_lift = self.calculate_demand_lift(discount_pct, category, channel, city)
        
        # Simulate campaign period
        expected_daily_orders = daily_avg_orders * demand_lift
        expected_total_orders = expected_daily_orders * campaign_days
        
        # Revenue impact
        avg_selling_price = valid_data['selling_price_aed'].mean()
        discounted_price = avg_selling_price * (1 - discount_pct / 100)
        avg_qty_per_order = valid_data['qty'].mean()
        
        expected_daily_revenue = expected_daily_orders * discounted_price * avg_qty_per_order
        expected_total_revenue = expected_daily_revenue * campaign_days
        
        # Cost calculation
        avg_cost_per_unit = valid_data['unit_cost_aed'].mean() if 'unit_cost_aed' in valid_data.columns else 0
        expected_total_cost = expected_total_orders * avg_cost_per_unit * avg_qty_per_order
        
        # Fulfillment cost
        fulfillment_cost = expected_total_revenue * self.config['fulfillment_cost_pct']
        
        # Promo cost
        incremental_orders = expected_total_orders - (daily_avg_orders * campaign_days)
        acquisition_cost = incremental_orders * self.config['promo_cost_per_order']
        total_promo_cost = promo_budget + acquisition_cost
        
        # Profit calculation
        expected_gross_profit = expected_total_revenue - expected_total_cost
        expected_net_profit = expected_gross_profit - fulfillment_cost - total_promo_cost
        
        # Margin calculation
        expected_margin_pct = (expected_net_profit / expected_total_revenue * 100) if expected_total_revenue > 0 else 0
        
        # ROI calculation
        roi = ((expected_net_profit - promo_budget) / promo_budget * 100) if promo_budget > 0 else 0
        
        # Baseline comparison
        baseline_revenue = daily_avg_revenue * campaign_days
        baseline_profit = daily_avg_profit * campaign_days
        baseline_orders = daily_avg_orders * campaign_days
        
        # Store results
        results['outputs'] = {
            'demand_lift_pct': (demand_lift - 1) * 100,
            'expected_orders': round(expected_total_orders),
            'expected_revenue': round(expected_total_revenue, 2),
            'expected_cost': round(expected_total_cost, 2),
            'fulfillment_cost': round(fulfillment_cost, 2),
            'promo_cost': round(total_promo_cost, 2),
            'expected_gross_profit': round(expected_gross_profit, 2),
            'expected_net_profit': round(expected_net_profit, 2),
            'expected_margin_pct': round(expected_margin_pct, 2),
            'roi_pct': round(roi, 2)
        }
        
        results['comparison'] = {
            'baseline_revenue': round(baseline_revenue, 2),
            'baseline_profit': round(baseline_profit, 2),
            'baseline_orders': round(baseline_orders),
            'revenue_change': round(expected_total_revenue - baseline_revenue, 2),
            'revenue_change_pct': round((expected_total_revenue - baseline_revenue) / baseline_revenue * 100, 2) if baseline_revenue > 0 else 0,
            'profit_change': round(expected_net_profit - baseline_profit, 2),
            'profit_change_pct': round((expected_net_profit - baseline_profit) / baseline_profit * 100, 2) if baseline_profit > 0 else 0,
            'order_change': round(expected_total_orders - baseline_orders),
            'order_change_pct': round((expected_total_orders - baseline_orders) / baseline_orders * 100, 2) if baseline_orders > 0 else 0
        }
        
        # Generate warnings
        if expected_margin_pct < margin_floor:
            results['warnings'].append(f"⚠️ Expected margin ({expected_margin_pct:.1f}%) is below floor ({margin_floor}%)!")
        
        if roi < 0:
            results['warnings'].append(f"⚠️ Negative ROI ({roi:.1f}%) - Campaign may not be profitable!")
        
        if discount_pct > 30:
            results['warnings'].append(f"⚠️ High discount ({discount_pct}%) may impact brand perception!")
        
        if expected_net_profit < 0:
            results['warnings'].append(f"⚠️ Expected NET LOSS of AED {abs(expected_net_profit):,.2f}!")
        
        return results
