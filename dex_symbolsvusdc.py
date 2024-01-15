import requests
import pandas as pd
import json

url = "https://token.jup.ag/strict"

# Fetch data from the URL
response = requests.get(url)
data = response.json()

# Extract symbol names
symbol_names = [token["symbol"] for token in data]

# Create a DataFrame
symbol_name = pd.DataFrame({"Symbol": symbol_names})

symbols = symbol_name.drop_duplicates(subset="Symbol", keep="first")


# Export DataFrame to CSV
#symbols.to_csv("symbol_names.csv", index=False)

print("Symbol names exported to symbol_names.csv")

# Load the CSV file into a DataFrame
df = pd.read_csv('symbol_names.csv')

first_value = df.iloc[0, 0]



# Create an empty DataFrame to store the results
result_df = pd.DataFrame(columns=['Symbol', 'Price_vs_USDC'])

# Loop through each symbol in the CSV file
for symbol in first_value['Symbol']:
    # Make the API request
    url = f'https://price.jup.ag/v4/price?ids={symbol}&vsToken=USDC'
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        try:
            data = response.json()
            price_vs_usdc = data['data'][symbol]['price']
            
            # Append the result to the DataFrame
            result_df = result_df.append({'Symbol': symbol, 'Price_vs_USDC': price_vs_usdc}, ignore_index=True)
        except KeyError:
            print(f"Data not available for {symbol}")
    else:
        print(f"Error fetching data for {symbol}. Status code: {response.status_code}")

# Save the result DataFrame to a new CSV file
#result_df.to_csv('symbol_prices_vs_usdc.csv', index=False)



symbolvusdc_df = result_df[result_df['Price_vs_USDC'] >= 0.001]
print(symbolvusdc_df.head())



symbolvusdc = symbolvusdc_df[['Symbol']]
#symbolvusdc.to_csv('symbolvUSDC.csv', index=False)
print("saved names of symbols vsUSDC")
