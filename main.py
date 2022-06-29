import asyncio
import aiohttp
from headers import *
from config import config


USDT_RUB_PAIR = {
    "binance": {"buy": 0, "sell": 0},
    "AAX": {"buy": 0, "sell": 0},
    "kucoin": {"buy": 0, "sell": 0},
    "yobit": {"buy": 0, "sell": 0},
    "huobi": {"buy": 0, "sell": 0},
    "phemex": {"buy": 0, "sell": 0},
}


async def get_data(session, resource):
    """
    Args:
        session (ClienSession): aiohttp ClienSession object
        resource (str): resource name
    """
    if resource == "binance":
        try:
            async with session.get(
                "https://api.binance.com/api/v3/ticker/price?symbol=USDTRUB",
                headers=HEADERS,
            ) as resp:
                data = await resp.json()
        except:
            return None

        USDT_RUB_PAIR["binance"]["buy"] = float(data["price"])
        USDT_RUB_PAIR["binance"]["sell"] = float(data["price"])

        return True

    if resource == "exmpo":
        try:
            async with session.get(
                "https://api.exmo.com/v1.1/ticker", headers=HEADERS
            ) as resp:
                data = await resp.json()
        except:
            return None

        try:
            USDT_RUB_PAIR["exmpo"].update(
                {
                    "buy": data["USDT_RUB"]["sell_price"],
                    "sell": data["USDT_RUB"]["buy_price"],
                }
            )
        except:
            USDT_RUB_PAIR["exmpo"].update({"buy": 0, "sell": 0})

    if resource == "AAX":
        try:
            async with session.get(
                "https://api.aax.com/common/v2/market/rfqPrice?base=USDT&quote=RUB",
                headers=HEADERS,
            ) as resp:
                data = await resp.json()
        except:
            return None

        try:
            USDT_RUB_PAIR["AAX"].update(
                {
                    "buy": data["data"]["prices"][0]["buy"],
                    "sell": data["data"]["prices"][0]["sell"],
                }
            )
        except:
            USDT_RUB_PAIR["AAX"].update({"buy": 0, "sell": 0})

        return True

    if resource == "kucoin_buy":
        try:
            async with session.get(
                "https://www.kucoin.com/_api/dispatch/v1/quotes?fiatCurrency=RUB&cryptoCurrency=USDT&quoteType=CRYPTO&source=WEB&side=BUY&platform=KUCOIN&lang=en_US",
                headers=HEADERS,
            ) as resp:
                data = await resp.json()
        except:
            return None

        try:
            USDT_RUB_PAIR["kucoin"].update(
                {"buy": float(data["data"]["quotes"][0]["price"])}
            )
        except:
            USDT_RUB_PAIR["kucoin"].update({"buy": 0})
        return True

    if resource == "kucoin_sell":
        try:
            async with session.get(
                "https://www.kucoin.com/_api/dispatch/v1/quotes?fiatCurrency=RUB&cryptoCurrency=USDT&quoteType=CRYPTO&source=WEB&side=SELL&platform=KUCOIN&lang=en_US",
                headers=HEADERS,
            ) as resp:
                data = await resp.json()
        except:
            return None

        try:
            USDT_RUB_PAIR["kucoin"].update(
                {"sell": float(data["data"]["quotes"][0]["price"])}
            )
        except:
            USDT_RUB_PAIR["kucoin"].update({"sell": 0})
        return True

    if resource == "yobit":
        try:
            async with session.get(
                "https://yobit.net/api/3/ticker/usdt_rur", headers=HEADERS
            ) as resp:
                data = await resp.json(content_type=None)
        except Exception as e:
            print(e)
            return None

        try:
            USDT_RUB_PAIR["yobit"].update(
                {"buy": data["usdt_rur"]["sell"], "sell": data["usdt_rur"]["buy"]}
            )
        except:
            USDT_RUB_PAIR["yobit"].update({"buy": 0, "sell": 0})

    if resource == "huobi_buy":
        try:
            async with session.get(
                "https://otc-api.bitderiv.com/v1/trade/fast/quote?quoteAsset=rub&cryptoAsset=usdt&side=buy&amount=100&type=quantity&areaType=1&p2pPayment=1&acceptOrder=0",
                headers=HEADERS_HUOBI,
            ) as resp:
                data = await resp.json()
        except:
            return None

        try:
            USDT_RUB_PAIR["huobi"].update(
                {"buy": float(data["data"][0]["quoteDetail"][0]["price"])}
            )
        except:
            USDT_RUB_PAIR["huobi"].update({"buy": 0})

        return True

    if resource == "huobi_sell":
        try:
            async with session.get(
                "https://otc-api.trygofast.com/v1/fiat/fast/quote?quoteAsset=rub&cryptoAsset=usdt&side=sell&amount=100.000000&type=quantity",
                headers=HEADERS_HUOBI_SELL,
                ssl=False,
            ) as resp:
                data = await resp.json()
        except Exception as e:
            print(e)
            return None

        try:
            USDT_RUB_PAIR["huobi"].update(
                {"sell": float(data["data"][0]["detail"][0]["price"])}
            )
        except:
            USDT_RUB_PAIR["huobi"].update({"sell": 0})

    if resource == "phemex":
        HEADERS_PHEMEX["phemex-auth-token"] = config["SETTINGS"]["phemex_auth_token"]
        try:
            async with session.get(
                "https://phemex.com/api/phemex-user/fiatPayment/smartPricing?chainName=TRX&cryptoCurrency=USDT&fiat=RUB&fiatAmount=100000&paymentWay=VISA",
                headers=HEADERS_PHEMEX,
            ) as resp:
                data = await resp.json()
        except:
            return None

        try:
            USDT_RUB_PAIR["phemex"].update(
                {
                    "buy": float(data["data"][0]["priceWithFee"]),
                    "sell": float(data["data"][0]["priceWithFee"]),
                }
            )
        except:
            USDT_RUB_PAIR["phemex"].update({"buy": 0, "sell": 0})
        return True


async def main(resource_list):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for selected_resoruce in resource_list:
            if selected_resoruce == "kucoin":
                tasks.append(asyncio.ensure_future(get_data(session, "kucoin_buy")))
                tasks.append(asyncio.ensure_future(get_data(session, "kucoin_sell")))
                continue
            if selected_resoruce == "huobi":
                tasks.append(asyncio.ensure_future(get_data(session, "huobi_buy")))
                tasks.append(asyncio.ensure_future(get_data(session, "huobi_sell")))
                continue
            tasks.append(asyncio.ensure_future(get_data(session, selected_resoruce)))
        await asyncio.gather(*tasks)
    return USDT_RUB_PAIR
