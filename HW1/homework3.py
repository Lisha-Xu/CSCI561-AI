import numpy as np
from queue import Queue, PriorityQueue
import math

# the front four is east,north , west, south
# the end four is Northeast, Southeast, Southwest, Northwest
direction = [(1, 0), (0, -1), (-1, 0), (0, 1), (1, 1), (1, -1), (-1, -1), (-1, 1)]
output = ''


class Point:
    def __init__(self, coor, distance, value, parent):
        self.coor = coor
        self.distance = distance
        if value >= 0:
            self.height = 0
            self.mud = value
        else:
            self.height = -value
            self.mud = 0
        self.parent = parent

    def __lt__(self, other):  # operator <
        return self.distance < other.distance


class APoint:
    def __init__(self, coor, distance, cost, value, parent):
        self.coor = coor
        self.distance = distance
        self.cost = cost
        if value >= 0:
            self.height = 0
            self.mud = value
        else:
            self.height = -value
            self.mud = 0
        self.parent = parent

    def __lt__(self, other):  # operator <
        return self.cost < other.cost


def BFS(W, H, startPoint, targetPoint, hightLimit, graph):
    visited = np.zeros([H, W])
    startX = startPoint[0]
    startY = startPoint[1]
    visited[startY][startX] = 1
    queue = Queue()
    queue.put(Point(startPoint, 0, graph[startPoint[1]][startPoint[0]], None))
    res = []
    while not queue.empty():
        curPoint = queue.get()
        if curPoint.coor == targetPoint:
            prev = curPoint
            res = [prev.coor]

            while prev.parent is not None:
                prev = prev.parent
                res.append(prev.coor)
            res.reverse()

        for direct in direction:
            childCoor = (curPoint.coor[0] + direct[0], curPoint.coor[1] + direct[1])
            if 0 <= childCoor[0] < W and 0 <= childCoor[1] < H:
                if visited[childCoor[1]][childCoor[0]] == 0:
                    if graph[childCoor[1]][childCoor[0]] >= 0 or abs(
                            graph[childCoor[1]][childCoor[0]] - curPoint.height) <= hightLimit:
                        visited[childCoor[1]][childCoor[0]] = 1
                        queue.put(Point(childCoor, curPoint.distance + 1, graph[childCoor[1]][childCoor[0]], curPoint))
    return res


def UCS(W, H, startPoint, targetPoint, hightLimit, graph):
    visited = np.zeros([H, W])
    searched = np.zeros([H, W])
    visited[startPoint[1]][startPoint[0]] = 1
    queue = PriorityQueue()
    queue.put(Point(startPoint, 0, graph[startPoint[1]][startPoint[0]], None))
    res = []
    while not queue.empty():
        curPoint = queue.get()
        if searched[curPoint.coor[1]][curPoint.coor[0]] == 1 and visited[startPoint[1]][startPoint[0]] == 1:
            continue
        searched[curPoint.coor[1]][curPoint.coor[0]] = 1
        if curPoint.coor == targetPoint:
            prev = curPoint

            res = [prev.coor]
            while prev.parent is not None:
                prev = prev.parent
                res.append(prev.coor)
            res.reverse()
            # print(res)
        for i in range(0, 4):
            childCoor = (curPoint.coor[0] + direction[i][0], curPoint.coor[1] + direction[i][1])
            if 0 <= childCoor[0] < W and 0 <= childCoor[1] < H:
                if visited[childCoor[1]][childCoor[0]] == 0 or searched[childCoor[1]][childCoor[0]] == 0:
                    childPoint = Point(childCoor, curPoint.distance + 10, graph[childCoor[1]][childCoor[0]], curPoint)
                    if abs(childPoint.height - curPoint.height) <= hightLimit:
                        visited[childCoor[1]][childCoor[0]] = 1
                        queue.put(childPoint)

        for i in range(4, 8):
            childCoor = (curPoint.coor[0] + direction[i][0], curPoint.coor[1] + direction[i][1])
            if 0 <= childCoor[0] < W and 0 <= childCoor[1] < H:
                if visited[childCoor[1]][childCoor[0]] == 0 or searched[childCoor[1]][childCoor[0]] == 0:
                    childPoint = Point(childCoor, curPoint.distance + 14, graph[childCoor[1]][childCoor[0]], curPoint)
                    if abs(childPoint.height - curPoint.height) <= hightLimit:
                        visited[childCoor[1]][childCoor[0]] = 1
                        queue.put(childPoint)

    return res


