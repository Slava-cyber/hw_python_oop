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

    def res(self):
        """Подсчет остатка."""
        current = self.get_today_stats()
        return self.limit - current


class CashCalculator(Calculator):
    """Класс - калькулятор денег."""
    USD_RATE = 75.73
    EURO_RATE = 90.58

    def get_today_cash_remained(self, currency):
        """Метод определения остатка денег."""
        if self.res() == 0:
            return 'Денег нет, держись'
        else:
            curr = {'rub': [1, 'руб'],
                    'usd': [CashCalculator.USD_RATE, 'USD'],
                    'eur': [CashCalculator.EURO_RATE, 'Euro']}
            currency_rate, currency_name = curr[currency]
            current = self.get_today_stats()
            current = current / currency_rate
            lim = self.limit / currency_rate
            remainder = round(abs(lim - current), 2)
            if self.res() > 0:
                return f'На сегодня осталось {remainder} {currency_name}'
            else:
                return (f'Денег нет, держись: твой долг - {remainder} '
                        f'{currency_name}')


class CaloriesCalculator(Calculator):
    """Класс - калькулятор калорий."""

    def get_calories_remained(self):
        """Метод определения остатка калорий."""
        if self.res() > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {self.res()} кКал')
        else:
            return 'Хватит есть!'
