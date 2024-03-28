# PIECE KEY
# 0 - no piece
# 1/O - white pawn
# 2/@ - white king
# 3/o - black pawn
# 4/# - black King
def get_2d_Pos(square):
    return square%8, square//8

class Move:
    def __init__(self, fromPos, toPos, isCapture):
        self.fromPos = fromPos
        self.toPos = toPos
        self.isCapture = isCapture

        self.jumpLength = len(toPos) * isCapture
        self.multiJump = self.jumpLength > 1
        self.isKingMove = abs(fromPos-toPos[0]) > 9

    def __str__(self):
        return f"{self.fromPos}|{self.toPos}"

class CheckersBoard:
    def __init__(self, piecesList, allPositions):
        self.pieceList = piecesList # initialise all the pieces
        self.piecePositions = allPositions

    def get_PieceColorPos(self, color):

        pieceList = []
        for piecePos in self.piecePositions:
            if not is_enemyPiece(self.pieceList[piecePos], color):
                pieceList.append(piecePos)

        return pieceList


    def convertBoardToFEN(self):
        counter = 0
        normalCounter = 0
        fenString = ""
        for piece in self.pieceList:

            if piece == 1:
                if counter:
                    fenString += str(counter)
                fenString += "O"
                counter = 0
            elif piece == 2:
                if counter:
                    fenString += str(counter)
                fenString += "@"
                counter = 0
            elif piece == 3:
                if counter:
                    fenString += str(counter)
                fenString += "o"
                counter = 0
            elif piece == 4:
                if counter:
                    fenString += str(counter)
                fenString += "#"
                counter = 0
            else:
                counter += 1

            if normalCounter % 8 == 7:
                if counter:
                    fenString += str(counter)
                fenString += "/"

                counter = 0




            normalCounter += 1
        return fenString

    def initialiseBoardWithFEN(self, FEN):
        counter = 0
        self.pieceList = [0 for i in range(64)]
        self.piecePositions = []

        for letter in FEN:
            try:
                counter += int(letter)
                continue

            except:
                pass

            if letter == "O":
                self.pieceList[counter] = 1
                self.piecePositions.append(counter)

            elif letter == "o":
                self.pieceList[counter] = 3
                self.piecePositions.append(counter)

            elif letter == "@":
                self.pieceList[counter] = 2
                self.piecePositions.append(counter)

            elif letter == "#":
                self.pieceList[counter] = 4
                self.piecePositions.append(counter)

            if letter != "/":
                counter += 1

    def printBoard(self):
        counter = 0
        print()
        for piece in self.pieceList:

            if piece == 1:
                print("O", end=" ")
            elif piece == 3:
                print("o", end = " ")
            elif piece == 2:
                print("@", end = " ")
            elif piece == 4:
                print("#", end = " ")
            else:
                print("_", end=" ")

            counter += 1
            if counter % 8 == 0:
                print()

def normalise_moveSquareVec(fromPos, toPos):
    x_pos_from, y_pos_from = get_2d_Pos(fromPos)
    x_pos_to, y_pos_to = get_2d_Pos(toPos)
    sum_ = 0

    if x_pos_to > x_pos_from:
        sum_ += 1
    else:
        sum_ -= 1

    if y_pos_to > y_pos_from:
        sum_ += 8
    else:
        sum_ -= 8

    return sum_

def inBounds(x_pos, y_pos):
    return x_pos >= 0 and x_pos <= 7 and y_pos >= 0 and y_pos <= 7

