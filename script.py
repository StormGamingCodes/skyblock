import requests

class product:
    # Simple class to store products
    id: str                     # Id
    name: str                   # Name
    bazaar_buy_price: float     # Bazaar buy price
    npc_sell_price: float       # NPC sell price
    sell_moving_week: int       # Insta-sell of past week

def get_items_from_API():
    url = 'https://api.hypixel.net/resources/skyblock/items'

    resp = requests.get(url=url)
    data = resp.json()

    items_api = data['items']
    items = {}
    for item in items_api:
        if 'npc_sell_price' in item:
            items[item['id']] = {
                'name': item['name'],
                'npc_sell_price': item['npc_sell_price']
            }

    return items

def get_products_from_API():
    url = 'https://api.hypixel.net/skyblock/bazaar'

    resp = requests.get(url=url)
    data = resp.json()

    return data['products']

def add_product(id, name, npc_price, bazaar_price, sell_moving_week):
    p = product()
    p.id = id
    p.name = name
    p.npc_sell_price = npc_price
    p.bazaar_buy_price = bazaar_price
    p.sell_moving_week = sell_moving_week
    
    return p

def calculate_max_profit_per_day(item_npc_price, profit_per_item):
    # Limit to amount of gold earned in NPC shops
    limit_gold_earn = 200000000

    # Number of items that can be sold to npc each day
    number_of_items = int(limit_gold_earn / item_npc_price)

    # Return daily profit with this item
    return int(number_of_items * profit_per_item), number_of_items

def calculate_profit_and_sort(all_products):
    profit_by_product = {}
    for p in all_products:
        # Profit calculation
        profit = round(p.npc_sell_price - p.bazaar_buy_price, 1)

        # Keep only positive profit
        if profit > 0.0 and p.bazaar_buy_price > 0.0:
            # Calculate max profit per day
            max_daily_profit, number_of_items = calculate_max_profit_per_day(p.npc_sell_price, profit)

            # Add values to dictionary
            profit_by_product[p.id] = {
                "name": p.name,
                "npc_price": float(p.npc_sell_price),
                "bazaar_price": p.bazaar_buy_price,
                "profit": profit,
                "sell_moving_week": p.sell_moving_week,
                "max_profit_day": max_daily_profit,
                "number_of_items": number_of_items
            }

    # Sort by profit
    sorted_by_profit = dict(sorted(profit_by_product.items(), key=lambda k_v: k_v[1]['profit'], reverse=True))

    # Create a formated copy of items
    sorted_by_profit_formated = sorted_by_profit.copy()
    for p in sorted_by_profit:
        sorted_by_profit_formated[p]['npc_price'] = '{:,}'.format(sorted_by_profit[p]['npc_price']).replace(',', "'")
        sorted_by_profit_formated[p]['bazaar_price'] = '{:,}'.format(sorted_by_profit[p]['bazaar_price']).replace(',', "'")
        sorted_by_profit_formated[p]['profit'] = '{:,}'.format(sorted_by_profit[p]['profit']).replace(',', "'")
        sorted_by_profit_formated[p]['sell_moving_week'] = '{:,}'.format(sorted_by_profit[p]['sell_moving_week']).replace(',', "'")
        sorted_by_profit_formated[p]['max_profit_day'] = '{:,}'.format(sorted_by_profit[p]['max_profit_day']).replace(',', "'")
        sorted_by_profit_formated[p]['number_of_items'] = '{:,}'.format(sorted_by_profit[p]['number_of_items']).replace(',', "'")
    
    return sorted_by_profit, sorted_by_profit_formated

def print_table(dict_products):
    # Define header for each column
    header_name = 'Item'
    header_profit = 'Profit'
    header_npc = 'NPC sell price'
    header_bazaar = 'Bazaar buy price'
    header_insta_sell = 'Insta-sell 7 days'
    header_max_profit_day = 'Max profit / day'
    header_number_of_items = '# items for max profit'

    # Get max lenth for each column
    longest_name = max(len(max(dict_products.items(), key=lambda k_v: len(k_v[1]['name']))[1]['name']), len(header_name))
    longest_profit = max(len(max(dict_products.items(), key=lambda k_v: len(k_v[1]['profit']))[1]['profit']), len(header_profit))
    longest_npc_price = max(len(max(dict_products.items(), key=lambda k_v: len(k_v[1]['npc_price']))[1]['npc_price']), len(header_npc))
    longest_bazaar_price = max(len(max(dict_products.items(), key=lambda k_v: len(k_v[1]['bazaar_price']))[1]['bazaar_price']), len(header_bazaar))
    longest_sell_moving_week = max(len(max(dict_products.items(), key=lambda k_v: len(k_v[1]['sell_moving_week']))[1]['sell_moving_week']), len(header_insta_sell))
    longest_max_pofit_day = max(len(max(dict_products.items(), key=lambda k_v: len(k_v[1]['max_profit_day']))[1]['max_profit_day']), len(header_max_profit_day))
    longest_number_of_items = max(len(max(dict_products.items(), key=lambda k_v: len(k_v[1]['number_of_items']))[1]['number_of_items']), len(header_number_of_items))

    # Print header (22 is for esapces and | char)
    total_length = 22 + longest_name + longest_profit + longest_npc_price + longest_bazaar_price + longest_sell_moving_week + longest_max_pofit_day + longest_number_of_items
    print("-"*total_length)
    print("| {: ^{}} | {: ^{}} | {: ^{}} | {: ^{}} | {: ^{}} | {: ^{}} | {: ^{}} |".format(
            header_name, longest_name, 
            header_profit, longest_profit,
            header_npc, longest_npc_price,
            header_bazaar, longest_bazaar_price,
            header_insta_sell, longest_sell_moving_week,
            header_max_profit_day, longest_max_pofit_day,
            header_number_of_items, longest_number_of_items
        ))
    print("-"*total_length)

    for _, value in dict_products.items():
        print("| {: <{}} | {: >{}} | {: >{}} | {: >{}} | {: >{}} | {: >{}} | {: >{}} |".format(
            value['name'], longest_name, 
            value['profit'], longest_profit,
            value['npc_price'], longest_npc_price,
            value['bazaar_price'], longest_bazaar_price,
            value['sell_moving_week'], longest_sell_moving_week,
            value['max_profit_day'], longest_max_pofit_day,
            value['number_of_items'], longest_number_of_items
        ))
    
    print("-"*total_length)

if __name__ == "__main__":
    # Get npc prices from API
    items_API = get_items_from_API()

    # Get values from API
    products_API = get_products_from_API()

    # Add products
    all_products = []
    for p in products_API:
        # Hide Gemstones (bugged at the moment)
        if p in items_API and not "GEM" in p:
            all_products.append(add_product(
                p,
                items_API[p]['name'],
                items_API[p]['npc_sell_price'],
                round(products_API[p]['quick_status']['sellPrice'], 1),
                products_API[p]['quick_status']['sellMovingWeek']
            ))

    # Calculate profit by product and sort
    sorted_by_profit, sorted_by_profit_formated = calculate_profit_and_sort(all_products)

    # Print table
    print_table(sorted_by_profit_formated)