import functools

class Animal(object):
    def run(self):
        print('Animal is running...')

class Dog(Animal):

    def run(self):
        print('Dog is running...')

class Tortoise(Animal):
    def run(self):
        print('Tortoise is running slowly...')

def run_twice(animal):
    animal.run()
    animal.run()


if __name__ == '__main__':
    run_twice(Dog())