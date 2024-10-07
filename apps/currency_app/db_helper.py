from apps.currency_app.utils import calculate_income_price, calculate_selling_price


def update_prices_and_bulk_update(item_balances, model_class, new_currency):
    updated_items = []

    for item in item_balances:
        if item.income_price_usd > 0:
            updated_income_price = calculate_income_price(item.income_price_usd, new_currency.value)
            updated_selling_price = calculate_selling_price(updated_income_price, item.selling_percentage)

            item.income_price = updated_income_price
            item.selling_price = updated_selling_price  # Ensure this attribute exists in your model

            updated_items.append(item)

    # Perform a bulk update for better performance
    model_class.objects.bulk_update(updated_items, ['income_price', 'selling_price'])
