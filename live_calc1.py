import requests  # Handles HTTP requests
import datetime

def get_real_rate(currency):
    try:
        # Using a public API for real-time exchange rates
        # NOTE: Replace 'YOUR_API_KEY_HERE' with your actual API key in a .env file for production
        url = f"http://api.exchangeratesapi.io/v1/latest?access_key=YOUR_API_KEY_HERE&symbols={currency}"
        
        # Sending the request...
        response = requests.get(url)
        
        # Parsing JSON response
        data = response.json()
        
        # Extracting the specific rate
        if "rates" in data:
            return data["rates"][currency]
        else:
            print(f"⚠️ API Error: {data}")
            return None
        
    except Exception as e:
        print(f"⚠️ Error fetching rate: {e}")
        return None

def calculate_nordic_cost(amount, currency):
    # 1. Fetching live rate
    print(f"⏳ Fetching live rate for {currency}...")
    rate = get_real_rate(currency)
    
    if rate is None:
        print("Could not fetch rate. Check internet connection or API key.")
        return

    # Finnish VAT (ALV) as of Sept 2024
    vat_rate = 0.255 

    # 2. Calculation
    # Formula: Foreign Currency / Rate = Euro (Based on standard EUR-base API)
    eur_amount = amount / rate
    
    vat_amount = eur_amount * vat_rate
    total_with_vat = eur_amount + vat_amount

    # 3. Printing the Invoice
    print("\n" + "="*45)
    print(f" 📡 LIVE LOGISTICS CALCULATOR - {datetime.date.today()}")
    print("="*45)
    print(f" Original Amount:   {amount:.2f} {currency}")
    print(f" Exchange Rate:     1 EUR = {rate} {currency}")
    print("-" * 45)
    print(f" Price (EUR):       {eur_amount:.2f} €")
    print(f" VAT (25.5%):       {vat_amount:.2f} €")
    print("=" * 45)
    print(f" TOTAL TO PAY:      {total_with_vat:.2f} €")
    print("=" * 45 + "\n")

# --- USER INTERFACE ---
if __name__ == "__main__":
    try:
        print("--- NORDIC LIVE CALCULATOR ---")
        user_amount = float(input("Enter amount: "))
        user_curr = input("Enter currency (NOK, SEK, USD, GBP): ").upper()

        calculate_nordic_cost(user_amount, user_curr)

    except ValueError:
        print("Error! Please enter a valid number.")
