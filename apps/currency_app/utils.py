from decimal import Decimal


def calculate_income_price(income_price_usd, new_currency_value):
    # Ensure both values are Decimal for proper multiplication
    income_price_usd = Decimal(income_price_usd)
    new_currency_value = Decimal(new_currency_value)
    return income_price_usd * new_currency_value


def calculate_selling_price(updated_income_price, selling_percentage):
    return (updated_income_price * selling_percentage) / 100 + updated_income_price
