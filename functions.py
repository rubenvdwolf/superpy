import csv
import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta, date


def def_buy_product(product_name, buy_price, expiration_date):
    with open('bought.csv', 'r') as bought_file, open('current_date.txt') as date_file:
        csv_reader = csv.reader(bought_file)
        id = (len(list(csv_reader))) + 1
        curr_date_str = date_file.readlines()

    with open('bought.csv', 'a', newline='') as bought_file:
        csv_writer = csv.writer(bought_file)
        csv_writer.writerow(
            [id, product_name, curr_date_str[0], buy_price, expiration_date])

    print(f'One {product_name} has been added to the inventory.')


def advance_time(delta_time):
    # advance (change) the date in the txt file
    with open('current_date.txt', 'r') as date_file:
        curr_date_line = date_file.readlines()
    old_date = datetime.strptime(curr_date_line[0], '%Y-%m-%d')
    delta = timedelta(days=delta_time)
    new_date = old_date + delta
    export_date = datetime.strftime(new_date, '%Y-%m-%d')
    with open('current_date.txt', 'w') as date_file, open('bought.csv', 'r') as bought_file, open('sold.csv', 'r') as sold_file:
        date_file.write(export_date)
        print(f'Date advanced with {delta_time} days and is now {export_date}')

        # gather the expired products, and move them to sold.csv with no revenue
        bought_list = list(csv.reader(bought_file))
        sold_list = list(csv.reader(sold_file))
        bought_list_copy = bought_list.copy()
        for bought_row in bought_list:
            for sold_row in sold_list:
                if bought_row[0] == sold_row[1]:
                    bought_list_copy.remove(bought_row)

        expired_products = []
        for product in bought_list_copy:
            if datetime.strptime(product[4], '%Y-%m-%d') < new_date:
                expired_products.append(product)

        with open('sold.csv', 'a', newline='') as sold_file:
            csv_writer = csv.writer(sold_file)
            for product2 in expired_products:
                id = (len(sold_list)) + 1
                csv_writer.writerow([id, product2[0], export_date, 0.0])
        if expired_products != []:
            print(f"In the meantime, {len(expired_products)} products expired.")


def make_table(inventory_list, product_list):
    table = Table(title=inventory_list)

    table.add_column("Product Name", justify="center")
    table.add_column("Count", justify="center")
    table.add_column("Buy Price", justify="center")
    table.add_column("Expiration date", justify="center")

    for row in product_list:
        column_1 = str(row[0])
        column_2 = str(row[1])
        column_3 = str(row[2])
        column_4 = str(row[3])
        table.add_row(column_1, column_2, column_3, column_4)

    console = Console()
    console.print(table)


def inventory_check_now():

    with open('bought.csv', 'r') as bought_file, open('sold.csv', 'r') as sold_file:
        bought_list = list(csv.reader(bought_file))
        sold_list = list(csv.reader(sold_file))
        bought_list_copy = bought_list.copy()
        for bought_row in bought_list:
            for sold_row in sold_list:
                if bought_row[0] == sold_row[1]:
                    bought_list_copy.remove(bought_row)
        count_dict = {}
        for product in bought_list_copy:
            if (product[1], product[3], product[4]) in count_dict:
                count_dict[(product[1], product[3], product[4])] += 1
            else:
                count_dict[(product[1], product[3], product[4])] = 1
        inventory_list = []
        for key in count_dict:
            inventory_list.append([key[0], count_dict[key], key[1], key[2]])

        make_table('Current Inventory', inventory_list)


def inventory_check_yesterday():
    with open('current_date.txt', 'r') as date_file:
        curr_date_line = date_file.readlines()
    curr_date = curr_date_line[0]

    with open('bought.csv', 'r') as bought_file, open('sold.csv', 'r') as sold_file:
        bought_list = list(csv.reader(bought_file))
        sold_list = list(csv.reader(sold_file))
        bought_list_copy = bought_list.copy()
        for bought_row in bought_list:
            for sold_row in sold_list:
                if (bought_row[0] == sold_row[1]) and (sold_row[2] != curr_date):
                    bought_list_copy.remove(bought_row)
        for product in bought_list_copy:
            if product[2] == curr_date:
                bought_list_copy.remove(product)
        count_dict = {}
        for product in bought_list_copy:
            if (product[1], product[3], product[4]) in count_dict:
                count_dict[(product[1], product[3], product[4])] += 1
            else:
                count_dict[(product[1], product[3], product[4])] = 1
        inventory_list = []
        for key in count_dict:
            inventory_list.append([key[0], count_dict[key], key[1], key[2]])

    make_table("Yesterday's Inventory", inventory_list)


