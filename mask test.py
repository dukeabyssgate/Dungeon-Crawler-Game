def aoihf(i):
    print(i)
    i += 1
    if i< 100:
        return aoihf(i)

aoihf(0)