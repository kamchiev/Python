try:
    file_products = open('C:\\Users\\khayo\\Desktop\\exam problems\\HACKING\\products.txt')
    file_purchases = open('C:\\Users\\khayo\\Desktop\\exam problems\\HACKING\\purchases.txt')
    f_products = file_products.readlines()
    f_purchases = file_purchases.readlines()
except IOError as myeror:
    print("Please, user be kind", myeror)


def main():

    rr = check(f_products, f_purchases)

    print('Suspicious transactions list')
    for i in rr:
        string = ''
        for k in i[2]:
            string += k + ' '
        if [i[1]] != i[2]:
            print(f'Product code: {i[0]}\nOfficial dialer: {i[1]}\nDealer list: {string.strip(",")}')
            print()


def check(products, purchases):

    lst_full = []
    for row in products:
        row_s = row.split()

        dealers = []
        for item in purchases:
            item_s = item.split()

            if row_s[0].strip('\n') == item_s[0].strip('\n'):

                dealers.append(item_s[1].strip('\n'))

        if len(dealers) > 0:
            lst_full.append([row_s[0], row_s[1], dealers])

    return lst_full


main()






