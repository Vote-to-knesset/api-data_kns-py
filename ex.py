#
#
#
# def calculate_series(week,days):
#     s = (days * ((2 * week) + (days - 1)*1)) // 2
#     return s
#
#
# def solution(n):
#     weeks = n // 7
#     days = n % 7
#     total = 0
#     for week in range(weeks):
#         total += calculate_series(week + 1, 7)
#     total += calculate_series(weeks + 1, days)
#     return total



#
#
def solution(S, n):
    dic = {}
    ans = 0
    if S == "":
        return n*2
    for i in range(1,len(S)):
        if S[i].isdigit():
            dic[i] = set(S[i-1]) if i not in dic else dic[i].union(S[i-1])
    for j in range(n):
        num = 2
        if len({'D', 'E'}&dic[j]):
            num -= 1
        if len({'F', 'G'} & dic[j]):
            num -= 1
            if num == 0:
                continue
        if len({'B', 'C'} & dic[j]):
            num -= 1
        if len({'H', 'I'} & dic[j]):
            num -= 1
        ans += num
    return ans

print(solution("A1 C2 D2",2))

