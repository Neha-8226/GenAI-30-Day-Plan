# This script has a bug!
def get_daily_sales():
    sales_data = [100, 200, 300]
    
    # INTENTIONAL BUG: This list has 3 items (indexes: 0, 1, 2)
    # We are trying to access index 3 (the 4th item), which doesn't exist.
    
    print(f"Monday Sales: {sales_data[0]}")
    print(f"Tuesday Sales: {sales_data[1]}")
    print(f"Wednesday Sales: {sales_data[2]}")
    print(f"Thursday Sales: {sales_data[3]}")  # <--- ERROR HERE
    
    get_daily_sales()