import pandas as pd

# Define standard tax rate data
data = {
    "Country Code": ["IN"],              # India
    "State Code": ["*"],                 # Applies to all states
    "Postcode / ZIP": [""],             # Applies to all postcodes
    "City": [""],                        # Applies to all cities
    "Rate %": [18.0],                    # 18% GST
    "Tax Name": ["Standard GST"],
    "Priority": [1],
    "Compound": [False],
    "Shipping": [True],
    "Tax Class": ["standard"]
}

# Create DataFrame
tax_rate_df = pd.DataFrame(data)

# Save to CSV file
tax_rate_df.to_csv("standard_tax_rate.csv", index=False)

print("CSV file 'standard_tax_rate.csv' has been created.")