def makeMove(checkerBoard, move):
    newPieceList = checkerBoard.pieceList.copy()
    newPiecePositions = checkerBoard.piecePositions.copy()

    if not move.multiJump:
        trueToMove = move.toPos[0]
        if not move.isKingMove:

            if move.isCapture:
                jumpToPos = trueToMove + trueToMove - move.fromPos
                piece = newPieceList[move.fromPos]
                if (piece == 1 and jumpToPos//8 == 7) or (piece == 3 and jumpToPos//8 == 0):
                    newPieceList[jumpToPos] = piece+1

                else:
                    newPieceList[jumpToPos] = piece

                newPieceList[move.fromPos] = 0
                newPieceList[trueToMove] = 0

                # print(newPiecePositions)

                newPiecePositions.remove(trueToMove)

                newPiecePositions.remove(move.fromPos)
                newPiecePositions.append(jumpToPos)

            else:
                piece = newPieceList[move.fromPos]



                if (piece == 1 and trueToMove//8 == 7) or (piece == 3 and trueToMove//8 == 0):
                    newPieceList[trueToMove] = piece + 1

                else:
                    newPieceList[trueToMove] = piece

                newPieceList[move.fromPos] = 0

                newPiecePositions.remove(move.fromPos)
                newPiecePositions.append(trueToMove)

        else: # king move

            tempMoveSquare = normalise_moveSquareVec(move.fromPos, trueToMove)
            tempSquare = move.fromPos + tempMoveSquare
            piece = newPieceList[move.fromPos]

            while tempSquare != trueToMove:
                if newPieceList[tempSquare] != 0: # piece
                    newPiecePositions.remove(tempSquare)
                    newPieceList[tempSquare] = 0

                    break

                tempSquare += tempMoveSquare

            newPieceList[move.fromPos] = 0
            newPieceList[trueToMove] = piece
            newPiecePositions.remove(move.fromPos)
            newPiecePositions.append(trueToMove)

    else:
        if not move.isKingMove: # is not a king move
            tempFromPos = move.fromPos
            piece = newPieceList[move.fromPos]

            for toPos in move.toPos:
                newPieceList[toPos] = 0
                tempFromPos = toPos + toPos - tempFromPos

                try:
                    newPiecePositions.remove(toPos)
                except:
                    checkerBoard.printBoard()
                    print(checkerBoard.convertBoardToFEN())

                    1/0

            if (piece == 1 and tempFromPos // 8 == 7) or (piece == 3 and tempFromPos // 8 == 0):
                newPieceList[tempFromPos] = piece + 1

            else:
                newPieceList[tempFromPos] = piece

            newPieceList[move.fromPos] = 0

            newPiecePositions.remove(move.fromPos)
            newPiecePositions.append(tempFromPos)

        else: # king move

            tempFromPos = move.fromPos
            piece = newPieceList[move.fromPos]

            for toPos in move.toPos:
                tempMoveSquare = normalise_moveSquareVec(tempFromPos, toPos)
                tempSquare = tempFromPos + tempMoveSquare

                while tempSquare != toPos:


                    if is_enemyPiece(newPieceList[tempSquare], piece<=2):  # piece
                        newPiecePositions.remove(tempSquare)
                        newPieceList[tempSquare] = 0
                        break

                    tempSquare += tempMoveSquare

                tempFromPos = toPos

            newPiecePositions.remove(move.fromPos)
            newPiecePositions.append(move.toPos[-1])

            newPieceList[move.fromPos] = 0
            newPieceList[move.toPos[-1]] = piece

    return CheckersBoard(newPieceList, newPiecePositions)

def printSquare(square):

    for i in range(64):
        if i % 8 == 0:
            print()
        if i == square:
            print("O", end=" ")
        else:
            print("_", end=" ")
    print()

def is_enemyPiece(piece, color):
    if color:
        return piece > 2

    else:
        return piece <= 2 and piece != 0






kingMoveVectorList_x = [1, 1, -1, -1]
kingMoveVectorList_y = [-1, 1, -1, 1]


def getSingleMove(pos, checkerBoard, color, isKing):
    x_pos, y_pos = get_2d_Pos(pos)
    moveList = []

    hasCaptures = False

    if not isKing:
        if color: # white
            if x_pos < 7: # not on the right edge

                if y_pos < 7 and checkerBoard.pieceList[pos + 9] == 0:
                    moveList.append(Move(pos, [pos+9], False))

                if x_pos <= 5 and y_pos <= 5: # needs to be smaller than this for captures

                    if checkerBoard.pieceList[pos + 9] > 2 and checkerBoard.pieceList[pos + 18] == 0:
                        hasCaptures = True
                        moveList = [Move(pos, [pos+9], True)]

                        tempCheckerBoard = makeMove(checkerBoard, moveList[0])
                        cascadingMoves = getSingleMove(pos + 18, tempCheckerBoard, color, False)


                        if len(cascadingMoves) > 0:


                            if moveList[0].jumpLength <= cascadingMoves[0].jumpLength+1:

                                if moveList[0].jumpLength < cascadingMoves[0].jumpLength+1:
                                    moveList.clear()

                                for move in cascadingMoves:

                                    if move.isCapture:
                                        toPosMoves = [pos + 9]
                                        toPosMoves += move.toPos

                                        moveList.append(Move(pos, toPosMoves, True))


            if x_pos > 0: # not on the left edge
                if y_pos < 7 and checkerBoard.pieceList[pos + 7] == 0 and not hasCaptures:
                    moveList.append(Move(pos, [pos + 7], False))

                if x_pos >= 2 and y_pos <= 5:  # needs to be smaller than this for captures

                    if checkerBoard.pieceList[pos + 7] > 2 and checkerBoard.pieceList[pos + 14] == 0:
                        moveTemp = Move(pos, [pos + 7], True)

                        if len(moveList) != 0 and moveList[0].isCapture:
                            competingMoveLength = moveList[0].jumpLength
                        else:
                            competingMoveLength = -1

                        tempCheckerBoard = makeMove(checkerBoard, moveTemp)

                        cascadingMoves = getSingleMove(pos + 14, tempCheckerBoard, color, False) # all the following moves

                        if len(cascadingMoves) == 0 or not cascadingMoves[0].isCapture: # not more following captures

                            if competingMoveLength > 1:  # less the current most moves | disregard move
                                pass

                            elif competingMoveLength == 1:  # same as current most moves | add move

                                moveList.append(moveTemp)

                            else:  # more than current most moves | replace move
                                moveList = [moveTemp]

                        elif cascadingMoves[0].isCapture:
                            toPosMoves = [pos + 7]
                            toPosMoves += cascadingMoves[0].toPos

                            moveJumpLength = cascadingMoves[0].jumpLength + 1

                            if competingMoveLength > moveJumpLength:  # less the current most moves | disregard move
                                pass

                            elif competingMoveLength == moveJumpLength:  # same as current most moves | add move
                                for toMove_cascading in cascadingMoves:
                                    toPosMoves = [pos+7] + toMove_cascading.toPos
                                    moveList.append(Move(pos, toPosMoves, True))

                            else:  # more than current most moves | replace move
                                moveList.clear()
                                for toMove_cascading in cascadingMoves:
                                    toPosMoves = [pos+7] + toMove_cascading.toPos
                                    moveList.append(Move(pos, toPosMoves, True))


                        # else:
                        #     moveList = [moveTemp]






        else: # black
            hasCaptures = False
            if x_pos < 7:  # not on the right edge
                if y_pos > 0 and checkerBoard.pieceList[pos - 7] == 0:
                    moveList.append(Move(pos, [pos - 7], False))

                if x_pos <= 5 and y_pos >= 2:  # needs to be smaller than this for captures

                    if checkerBoard.pieceList[pos - 7] != 0 and checkerBoard.pieceList[pos - 7] <= 2 and checkerBoard.pieceList[pos - 14] == 0:

                        moveList = [Move(pos, [pos - 7], True)]
                        hasCaptures = True
                        tempCheckerBoard = makeMove(checkerBoard, moveList[0])
                        cascadingMoves = getSingleMove(pos - 14, tempCheckerBoard, color, False)

                        if len(cascadingMoves) > 0:

                            if moveList[0].jumpLength <= cascadingMoves[0].jumpLength + 1:

                                if moveList[0].jumpLength < cascadingMoves[0].jumpLength + 1:
                                    moveList.clear()

                                for move in cascadingMoves:
                                    if move.isCapture:
                                        toPosMoves = [pos - 7]
                                        toPosMoves += move.toPos

                                        moveList.append(Move(pos, toPosMoves, True))

            if x_pos > 0:  # not on the left edge

                if y_pos > 0 and checkerBoard.pieceList[pos - 9] == 0 and not hasCaptures:

                    moveList.append(Move(pos, [pos - 9], False))

                if x_pos >= 2 and y_pos >= 2:  # needs to be smaller than this for captures
                    if checkerBoard.pieceList[pos - 9] != 0 and checkerBoard.pieceList[pos - 9] <= 2 and checkerBoard.pieceList[pos - 18] == 0:

                        moveTemp = Move(pos, [pos - 9], True)

                        if len(moveList) != 0 and moveList[0].isCapture:
                            competingMoveLength = moveList[0].jumpLength
                        else:
                            competingMoveLength = -1

                        tempCheckerBoard = makeMove(checkerBoard, moveTemp)



                        cascadingMoves = getSingleMove(pos - 18, tempCheckerBoard, color, False)  # all the following moves


                        if len(cascadingMoves) == 0 or not cascadingMoves[0].isCapture:
                            if competingMoveLength > 1:  # less the current most moves | disregard move
                                pass

                            elif competingMoveLength == 1:  # same as current most moves | add move
                                moveList.append(moveTemp)


                            else:  # more than current most moves | replace move
                                moveList = [moveTemp]


                        elif cascadingMoves[0].isCapture:
                            toPosMoves = [pos - 9]
                            moveJumpLength = cascadingMoves[0].jumpLength + 1

                            if competingMoveLength > moveJumpLength:  # less the current most moves | disregard move
                                pass

                            elif competingMoveLength == moveJumpLength:  # same as current most moves | add move
                                for toMove_cascading in cascadingMoves:
                                    toPosMoves_temp = toPosMoves + toMove_cascading.toPos
                                    moveList.append(Move(pos, toPosMoves_temp, True))

                            else:  # more than current most moves | replace move
                                moveList.clear()
                                for toMove_cascading in cascadingMoves:
                                    toPosMoves_temp = toPosMoves + toMove_cascading.toPos
                                    moveList.append(Move(pos, toPosMoves_temp, True))



    else: # is a king
        x_pos, y_pos = get_2d_Pos(pos)

        for i in range(4):

            move_x_pos, move_y_pos = kingMoveVectorList_x[i], kingMoveVectorList_y[i]
            temp_x_pos, temp_y_pos = x_pos + move_x_pos, y_pos + move_y_pos
            tempPos = temp_y_pos*8 + temp_x_pos

            tempMoveList = []
            is_a_capture = False

            while inBounds(temp_x_pos, temp_y_pos):
                if checkerBoard.pieceList[tempPos] != 0: # it is a piece
                    if is_a_capture:
                        break

                    if is_enemyPiece(checkerBoard.pieceList[tempPos], color): #enemy piece

                        is_a_capture = True

                        lookAtPos_x = temp_x_pos + move_x_pos
                        lookAtPos_y = temp_y_pos + move_y_pos

                        if inBounds(lookAtPos_x, lookAtPos_y):
                            if checkerBoard.pieceList[lookAtPos_y*8+lookAtPos_x] == 0:
                                tempMoveList.clear()

                            else:
                                break

                    else: # friendly piece
                        break

                else: # it is not a piece

                    tempMove = Move(pos, [tempPos], is_a_capture)
                    tempMoveList_isEmpty = len(tempMoveList) == 0

                    if is_a_capture:
                        tempCheckerBoard = makeMove(checkerBoard, tempMove)

                        cascadingMoves = getSingleMove(tempPos, tempCheckerBoard, color, True)

                        if not tempMoveList_isEmpty:
                            competingMoveLength = tempMoveList[0].jumpLength
                        else:
                            competingMoveLength = -1

                        if len(cascadingMoves) == 0 or not cascadingMoves[0].isCapture: # no forced captures
                            if competingMoveLength == tempMove.jumpLength:
                                tempMoveList.append(tempMove)

                            elif competingMoveLength < tempMove.jumpLength:
                                tempMoveList = [tempMove]

                        elif cascadingMoves[0].isCapture:
                            tempMoveLength = cascadingMoves[0].jumpLength + 1

                            if competingMoveLength == tempMoveLength:
                                for move_cas in cascadingMoves:
                                    tempMoveList.append(Move(pos, [tempPos]+move_cas.toPos, True))


                            elif competingMoveLength < tempMoveLength:
                                tempMoveList.clear()

                                for move_cas in cascadingMoves:
                                    tempMoveList.append(Move(pos, [tempPos]+move_cas.toPos, True))

                    else:
                        tempMoveList.append(Move(pos, [tempPos], False))

                temp_x_pos += move_x_pos
                temp_y_pos += move_y_pos
                tempPos = temp_y_pos*8 + temp_x_pos

            if len(moveList) == 0:
                moveList += tempMoveList

            elif len(tempMoveList) > 0:

                if moveList[0].jumpLength < tempMoveList[0].jumpLength:
                    moveList.clear()
                    moveList += tempMoveList

                elif moveList[0].jumpLength == tempMoveList[0].jumpLength:
                    moveList += tempMoveList

    return moveList



def getAllPossibleMoves(checkerBoard, color):

    allPossibleMoves = []
    for piecePos in checkerBoard.piecePositions:
        piece = checkerBoard.pieceList[piecePos]

        pieceColor = piece <= 2
        # print(pieceColor)

        if pieceColor == color: #only happens if the piece is the right color
            if piece % 2 == 1: #not a king


                allPossibleMoves += getSingleMove(piecePos, checkerBoard, color, False)

            else: # is a king
                allPossibleMoves += getSingleMove(piecePos, checkerBoard, color, True)

    prevMaxJumpLength = -1
    newPossibleMoveArray = []
    for move in allPossibleMoves:
        if move.jumpLength > prevMaxJumpLength:
            prevMaxJumpLength = move.jumpLength
            newPossibleMoveArray.clear()
            newPossibleMoveArray.append(move)

        elif move.jumpLength == prevMaxJumpLength:
            newPossibleMoveArray.append(move)

    return newPossibleMoveArray







# random_thing = "".join([letter for letter in "o1o1o1o1/1o1o1o1o/o1o1o1o1/1#6/2O5/1O111O1O/O1O111O1/1O1O1O1O"][::-1])





# for move in getSingleMove(8*4+6,board1, 0,True):
#     print(move.fromPos, move.toPos, move.isCapture)


# BOT CODE

maxDepth = 6

pieceValues = [0, 100, 300, -100, -300]

def pieceValueEval(checkersBoard):
    pieceSum = 0
    for piecePos in checkersBoard.piecePositions:
        pieceSum += pieceValues[checkersBoard.pieceList[piecePos]]


    return pieceSum
def evaluatePosition(checkersBoard):
    totalEval = 0

    totalEval += pieceValueEval(checkersBoard)

    return totalEval

def getBestMove(checkersBoard, color, depth):

    allPossibleMoves = getAllPossibleMoves(checkersBoard, color)

    if len(allPossibleMoves) == 0:
        if len(checkersBoard.get_PieceColorPos(color)) == 0:
            if color:
                return -10000, "NA"
            else:
                return 10000, "NA"
        else:
            return 0, "NA"

    if color:
        bestEval = -10000
    else:
        bestEval = 10000
    bestMove = allPossibleMoves[0]

    for move in allPossibleMoves:
        temp_checkersBoard = makeMove(checkersBoard, move)

        if depth + 1 >= maxDepth:
            evaluation = evaluatePosition(temp_checkersBoard)

        else:
            evaluation = getBestMove(temp_checkersBoard, not color, depth + 1)[0]

        if color:
            if evaluation > bestEval:
                bestEval = evaluation
                bestMove = move
        else:
            if evaluation < bestEval:
                bestEval = evaluation
                bestMove = move

    return evaluation, bestMove

# print(getBestMove(board1, 0, 0))
