from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
from misc import config


uo = urlopen(config['EXCHANGE_RATE']['url'], context=ssl.SSLContext())
page = uo.read()
soup = BeautifulSoup(page, "html.parser")
divWrap = soup.find('div', {'class': 'exchangeRates__content--wraps-content'})
divList = divWrap.find('div')
rows = divList.find_all('ul')

cb = []
sale = []
purchase = []

i = 0
for row_num in range(1, 6):
    row = rows[row_num]
    cells = row.find_all('li')
    st = ''
    for cell in cells:
        i += 1
        if i == 3:
            txt = cell.getText()
            cb.append(txt)
        elif i == 4:
            txt = cell.getText()
            purchase.append(txt)
        elif i == 5:
            txt = cell.getText()
            sale.append(txt)
    i = 0


cb_ex_rates = "🇺🇸 1 USD: %s\n" \
              "🇪🇺 1 EUR: %s\n" \
              "🇬🇧 1 GBP: %s\n" \
              "🇯🇵 1 JPY: %s\n" \
              "🇨🇭 1 CHF: %s" % (str(cb[0]), str(cb[1]), str(cb[2]), str(cb[3]), str(cb[4]))
purchase_sale_ex_rates = "🇺🇸 1 USD: %s - %s\n" \
                         "🇪🇺 1 EUR: %s - %s\n" \
                         "🇬🇧 1 GBP: %s - %s\n" \
                         "🇯🇵 1 JPY: %s - %s\n" \
                         "🇨🇭 1 CHF: %s - %s" % (
                             str(sale[0]), str(purchase[0]), str(sale[1]), str(purchase[1]), str(sale[2]),
                             str(purchase[2]),
                             str(sale[3]), str(purchase[3]), str(sale[4]), str(purchase[4]))


def purchase_calculator(cost, lang):
    result = cost * float(purchase[0])
    if lang == 2:
        return "$" + str(cost) + " sotib olish uchun, " + str(f"{result:,}") + " so'm kerak bo'ladi"
    elif lang == 1:
        return "Для покупки $" + str(cost) + ", вам необходимо " + str(f"{result:,}") + " сум"
    elif lang == 3:
        return "$" + str(cost) + " сотиб олиш учун, " + str(f"{result:,}") + " сўм керак бўлади"


def sale_calculator(cost, lang):
    result = cost * float(sale[0])
    if lang == 2:
        return "$" + str(cost) + " sotish uchun, " + str(f"{result:,}") + " so'm kerak bo'ladi"
    elif lang == 1:
        return "Для продажи $" + str(cost) + ", вам необходимо " + str(f"{result:,}") + " сум"
    elif lang == 3:
        return "$" + str(cost) + " сотиш учун, " + str(f"{result:,}") + " сўм керак бўлади"