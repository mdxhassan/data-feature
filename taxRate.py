import requests

# function to get the user's public IP address
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        if response.status_code == 200:
            ip_data = response.json()
            return ip_data["ip"]
        else:
            print(f"Error: Could not retrieve public IP (status code {response.status_code})")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# function to get location information from IP address using IPstack API
def get_location_from_ip(ip_address, ipstack_api_key):
    url = f"http://api.ipstack.com/{ip_address}?access_key={ipstack_api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Failed to get location data (status code {response.status_code})")
        return None

# function to get US tax rates by state using the Tax Data API
def get_us_tax_rates(state_code, tax_data_api_key):
    tax_api_url = f"https://api.apilayer.com/tax_data/us_rate_list?state={state_code}"
    
    headers = {
        "apikey": tax_data_api_key
    }

    response = requests.get(tax_api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print(f"Error: Tax data not found for state {state_code}. (status code 404)")
        return None
    else:
        print(f"Error: Failed to get tax data (status code {response.status_code})")
        return None

# function to get global tax rates for non-US locations using the Tax Data API based on country code
def get_global_tax_info(country_code, tax_data_api_key):
    tax_api_url = f"https://api.apilayer.com/tax_data/rates?country_code={country_code}"
    
    headers = {
        "apikey": tax_data_api_key
    }

    response = requests.get(tax_api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print(f"Error: Tax data not found for country {country_code}. (status code 404)")
        return None
    else:
        print(f"Error: Failed to get global tax data (status code {response.status_code})")
        return None

# function to validate VAT number using the Tax Data API
def validate_tax_number(vat_number, country_code, tax_data_api_key):
    tax_api_url = f"https://api.apilayer.com/tax_data/validate?vat_number={vat_number}&country_code={country_code}"
    
    headers = {
        "apikey": tax_data_api_key
    }

    response = requests.get(tax_api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print(f"Error: VAT data not found for VAT number {vat_number} in country {country_code}. (status code 404)")
        return None
    else:
        print(f"Error: Failed to get VAT data (status code {response.status_code})")
        return None

# function to perform tax-compliant price calculation
def calculate_sales_tax(price, tax_rate):
    tax_amount = price * (tax_rate / 100)
    total_price = price + tax_amount
    # round both tax_amount and total_price to two decimal places
    tax_amount = round(tax_amount, 2)
    total_price = round(total_price, 2)
    return tax_amount, total_price

# function to show the main menu
def show_menu():
    print("\nPlease choose an option:")
    print("1. Get Tax Rates")
    print("2. Validate Tax Number")
    print("3. Exit")
    choice = input("Enter your choice (1-3): ")
    return choice

# main function to run the program
def main():
    ipstack_api_key = "8ac3153cf81bb5233c241d852f552f42"  #IPstack API key
    tax_data_api_key = "Dc5YsBU8EhnDYvHU5V4h9Bu8dapaZAIu"  # Tax Data API key

    while True:
        choice = show_menu()

        if choice == '1':  #get tax rates
            # automatically get the user's public IP address
            ip_address = get_public_ip()
            if not ip_address:
                print("Error: Could not retrieve public IP address.")
                continue

            # get location data from IPstack
            location_data = get_location_from_ip(ip_address, ipstack_api_key)
            
            if location_data:
                # extract country code and state code from location data
                country_code = location_data.get("country_code")
                state_code = location_data.get("region_code")
                city = location_data.get("city")
                zip_code = location_data.get("zip")

                if country_code == "US" and state_code:
                    # get US-specific tax rates
                    tax_data = get_us_tax_rates(state_code, tax_data_api_key)
                    if tax_data:
                        # extract the combined tax rate
                        combined_rate = tax_data["data"][0].get("combined_rate", 0) * 100
                        print(f"Tax Data for ZIP: {zip_code}:")
                        print(f"State Rate: {tax_data['data'][0].get('state_rate', 0) * 100}%")
                        print(f"County Rate: {tax_data['data'][0].get('county_rate', 0) * 100}%")
                        print(f"City Rate: {tax_data['data'][0].get('city_rate', 0) * 100}%")
                        print(f"Combined Rate: {combined_rate}%")
                        print(f"Freight Taxable: {'Yes' if tax_data['data'][0].get('freight_taxable') else 'No'}")

                        # ask for the product price to calculate sales tax
                        price = float(input("Enter the product price: "))
                        tax_amount, total_price = calculate_sales_tax(price, combined_rate)
                        print(f"Sales tax amount: {tax_amount}")
                        print(f"Total price (including tax): {total_price}")
                    else:
                        print(f"No tax data available for state {state_code}.")
                else:
                    # get global tax rates for non-US locations
                    tax_data = get_global_tax_info(country_code, tax_data_api_key)
                    if tax_data:
                        combined_rate = tax_data["standard_rate"]
                        print(f"Combined sales tax rate for {city}, {country_code}: {combined_rate}%")

                        # ask for the product price to calculate sales tax
                        price = float(input("Enter the product price: "))
                        tax_amount, total_price = calculate_sales_tax(price, combined_rate)
                        print(f"Sales tax amount: {tax_amount}")
                        print(f"Total price (including tax): {total_price}")
                    else:
                        print(f"No tax data available for country {country_code}.")
            else:
                print("Could not retrieve location information.")

        elif choice == '2':  # validate Tax Number
            # user input for the country code and VAT number
            country_code = input("Enter the country code (e.g., 'AT' for Austria): ")
            vat_number = input(f"Enter the VAT number for {country_code}: ")

            # validate VAT number using the Tax Data API
            vat_data = validate_tax_number(vat_number, country_code, tax_data_api_key)
            if vat_data and vat_data.get("valid"):
                vat_rate = vat_data["format_valid"]
                print(f"VAT number is valid for {vat_data['name']} in {vat_data['address']}.")
                print(f"Combined VAT rate: {vat_rate}%")
            else:
                print(f"Invalid or unavailable VAT data for VAT number {vat_number}.")

        elif choice == '3':  # exit
            print("Exiting program")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
