import json
import os
import hashlib
FILENAME = "data.json"
user_items = { # Список предметов и их описаний
    "Экскалибур": {"description": "Легендарный меч короля Артура"},
    "Кольцо": {"description": "Магическое кольцо"},
    "Меч": {"description": "Обычный меч"},
    "Щит": {"description": "Обычный щит"},
    "Зелье": {"description": "Волшебное зелье"},
    "Лук": {"description": "Длинный лук"}

}
# Команды для консоли администратора и создателя
def delete_user(): # Команда для удаления пользователя
    users_list()
    user_name = input("Введите имя пользователя для удаления: ").strip()
    
    if user_name not in users:
        print("Пользователь не найден.")
        return
    elif user_name == name:
        print("Вы не можете удалить самого себя.")
        return
    else: 
        confirm = input(f"Вы точно хотите удалить пользователя {user_name}? (да/нет) ").strip().lower()
        if confirm == "да":
            users.pop(user_name)  # или del users[user_name]
            save_users(users)
            print(f"Пользователь {user_name} успешно удалён.")
        else:
            print("Удаление отменено.")
            
def help_console(): # Команда для вывода списка команд
    print("Доступные команды:")
    for cmd, details in commands.items():
        minimum_level = details.get("min_level")
        print(f"Команда = {cmd}, минимальный уровень = {minimum_level}")

def add_item(): # Команда для добавления предмета в инвентарь пользователя
    users_list()
    user_name = input("Введите имя пользователя для добавления предмета: ").strip()
    item = input("Введите название предмета для добавления в инвентарь: ").strip().capitalize()
    inventory = users[user_name].get("inventory", [])
    if any(i["name"] == item for i in inventory):
        print("У пользователя уже есть этот предмет в инвентаре.")
        return
    else:
        if item not in user_items:
            print("Такого предмета не существует.")
            return
        elif user_name not in users:
            print("Пользователь не найден.")
            return
        else:
            # Получаем описание предмета
            description = user_items[item]["description"]
            # Добавляем предмет и описание в инвентарь пользователя
            users[user_name].setdefault("inventory", []).append({"name": item, "description": description})
            save_users(users)
            print(f"Предмет '{item}' добавлен в инвентарь игрока {user_name}. Описание: {description}")
            return
    
def view_users(): # Команда для просмотра списка всех пользователей
    users_list()
    return

def ban_user(): # Команда для бана пользователя
    users_list()
    user_to_ban = input("Введите имя пользователя для бана: ").strip()
    if user_to_ban == name:
        print("Вы не можете забанить самого себя.")
        return
    else:
        if user_to_ban in users:
            users[user_to_ban]["banned"] = True
            save_users(users)
            print(f"Пользователь {user_to_ban} забанен.")
        else:
            print("Пользователь не найден.")
            return
    
def unban_user(): # Команда для разбана пользователя
    users_list()
    user_to_unban = input("Введите имя пользователя для разбана: ").strip()
    if user_to_unban in users:
        users[user_to_unban]["banned"] = False
        save_users(users)
        print(f"Пользователь {user_to_unban} разбанен.")
        return
    else:
        print("Пользователь не найден.")
        return
    
def promote_user(): # Команда для повышения уровня пользователя
    users_list()
    user_to_promote = input("Введите имя пользователя для повышения: ").strip()
    if user_to_promote not in users:
        print("Такого пользователя не существует.")
        return
    elif users[user_to_promote].get("admin_level", 0) >= users[name].get("admin_level", 0):
        print("Вы не можете повысить пользователя до уровня равного или выше вашего.")
        return
    elif user_to_promote == name:
        print("Вы не можете повысить самого себя.")
        return
    else:
        if user_to_promote in users:
            users[user_to_promote]["admin_level"] += 1
            save_users(users)
            print(f"Пользователь {user_to_promote} повышен до уровня {users[user_to_promote]['admin_level']}.")
            return
        else:
            print("Пользователь не найден.")
            return
    
def leave_console(): # Команда для выхода из консоли
    print("Выход из консоли.")
    return   


# Функции для работы с файлами    
def load_users(): # Функция для загрузки пользователей из файла
        if not os.path.exists("data.json"):
            return {}

        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("users", {})

