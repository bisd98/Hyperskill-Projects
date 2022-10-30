class CoffeeMachine:
    recipes = {'espresso': [250, 0, 16, 4, 1], 'latte': [350, 75, 20, 7, 1], 'cappuccino': [200, 100, 12, 6, 1]}
    resources = {'water': 400, 'milk': 540, 'beans': 120, 'money': 550, 'cups': 9}

    @staticmethod
    def action(option):
        if option == 'buy':
            CoffeeMachine.buy()
        elif option == 'fill':
            CoffeeMachine.fill()
        elif option == 'take':
            CoffeeMachine.take()
        elif option == 'remaining':
            CoffeeMachine.remaining()
        elif option == 'exit':
            exit()

    @staticmethod
    def remaining():
        print('\nThe coffee machine has:\n'
              f"{CoffeeMachine.resources['water']} ml of water\n"
              f"{CoffeeMachine.resources['milk']} ml of milk\n"
              f"{CoffeeMachine.resources['beans']} g of coffee beans\n"
              f"{CoffeeMachine.resources['cups']} disposable cups\n"
              f"${CoffeeMachine.resources['money']} of money")

    @staticmethod
    def check_status(coffee):
        index = 0
        if CoffeeMachine.recipes[coffee][3] > CoffeeMachine.resources['money']:
            return 'money'
        for v in CoffeeMachine.resources.values():
            if v < CoffeeMachine.recipes[coffee][index]:
                out_of_stock = [x for x in CoffeeMachine.resources if CoffeeMachine.resources[x] == v]
                return out_of_stock[0]
            index += 1
        return 'good'

    @staticmethod
    def buy():
        choice = input('\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:\n')
        if choice == '1':
            coffee = 'espresso'
        elif choice == '2':
            coffee = 'latte'
        elif choice == '3':
            coffee = 'cappuccino'
        else:
            return 0
        status = CoffeeMachine.check_status(coffee)
        if status in CoffeeMachine.resources.keys():
            print(f'Sorry, not enough {status}!')
        else:
            print('I have enough resources, making you a coffee!')
            CoffeeMachine.resources['water'] -= CoffeeMachine.recipes[coffee][0]
            CoffeeMachine.resources['milk'] -= CoffeeMachine.recipes[coffee][1]
            CoffeeMachine.resources['beans'] -= CoffeeMachine.recipes[coffee][2]
            CoffeeMachine.resources['money'] += CoffeeMachine.recipes[coffee][3]
            CoffeeMachine.resources['cups'] -= CoffeeMachine.recipes[coffee][4]

    @staticmethod
    def fill():
        CoffeeMachine.resources['water'] += int(input('Write how many ml of water you want to add:\n'))
        CoffeeMachine.resources['milk'] += int(input('Write how many ml of milk you want to add:\n'))
        CoffeeMachine.resources['beans'] += int(input('Write how many grams of coffee beans you want to add:\n'))
        CoffeeMachine.resources['cups'] += int(input('Write how many disposable cups you want to add:\n'))

    @staticmethod
    def take():
        print(f"I gave you ${CoffeeMachine.resources['money']}")
        CoffeeMachine.resources['money'] = 0


while True:
    CoffeeMachine.action(input('Write action (buy, fill, take, remaining, exit):\n'))
