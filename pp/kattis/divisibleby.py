import sys

def divisible_by_p_q(m, n, p, q):
    # Use the variable rv to accumulate the sum of the values that are
    # divisible by both p and q.
    rv = 0

    for i in range(m, n + 1):
        if i % p == 0:
            if i % q == 0:
                rv += i
        else:
            pass

    return rv


if __name__ == "__main__":
    # parse the input
    (m, n, p, q) = [int(item.strip()) for item  in sys.stdin.read().split()]

    rv = divisible_by_p_q(m, n, p, q)

    print(rv)