def inventory_check_date(requested_date):
    requested_date_datetime = datetime.strptime(requested_date, '%Y-%m-%d')

    with open('bought.csv', 'r') as bought_file, open('sold.csv', 'r') as sold_file:
        bought_list = list(csv.reader(bought_file))
        sold_list = list(csv.reader(sold_file))
        bought_list_copy = bought_list.copy()
        for bought_row in bought_list:
            for sold_row in sold_list:
                if (bought_row[0] == sold_row[1]) and (datetime.strptime(sold_row[2], '%Y-%m-%d') <= requested_date_datetime):
                    bought_list_copy.remove(bought_row)
        bought_list_copy2 = bought_list_copy.copy()
        for product in bought_list_copy:
            if datetime.strptime(product[2], '%Y-%m-%d') > requested_date_datetime:
                bought_list_copy2.remove(product)

        count_dict = {}
        for product in bought_list_copy2:
            if (product[1], product[3], product[4]) in count_dict:
                count_dict[(product[1], product[3], product[4])] += 1
            else:
                count_dict[(product[1], product[3], product[4])] = 1
        inventory_list = []
        for key in count_dict:
            inventory_list.append([key[0], count_dict[key], key[1], key[2]])

    make_table(f"Inentory on {requested_date}", inventory_list)


def def_sell_product(product_name, sell_price):
    with open('bought.csv', 'r') as bought_file, open('sold.csv', 'r') as sold_file:
        bought_list = list(csv.reader(bought_file))
        sold_list = list(csv.reader(sold_file))
        id = (len(sold_list)) + 1
        bought_list_copy = bought_list.copy()
        for bought_row in bought_list:
            for sold_row in sold_list:
                if bought_row[0] == sold_row[1]:
                    bought_list_copy.remove(bought_row)

    with open('current_date.txt') as file:
        curr_date_str = file.readlines()

    product_to_sell = []
    for product in bought_list_copy:
        if product[1] == product_name:
            product_to_sell.append(product)
            break

    if product_to_sell == []:
        print('Error: Product not in stock!')
    else:
        with open('sold.csv', 'a', newline='') as sold_file:
            csv_writer = csv.writer(sold_file)
            csv_writer.writerow(
                [id, product_to_sell[0][0], curr_date_str[0], sell_price])
        print(f'One {product_name} sold for {sell_price}!')


def expired_products():
    product_list = []
    with open('sold.csv', 'r') as sold_file, open('bought.csv', 'r') as bought_file:
        sold_list = list(csv.reader(sold_file))
        bought_list = list(csv.reader(bought_file))
        for sold_item in sold_list:
            if sold_item[3] == '0.0':
                product_list.append(sold_item)
    expired_product_list = []
    for expired_product in product_list:
        for bought_item in bought_list:
            if expired_product[1] == bought_item[0]:
                expired_product_list.append([bought_item[1], bought_item[3], sold_item[2]])

    table = Table(title='Expired Products')

    table.add_column("Product Name", justify="center")
    table.add_column("Money Wasted", justify="center")
    table.add_column("Date Expired", justify="center")

    for row in expired_product_list:
        column_1 = str(row[0])
        column_2 = str(row[1])
        column_3 = str(row[2])
        table.add_row(column_1, column_2, column_3)

    console = Console()
    console.print(table)


def def_revenue_today():
    revenue = 0

    with open('sold.csv', 'r') as sold_file, open('current_date.txt', 'r') as date_file:
        sold_list = list(csv.reader(sold_file))
        curr_date = date_file.readlines()[0]
        for product in sold_list:
            if product[2] == curr_date:
                revenue += float(product[3])

    print(f"Today's revenue so far: {revenue}")


def def_revenue_yesterday():
    revenue = 0

    with open('sold.csv', 'r') as sold_file, open('current_date.txt', 'r') as date_file:
        sold_list = list(csv.reader(sold_file))
        curr_date = date_file.readlines()[0]
        yesterday_date = datetime.strptime(
            curr_date, '%Y-%m-%d') - timedelta(days=1)
        for product in sold_list:
            if datetime.strptime(product[2], '%Y-%m-%d') == yesterday_date:
                revenue += float(product[3])

    print(f"Yesterday's revenue: {revenue}")


def def_revenue_date(requested_date):
    revenue = 0

    try:
        with open('sold.csv', 'r') as sold_file:
            sold_list = list(csv.reader(sold_file))
            requested_date_obj = datetime.strptime(requested_date, '%Y-%m')

            for product in sold_list:
                if (datetime.strptime(product[2], '%Y-%m-%d')).month == requested_date_obj.month and (datetime.strptime(product[2], '%Y-%m-%d')).year == requested_date_obj.year:
                    revenue += float(product[3])

        print(f"The revenue in {requested_date_obj.strftime('%B %Y')} was: {revenue}")
    except ValueError:
        try:
            with open('sold.csv', 'r') as sold_file:
                sold_list = list(csv.reader(sold_file))
                requested_date_obj = datetime.strptime(requested_date, '%Y-%m-%d')

                for product in sold_list:
                   if (datetime.strptime(product[2], '%Y-%m-%d')) == requested_date_obj:
                       revenue += float(product[3])

            print(f"The revenue on {requested_date_obj.strftime('%Y-%m-%d')} was: {revenue}")
        except ValueError:
            print('Please enter a month (format: YYYY-MM) or day (format: YYYY-MM-DD) to view the revenue')