def Astar(W, H, startPoint, targetPoint, hightLimit, graph):
    visited = np.zeros([H, W])
    searched = np.zeros([H, W])
    visited[startPoint[1]][startPoint[0]] = 1
    queue = PriorityQueue()
    queue.put(APoint(startPoint, 0, heuristic(startPoint, targetPoint), graph[startPoint[1]][startPoint[0]], None))
    res = []
    while not queue.empty():
        curPoint = queue.get()

        if searched[curPoint.coor[1]][curPoint.coor[0]] == 1 and visited[startPoint[1]][startPoint[0]] == 1:
            continue
        searched[curPoint.coor[1]][curPoint.coor[0]] = 1
        if curPoint.coor == targetPoint:
            prev = curPoint
            res = [prev.coor]

            while prev.parent is not None:
                prev = prev.parent
                res.append(prev.coor)
            res.reverse()
            # print(res)

        for i in range(0, 4):
            childCoor = (curPoint.coor[0] + direction[i][0], curPoint.coor[1] + direction[i][1])
            if 0 <= childCoor[0] < W and 0 <= childCoor[1] < H:
                if visited[childCoor[1]][childCoor[0]] == 0 or searched[childCoor[1]][childCoor[0]] == 0:
                    childPoint = Point(childCoor, curPoint.distance + 10, graph[childCoor[1]][childCoor[0]], curPoint)
                    if abs(childPoint.height - curPoint.height) <= hightLimit:
                        visited[childCoor[1]][childCoor[0]] = 1
                        childPoint.distance = curPoint.distance + 10 + childPoint.mud + abs(
                            childPoint.height - curPoint.height)
                        cost = childPoint.distance + heuristic(childPoint.coor, targetPoint)
                        queue.put(APoint(childPoint.coor, childPoint.distance, cost, graph[childCoor[1]][childCoor[0]],
                                         curPoint))

        for i in range(4, 8):
            childCoor = (curPoint.coor[0] + direction[i][0], curPoint.coor[1] + direction[i][1])
            if 0 <= childCoor[0] < W and 0 <= childCoor[1] < H:
                if visited[childCoor[1]][childCoor[0]] == 0 or searched[childCoor[1]][childCoor[0]] == 0:
                    childPoint = Point(childCoor, curPoint.distance + 14, graph[childCoor[1]][childCoor[0]], curPoint)
                    if abs(childPoint.height - curPoint.height) <= hightLimit:
                        visited[childCoor[1]][childCoor[0]] = 1
                        childPoint.distance = curPoint.distance + 14 + childPoint.mud + abs(
                            childPoint.height - curPoint.height)
                        cost = childPoint.distance + heuristic(childPoint.coor, targetPoint)
                        queue.put(APoint(childPoint.coor, childPoint.distance, cost, graph[childCoor[1]][childCoor[0]],
                                         curPoint))

    return res


def heuristic(point, target):
    dx = abs(point[0] - target[0])
    dy = abs(point[1] - target[1])
    return int(math.sqrt(dx * dx + dy * dy)) * 10


if __name__ == "__main__":
    # Get Data from the file
    inputFile = open("input.txt")
    fileData = inputFile.readlines()
    method = fileData.pop(0).rstrip()
    boundary = fileData.pop(0).strip().split()
    W, H = int(boundary[0]), int(boundary[1])
    startPoint = fileData.pop(0).strip().split()
    startX, startY = int(startPoint[0]), int(startPoint[1])
    startPoint = (startX, startY)
    hightLimit = int(fileData.pop(0))
    targetNum = int(fileData.pop(0))
    targetPointList = []
    for i in range(0, targetNum):
        targetPoint = fileData.pop(0).strip().split()
        targetX = int(targetPoint[0])
        targetY = int(targetPoint[1])
        targetPointList.append((targetX, targetY))
    graph = np.zeros([H, W])
    row_count = 0
    for line in fileData:
        line = line.strip().split()
        graph[row_count, :] = line[:]
        row_count += 1
    inputFile.close()

    # Search Algorithm
    for i in range(0, targetNum):
        if i > 0:
            output = output + '\n'
        targetPoint = targetPointList[i]
        if method == "BFS":
            res = BFS(W, H, startPoint, targetPoint, hightLimit, graph)
        elif method == 'UCS':
            res = UCS(W, H, startPoint, targetPoint, hightLimit, graph)
        else:
            res = Astar(W, H, startPoint, targetPoint, hightLimit, graph)
        if not res:
            output = output + 'FAIL'
        else:
            for coor in res:
                output = output + str(coor[0]) + ',' + str(coor[1]) + ' '

    with open("output.txt", 'w') as file:
        file.write(output)
