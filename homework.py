import datetime as dt


class Record:
    """Класс для объектов ввода данных."""
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = date
        if self.date is None:
            self.date = dt.date.today()
        else:
            date_format = '%d.%m.%Y'
            self.date = dt.datetime.strptime(self.date, date_format).date()


class Calculator:
    """Объявление родительского класса."""
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, new_record):
        """Метод сохранения новой записи."""
        self.records.append(new_record)

    def get_today_stats(self):
        """Метод для вычисления дневного расхода денег/калорий."""
        day = dt.date.today()
        val = [i.amount for i in self.records if i.date == day]
        return sum(val)

    def get_week_stats(self):
        """Метод для определения трат денег/калорий за последний 7 дней."""
        day = dt.date.today()
        val = [i.amount for i in self.records if -1 < (day - i.date).days < 7]
        return sum(val)


class CashCalculator(Calculator):
    """Класс - калькулятор денег."""
    USD_RATE = 75.73
    EURO_RATE = 90.58

    def get_today_cash_remained(self, currency):
        """Метод определения остатка денег."""
        ans = ''
        curr = {'rub': [1, 'руб'],
                'usd': [CashCalculator.USD_RATE, 'USD'],
                'eur': [CashCalculator.EURO_RATE, 'Euro']}
        currency_rate, currency_name = curr[currency]
        current = self.get_today_stats()
        current = current / currency_rate
        lim = self.limit / currency_rate
        res = lim - current
        if res > 0:
            remainder = round(res, 2)
            ans = f'На сегодня осталось {remainder} {currency_name}'
        elif res == 0:
            ans = 'Денег нет, держись'
        else:
            remainder = round(res * (-1), 2)
            ans = (f'Денег нет, держись: твой долг - {remainder} '
                   f'{currency_name}')
        if ans != '':
            return ans
        else:
            return None


class CaloriesCalculator(Calculator):
    """Класс - калькулятор калорий."""

    def get_calories_remained(self):
        """Метод определения остатка калорий."""
        ans = ''
        current = self.get_today_stats()
        res = self.limit - current
        if res > 0:
            ans = ('Сегодня можно съесть что-нибудь ещё, '
                   f'но с общей калорийностью не более {res} кКал')
        else:
            ans = 'Хватит есть!'
        if ans != '':
            return ans
        else:
            return None
