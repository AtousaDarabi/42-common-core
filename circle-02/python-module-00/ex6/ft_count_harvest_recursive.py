def ft_count_harvest_recursive(val = None):
    if val == 0:
        return
    if (val is None):
        days = int(input("Days until harvest: "))
        ft_count_harvest_recursive(days - 1)
        print(f"Day {days}")
        print("Harvest time!")
    else:
        ft_count_harvest_recursive(val - 1)
        print(f"Day {val}")


# ft_count_harvest_recursive()
