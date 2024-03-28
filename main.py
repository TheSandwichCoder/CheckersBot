import random

import pygame
import checkerBot
from checkerBot import CheckersBoard

pygame.init()
pygame.font.init()
pygame.display.init()

screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("Checkers")
clock = pygame.time.Clock()

running = True
randomTempThing = False

background = pygame.Surface((600, 600))
background.fill(((238,238,210)))

squareSize = 600/8

font1 = pygame.font.Font("assets/Poppins-Regular.ttf", 60)
font2 = pygame.font.Font("assets/Poppins-Regular.ttf", 35)

for x in range(8):
    for y in range(8):
        if x%2 == y%2:
            pygame.draw.rect(background, (237, 85, 116), pygame.Rect(x*squareSize, y*squareSize, squareSize, squareSize))


mainCheckerBoard = CheckersBoard(0, 0)

# O1O1O1O1/1O1O1O1O/O1O1O1O1/8/8/1o1o1o1o/o1o1o1o1/1o1o1o1o/
mainCheckerBoard.initialiseBoardWithFEN("O1O1O1O1/1O1O1O1O/O1O1O1O1/8/8/1o1o1o1o/o1o1o1o1/1o1o1o1o/")

def get_SelectMoveCoordinates(move):
    if not move.isKingMove:
        if not move.isCapture:
            return move.toPos[0]

        else:
            temp_fromPos = move.fromPos
            for toPos in move.toPos:
                temp_fromPos = toPos*2 - temp_fromPos

            return temp_fromPos
    else:
        return move.toPos[-1]



def get_moveDisplayCoordinates(move):
    if not move.isKingMove:

        if not move.isCapture:
            return move.toPos

        else:
            moveThingArray = []
            temp_fromPos = move.fromPos

            for toPos in move.toPos:
                temp_fromPos = toPos*2 - temp_fromPos
                moveThingArray.append(temp_fromPos)

            return moveThingArray
    else:
        return move.toPos

def drawCheckerBoard(checkerBoard):
    for piecePos in checkerBoard.piecePositions:
        x, y = checkerBot.get_2d_Pos(piecePos)
        x = 7-x
        y = 7-y
        if piecePos == selectedSquare:
            continue

        pos = (x*squareSize+squareSize/2, y*squareSize+squareSize/2)
        if checkerBoard.pieceList[piecePos] == 1:
            pygame.draw.circle(screen,  (255, 255, 255), pos, squareSize*0.4)

        elif checkerBoard.pieceList[piecePos] == 3:
            pygame.draw.circle(screen,  (0, 0, 0), pos, squareSize * 0.4)

        elif checkerBoard.pieceList[piecePos] == 2:
            pygame.draw.circle(screen, (255, 209, 209), pos, squareSize * 0.4)
            pygame.draw.circle(screen, (255, 255, 255), pos, squareSize * 0.3)

        elif checkerBoard.pieceList[piecePos] == 4:

            pygame.draw.circle(screen, (84, 42, 42), pos, squareSize * 0.4)
            pygame.draw.circle(screen, (0, 0, 0), pos, squareSize * 0.3)


def drawPiece(type, pos):
    if type == 1:
        pygame.draw.circle(screen, (255, 255, 255), pos, squareSize * 0.4)
    elif type == 3:
        pygame.draw.circle(screen, (0, 0, 0), pos, squareSize * 0.4)

    elif type == 2:
        pygame.draw.circle(screen, (255, 209, 209), pos, squareSize * 0.4)
        pygame.draw.circle(screen, (255, 255, 255), pos, squareSize * 0.3)

    elif type == 4:
        pygame.draw.circle(screen, (84, 42, 42), pos, squareSize * 0.4)
        pygame.draw.circle(screen, (0, 0, 0), pos, squareSize * 0.3)

    elif type == 10:
        pygame.draw.circle(screen, (158, 212, 175), pos, squareSize * 0.4)

    elif type == 11:
        pygame.draw.circle(screen, (196, 212, 202), pos, squareSize * 0.4)

def drawCoordinates():
    coordFont = pygame.font.Font("assets/Poppins-Regular.ttf", 20)
    for i in range(8):
        screen.blit(coordFont.render(str(8-i), 1, (0,0,0)), (0, i*squareSize))

    letterThing = "abcdefgh"
    height = coordFont.render(letterThing[i], 1, (0, 0, 0)).get_height()
    for i in range(1,9):
        screen.blit(coordFont.render(letterThing[i-1], 1, (0, 0, 0)), (i*squareSize-height, squareSize * 8 - height))

def convertSquareToCoordinates(square):
    y_pos = (63-square)//8
    x_pos = (63-square)%8
    letterThing = "abcdefgh"

    return letterThing[x_pos]+str(8-y_pos)

allPossibleMoves_white = checkerBot.getAllPossibleMoves(mainCheckerBoard, 1)

# for move in allPossibleMoves_white:
#     print(move.fromPos, move.toPos, move.isCapture)
# print(mainCheckerBoard.pieceList[32], "sadasdas")

allPossibleMoves_black = checkerBot.getAllPossibleMoves(mainCheckerBoard, 0)

# print(allPossibleMoves_black)

selectingPiece = False

from_selected_x = 0
from_selected_y = 0

selected_x = 0
selected_y = 0

selectedSquare = 65

gameState = 1

