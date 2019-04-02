# 判断输赢函数


def judgeWin(pointState, chess):
    chessType = 1 if chess["chessType"] == "black" else 2
    chessPoint = chess["chessPoint"]
    # 起始点
    pointX = chessPoint[0]
    pointY = chessPoint[1]

    # 竖向棋子判断
    chessCount = 1  # 同向棋子计数初始化
    cTime = 0  # 循环次数初始化
    tempX = pointX
    tempY = pointY
    while tempY - 1 >= 0 and pointState[tempX][tempY - 1] == chessType and cTime < 5:
        chessCount += 1
        cTime += 1
        tempY -= 1
    cTime = 0  # 循环次数初始化
    tempY = pointY
    while tempY + 1 < 14 and pointState[tempX][tempY + 1] == chessType and cTime < 5:
        chessCount += 1
        cTime += 1
        tempY += 1
    if chessCount >= 5:
        return True

    # 横向棋子判断
    chessCount = 1  # 同向棋子计数初始化
    cTime = 0  # 循环次数初始化
    tempX = pointX
    tempY = pointY
    while tempX - 1 >= 0 and pointState[tempX - 1][tempY] == chessType and cTime < 5:
        chessCount += 1
        cTime += 1
        tempX -= 1
    cTime = 0  # 循环次数初始化
    tempX = pointX
    while tempX + 1 < 14 and pointState[tempX + 1][tempY] == chessType and cTime < 5:
        chessCount += 1
        cTime += 1
        tempX += 1
    if chessCount >= 5:
        return True

    # 左上右下斜向判断
    chessCount = 1  # 同向棋子计数初始化
    cTime = 0  # 循环次数初始化
    tempX = pointX
    tempY = pointY
    while tempX - 1 >= 0 and tempY - 1 < 14 and pointState[tempX - 1][tempY - 1] == chessType and cTime < 5:
        chessCount += 1
        cTime += 1
        tempX -= 1
        tempY -= 1
    cTime = 0  # 循环次数初始化
    tempX = pointX
    tempY = pointY
    while tempX + 1 < 14 and tempY + 1 < 14 and pointState[tempX + 1][tempY + 1] == chessType and cTime < 5:
        chessCount += 1
        cTime += 1
        tempX += 1
        tempY += 1
    if chessCount >= 5:
        return True

    # 右上左下斜向判断
    chessCount = 1  # 同向棋子计数初始化
    cTime = 0  # 循环次数初始化
    tempX = pointX
    tempY = pointY
    while tempX + 1 < 14 and tempY - 1 >= 0 and pointState[tempX + 1][tempY - 1] == chessType and cTime < 5:
        chessCount += 1
        cTime += 1
        tempX += 1
        tempY -= 1
    cTime = 0  # 循环次数初始化
    tempX = pointX
    tempY = pointY
    while tempX - 1 >= 0 and tempY + 1 < 14 and pointState[tempX - 1][tempY + 1] == chessType and cTime < 5:
        chessCount += 1
        cTime += 1
        tempX -= 1
        tempY += 1
    if chessCount >= 5:
        return True

    return False
