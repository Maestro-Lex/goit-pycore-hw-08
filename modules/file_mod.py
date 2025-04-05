'''
Додатковий модуль для еспорту / імпорту даних AddressBook до файлу
'''
from datetime import datetime
from colorama import Fore
import pickle
from .AddressBook import AddressBook
from .classes import Record 

def load_data(filename="addressbook.pkl"):
    '''
    Функція загрузки книги контактів з файлу
    '''
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено
    
def save_data(book, filename="addressbook.pkl"):
    '''
    Функція збереження у бінарний файл книги контактів 
    '''
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def import_contacts_from_csv(args: list, book: AddressBook) -> str:
    '''
    Функція імпорту записів з файлу. Повертає назву файлу
    '''
    # Перевіряємо на введення назви файлу
    try:
        file_name = args[0].lower().strip()
        # претворюємо назу файйлу на формат csv
        file_name = file_name.split(".")
        if len(file_name) > 1:
            if file_name[1] != "csv":
                file_name = ".".join(file_name) + ".csv"
            else:
                file_name = ".".join(file_name)
        else:
            file_name = file_name[0] + ".csv"
    except Exception:
        print(f"{Fore.LIGHTRED_EX}ERROR: Enter a valid file-name!{Fore.RESET}")
        return
    # Перевіряємо чи файл існує
    try:
        with open(file_name, "r", encoding="UTF-8") as file:            
            for line in file:
                # Перевіряємо, якщо строка не пустаб тощо
                if line not in ["", " ", "-", "\n"]:
                    # Розбираємо нашу строку на елементи ра роздільником та видаляємо пробіли
                    name, phones, birthday = [value.strip() for value in line.split(";")]
                    record = Record(name) # Створюємо запис з імэям з файлу
                    book.add_record(record) # Додаємо запис до книги записів
                    # Додаємо до запису номера телефонів з файлу (із створенням об'єктів Phone)
                    for phone in phones.split(","):
                        record.add_phone(phone)
                    # Додаємо до запису дату народження з файлу (із створенням об'єктів Birthday), 
                    # у разі наявної інформації   
                    if birthday not in ["-", ""]:
                        record.add_birthday(birthday.strip())
            print(f"{Fore.LIGHTBLUE_EX}Contacts added from file {file_name}!{Fore.RESET}")
        return file_name
    except Exception as e:
        if e == FileNotFoundError:
            print(f"{Fore.LIGHTRED_EX}ERROR: File {file_name} not found!{Fore.RESET}")
        else:
            # Якщо дані у файлі з помилками, то отримаємо повідомлення
            print(f"{Fore.LIGHTRED_EX}An ERROR occurred! Check the format for {file_name} data.{Fore.RESET}")

def export_contacts_to_csv(args: list, book: AddressBook):
    '''
    Функція експорту записів до файлу.
    '''
    # Перевіряємо на введення назви файлу
    try:
        file_name = args[0].lower().strip()
        # претворюємо назу файйлу на формат csv
        file_name = file_name.split(".")
        if len(file_name) > 1:
            if file_name[1] != "csv":
                file_name = ".".join(file_name) + ".csv"
            else:
                file_name = ".".join(file_name)
        else:
            file_name = file_name[0] + ".csv"
    except Exception:
        print(f"{Fore.LIGHTRED_EX}ERROR: Enter a valid file-name!{Fore.RESET}")
        return
    # Перевіряємо чи файл існує
    try:
        with open(file_name, "w+", encoding="UTF-8") as file:  
            # У відсортованній книзі беремо значення об'єктів та заносимо їх до файлу
            for name, record in sorted(book.data.items()):
                phones = ",".join(p.value for p in record.phones)
                # Якщо об'єкт Birthday у записі існує, то записуємо його значення у змінну
                if record.birthday:
                    birthday = record.birthday.value.strftime("%d.%m.%Y")
                else:
                    birthday = "-"
                # Записуємо строку з інформацією запису у файл
                file.write(f"{name};{phones};{birthday}\n")
        print(f"{Fore.LIGHTBLUE_EX}Contacts saved to file {file_name}!{Fore.RESET}")
    except FileNotFoundError:
        # Якщо дані у файлі з помилками, то отримаємо повідомлення
        print(f"{Fore.LIGHTRED_EX}ERROR: File {file_name} can't be writed!{Fore.RESET}")