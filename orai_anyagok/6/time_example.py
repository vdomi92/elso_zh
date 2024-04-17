import time

start = time.time() #rögzítjük a kezdő idő
time.sleep(2)       #csinálunk valami hasznosat
end = time.time()   #rögzítjük a tevékenység utáni időt
difference = end - start
print(f"{end-start} seconds have elapsed")