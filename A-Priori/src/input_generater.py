import random

# This is used to create all the test data that the algorithems will be tested on

# creates a file that holds 1000 baskets of test data
def populat_data(file_name):
    with open("data/"+file_name, "w") as file:
        for num in range(1000):
            file.write(create_basket())

# Creates a basket that is 5 numbers between 1 and 100
# and 5 numbers that are between 101 and 2000 
def create_basket():
    basket = []
    while len(basket) < 5:
        num = random.randint(1, 100)
        if num not in basket:
            basket.append(num)
    while len(basket) < 10:
        num = random.randint(101, 2000)
        if num not in basket:
            basket.append(num)
    basket.sort()
    strBasket = ",".join(str(i) for i in basket)
    strBasket+='\n'
    print(strBasket)
    return strBasket


if __name__ == '__main__':
    populat_data("test_data.txt")
    print('Data Populated')