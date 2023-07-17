L = []

x = ""
while x != 'x':
    L.append(x)
    x = input("Input a word in the language, input 'x' to stop: ")

limit = int(input("Input size limit: "))
L_star = L.copy()
for a in L_star:
    for b in L_star:
        c = a + b
        if len(c) <= limit:
            if c not in L_star:
                L_star.append(c)

print(L_star)