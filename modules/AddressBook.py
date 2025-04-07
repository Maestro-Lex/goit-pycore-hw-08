from collections import UserDict
from datetime import datetime, timedelta
from colorama import Fore
from .classes import Record 


class AddressBook(UserDict):
    def add_record(self, record: Record):
        '''
        Метод додавання запису до книги, у разі його відсутності
        '''
        # ключ - значення імені запису; значення - сам запис як об'єкт Record
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        '''
        Пошук запису за ім'ям
        '''
        # Приводимо введене ім'я до уніфікованого вигляду
        name = name.lower().capitalize().strip(",")
        # Виконуємо пошук елементу та у разі його відстуності викликаємо помилку із повідомленням
        if name in self.data.keys():
            return self.data.get(name)
        print(f"{Fore.LIGHTYELLOW_EX}INFO:{Fore.RESET} There is no contact {name} in our AddressBook!")
        raise KeyError

    def delete(self, name: str) -> Record:
        '''
        Видалення запису за ім'ям (з поверненням видаленого запису)
        '''
        # Приводимо введене ім'я до уніфікованого вигляду
        name = name.lower().capitalize().strip(",")
        # Виконуємо пошук елементу та у разі його відстуності викликаємо помилку із повідомленням
        if name in self.data.keys():
            return self.data.pop(name)
        print(f"{Fore.LIGHTYELLOW_EX}INFO:{Fore.RESET} There is no contact {name} in our AddressBook!")
        raise KeyError
    
    def get_upcoming_birthdays(self, days_to):
        '''
        Функція повернутає список всіх, у кого день народження вперед на 7 днів включаючи поточний день, 
        з перенесенням вихідних.
        '''
        today = datetime.today().date()
        congrats_list = []
        # Проходимося по списку та аналізуємо дати народження кожного користувача
        for name, record in self.data.items():
            if not record.birthday:
                continue
            user_birthday_this_year = record.birthday.value.replace(year = today.year)
            # Перевіряємо, чи вже минув день народження в цьому році
            if user_birthday_this_year < today:
                user_birthday_this_year = record.birthday.value.replace(year = today.year + 1)
            # Визначаємо різницю між днем народження та поточним днем
            days_to_user_birthday_this_year = user_birthday_this_year.toordinal() - today.toordinal()
            # Перевіряємо, чи день народження припадає на вихідний
            if user_birthday_this_year.weekday() > 4:
                days_to_user_congrats = days_to_user_birthday_this_year + (7 - user_birthday_this_year.weekday())
            else:
                days_to_user_congrats = days_to_user_birthday_this_year
            # Відбираємо тих, чий день народження відбувається протягом наступного тижня
            if days_to_user_birthday_this_year < days_to:
                user_congrats_day = today + timedelta(days = days_to_user_congrats)
                user_congrats_day = user_congrats_day.strftime("%d.%m.%Y")
                congrats_list.append({"name": name, "congratulation_date": user_congrats_day})
        return congrats_list