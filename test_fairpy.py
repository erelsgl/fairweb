import fairpy

instance = {
    "Ami": {"green": 8, "red":7, "blue": 6, "yellow": 5},
    "Tami": {"green": 12, "red":8, "blue": 4, "yellow": 2} }
allocation = fairpy.divide(fairpy.items.round_robin, instance)
print(allocation)
print("fairpy OK!")
