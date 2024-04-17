import hashlib

#Az output mérete független az inputtól
h = hashlib.sha1()
print(h.digest_size)
h.update(("alma").encode())
print(h.hexdigest().encode())

#A digest kiolvasása nem nullázza a hasht
h = hashlib.sha1()
print(h.digest_size)
h.update("al".encode())
h.update("ma".encode())
print(h.digest())
h.update("al".encode())
h.update("ma".encode())
print(h.digest()) 