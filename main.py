from colorama import Fore, init
from modules import *


def main():
    book = load_data() # За замовчунням завантажуємо з addressbook.pkl, якщо існує
    init() # Викликаємо метод init() бібліотеки colorama для коректної роботи
    print("\nWelcome to the assistant bot! Say 'hello' for greetings!")
    while True:
        user_input = input("Enter a command: ")
        # Перевіряємо наявність вводу і, якщо нічого не введено, повторюємо запит
        try:
            command, *args = methods.parse_input(user_input)
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Please, enter any command!{Fore.RESET}")
            continue
        # Обробка введеного запиту
        if command in ["close", "exit"]:
            save_data(book) # За замовчунням зберігаємо в addressbook.pkl при виході
            print("Good bye!\n")
            break
        elif command == "hello":
            print("How can I help you? (Enter 'help' to see commands description)")
        elif command == "help":
            print(help())
        elif command == "add":
            print(methods.add_contact(args, book))
        elif command == "change":
            print(methods.change_contact(args, book))
        elif command == "phone":
            print(f"{Fore.LIGHTBLUE_EX}{methods.show_phone(args, book)}{Fore.RESET}")
        elif command == "add-birthday":
            print(methods.add_contact_birthday(args, book))
        elif command == "show-birthday":
            print(f"{Fore.LIGHTBLUE_EX}{methods.show_birthday(args, book)}{Fore.RESET}")
        elif command == "birthdays":
            methods.show_upcoming_list(book)
        elif command == "del":
            print(f"{Fore.LIGHTBLUE_EX}{methods.remove_contact(args, book)}{Fore.RESET}")    
        elif command == "all":
            methods.show_all(book)

        # Додаткові команди експорту та імпорту даних з csv-файлу
        # Виклик команди імпорту даних з файлу
        elif command == "import-csv":
            if args == []:
                print(f"{Fore.LIGHTRED_EX}ERROR: Enter a valid file-name!{Fore.RESET}")
                continue
            print(f"{Fore.RED}WARNING:{Fore.RESET} All dublicates will be recovered!")
            # Запитуємо підтвердження на імпорт данних з затиранням вже існуючих при співпадінні
            while True:
                command = input("Continue? (y/n): ")
                if command == "y":
                    # Викликаємо функцію імпорту контактів та повертаємо назву 
                    # файлу до змінної file_name_default
                    file_name_default = import_contacts_from_csv(args, book)
                    break
                elif command == "n":
                    break
                else:
                    print(f"{Fore.LIGHTRED_EX}Invalid command.{Fore.RESET}")
        # Виклик команди експорту даних до файлу
        elif command == "export":
            # Якщо книга не пуста
            if book:
                # Якщо не введено назу файлу та раніше було здійснено імпорт, 
                # пропонуємо зберігти дані до раніше відкритого файлу
                if args == [] and file_name_default:
                    if input(f"Would you like to save AddressBook to the file {file_name_default}? (y/n): ") == "y":
                        args = [file_name_default]
                    else: 
                        args = [input("Then give me the file-name!: ")]
                elif args == [] and not file_name_default:
                    print(f"{Fore.LIGHTRED_EX}ERROR: Enter a valid file-name!{Fore.RESET}")
                    break
                export_contacts_to_csv(args, book)
            else:
                print(f"{Fore.LIGHTRED_EX}ERROR: The AddressBook is empty. There is nothing to save!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}Invalid command.{Fore.RESET}")


if __name__ == "__main__":
    main()