def def_profit_today():
    profit = 0

    with open('bought.csv', 'r') as bought_file, open('sold.csv', 'r') as sold_file, open('current_date.txt', 'r') as date_file:
        bought_list = list(csv.reader(bought_file))
        sold_list = list(csv.reader(sold_file))
        curr_date = date_file.readlines()[0]
        sold_today_list = []
        for sold_item in sold_list:
            if sold_item[2] == curr_date:
                sold_today_list.append(sold_item)
        for sold_item2 in sold_today_list:
            for bought_item in bought_list:
                if sold_item2[1] == bought_item[0]:
                    profit += (float(sold_item2[3]) - float(bought_item[3]))

    print(f"Today's profit so far is: {profit}")


def def_profit_yesterday():
    profit = 0

    with open('bought.csv', 'r') as bought_file, open('sold.csv', 'r') as sold_file, open('current_date.txt', 'r') as date_file:
        bought_list = list(csv.reader(bought_file))
        sold_list = list(csv.reader(sold_file))
        curr_date = date_file.readlines()[0]
        yesterday_date = datetime.strptime(curr_date, '%Y-%m-%d') - timedelta(days=1)
        sold_yesterday_list = []
        for sold_item in sold_list:
            if datetime.strptime(sold_item[2], '%Y-%m-%d') == yesterday_date:
                sold_yesterday_list.append(sold_item)
        for sold_item2 in sold_yesterday_list:
            for bought_item in bought_list:
                if sold_item2[1] == bought_item[0]:
                    profit += (float(sold_item2[3]) - float(bought_item[3]))

    print(f"Yesterday's profit was: {profit}")


def def_profit_date(requested_date):
    profit = 0
    
    try:
        requested_date_obj = datetime.strptime(requested_date, '%Y-%m')

        with open('bought.csv', 'r') as bought_file, open('sold.csv', 'r') as sold_file:
            bought_list = list(csv.reader(bought_file))
            sold_list = list(csv.reader(sold_file))
            sold_date_list = []
            for sold_item in sold_list:
                if (datetime.strptime(sold_item[2], '%Y-%m-%d')).month == requested_date_obj.month and (datetime.strptime(sold_item[2], '%Y-%m-%d')).year == requested_date_obj.year:
                    sold_date_list.append(sold_item)
            for sold_item2 in sold_date_list:
                for bought_item in bought_list:
                    if sold_item2[1] == bought_item[0]:
                        profit += (float(sold_item2[3]) - float(bought_item[3]))

        print(f"The total profit in {requested_date_obj.strftime('%B %Y')} was: {profit}")
    except ValueError:
        try:
            requested_date_obj = datetime.strptime(requested_date, '%Y-%m-%d')

            with open('bought.csv', 'r') as bought_file, open('sold.csv', 'r') as sold_file:
                bought_list = list(csv.reader(bought_file))
                sold_list = list(csv.reader(sold_file))
                sold_date_list = []
                for sold_item in sold_list:
                    if (datetime.strptime(sold_item[2], '%Y-%m-%d')) == requested_date_obj:
                        sold_date_list.append(sold_item)
                for sold_item2 in sold_date_list:
                    for bought_item in bought_list:
                        if sold_item2[1] == bought_item[0]:
                            profit += (float(sold_item2[3]) - float(bought_item[3]))

            print(f"The total profit on {requested_date_obj.strftime('%Y-%m-%d')} was: {profit}")
        except ValueError:
            print('Please enter a month (format: YYYY-MM) or day (format: YYYY-MM-DD) to view the profit')


def def_chart(year):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    revenue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    profit = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    with open('sold.csv', 'r') as sold_file, open('bought.csv', 'r') as bought_file:
            sold_list = list(csv.reader(sold_file))
            requested_year_obj = datetime.strptime(year, '%Y')
            sold_date_list = []
            for product in sold_list:
                count = 0
                for month1 in months:
                    if (datetime.strptime(product[2], '%Y-%m-%d')).month == datetime.strptime(month1, '%b').month and (datetime.strptime(product[2], '%Y-%m-%d')).year == requested_year_obj.year:
                        sold_date_list.append(product)
                        revenue[count] += float(product[3])
                    count += 1
            bought_list = list(csv.reader(bought_file))   
            for sold_item in sold_date_list:
                for bought_item in bought_list:
                    if sold_item[1] == bought_item[0]:
                        count = 0
                        for month1 in months:
                            if (datetime.strptime(sold_item[2], '%Y-%m-%d')).month == datetime.strptime(month1, '%b').month and (datetime.strptime(sold_item[2], '%Y-%m-%d')).year == requested_year_obj.year:
                                profit[count] += (float(sold_item[3]) - float(bought_item[3]))
                            count += 1
    
    xpos = np.arange(len(months))

    plt.xticks(xpos, months)
    plt.xlabel('Profit/Revenue(Month)')
    plt.title(f'Profit and revenue in {year}')
    plt.bar(xpos-0.2, revenue, width=0.4, label="Revenue")
    plt.bar(xpos+0.2, profit, width=0.4, label="Profit")
    plt.legend()
    plt.show()
