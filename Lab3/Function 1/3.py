def solve(numheads, numlegs):
    rabbit = (numlegs - 2 * numheads) / 2
    chicken = numheads - rabbit
    print(f"Chicken: {chicken}, rabbits: {rabbit}")

heads, legs = map(int, input().split())
solve(heads, legs)
