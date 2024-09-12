# Tax Rate and VAT Validator Tool

This is a Python project that allows users to:
- Retrieve tax rates based on their location (using their public IP) and calculate sales tax.
- Validate VAT numbers for different countries.
- Get both US and global tax rates using the [Tax Data API](https://apilayer.com/marketplace/tax_data-api).
  
The project utilizes external APIs to fetch tax data, location information, and VAT validation to provide accurate tax-related information.

## Features
- **Get Tax Rates**: Automatically retrieves the user's public IP, then fetches tax rate data based on their location. It supports both US and global tax rates.
- **Validate Tax Number**: Allows users to validate VAT numbers from different countries using the Tax Data API.
- **Sales Tax Calculation**: Given a product price, the program calculates the applicable sales tax based on location-specific rates.

## APIs Used
### 1. [IPify API](https://www.ipify.org/)
- **Purpose**: Retrieves the user's public IP address.
- **Reason for Choice**: Simple, reliable, and lightweight API that provides accurate public IP information.

### 2. [IPstack API](https://ipstack.com/)
- **Purpose**: Fetches geographical location details based on the public IP address.
- **Reason for Choice**: Provides comprehensive location data, including country code and region (state) information, necessary for determining local tax rates.

### 3. [Tax Data API](https://apilayer.com/marketplace/tax_data-api)
- **Purpose**: Fetches tax rates for both US states and global locations and validates VAT numbers.
- **Reason for Choice**: The API provides real-time tax data and VAT validation, which is crucial for accurate tax calculations.

## Prerequisites
Before using this feature, ensure you have the following:
- **Python 3.x** installed on your machine.
- **API keys** for the following services:
  - [IPstack API](https://ipstack.com/)
  - [Tax Data API](https://apilayer.com/marketplace/tax_data-api)
  
You can sign up for these services and obtain free API keys by visiting their respective websites.

## Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/tax-rate-vat-validator.git
    cd tax-rate-vat-validator
    ```

2. **Install dependencies**:
    Install the `requests` package, which is required for making API calls:
    ```bash
    pip install requests
    ```

3. **Set up API keys**:
    In the `main` function, replace the placeholder values for the API keys with your actual keys:
    ```python
    ipstack_api_key = "your_ipstack_api_key"
    tax_data_api_key = "your_tax_data_api_key"
    ```

4. **Run the program**:
    Run the Python script using the following command:
    ```bash
    python main.py
    ```

## How to Use
Upon running the program, you will be presented with a menu offering two main features:

1. **Get Tax Rates**: Automatically retrieves your public IP, gets location data, and provides tax rates based on the region. The program supports US state-specific rates and global tax rates.
   
    - Enter the product price to calculate the sales tax and total price based on the retrieved rates.

2. **Validate Tax Number**: Validate a VAT number by inputting the country code and VAT number.

3. **Exit**: End the program. 
