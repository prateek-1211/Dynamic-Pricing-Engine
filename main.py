import pandas as pd

# Load CSV files
products_df = pd.read_csv('products.csv')
sales_df = pd.read_csv('sales.csv')

# Merge product and sales data using SKU
df = pd.merge(products_df, sales_df, on='sku', how='left')
df['quantity_sold'] = df['quantity_sold'].fillna(0).astype(int)

# Final output list
output_data = []

for _, row in df.iterrows():
    sku = row['sku']
    current_price = row['current_price']
    cost_price = row['cost_price']
    stock = row['stock']
    quantity_sold = row['quantity_sold']
    
    new_price = current_price  # Default

    # Apply Pricing Rules
    if stock < 20 and quantity_sold > 30:
        # Rule 1
        new_price = current_price * 1.15
    elif stock > 200 and quantity_sold == 0:
        # Rule 2
        new_price = current_price * 0.7
    elif stock > 100 and quantity_sold < 20:
        # Rule 3
        new_price = current_price * 0.9
    
    # Rule 4 - Ensure Minimum 20% Profit Margin
    min_price = cost_price * 1.2
    if new_price < min_price:
        new_price = min_price

    # Round final price
    new_price = round(new_price, 2)

    # Append results with units
    output_data.append({
        'sku': sku,
        'old_price': f"{current_price:.2f} INR",
        'new_price': f"{new_price:.2f} INR"
    })

# Convert to DataFrame
output_df = pd.DataFrame(output_data)

# Save to CSV
output_df.to_csv('updated_prices.csv', index=False)

print("✅ updated_prices.csv created successfully!")