# GAMESTATES:
# 1 - playing
# 2 - white wins
# 3 - black wins
# 4 - draw

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    mousePos = pygame.mouse.get_pos()

    screen.blit(background, (0,0))
    drawCheckerBoard(mainCheckerBoard)



    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        drawCoordinates()
    if keys[pygame.K_f]:
        print(mainCheckerBoard.convertBoardToFEN())

    if gameState == 1:

        if pygame.mouse.get_pressed()[0]:
            if not selectingPiece:
                from_selected_x = int(mousePos[0] // squareSize)
                from_selected_y = int(mousePos[1] // squareSize)

                tempSelected = 63-(from_selected_y*8 + from_selected_x)

                if mainCheckerBoard.pieceList[tempSelected] <= 2:

                    selectedSquare = tempSelected
                else:
                    selectedSquare = 65

            selectingPiece = True

            selected_x = int(mousePos[0]//squareSize)
            selected_y = int(mousePos[1]//squareSize)

            foundThing = False
            for move in allPossibleMoves_white:
                if move.fromPos == selectedSquare:
                    for toPos in get_moveDisplayCoordinates(move):
                        temp_x, temp_y = checkerBot.get_2d_Pos(toPos)
                        temp_x = 7 - temp_x
                        temp_y = 7 - temp_y
                        drawPiece(10, (temp_x*squareSize + squareSize/2, temp_y*squareSize + squareSize/2))
                    foundThing = True

            if not foundThing:
                for move in allPossibleMoves_white:
                    for toPos in get_moveDisplayCoordinates(move):
                        temp_x, temp_y = checkerBot.get_2d_Pos(toPos)
                        temp_x = 7 - temp_x
                        temp_y = 7 - temp_y
                        drawPiece(11, (temp_x*squareSize + squareSize/2, temp_y*squareSize + squareSize/2))

                    temp_x, temp_y = checkerBot.get_2d_Pos(move.fromPos)
                    temp_x = 7 - temp_x
                    temp_y = 7 - temp_y
                    drawPiece(10, (temp_x * squareSize + squareSize / 2, temp_y * squareSize + squareSize / 2))

            if selectedSquare != 65:
                drawPiece(mainCheckerBoard.pieceList[selectedSquare], mousePos)


        else:
            if selectingPiece:


                # print(selectedSquare, (selected_y*8+selected_x))
                for move in allPossibleMoves_white:
                    # print(move.fromPos, move.toPos)
                    if move.fromPos == selectedSquare and 63-(selected_y*8+selected_x) == get_SelectMoveCoordinates(move):
                        mainCheckerBoard = checkerBot.makeMove(mainCheckerBoard, move)
                        allPossibleMoves_white = checkerBot.getAllPossibleMoves(mainCheckerBoard, 1)

                        allPossibleMoves_black = checkerBot.getAllPossibleMoves(mainCheckerBoard, 0)

                        if len(allPossibleMoves_black) == 0:
                            if len(mainCheckerBoard.get_PieceColorPos(0)) == 0:
                                gameState = 2
                            else:
                                gameState = 4

                        if gameState == 1:
                            # randomMove = random.choice(allPossibleMoves_black)

                            # bestMove = random.choice(allPossibleMoves_black)

                            eval, bestMove = checkerBot.getBestMove(mainCheckerBoard, False, 0)
                            mainCheckerBoard = checkerBot.makeMove(mainCheckerBoard, bestMove)
                            allPossibleMoves_white = checkerBot.getAllPossibleMoves(mainCheckerBoard, 1)
                            if len(allPossibleMoves_white) == 0:
                                if len(mainCheckerBoard.get_PieceColorPos(1)) == 0:
                                    gameState = 3
                                    break

                            # print(mainCheckerBoard.convertBoardToFEN())
                            whiteBestMove = checkerBot.getBestMove(mainCheckerBoard, True, 0)[1]

                            print(f"\nBot Made Move:{convertSquareToCoordinates(bestMove.fromPos)}|{convertSquareToCoordinates(get_SelectMoveCoordinates(bestMove))}")
                            print("botEval",eval, f"   Your Best Move:{convertSquareToCoordinates(whiteBestMove.fromPos)}|{convertSquareToCoordinates(get_SelectMoveCoordinates(whiteBestMove))}")
                            break

                selectedSquare = 65
            selectingPiece = False

    elif gameState == 2:
        text1 = font1.render("WHITE WINS", 1, (0,0,0))
        width, height = text1.get_size()

        screen.blit(text1, ((600-width)/2, (600-height)/2))


    elif gameState == 3:
        text1 = font2.render("BLACK WINS", 1, (0, 0, 0))
        width, height = text1.get_size()

        screen.blit(text1, ((600 - width) / 2, (600 - height) / 2))

    elif gameState == 4:
        text1 = font2.render("DRAW", 1, (0, 0, 0))
        width, height = text1.get_size()

        screen.blit(text1, ((600 - width) / 2, (600 - height) / 2))

    if gameState >= 2:
        text1 = font2.render("press [space] to play again", 1, (0, 0, 0))
        width, height = text1.get_size()


        screen.blit(text1, ((600 - width) / 2, (600 - height) / 2 + 60))

        if keys[pygame.K_SPACE]:
            mainCheckerBoard = CheckersBoard(0, 0)
            mainCheckerBoard.initialiseBoardWithFEN("O1O1O1O1/1O1O1O1O/O1O1O1O1/8/8/1o1o1o1o/o1o1o1o1/1o1o1o1o/")
            gameState = 1

    clock.tick(60)
    pygame.display.flip()
