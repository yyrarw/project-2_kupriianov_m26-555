import prompt


def print_welcome_help():
    """Печатает список доступных команд."""
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")


def welcome():
    """Приветствует пользователя и обрабатывает команды help и exit."""
    print("Первая попытка запустить проект!")
    print()
    print("***")
    print_welcome_help()
    while True:
        command = prompt.string("Введите команду: ").strip()
        if command == "exit":
            break
        if command == "help":
            print()
            print_welcome_help()
