import sys

def outside_range(x, y, z):
    if y < x and x < z:
        return False
    else:
        return True


    if __name__ == "__main__":
        # parse the input
        (x,y,z) = [float(item.strip()) for item  in sys.stdin.read().split()]

        rv = outside_range(x, y, z)

        print(rv)
