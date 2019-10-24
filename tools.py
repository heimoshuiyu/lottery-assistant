with open('名单.txt', 'r') as f:
    data = f.read()

count = 0
result = ''
for letter in data:
    count += 1
    result += letter
    if count/3 == 1:
        count = 0
        result += '\n'
print(result)
with open('名单.txt', 'w') as f:
    f.write(result)
    
