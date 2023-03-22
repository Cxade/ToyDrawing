import json
import os
import random

class Toy:
    def __init__(self, id, name, quantity, probability):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.probability = probability


    def add_toy(self):
        toys_list = []

        with open('toys.json', 'r') as f:
            toys_list = json.load(f)

        toys_list.append(self.__dict__)
        with open('toys.json', 'w') as f:
            json.dump(toys_list, f)

    def change_probability(self, new_probability):
        toys_list = []
        with open('toys.json', 'r') as f:
            toys_list = json.load(f)

        for idx, toy in enumerate(toys_list):
            if toy['id'] == self.id:
                toys_list[idx]['probability'] = new_probability
                break

        with open('toys.json', 'w') as f:
            json.dump(toys_list, f)

    @staticmethod
    def choose_toy():
        toys_list = []
        with open('toys.json', 'r') as f:
            toys_list = json.load(f)

        valid_toys = [toy for toy in toys_list if toy['probability'] > 0 and toy['quantity'] > 0]
   
        total_probability = sum([toy['probability'] for toy in valid_toys])

        random_number = random.uniform(0, total_probability)
        for toy in valid_toys:
            if random_number < toy['probability']:
                toy_object = Toy(toy['id'], toy['name'], toy['quantity'], toy['probability'])
                toy_object.save_winner()
                toy_object.decrease_quantity()
                print('Выпала игрушка {}'.format(toy_object.name))
                return toy_object

            random_number -= toy['probability']

        return None
    

    def decrease_quantity(self):
        toys_list = []
        with open('toys.json', 'r') as f:
            toys_list = json.load(f)

        for idx, toy in enumerate(toys_list):
            if toy['id'] == self.id:
                toys_list[idx]['quantity'] -= 1
                break

        with open('toys.json', 'w') as f:
            json.dump(toys_list, f)


    def save_winner(self):
        winners_list = []
        if os.path.isfile('winners.json'):
            with open('winners.json', 'r') as f:
                winners_list = json.load(f)

        winners_list.append(self.__dict__)
        with open('winners.json', 'w') as f:
            json.dump(winners_list, f)


    @staticmethod
    def get_prize():
        winners_list = []
        with open('winners.json', 'r') as f:
            winners_list = json.load(f)

        prize = None
        if winners_list:
            prize = Toy(winners_list[0]['id'], winners_list[0]['name'], winners_list[0]['quantity'], winners_list[0]['probability'])
            del winners_list[0]
            with open('winners.json', 'w') as f:
                json.dump(winners_list, f)

        return prize
    

def main():
    while True:
        print('\nВыберите действие:')
        print('1. Добавление новой игрушки')
        print('2. Изменение вероятности выпадения игрушки')
        print('3. Розыгрыш игрушек')
        print('4. Получение призовой игрушки')
        print('0. Выход')

        choice = input()

        if choice == '1':
            id = input('Введите id игрушки: ')
            name = input('Введите название игрушки: ')
            quantity = int(input('Введите количество игрушек: '))
            probability = int(input('Введите вероятность выпадения игрушки: '))

            new_toy = Toy(id, name, quantity, probability)
            new_toy.add_toy()
            print('Игрушка добавлена')

        elif choice == '2':
            toy_id = input('Введите id игрушки: ')
            new_probability = int(input('Введите новую вероятность выпадения игрушки: '))

            toy = Toy(toy_id, '', 0, new_probability)
            toy.change_probability(new_probability)
            print('Вероятность изменена')

        elif choice == '3':
            Toy.choose_toy()

        elif choice == '4':
            prize = Toy.get_prize()
            if prize:
                print('Ваш приз - игрушка "{}"'.format(prize.name))
            else:
                print('Выигранных игрушек нет')

        elif choice == '0':
            break

        else:
            print('Неправильный выбор, пожалуйста, повторите')

if __name__ == '__main__':
    main()
