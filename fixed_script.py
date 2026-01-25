# This script has a bug!
def get_daily_sales():
    sales_data = [100, 200, 300]
    
    # INTENTIONAL BUG: This list has 3 items (indexes: 0, 1, 2)
    # We are trying to access index 3 (the 4th item), which doesn't exist.
    
    print(f"Monday Sales: {sales_data[0]}")
    print(f"Tuesday Sales: {sales_data[1]}")
    print(f"Wednesday Sales: {sales_data[2]}")
    
    # FIX: Handle the potential IndexError gracefully for Thursday sales.
    # We check if the list has enough elements before trying to access index 3.
    if len(sales_data) > 3:
        print(f"Thursday Sales: {sales_data[3]}")
    else:
        print("Thursday Sales: Data not available in the current dataset.")
    
    # ORIGINAL BUG: The line 'get_daily_sales()' here caused infinite recursion.
    # It has been removed.

# Call the function to execute the daily sales report.
# This ensures the function is called once when the script is run directly,
# preventing the infinite recursion that was previously within the function itself.
if __name__ == "__main__":
    get_daily_sales()