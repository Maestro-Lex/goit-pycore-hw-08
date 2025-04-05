from datetime import datetime
from colorama import Fore


def make_phone_valid(phone: str) -> str:
    '''
    Функція, яка перевіряє на валідність номери телефонів 
    та приводить їх до виду +38(ХХХ)ХХХ-ХХ-ХХ
    '''
    # Визначаємо фільтр з допустимими цифрами
    acceptable_symbols = "+0123456789"
    # Видаляємо з номеру телефону всі потрібні нам символи
    trans_table = str.maketrans('', '', acceptable_symbols)
    unwanted_symbols = phone.translate(trans_table)
    # Видаляємо в номері телефону символи, які були виявлені та поміщені до unwanted_symbols
    for ch in unwanted_symbols:
        phone = phone.replace(ch, "")
    # Якщо введений номер менший за 10 цифр та більший за 13 символів, 
    # то повертаємо помилку значення
    if len(phone) < 10 or len(phone) > 13:
        print(f"{Fore.LIGHTYELLOW_EX}INFO:{Fore.RESET} Invalid phone format. \
Must have at least 10 digits, but no more than 12!") 
        raise ValueError
    # Додаємо код країни
    return f"+38({phone[len(phone)-10:-7]}){phone[len(phone)-7:-4]}\
-{phone[len(phone)-4:-2]}-{phone[len(phone)-2:]}"


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # Приводимо ім'я контакту до уніфікованого вигляду при ініціалізації об'єкту
    def __init__(self, value):
        super().__init__(value)
        self.value = self.value.lower().capitalize().strip(",")


class Phone(Field):
    # Робимо переініціалізацію методу __init__ з метою додання перевірки валідності номеру телефону
    def __init__(self, value):
        super().__init__(value)
        self.value = make_phone_valid(self.value)

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        # Перевірка коректності даних
        try:            
            # Перетворюємо рядок на об'єкт datetime
            self.value = datetime.strptime(self.value, "%d.%m.%Y").date()            
        except ValueError:
            print(f"{Fore.LIGHTYELLOW_EX}INFO:{Fore.RESET} Invalid date format. Use DD.MM.YYYY!") 
            raise ValueError

class Record:
    def __init__(self, name: str):
        # Реалізовано зберігання об'єкта Name в окремому атрибуті.
        self.name = Name(name)
        # Реалізовано зберігання списку об'єктів Phone в окремому атрибуті.
        self.phones = []
        # Додаємо поле "birthday"
        self.birthday = None

    def add_phone(self, phone: str):
        '''
        Додання номеру телефону до запису
        '''
        # Приводимо структуру номеру до валідної форми
        phone = make_phone_valid(phone)
        # При доданні номеру телефону до контакту перевіряємо на повтор
        if self.phones: # Якщо список об'єктів запису вже містить номери
            # заносимо значення (телефони) об'єктів Phone в окремий список 
            phone_values_list = [p.value for p in self.phones]
            # Якщо новий телефон ще відстуній, то додаємо новий об'єкт Phone
            if phone not in phone_values_list:
                self.phones.append(Phone(phone))
            else:
                return f"{Fore.LIGHTYELLOW_EX}INFO:{Fore.RESET} {self.name.value} \
already has {phone} among his phone numbers!"
        # Якщо список об'єктів запису ще пустий, то додаємо перший об'єкт Phone
        else:
            self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        '''
        Видалення номеру телефону
        '''
        # Приводимо структуру номеру до валідної форми
        phone = make_phone_valid(phone)
        # Видаляємо номер тільки, якщо він присутній у записі
        for p in self.phones:
            if p.value == phone:
                return [self.phones.remove(p) for p in self.phones if p.value == phone]
        # Якщо номер не знайдено, то повертаємо повідомлення про неможливість операції
        print(f"{Fore.LIGHTYELLOW_EX}INFO:{Fore.RESET} {self.name.value} \
has no {phone} among his phone numbers!")

    def edit_phone(self, old_phone: str, new_phone: str):
        '''
        Редагування номеру телефону
        '''
        # Приводимо структуру номерів до валідної форми
        old_phone = make_phone_valid(old_phone)
        new_phone = make_phone_valid(new_phone)
        # При коригуванні номеру телефону контакта перевіряємо на співпадіння
        if self.phones: # Якщо список об'єктів запису не попржній
            # заносимо значення (телефони) об'єктів Phone в окремий список 
            phone_values_list = [p.value for p in self.phones]
        # Просто видаляємо старий номер, якщо новий співпадає з вже іншим існуючим
        if new_phone in phone_values_list:
            self.remove_phone(old_phone)
            return # прериваємо виконання методу при знайденному співпадінні
        # Інакше, замінюємо старий номер на новий
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return # прериваємо виконання методу при знайденному співпадінні
        print(f"{Fore.LIGHTYELLOW_EX}INFO:{Fore.RESET} {self.name.value} has no {old_phone} among his phone numbers!")

    def find_phone(self, phone: str) -> str:
        '''
        Пошук номеру телефону
        '''
        # Приводимо структуру номеру до валідної форми
        phone = make_phone_valid(phone)
        for p in self.phones:
            if p.value == phone:
                return p.value # Повертаємо значення (номер телефону) об'єкта Phone при співпадінні
        # інакше повертаємо повідомлення про неможливість операції
        print(f"{Fore.LIGHTYELLOW_EX}INFO:{Fore.RESET} {self.name.value} has no {phone} among his phone numbers!")

    def add_birthday(self, birthday: str):
        '''
        Додання дати народження до запису
        '''
        self.birthday = Birthday(birthday)                
            
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"