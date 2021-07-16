from math import *

import numpy as np
from PIL import Image

n = int(input())
row = int(input())
col = int(input())

round = np.zeros((row, n), dtype=np.int)
for i in range(0,row):
    line = input().split(' ')
    for j in range(int(line[0]),int(line[1])):
        round[i][j-1] = int(line[2])
sum = np.zeros(n, dtype=np.int)
for index in range(0,n):
    for i in range(0,row):
        sum[index] += round[i][index]
print(max(sum))

print(round)



# saving = int(input())
# currrent_n = int(input())
# currentValue = []
# futureValue = []
# for i in range(0,currrent_n):
#     currentValue.append(int(input()))
# future_n = int(input())
# for i in range(0,future_n):
#     futureValue.append(int(input()))
#
# print(currentValue)
# print(futureValue)
#
# diff = []
# for i in range(0,currrent_n):
#     diff.append((i,futureValue[i]-currentValue[i]))
#     # 遍历所有数组元素
# print(diff)
# for i in range(currrent_n):
#
#     # Last i elements are already in place
#     for j in range(0, currrent_n - i - 1):
#
#         if diff[j][1] < diff[j + 1][1]:
#             diff[j], diff[j + 1] = diff[j + 1], diff[j]
#
# print(diff)
# rest = saving
# index = 0
# profit = 0
# while(rest > 0):
#     temp = rest/currentValue[diff[index][0]]
#     profit = profit+diff[index][1]*temp
#     index += 1
#     rest = rest % currentValue[diff[index][0]]
# print(profit)


# value = [[1,2,3,4,5,6,7,8,9,0,1,2],
#          [0,1,2,3,4,5,6,7,8,9,0,1],
#          [9,0,1,2,3,4,5,6,7,8,9,0],
#          [8,9,0,1,2,3,4,5,6,7,8,9],
#          [7,8,9,0,1,2,3,4,5,6,7,8],
#          [6,7,8,9,0,1,2,3,4,5,6,7],
#          [5,6,7,8,9,0,1,2,3,4,5,6],
#          [4,5,6,7,8,9,0,1,2,3,4,5]]
# D = [[6,8,4],[1,0,3],[5,2,7]]
# res = np.zeros((8, 12), dtype=np.float)
# for i in range(0,8):
#     for j in range(0,12):
#         row = (i+1) % 3
#         col = (j+1) %3
#         if value[i][j]<=D[row][col]:
#             # res[i][j] = -255/9 *value[i][j] + 255
#             res[i][j] = 255
#         else:
#             res[i][j] = 0
#
# im = Image.fromarray(res)
# im = im.convert('L')
# im.save('outfile.png')

# xx = np.zeros((8, 8), dtype=np.int)
# for u in range(0,8):
#     for v in range(0,8):
#         if u == 0:
#             Cu = 1.0/sqrt(2)
#         else:
#             Cu = 1
#         if v == 0:
#             Cv = 1.0/sqrt(2)
#         else:
#             Cv = 1
#         for i in range(0,8):
#             for j in range(0,8):
#                 ori_index = j + i*8
#                 res[u][v] += value[ori_index] * cos((2 * i + 1) * u * pi / 16) * cos((2 * j + 1) * v * pi / 16)
#         res[u][v] *= 0.25*Cu*Cv
#
# for u in range(0,8):
#     for v in range(0,8):
#         print(res[u][v], end=' ')
#         xx[u][v] = round(res[u][v]/100)
#     print("\n")
# # print(res)
# for u in range(0,8):
#     for v in range(0,8):
#         print(xx[u][v], end=' ')
#     print("\n")