def save_users(users): # Функция для сохранения пользователей в файл
    data = {}

        # если файл уже есть — не затираем items
    if os.path.exists("data.json"):
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

    data["users"] = users

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# Консоли
def admin_console(name): # Консоль администратора
    password = input("Введите ваш пароль администратора: ").strip()
    if check_login(name, password):
        print(f"Добро пожаловать, администратор {name}!")
        move = input("Выберите действие:  1. Войти в консоль администратора, 2. Просмотреть инвентарь, 3. Выйти из аккаунта").strip()

        if move == "1":
            print("(Чтобы выйти из консоли, введите 'comm.leave'), чтобы получить список команд, введите 'comm.help'")
            while True:
                    cmd = input("Введите команду").strip()
                    if cmd in commands:
                        result = check_level(name, cmd)
                        if cmd == "comm.leave":
                            leave_console()
                            break
                        else:
                            if result:
                                commands[cmd]["func"]()
                                continue
                            else:
                                print("У вас недостаточно прав для выполнения этой команды.")
                                continue

                    else:
                        print("Неизвестная команда.")
                        continue
        elif move == "2":
            inventory = users[name].get("inventory", [])
            if inventory:
                print("Ваш инвентарь:")
                for item in inventory:
                    it_name = item.get("name", "Нет имени")
                    description = item.get("description", "Нет описания")
                    print(f"- {it_name}, ({description})")
                    continue
            else:
                print("Ваш инвентарь пуст.")
                return
        elif move == "3":
            print("Выход из аккаунта.")
            return
        else:
            print("Неверное действие.")
            return
    else:
        print("Неверный пароль администратора")
        return
    
def creator_console(name): # Консоль создателя
    password = input("Введите ваш пароль создателя: ").strip()
    if check_login(name, password):
        print(f"Добро пожаловать, создатель {name}!")
        while True:
            move = input("Выберите действие:  1. Войти в консоль создателя, 2. Просмотреть инвентарь, 3. Выйти из аккаунта").strip()

            if move == "1":
                print("(Чтобы выйти из консоли, введите 'comm.leave'), чтобы получить список команд, введите 'comm.help'")
                while True:
                        cmd = input("Введите команду").strip()
                        if cmd in commands:
                            result = check_level(name, cmd)
                            if cmd == "comm.leave":
                                leave_console()
                                break
                            else:
                                if result:
                                    commands[cmd]["func"]()
                                    continue
                                else:
                                    print("У вас недостаточно прав для выполнения этой команды.")
                                    continue

                        else:
                            print("Неизвестная команда.")
                            continue
            elif move == "2":
                inventory = users[name].get("inventory", [])
                if inventory:
                    print("Ваш инвентарь:")
                    for item in inventory:
                        it_name = item.get("name", "Нет имени")
                        description = item.get("description", "Нет описания")
                        print(f"- {it_name}, ({description})")
                        continue
                else:
                    print("Ваш инвентарь пуст.")
                    continue
            elif move == "3":
                print("Выход из аккаунта.")
                return
            else:
                print("Неверное действие.")
                return
    else:
        print("Неверный пароль создателя")
        return

def user_console(name): # Консоль обычного пользователя
    while True:
        password = input("Введите ваш пароль: ").strip()

        if check_login(name, password):
            print(f"Добро пожаловать, пользователь {name}!")
            action = input("Выберите действие: 1. Просмотреть инвентарь 2. Выйти")
            if action == "1":
                inventory = users[name].get("inventory", [])
                if inventory:
                    print("Ваш инвентарь:")
                    for item in inventory:
                        it_name = item.get("name", "Нет имени")
                        description = item.get("description", "Нет описания")
                        print(f"- {it_name}, ({description})")
                        continue
                else:
                    print("Ваш инвентарь пуст.")
                    continue
            if action == "2":
                print("Выход.")
                return
        else:
            print("Неверный пароль")
            return False
        return
    

# Вспомогательные функции
users = load_users()
def check_login(name, password): # Функция для проверки логина и пароля
    hashed_input = hash_password(password)
    if users[name]["password"] == hashed_input:
        return True
    else:
        return False

def hash_password(password): # Функция для хеширования пароля
    return hashlib.sha256(password.encode()).hexdigest()

