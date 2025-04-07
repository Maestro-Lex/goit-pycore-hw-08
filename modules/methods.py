'''
Модуль, який містить всі наші методи для бота
'''
from datetime import datetime
from colorama import Fore
from .AddressBook import AddressBook
from .classes import Record 


def parse_input(user_input: str) -> list:
    '''
    Парсер команд
    '''
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower() # Робимо введення команд нечутливим до регистру
    return cmd, *args


def input_error(func):
    '''
    Функція-декоратор для обробки помилок команд.
    '''
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)        
        except ValueError:
            if func.__name__ == "add_contact_birthday":
                return f"{Fore.LIGHTRED_EX}ERROR: Give me name and valid birthday, please!{Fore.RESET}"
            if func.__name__ == "show_upcoming_list":
                return f"{Fore.LIGHTRED_EX}ERROR: Give me name and valid days number, please!{Fore.RESET}"
            return f"{Fore.LIGHTRED_EX}ERROR: Give me name and valid phone, please!{Fore.RESET}"            
        except KeyError:
            return f"{Fore.LIGHTRED_EX}ERROR: There is no such user!{Fore.RESET}"     
        except IndexError:
            return f"{Fore.LIGHTRED_EX}ERROR: Enter user name!{Fore.RESET}"
        except AttributeError:
            return f"{Fore.LIGHTRED_EX}ERROR: Contact has not that value yet!{Fore.RESET}"
    return inner

@input_error
def add_contact(args: list, book: AddressBook):
    '''
    Команда додання імені та номерів до списку контактів 
    '''
    name, *phones = args
    # Приводимо введене ім'я до уніфікованого вигляду
    name = name.lower().capitalize().strip(",")
    # Не через book.find(name), бо за відсутності запису при його доданні 
    # ще повертає й повідомлення про його відсутність
    record = book.data.get(name)
    # Якщо запис відсутній, то створюємо його
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."
    # Якщо не введено жодного номеру, то викликаємо помилку
    if not phones:
        raise ValueError
    # Заносимо до запису всі введені телефони та формуємо повідомлення у разі повторення деяких з них
    for phone in phones:
        # Водночас викликаємо метод add_phone та передаємо те, що він повертає до змінної 
        # add_phone_message (або None або повідомлення)
        add_phone_message = record.add_phone(phone.strip(","))
        if add_phone_message:
            message += f"\n{add_phone_message}"
    return f"{Fore.LIGHTGREEN_EX}{message}{Fore.RESET}"

@input_error
def change_contact(args: list, book: AddressBook) -> str:
    '''
    Команда зміни старого номеру телефону за ім'ям контакту на новий
    '''
    name, *phones = args
    # Приводимо введене ім'я до уніфікованого вигляду
    name = name.lower().capitalize().strip(",")
    # Робимо пошук запису у книзі та повертаємо його за наявності. Інакше викликаємо помилку
    record = book.find(name)
    if record is None:
        raise KeyError
    # Перевіряємо, що введено не менше двох валідних номерів телефону - старого та нового
    if len(phones) < 2:
        print(f"{Fore.LIGHTYELLOW_EX}INFO:{Fore.RESET} There are must be 2 phone numbers for change!")
        raise ValueError
    # Якщо старий номер телефону знайдено у записі контакту, 
    # то замінюємо його на новий. Інакше викликаємо помилку
    if record.find_phone(phones[0]):
        record.edit_phone(phones[0], phones[1])
        return f"{Fore.LIGHTGREEN_EX}Contact updated.{Fore.RESET}"
    else:
        raise ValueError

@input_error
def show_phone(args: list, book: AddressBook) -> str:
    '''
    Команда, що виводить номер телефону за ім'ям контакту, у разі його наявності
    '''
    # Приводимо введене ім'я до уніфікованого вигляду
    name = args[0].lower().capitalize().strip(",")
    # Повертаємо знайдені номери телефонів
    return '; '.join(p.value for p in book.find(name).phones)

@input_error
def add_contact_birthday(args: list, book: AddressBook) -> str:
    '''
    Команда додання контакту дати народження за його ім'ям
    '''
    name, birthday = args
    # Приводимо введене ім'я до уніфікованого вигляду
    name = name.lower().capitalize().strip(",")
    # Робимо пошук запису у книзі та повертаємо його за наявності. Інакше викликаємо помилку
    record = book.find(name)
    record.add_birthday(birthday)
    return f"{Fore.LIGHTGREEN_EX}Birthday added.{Fore.RESET}"

@input_error
def show_birthday(args: list, book: AddressBook) -> str:
    '''
    Команда, що виводить дату народження за ім'ям контакту, у разі його наявності
    '''
    # Приводимо введене ім'я до уніфікованого вигляду
    name = args[0].lower().capitalize().strip(",")
    # Повертаємо дату у вигляді рядка формату "ДД.ММ.РРРР"
    return book.find(name).birthday.value.strftime("%d.%m.%Y")

@input_error
def show_upcoming_list(args: list, book: AddressBook) -> list:
    '''
    Команда формавання таблиці із мписком іменинників на найближчі days_to дні
    '''
    try:
        days_to = args[0].strip(" ").strip(",")
        days_to = int(days_to)
    except IndexError:
        days_to = 7
    # Отримаємо список найближчих іменинників з AddressBook та редагуємо для табличного виводу
    congrats_list = book.get_upcoming_birthdays(days_to)
    if congrats_list:       
        congrats_list_str = f"  Список іменинників на наступні {days_to} днів: \n-------------------------------------------\n\
|{'name':^15}|{'congratulation_date':^25}|\n-------------------------------------------\n"   
        for item in congrats_list:
            congrats_list_str += f"|{item["name"]:<15}|{item["congratulation_date"]:^25}|\n"
        congrats_list_str += "-------------------------------------------"
        return congrats_list_str
    return f"В найближчі {days_to} днів немає іменинників!"

@input_error
def remove_contact(args: list, book: AddressBook) -> str:
    '''
    Команда, що видаляє контакт за ім'ям користувача, у разі його наявності
    '''
    book.delete(args[0].lower().capitalize().strip(","))
    return f"{Fore.LIGHTGREEN_EX}Contact deleted.{Fore.RESET}"

def show_all(book: AddressBook) -> str:
    '''
    Команда виводу всього списку контактів із сортуванням за ім'ям користувача у вигляді таблиці
    '''
    if book:            
        contacts_list_str = f"------------------------------------------------\n\
|{'name':^15}|{'birthday':^12}|{'phone number':^17}|\n------------------------------------------------\n"   
        for name, record in sorted(book.data.items()):
            if record.birthday:
                birthday = record.birthday.value.strftime("%d.%m.%Y")
            else:
                birthday = ''
            phone_values_list = [p.value for p in record.phones]
            contacts_list_str += f"|{name:<15}|{birthday:^12}|{'|\n|               |            |'.join(phone_values_list):<17}|\n"
        contacts_list_str += "------------------------------------------------"
        print(f"{Fore.LIGHTBLUE_EX}{contacts_list_str}{Fore.RESET}")
        # Повертаємо список контактів для можливих подальших обробок
        return contacts_list_str
    print(f"{Fore.LIGHTRED_EX}Contact list is empty!{Fore.RESET}")
    #{book.find(name).birthday.value.strftime("%d.%m.%Y")}|