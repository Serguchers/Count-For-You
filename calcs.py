def find_best_offer(data):
    buy_to_check = {
        resource: data[resource]["buy"]
        for resource in data
        if data[resource]["buy"] != 0
    }
    sell_to_check = {
        resource: data[resource]["sell"]
        for resource in data
        if data[resource]["sell"] != 0
    }
    best_buy = min(buy_to_check, key=lambda x: buy_to_check[x])
    best_sell = max(sell_to_check, key=lambda x: sell_to_check[x])
    return best_buy, best_sell


def compare_values(binance, current, previous, operation):
    if abs(current - previous) >= 0.1:
        if operation == "buy":
            try:
                difference_percents = round((float(binance / current) - 1) * 100, 3)
            except ZeroDivisionError:
                raise ZeroDivisionError
        else:
            try:
                difference_percents = round(
                    (float(current * 0.999 / binance * 0.999) - 1) * 100, 3
                )
            except ZeroDivisionError:
                raise ZeroDivisionError

        return difference_percents

    return False