def users_list(): # Функция для вывода списка всех пользователей с их статусами
    for name, info in users.items():
        if info.get("banned"):
            status = "забанен"
        else:
            status = "не забанен"

        if info.get("admin_level", 0) == 5:
            status1 = "создатель"
        elif info.get("admin_level", 0) >= 1:
            status1 = "администратор"
        else:
            status1 = "обычный пользователь"
        print(f"{name} = {status}, {status1}")

def check_level(name, cmd): # Функция для проверки уровня пользователя для выполнения команды
    user_level = users[name].get("admin_level", 0)
    command_info = commands.get(cmd)
    if command_info and user_level >= command_info["min_level"]:
        return True
    else:
        return False
    
def check_user(name): # Функция для проверки имени пользователя
    if not name:
        return"Имя не может быть пустым."
    elif any(c in name for c in '\\/:*?"<>|-)(№@;$,=+'):
        return "Имя содержит недопустимые символы."
    elif users.get(name, {}).get("banned", False):
        return "Ваш аккаунт заблокирован. Обратитесь к администратору."
    else:
        return True

def check_password(password): # Функция для проверки пароля пользователя
    if not password:
        return"Пароль не может быть пустым."
    elif any(c in password for c in '\\/:?"<>|`~'):
        return "Пароль содержит недопустимые символы."

    elif len(password) < 4:
        return "Пароль должен быть не менее 4 символов."
    return True

def registration(): # Функция для регистрации нового пользователя
    while True:
        password = input("Придумайте пароль: ").strip()
        password_check = check_password(password)
        if password_check != True:
            print(password_check)
            continue
        else:
            users[name] = {
                "password": hash_password(password),
                "banned": False,
                "inventory": [],  # <-- создаём пустой инвентарь сразу
                "admin_level": 0

            }

            save_users(users)
            print(f"Аккаунт {name} создан")
            return

def get_status(info): # Функция для получения статуса пользователя
    if info.get("admin_level", 0) == 5:
        return "создатель"
    elif info.get("admin_level", 0) >= 1:
        return "администратор"
    else:
        return "обычный пользователь"

commands = { # Команды и их минимальные уровни
    "comm.view": {
        "min_level": 1,
        "func": view_users
    },
    "comm.ban": {
        "min_level": 2,
        "func": ban_user
    },
    "comm.unban": {
        "min_level": 2,
        "func": unban_user
    },
    "comm.promote": {
        "min_level": 4,
        "func": promote_user
    },
    "comm.leave": {
        "min_level": 1,
        "func": leave_console
    },
    "comm.help": {
        "min_level": 1,
        "func": help_console
    },
    "comm.additem": {
        "min_level": 3,
        "func": add_item
    },
    "comm.deleteuser": {
        "min_level": 5,
        "func": delete_user
    }
}
# Главный цикл программы
while True:
    name = input("Введите ваше имя: ").strip()
    result = check_user(name)
    if result != True:
        print(result)
        continue
    else:
        if name not in users:
            choice = input("Пользователь не найден, хотите создать новый аккаунт? (да/нет)").strip().lower()
            if choice == "да":
                registration()
            elif choice == "нет":
                print("Регистрация отменена.")
                continue
            else:
                print("Некорректный ввод. Пожалуйста, введите 'да' или 'нет'.")
                continue
        else:   
            if get_status(users[name]) == "создатель":
                creator_console(name)
                answer = input("Хотите выйти из приложения? (да/нет)").strip().lower()
                if answer == "да":
                    print("Выход из приложения.")
                    break
                elif answer == "нет":
                    continue
                else:
                    print("Некорректный ввод. Продолжаем работу.")
                    continue
            elif get_status(users[name]) == "администратор":
                admin_console(name)
                answer = input("Хотите выйти из приложения? (да/нет)").strip().lower()
                if answer == "да":
                    print("Выход из приложения.")
                    break
                elif answer == "нет":
                    continue
                else:
                    print("Некорректный ввод. Продолжаем работу.")
                    continue
            else:
                user_console(name)
                answer = input("Хотите выйти из приложения? (да/нет)").strip().lower()
                if answer == "да":
                    print("Выход из приложения.")
                    break
                elif answer == "нет":
                    continue
                else:
                    print("Некорректный ввод. Продолжаем работу.")
                    continue