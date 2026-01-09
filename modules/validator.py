"""
File Validator Module - UAE Pulse Simulator
Validates uploaded files match expected schema for each file type.
"""

import pandas as pd


class FileValidator:
    """Validates uploaded files against expected schemas."""
    
    # Required columns for each file type (with variations)
    SCHEMAS = {
        'products': {
            'required': [
                ['sku', 'product_id', 'productid', 'SKU'],  # At least one required
                ['category'],
                ['base_price_aed', 'base_price', 'price'],
            ],
            'optional': ['unit_cost_aed', 'unit_cost', 'brand', 'launch_flag', 'tax_rate'],
            'unique_identifiers': ['sku', 'product_id', 'category', 'brand', 'launch_flag']
        },
        'stores': {
            'required': [
                ['store_id', 'storeid'],
                ['city'],
                ['channel']
            ],
            'optional': ['fulfillment_type', 'store_name'],
            'unique_identifiers': ['store_id', 'city', 'channel', 'fulfillment_type']
        },
        'sales': {
            'required': [
                ['order_id', 'orderid', 'transaction_id'],
                ['sku', 'product_id', 'productid'],
                ['store_id', 'storeid'],
                ['qty', 'quantity', 'units'],
                ['selling_price_aed', 'selling_price', 'price', 'amount']
            ],
            'optional': ['order_time', 'discount_pct', 'payment_status', 'return_flag'],
            'unique_identifiers': ['order_id', 'qty', 'selling_price', 'payment_status', 'discount_pct']
        },
        'inventory': {
            'required': [
                ['sku', 'product_id', 'productid'],
                ['store_id', 'storeid'],
                ['stock_on_hand', 'stock', 'inventory', 'on_hand', 'quantity']
            ],
            'optional': ['snapshot_date', 'reorder_point', 'lead_time_days'],
            'unique_identifiers': ['stock_on_hand', 'stock', 'reorder_point', 'lead_time_days', 'snapshot_date']
        }
    }
    
    @classmethod
    def validate_file(cls, df, expected_type):
        """
        Validate if uploaded file matches expected type.
        
        Args:
            df: pandas DataFrame of uploaded file
            expected_type: 'products', 'stores', 'sales', or 'inventory'
        
        Returns:
            dict: {
                'valid': bool,
                'message': str,
                'missing_columns': list,
                'detected_type': str or None
            }
        """
        if df is None or df.empty:
            return {
                'valid': False,
                'message': '❌ File is empty or could not be read.',
                'missing_columns': [],
                'detected_type': None
            }
        
        # Normalize column names
        df_columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
        
        # Check if file matches expected type
        expected_schema = cls.SCHEMAS.get(expected_type)
        if not expected_schema:
            return {
                'valid': False,
                'message': f'❌ Unknown file type: {expected_type}',
                'missing_columns': [],
                'detected_type': None
            }
        
        # Check required columns for expected type
        missing_required = []
        for col_variants in expected_schema['required']:
            col_variants_lower = [c.lower() for c in col_variants]
            if not any(col in df_columns for col in col_variants_lower):
                missing_required.append(col_variants[0])  # Show primary column name
        
        # If all required columns present, file is valid
        if not missing_required:
            return {
                'valid': True,
                'message': f'✅ Valid {expected_type} file detected.',
                'missing_columns': [],
                'detected_type': expected_type
            }
        
        # File doesn't match expected type - try to detect actual type
        detected_type = cls._detect_file_type(df_columns)
        
        if detected_type and detected_type != expected_type:
            return {
                'valid': False,
                'message': f'❌ Wrong file! This looks like a **{detected_type.upper()}** file, not {expected_type.upper()}.',
                'missing_columns': missing_required,
                'detected_type': detected_type
            }
        else:
            # Check if file matches ANY known type
            any_match = cls._detect_file_type(df_columns)
            
            if any_match is None:
                # Completely unrecognized file
                return {
                    'valid': False,
                    'message': f'❌ Unrecognized file! This doesn\'t match any expected format (Products, Stores, Sales, or Inventory).',
                    'missing_columns': missing_required,
                    'detected_type': None,
                    'uploaded_columns': list(df_columns)[:10]  # Show first 10 columns
                }
            else:
                return {
                    'valid': False,
                    'message': f'❌ Invalid {expected_type} file. Missing required columns.',
                    'missing_columns': missing_required,
                    'detected_type': None
                }
    
    @classmethod
    @classmethod
    def _detect_file_type(cls, df_columns):
        """Detect the actual file type based on columns - STRICT matching."""
        scores = {}
        required_counts = {}
        
        for file_type, schema in cls.SCHEMAS.items():
            score = 0
            required_matched = 0
            total_required = len(schema['required'])
            
            # Check required columns (most important)
            for col_variants in schema['required']:
                col_variants_lower = [c.lower() for c in col_variants]
                if any(col in df_columns for col in col_variants_lower):
                    score += 3  # High weight for required columns
                    required_matched += 1
            
            # Check unique identifiers (secondary)
            for identifier in schema.get('unique_identifiers', []):
                if identifier.lower() in df_columns:
                    score += 1
            
            scores[file_type] = score
            required_counts[file_type] = (required_matched, total_required)
        
        # Only return a match if:
        # 1. At least 60% of required columns are present
        # 2. Score is significant
        if scores:
            best_match = max(scores, key=scores.get)
            matched, total = required_counts[best_match]
            match_percentage = (matched / total * 100) if total > 0 else 0
            
            # STRICT: Must have at least 60% of required columns
            if match_percentage >= 60 and scores[best_match] >= 6:
                return best_match
        
        return None
    
    @classmethod
    def get_expected_columns(cls, file_type):
        """Get list of expected columns for a file type."""
        schema = cls.SCHEMAS.get(file_type, {})
        required = [cols[0] for cols in schema.get('required', [])]
        optional = schema.get('optional', [])
        return {
            'required': required,
            'optional': optional
        }
    
    @classmethod
    def get_validation_summary(cls, df, file_type):
        """Get detailed validation summary for display."""
        result = cls.validate_file(df, file_type)
        
        expected = cls.get_expected_columns(file_type)
        df_columns = [col.strip().lower().replace(' ', '_') for col in df.columns] if df is not None else []
        
        return {
            **result,
            'expected_required': expected['required'],
            'expected_optional': expected['optional'],
            'uploaded_columns': list(df.columns) if df is not None else [],
            'row_count': len(df) if df is not None else 0
        }
