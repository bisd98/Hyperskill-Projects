import random
import math
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
table = """ CREATE TABLE card (
            id INTEGER PRIMARY KEY,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0
        );"""

cur.execute('DROP TABLE card')
cur.execute(table)
conn.commit()

template = [1, 4000000000000000, '0000', 0]


def create_account():
    pin = str(random.randint(1000, 10000))
    card_id = template[1] + 10
    card_id += luhn_algorithm(card_id)
    insert = f'INSERT INTO card (id, number, pin, balance) VALUES ({template[0]}, {str(card_id)}, {pin}, 0);'
    cur.execute(insert)
    conn.commit()
    created_successfully(card_id, pin)


def luhn_algorithm(card_id):
    card_id = list(map(int, str(card_id)[:-1]))
    for x in range(0, 15, 2):
        card_id[x] *= 2
        if card_id[x] > 9:
            card_id[x] -= 9
    control_number = math.ceil(sum(card_id) / 10) * 10 - sum(card_id)
    return control_number


def created_successfully(card_id, pin):
    print(f'Your card has been created\nYour card number:\n\
{card_id}\nYour card PIN:\n{pin}')
    template[0] += 1
    template[1] += 10


def add_income(amount, card_id):
    cur.execute(f"UPDATE card SET balance=balance+{int(amount)} WHERE number={card_id};")
    conn.commit()
    print('Income was added!')


def do_transfer(card_id, recipient_card):
    if int(recipient_card[-1]) != luhn_algorithm(int(recipient_card)):
        print('Probably you made a mistake in the card number. Please try again!\n')
    elif card_id == int(recipient_card):
        print("You can't transfer money to the same account!\n")
    else:
        wrong = cur.execute(f'SELECT id FROM card WHERE number={recipient_card};')
        if wrong.fetchone() is None:
            print('Such a card does not exist.')
            return False
        funds = int(input("Enter how much money you want to transfer:"))
        payer_funds = cur.execute(f'SELECT balance FROM card WHERE number={card_id};')
        funds_amount = payer_funds.fetchone()
        if funds <= funds_amount[0]:
            cur.execute(f"UPDATE card SET balance=balance-{int(funds)} WHERE number={card_id};")
            cur.execute(f"UPDATE card SET balance=balance+{int(funds)} WHERE number={recipient_card};")
            conn.commit()
            print('Success!')
        else:
            print("Not enough money!")


def dashboard(card_id):
    option = int(input('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n'))
    if option == 1:
        balance = cur.execute(f'SELECT balance FROM card WHERE number={card_id}')
        value_balance = balance.fetchall()
        print(f'Balance: {value_balance[0]}')
        return True
    elif option == 2:
        add_income(int(input('Enter income:\n')), card_id)
        return True
    elif option == 3:
        do_transfer(card_id, input('Enter card number:\n'))
        return True
    elif option == 4:
        cur.execute(f"DELETE FROM card WHERE number={str(card_number)}")
        conn.commit()
        print('The account has been closed!\n')
        return False
    elif option == 5:
        return False
    elif option == 0:
        print('Bye!')
        exit()


while True:
    choice = input("1. Create an account\n2. Log into account\n0. Exit\n")
    if choice == '1':
        create_account()
    elif choice == '2':
        card_number = int(input('Enter your card number:\n'))
        card_pin = input('Enter your PIN:\n')
        correct_pin = cur.execute(f"SELECT pin FROM card WHERE number={str(card_number)}")
        value_pin = correct_pin.fetchone()
        try:
            if card_pin == value_pin[0]:
                print('You have successfully logged in!')
                while dashboard(card_number):
                    pass
            else:
                print('Wrong card number or PIN!\n')
        except TypeError:
            print('Wrong card number or PIN!\n')
    elif choice == '0':
        print('Bye!\n')
        break
