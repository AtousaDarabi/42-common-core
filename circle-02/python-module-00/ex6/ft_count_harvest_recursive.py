n = int(input("Days until harvest: "))
def ft_count_harvest_recursive(i, n):
    if (i == n):
        print("Harvest time!")
        return
    print("Days ", i)
    ft_count_harvest_recursive(i + 1, n)
ft_count_harvest_recursive(1, n)
