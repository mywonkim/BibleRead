s = input()
ans = s[0:1][::-1] + s[1:2][::-1] + s[2:][::-1]
for i in range(0, len(s) - 2):
    for j in range(i + 1, len(s) - 1):
        for k in range(j + 1, len(s)):
            tmp = s[0:j][::-1] + s[j:k][::-1] + s[k:][::-1]
            if tmp < ans:
                ans = tmp
print(ans)