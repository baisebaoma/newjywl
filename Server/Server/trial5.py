'''
find the value of
1
2
1 3
2 4
1 3 5
2 4 6
1 3 5 7
2 4 6 8
...
1 3 5 7 ... 97 99
2 4 6 8 ... 98 100
'''

odd_numbers = []
even_numbers = []
sum = 0

for i in range(1, 101):
    if i % 2 == 0:
        even_numbers.append(i)
    elif i % 2 == 1:
        odd_numbers.append(i)

print(odd_numbers)
print(even_numbers)

n = 50
for i in odd_numbers:
    sum += i * n
    n -= 1

n = 50
for i in even_numbers:
    sum += i * n
    n -= 1

print(sum)
