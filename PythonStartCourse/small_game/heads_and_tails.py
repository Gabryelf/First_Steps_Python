
def input_choice() -> bool:
    choice = input("Выбери сторону: орел или решка").strip().lower()
    print("Вы выбрали " + choice)
    return choice == "орел"


def is_win(coin: int, choice: bool):
    if coin == choice:
        print("Вы угадали! Победа!")
    else:
        print("Это не верно! Попробуй еще!")


def main():
    import random
    coin = random.randint(0, 1)
    choice = input_choice()
    is_win(coin, choice)


while True:
    main()



