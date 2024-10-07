def calculate_income_price(income_price_usd, new_currency):
    return income_price_usd * new_currency


def calculate_selling_price(updated_income_price, selling_percentage):
    return (updated_income_price * selling_percentage) / 100 + updated_income_price
