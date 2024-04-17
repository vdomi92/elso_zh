def is_leap(year):
    leap = False
    if year % 4 == 0:
        leap = True
        if year % 100 == 0:
            leap = False
            if year % 400 == 0:
                leap = True
    return leap

f = open("years.txt", "r")
lines = f.readlines()
f.close()
print(lines)
lines = [int(line) for line in lines]
print(lines)
#lines_as_int = []
#for line in lines:
#    lines_as_int.append(int(line))
for year in lines:
    if is_leap(year):
        print(f"{year} szökőév")
        #print(str(year) + " szökőév")
    else:
        print(f"{year} nem szökőév")