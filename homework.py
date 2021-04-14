import datetime as dt


class Record:
    """Класс для объектов ввода данных."""
    def __init__(self, amount, comment, date=dt.datetime.now().date()):
        self.amount = amount
        self.comment = comment
        self.date = date
        if type(self.date) == str:
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
        count = 0
        day = dt.datetime.now().date()
        for i in self.records:
            if i.date == day:
                count = count + i.amount
        return count

    def get_week_stats(self):
        """Метод для определения трат денег/калорий за последний 7 дней."""
        count = 0
        day = dt.datetime.now().date()
        for i in self.records:
            if -1 < (day-i.date).days < 7:
                count = count + i.amount
        return count


class CashCalculator(Calculator):
    """Класс - калькулятор денег."""
    USD_RATE = 75.73
    EURO_RATE = 90.58

    def get_today_cash_remained(self, currency):
        """Метод определения остатка денег."""
        ans = ''
        index = ''
        current = 0
        day = dt.datetime.now()
        for i in self.records:
            if i.date == day.date():
                current = current + i.amount
        if currency == 'usd':
            current = current / CashCalculator.USD_RATE
            lim = self.limit / CashCalculator.USD_RATE
            index = 'USD'
        elif currency == 'eur':
            current = current / CashCalculator.EURO_RATE
            lim = self.limit / CashCalculator.EURO_RATE
            index = 'Euro'
        else:
            lim = self.limit
            index = 'руб'
        if current < lim:
            remainder = round(lim - current, 2)
            ans = f'На сегодня осталось {remainder} {index}'
        elif current == lim:
            ans = 'Денег нет, держись'
        else:
            remainder = round(current - lim, 2)
            ans = f'Денег нет, держись: твой долг - {remainder} {index}'
        if ans != '':
            return ans
        else:
            return None


class CaloriesCalculator(Calculator):
    """Класс - калькулятор калорий."""

    def get_calories_remained(self):
        """Метод определения остатка калорий."""
        ans = ''
        current = 0
        day = dt.datetime.now()
        for i in self.records:
            if i.date == day.date():
                current = current + i.amount
        if current < self.limit:
            remainder = self.limit - current
            ans = (f'Сегодня можно съесть что-нибудь ещё, '
                   f'но с общей калорийностью не более {remainder} кКал')
        else:
            ans = 'Хватит есть!'
        if ans != '':
            return ans
        else:
            return None
