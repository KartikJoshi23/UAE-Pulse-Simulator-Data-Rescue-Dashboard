"""
Data Cleaner Module for UAE Pulse Dashboard
Handles data cleaning, validation, and multi-language text standardization
"""

import pandas as pd
import numpy as np
import json
import os
import re
from difflib import SequenceMatcher


class DataCleaner:
    """Data cleaning and validation for UAE e-commerce data."""
    
    def __init__(self):
        """Initialize the DataCleaner with config."""
        self.config_path = 'config/text_mappings.json'
        self.mappings = self.load_mappings()
        self.fuzzy_threshold = 0.85
        self.cleaning_report = {}
    
    def load_mappings(self):
        """Load mappings from JSON config file."""
        default_mappings = {
            "cities": {},
            "channels": {},
            "categories": {},
            "standard_values": {
                "cities": ["Dubai", "Abu Dhabi", "Sharjah", "Ajman", "Ras Al Khaimah", "Fujairah", "Umm Al Quwain"],
                "channels": ["Online", "Offline", "Store", "Website", "Mobile", "Marketplace"],
                "categories": ["Electronics", "Fashion", "Grocery", "Beauty", "Home", "Sports", "Toys", "Books"]
            }
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading mappings: {e}")
        
        return default_mappings
    
    def save_mappings(self):
        """Save current mappings to JSON config file."""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.mappings, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Error saving mappings: {e}")
            return False
    
    def add_mapping(self, category, original, standard):
        """Add a new mapping dynamically."""
        if category in self.mappings:
            self.mappings[category][original] = standard
            self.save_mappings()
            return True
        return False
    
    def has_non_english(self, text):
        """Check if text contains non-English/non-ASCII characters."""
        if pd.isna(text):
            return False
        return bool(re.search(r'[^\x00-\x7F]', str(text)))
    
    def fuzzy_match(self, value, standard_values, threshold=None):
        """Find the best fuzzy match from standard values."""
        if threshold is None:
            threshold = self.fuzzy_threshold
        
        if pd.isna(value):
            return None, 0
        
        str_value = str(value).strip().lower()
        best_match = None
        best_score = 0
        
        for standard in standard_values:
            if str_value == standard.lower():
                return standard, 1.0
            
            score = SequenceMatcher(None, str_value, standard.lower()).ratio()
            if score > best_score and score >= threshold:
                best_score = score
                best_match = standard
        
        return best_match, best_score
    
    def standardize_value(self, value, mapping_type):
        """Standardize a single value using mapping and fuzzy matching."""
        if pd.isna(value):
            return value, None, 'empty'
        
        str_value = str(value).strip()
        
        mapping_dict = self.mappings.get(mapping_type, {})
        if str_value in mapping_dict:
            return mapping_dict[str_value], str_value, 'mapped'
        
        for key, standard in mapping_dict.items():
            if str_value.lower() == key.lower():
                return standard, str_value, 'mapped'
        
        standard_values = self.mappings.get('standard_values', {}).get(mapping_type, [])
        match, score = self.fuzzy_match(str_value, standard_values)
        
        if match:
            return match, str_value, f'fuzzy ({score:.0%})'
        
        for standard in standard_values:
            if str_value.lower() == standard.lower():
                return standard, None, 'standard'
        
        return str_value, str_value, 'unknown'
    
    def standardize_column_dynamic(self, df, column, mapping_type):
        """Dynamically standardize a column with reporting."""
        if column not in df.columns:
            return df, {'changes': 0, 'mapped': [], 'fuzzy': [], 'unknown': []}
        
        report = {
            'changes': 0,
            'mapped': [],
            'fuzzy': [],
            'unknown': []
        }
        
        new_values = []
        
        for val in df[column]:
            new_val, original, method = self.standardize_value(val, mapping_type)
            new_values.append(new_val)
            
            if original:
                if method == 'mapped':
                    report['mapped'].append(f"'{original}' → '{new_val}'")
                    report['changes'] += 1
                elif method.startswith('fuzzy'):
                    report['fuzzy'].append(f"'{original}' → '{new_val}' {method}")
                    report['changes'] += 1
                elif method == 'unknown':
                    if self.has_non_english(original):
                        report['unknown'].append(f"'{original}' (non-English)")
                    else:
                        report['unknown'].append(f"'{original}'")
        
        df[column] = new_values
        
        report['mapped'] = list(set(report['mapped']))
        report['fuzzy'] = list(set(report['fuzzy']))
        report['unknown'] = list(set(report['unknown']))
        
        return df, report
    
    def standardize_all_text(self, df):
        """Dynamically standardize all text columns."""
        full_report = {
            'total_changes': 0,
            'cities': None,
            'channels': None,
            'categories': None
        }
        
        city_cols = ['city', 'City', 'store_city', 'location']
        for col in city_cols:
            if col in df.columns:
                df, report = self.standardize_column_dynamic(df, col, 'cities')
                full_report['cities'] = report
                full_report['total_changes'] += report['changes']
                break
        
        channel_cols = ['channel', 'Channel', 'sales_channel', 'store_channel']
        for col in channel_cols:
            if col in df.columns:
                df, report = self.standardize_column_dynamic(df, col, 'channels')
                full_report['channels'] = report
                full_report['total_changes'] += report['changes']
                break
        
        cat_cols = ['category', 'Category', 'product_category', 'cat']
        for col in cat_cols:
            if col in df.columns:
                df, report = self.standardize_column_dynamic(df, col, 'categories')
                full_report['categories'] = report
                full_report['total_changes'] += report['changes']
                break
        
        return df, full_report
    
    def detect_issues(self, df, df_name="DataFrame"):
        """Detect all data quality issues in a DataFrame."""
        issues = {
            'missing_values': {},
            'duplicates': 0,
            'outliers': {},
            'invalid_formats': {},
            'negative_values': {},
            'non_english': {}
        }
        
        for col in df.columns:
            missing = df[col].isna().sum()
            if missing > 0:
                issues['missing_values'][col] = int(missing)
        
        issues['duplicates'] = int(df.duplicated().sum())
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            outlier_count = ((df[col] < lower) | (df[col] > upper)).sum()
            if outlier_count > 0:
                issues['outliers'][col] = int(outlier_count)
            
            if col in ['qty', 'quantity', 'price', 'selling_price_aed', 'cost_aed', 'stock_on_hand']:
                neg_count = (df[col] < 0).sum()
                if neg_count > 0:
                    issues['negative_values'][col] = int(neg_count)
        
        text_cols = df.select_dtypes(include=['object']).columns
        for col in text_cols:
            non_english_count = df[col].apply(self.has_non_english).sum()
            if non_english_count > 0:
                issues['non_english'][col] = int(non_english_count)
        
        return issues
    
    def clean_missing_values(self, df):
        """Clean missing values based on column type."""
        changes = 0
        
        for col in df.columns:
            missing = df[col].isna().sum()
            if missing > 0:
                if df[col].dtype in ['float64', 'int64']:
                    median_val = df[col].median()
                    df[col] = df[col].fillna(median_val)
                    changes += missing
                elif df[col].dtype == 'object':
                    mode_val = df[col].mode()
                    if len(mode_val) > 0:
                        df[col] = df[col].fillna(mode_val[0])
                        changes += missing
        
        return df, changes
    
    def remove_duplicates(self, df):
        """Remove duplicate rows."""
        original_len = len(df)
        df = df.drop_duplicates()
        removed = original_len - len(df)
        return df, removed
    
    def fix_outliers(self, df, method='cap'):
        """Fix outliers using IQR method."""
        changes = 0
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            
            if method == 'cap':
                outlier_mask = (df[col] < lower) | (df[col] > upper)
                changes += outlier_mask.sum()
                df[col] = df[col].clip(lower=lower, upper=upper)
        
        return df, changes
    
    def fix_negative_values(self, df):
        """Fix negative values in columns that should be positive."""
        changes = 0
        positive_cols = ['qty', 'quantity', 'price', 'selling_price_aed', 'cost_aed', 'stock_on_hand', 'units']
        
        for col in positive_cols:
            if col in df.columns:
                neg_mask = df[col] < 0
                neg_count = neg_mask.sum()
                if neg_count > 0:
                    df.loc[neg_mask, col] = df.loc[neg_mask, col].abs()
                    changes += neg_count
        
        return df, changes
    
    def validate_foreign_keys(self, sales_df, products_df, stores_df):
        """Validate foreign key relationships."""
        issues = {
            'invalid_skus': 0,
            'invalid_stores': 0
        }
        
        sku_col_sales = None
        sku_col_products = None
        store_col_sales = None
        store_col_stores = None
        
        for col in ['sku', 'SKU', 'product_id', 'ProductID']:
            if col in sales_df.columns:
                sku_col_sales = col
            if col in products_df.columns:
                sku_col_products = col
        
        for col in ['store_id', 'StoreID', 'store']:
            if col in sales_df.columns:
                store_col_sales = col
            if col in stores_df.columns:
                store_col_stores = col
        
        if sku_col_sales and sku_col_products:
            valid_skus = set(products_df[sku_col_products].unique())
            invalid_mask = ~sales_df[sku_col_sales].isin(valid_skus)
            issues['invalid_skus'] = int(invalid_mask.sum())
        
        if store_col_sales and store_col_stores:
            valid_stores = set(stores_df[store_col_stores].unique())
            invalid_mask = ~sales_df[store_col_sales].isin(valid_stores)
            issues['invalid_stores'] = int(invalid_mask.sum())
        
        return issues
    
    def clean_dataframe(self, df, df_name="DataFrame"):
        """Clean a single DataFrame with all cleaning operations."""
        report = {
            'name': df_name,
            'original_rows': len(df),
            'missing_fixed': 0,
            'duplicates_removed': 0,
            'outliers_fixed': 0,
            'negatives_fixed': 0,
            'text_standardized': 0,
            'final_rows': 0
        }
        
        df, missing_fixed = self.clean_missing_values(df)
        report['missing_fixed'] = missing_fixed
        
        df, dups_removed = self.remove_duplicates(df)
        report['duplicates_removed'] = dups_removed
        
        df, outliers_fixed = self.fix_outliers(df)
        report['outliers_fixed'] = outliers_fixed
        
        df, negatives_fixed = self.fix_negative_values(df)
        report['negatives_fixed'] = negatives_fixed
        
        df, text_report = self.standardize_all_text(df)
        report['text_standardized'] = text_report['total_changes']
        report['text_details'] = text_report
        
        report['final_rows'] = len(df)
        
        return df, report
    
    def clean_all(self, products_df, stores_df, sales_df, inventory_df):
        """Clean all DataFrames and return cleaned versions with reports."""
        all_reports = {}
        
        clean_products, report = self.clean_dataframe(products_df.copy(), "Products")
        all_reports['products'] = report
        
        clean_stores, report = self.clean_dataframe(stores_df.copy(), "Stores")
        all_reports['stores'] = report
        
        clean_sales, report = self.clean_dataframe(sales_df.copy(), "Sales")
        all_reports['sales'] = report
        
        clean_inventory, report = self.clean_dataframe(inventory_df.copy(), "Inventory")
        all_reports['inventory'] = report
        
        fk_issues = self.validate_foreign_keys(clean_sales, clean_products, clean_stores)
        all_reports['foreign_key_issues'] = fk_issues
        
        return clean_products, clean_stores, clean_sales, clean_inventory, all_reports
