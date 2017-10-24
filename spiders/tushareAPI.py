
import tushare as ts

class Tushare:
    def __init__(self):
        pass

    def getStockList(self):
        stockList = ts.get_stock_basics()
        list = []
        for code in stockList.index:
            stock = {
                'code': code,
                'name': stockList.loc[code, 'name']
            }
            list.append(stock)
        return list


    def getStockTrade(self):
        return ts.get_today_all()


if __name__ == '__main__':
    Tushare = Tushare()
    print Tushare.getStockTrade()