import sys

# Skeleton code for problem https://uchicago.kattis.com/problems/ferryloading4
#
# Make sure you read the problem before editing this code.
#
# You should focus only on implementing the solve() function.
# Do not modify any other code.


def solve(l, cars):
    """
    Parameters:
     - l: Integer. The length of the ferry.
     - cars: List of tuples. Each tuple represents a car. The first element of the
             tuple is the length of the car, and the second element is "left" or "right"
             (the bank at which the car arrives). Cars appear in the list in the order
             in which they arrive.

    Returns: Integer. The number of times the ferry has to cross the river.
    """

    count = 0
    cars_length = 0

    for car_num, car in enumerate(cars):
        length, bank = car
        print("NEXT CAR:", length, bank)
        if count % 2 == 0:
            position = "left"
            print("LEFT: Ferry is currently at left bank")
        else:
            position = "right"
            print("RIGHT: Ferry is currently at right bank")

        if bank == position and cars_length + length <= l * 100:
            cars_length += length
            print("LOADED: car is put on ferry since it is in right position and fits")
            print("Length of cars on ferry is", cars_length)
        else:
            print("Car is on opposite bank or does not fit")
            print("Ferry moves to opposite bank and unloads cars")
            print("LOADED: car is put on ferry since it is in right position and fits")
            count += 1
            cars_length = length

        if car_num + 1 == len(cars):
            count += 1
            print("Last car so ferry must cross to drop it")

    return count


### The following code handles the input and output tasks for
### this problem.  Do not modify it!

if __name__ == "__main__":
    tokens = sys.stdin.read().split()
    tokens.reverse()

    ntests = int(tokens.pop())

    for i in range(ntests):
        l = int(tokens.pop())
        m = int(tokens.pop())
        cars = []
        for j in range(m):
            cars.append( (int(tokens.pop()), tokens.pop()) )

        print(solve(l, cars))


