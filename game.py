import pygame as py
import os
direct = os.getcwd()
os.chdir(direct)
py.init()
py.mixer.init()
clickSound = py.mixer.Sound("sound/click-21156.mp3")
screen = py.display.set_mode((800,400))
screen.fill("Black")
py.display.set_caption("connect4")
time = py.time.Clock()
titleFont = py.font.Font("font/windows_command_prompt.ttf", 50)
subTitleFont = py.font.Font("font/windows_command_prompt.ttf", 38)
buttonFont = py.font.Font("font/windows_command_prompt.ttf", 35)
arrowFont = py.font.Font(None, 38)
userNames = []
width = 7
height = 6
coinArray = [[0 for y in range(height)] for x in range(width)] 
winState = 0
maskBoxDict = {0: "box0", 1: "box1", 2: "box2", 3: "box3", 4: "box4", 5: "box5", 6: "box6"}
pointerText = "image/asdfghjk_2_38x38.png"
pointer = py.image.load(pointerText)
p1Counter = py.image.load("image/2yellowDotEdit_53x52.png")
p2Counter = py.image.load("image/2048px-Reddot.svg_53x52.png")
p1TotalCount = 21
p2TotalCount = 21
currentWinnerCount = 0

class Button():
    def __init__(self, text):
        self.loadText(text)
    
    def loadText(self, text):
        self.text = buttonFont.render(text, 1, py.Color("White"))
        self.size = self.text.get_size()
        self.surface = py.Surface(self.size)
        self.surface.blit(self.text,(0,0))

class Header():
    def __init__(self, text):
        self.loadText(text)
    
    def loadText(self, text):
        self.text = titleFont.render(text, 1, py.Color("White"))
        self.size = self.text.get_size()
        self.surface = py.Surface(self.size)
        self.surface.blit(self.text,(0,0))
        
class SubHeader():
    def __init__(self, text):
        self.loadText(text)
    
    def loadText(self, text):
        self.text = subTitleFont.render(text, 1, py.Color("White"))
        self.size = self.text.get_size()
        self.surface = py.Surface(self.size)
        self.surface.blit(self.text,(0,0))

class Image():
    def __init__(self,image):
        self.loadImage(image)
        
    def loadImage(self, image):
        self.image = image
        self.size = self.image.get_size()
        self.surface = py.Surface(self.size)
        self.surface.blit(self.image,(0,0))

def mainMenu():
    global p1TotalCount
    p1TotalCount = 21
    global p2TotalCount
    p2TotalCount = 21
    currentWinnerCount = 0
    mainMenuTitle = Header("Connect-4!")
    titlePos = 290, 10
    #mainMenuTitle size: 220, 44
    startButton = Button("Start Game")
    startPos = 321.5, 100
    #startButton size: 157, 31
    highScoreButton = Button("High Scores")
    highScorePos = 317.5, 150
    #highScoreButton size: 165, 32
    exitButton = Button("Exit")
    #exitButton size: 65, 31
    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.display.quit()
                py.quit()
                exit()
            if event.type == py.MOUSEBUTTONDOWN:
                clickPos = py.mouse.get_pos()
                if startButtonBox.collidepoint(clickPos) == True:
                    screen.fill("Black")
                    nameEntryScreen()
                elif highScoreBox.collidepoint(clickPos) == True:
                    screen.fill("Black")
                    highScoreMenu(tempWinner="")
                elif exitButtonBox.collidepoint(clickPos) == True:
                    py.display.quit()
                    py.quit()
                    exit()
        screen.blit(mainMenuTitle.surface,(400-(mainMenuTitle.size[0]/2), 10))
        screen.blit(startButton.surface,(400-(startButton.size[0]/2), 100))
        startButtonBox = py.Rect((400-(startButton.size[0]/2), 100), (startButton.size))
        screen.blit(highScoreButton.surface,(400-(highScoreButton.size[0]/2), 150))
        highScoreBox = py.Rect((400-(highScoreButton.size[0]/2), 150), (highScoreButton.size))
        screen.blit(exitButton.surface, ((400-exitButton.size[0]/2), 200))
        exitButtonBox = py.Rect((400-(exitButton.size[0]/2), 200), exitButton.size)
        py.display.update()
        time.tick(60)

def nameEntryScreen():
    curPlayer = 1
    nameEntryTitle = Header("--Name Entry--")
    titlePos = (245, 10)
    #nameEntryTitle size: 310, 45
    nameEntrySubTitle = SubHeader(f"--Player {curPlayer}--")
    subTitlePos = (303.5, 60)
    #nameEntrySubTitle size: 193, 35
    backButton = Button("Back")
    backPos = (721,10)
    user_text = ""
    inputBoxRect = py.Rect(370,150,60,32)
    colourActive = py.Color("Gray")
    colourPassive = py.Color("Light Gray")
    inputBoxColour = colourPassive
    letterCount = 0
    #backButton size: 69, 31
    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.display.quit()
                py.quit()
                exit()  
            if event.type == py.MOUSEBUTTONDOWN:
                clickPos = py.mouse.get_pos()
                if backButtonBox.collidepoint(clickPos) == True:
                    userNames.clear()
                    screen.fill("Black")
                    mainMenu()
                    break
                if inputBoxRect.collidepoint(clickPos) == True:
                    inputBoxColour = colourActive
                else:
                    inputBoxColour = colourPassive
            if event.type == py.KEYDOWN:
                # Check for backspace
                if event.key == py.K_BACKSPACE:
                    user_text = user_text[:-1]
                    letterCount -= 1
                #Check for Key Other Than K_BACKSPACE
                if event.key != py.K_BACKSPACE and letterCount < 3:
                    if event.key != py.K_RETURN:
                        user_text += event.unicode
                        letterCount += 1
                if letterCount == 3:
                    #Check for confirmation
                    if event.key == py.K_RETURN:
                        if curPlayer == 2 and user_text != userNames[0]:
                            userNames.append(f"{user_text}")
                            screen.fill("Black")
                            mainGame()
                            break
                        elif curPlayer == 1:
                            userNames.append(f"{user_text}")
                            user_text = ""
                            curPlayer += 1
                            letterCount = 0
                            nameEntrySubTitle = SubHeader(f"--Player {curPlayer}--")
                        elif curPlayer != 1 or 2:
                            print("Error in 'curPlayer', player not in list!")
                            exit()
        py.draw.rect(screen, inputBoxColour, inputBoxRect)
        inputBoxSurface = buttonFont.render(user_text, True, (255, 255, 255))
        screen.blit(backButton.surface, (backPos))
        screen.blit(inputBoxSurface, (inputBoxRect.x+5, inputBoxRect.y))
        screen.blit(nameEntryTitle.surface,(titlePos))
        screen.blit(nameEntrySubTitle.surface,(subTitlePos))
        backButtonBox = py.Rect((backPos), (backButton.size))
        py.display.update()
        time.tick(60)

def mainGame():
    imageText = "image/Connect4BoardEdited_467x350.png"
    connect4Board = py.image.load(imageText)
    #print(pointer.get_size())
    pointerArray = [1,0,0,0,0,0,0]
    pointerIndex = 0
    curPlayer = 0
    x = 183 #move by 66
    y = 5
    box0 = py.Surface((pointer.get_size()))
    box0.fill("Black")
    box1 = py.Surface((pointer.get_size()))
    box1.fill("Black")
    box2 = py.Surface((pointer.get_size()))
    box2.fill("Black")
    box3 = py.Surface((pointer.get_size()))
    box3.fill("Black")
    box4 = py.Surface((pointer.get_size()))
    box4.fill("Black")
    box5 = py.Surface((pointer.get_size()))
    box5.fill("Black")
    box6 = py.Surface((pointer.get_size()))
    box6.fill("Black")
    screen.blit(connect4Board, (166.5,50))
    screen.blit(pointer, (x, y))
    screen.blit(pointer, (x+66*1,y))
    screen.blit(pointer, (x+66*2,y))
    screen.blit(pointer, (x+66*3,y))
    screen.blit(pointer, (x+66*4,y))
    screen.blit(pointer, (x+66*5,y))
    screen.blit(pointer, (x+66*6,y))
    screen.blit(box1, (183+66*1,5))
    screen.blit(box2, (183+66*2,5))
    screen.blit(box3, (183+66*3,5))
    screen.blit(box4, (183+66*4,5))
    screen.blit(box5, (183+66*5,5))
    screen.blit(box6, (183+66*6,5))
    maskBoxDefArray = [box0,box1,box2,box3,box4,box5,box6]
    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.display.quit()
                py.quit()
                exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_LEFT:
                    if pointerIndex-1 >= 0:
                        c = 0
                        pointerArray[pointerIndex] = 0
                        while c != 2:
                            if maskBoxDefArray[pointerIndex] == box0:
                                changeBox(pointerArray[pointerIndex], pointerIndex, maskBoxDefArray, x, y)
                            elif maskBoxDefArray[pointerIndex] == box1:
                                changeBox(pointerArray[pointerIndex], pointerIndex, maskBoxDefArray, x, y)
                            elif maskBoxDefArray[pointerIndex] == box2:
                                changeBox(pointerArray[pointerIndex], pointerIndex, maskBoxDefArray, x, y)
                            elif maskBoxDefArray[pointerIndex] == box3:
                                changeBox(pointerArray[pointerIndex], pointerIndex, maskBoxDefArray, x, y)
                            elif maskBoxDefArray[pointerIndex] == box4:
                                changeBox(pointerArray[pointerIndex], pointerIndex, maskBoxDefArray, x, y)
                            elif maskBoxDefArray[pointerIndex] == box5:
                                changeBox(pointerArray[pointerIndex], pointerIndex, maskBoxDefArray, x, y)
                            elif maskBoxDefArray[pointerIndex] == box6:
                                changeBox(pointerArray[pointerIndex], pointerIndex, maskBoxDefArray, x, y)
                            if c != 1:
                                pointerIndex -= 1
                                pointerArray[pointerIndex] = 1
                            c += 1
                if event.key == py.K_RIGHT:
                    if pointerIndex+1 <= 6:
                        d = 0
                        pointerArray[pointerIndex] = 0
                        while d != 2:
                            if maskBoxDefArray[pointerIndex] == box0:
                                changeBox(pointerArray[pointerIndex], pointerIndex, maskBoxDefArray, x, y)
                            elif maskBoxDefArray[pointerIndex] == box1:
                                changeBox(pointerArray[pointerIndex], pointerIndex, maskBoxDefArray, x, y)
                            elif maskBoxDefArray[pointerIndex] == box2:
                                changeBox(pointerArray[pointerIndex], pointerIndex, maskBoxDefArray, x, y)
                            elif maskBoxDefArray[pointerIndex] == box3:
                                changeBox(pointerArray[pointerIndex], pointerIndex, maskBoxDefArray, x, y)
                            elif maskBoxDefArray[pointerIndex] == box4:
                                changeBox(pointerArray[pointerIndex], pointerIndex, maskBoxDefArray, x, y)
                            elif maskBoxDefArray[pointerIndex] == box5:
                                changeBox(pointerArray[pointerIndex], pointerIndex, maskBoxDefArray, x, y)
                            elif maskBoxDefArray[pointerIndex] == box6:
                                changeBox(pointerArray[pointerIndex], pointerIndex, maskBoxDefArray, x, y)
                            if d != 1:
                                pointerIndex += 1
                                pointerArray[pointerIndex] = 1
                            d += 1
                if event.key == py.K_RETURN:
                    if curPlayer == 0:
                        counterFunc = placeCounter(0, p1Counter, pointerIndex)
                        #py.time.wait(100)
                        if counterFunc == True:
                            tempWinner = ""
                            tempWinner += userNames[curPlayer]
                            displayWinName(1)
                            py.display.update()
                            py.time.wait(5000)
                            screen.fill("Black")
                            highScoreMenu(tempWinner)
                            break
                        curPlayer = 1
                    elif curPlayer == 1:
                        counterFunc = placeCounter(1, p2Counter, pointerIndex)
                        #py.time.wait(100)
                        if counterFunc == True:
                            tempWinner = ""
                            tempWinner += userNames[curPlayer]
                            displayWinName(2)
                            py.display.update()
                            py.time.wait(5000)
                            screen.fill("Black")
                            highScoreMenu(tempWinner)
                            break
                        curPlayer = 0
                    else:
                        print("Error in 'curPlayer'! Ending program...")
        py.display.update()
        time.tick(60)

def highScoreMenu(tempWinner):
    global currentWinnerCount
    index = 0
    invalid = 0
    backButton = Button("Back")
    backPos = (721,10)
    tempScoreArray = []
    highScoreTitle = Header("--High Scores--")
    scoreTitlePos = (237, 10)
    #highScoreTitle size: 326, 45
    try:
        with open("scores/scoreList.txt", "r") as scoreList:
            for line in scoreList:
                tempScoreArray.append(line.strip().split())
            scores = [[int(x[0]),x[1]] for x in tempScoreArray]
            scores = sorted(scores)
            scores.reverse()
        while index != len(scores):
            if scores[index][1] == tempWinner:
                scores[index][0] = currentWinnerCount
                scores = sorted(scores)
                scores.reverse()
                invalid = 1
                break
            else:
                index += 1
        if invalid == 0:
            if tempWinner != "":
                scores.append([currentWinnerCount, tempWinner])
                scores = sorted(scores)
                scores.reverse()
        with open("scores/scoreList.txt", "w") as outList:
            index = 0
            while index != len(scores):  
                outList.write(f"{scores[index][0]} {scores[index][1]}\n")
                index += 1
    except:
        print("Error in scoreList")
    # curNum = 1
    # for instance in range(len(scores)):
    #     instance = SubHeader(f"{curNum}. {scores[0][1]} ({scores[0][0]})")
    #     screen.blit(instance.surface, (400-(instance.size[0]/2),300))
    #     pass
    try:
        if scores[0] in scores:
            topScore1 = SubHeader(f"1. {scores[0][1]} ({scores[0][0]})")
            screen.blit(topScore1.surface, (240-(topScore1.size[0]/2),100))
        if scores[1] in scores:
            topScore2 = SubHeader(f"2. {scores[1][1]} ({scores[1][0]})")
            screen.blit(topScore2.surface, (240-(topScore2.size[0]/2),150))
        if scores[2] in scores:
            topScore3 = SubHeader(f"3. {scores[2][1]} ({scores[2][0]})")
            screen.blit(topScore3.surface, (240-(topScore3.size[0]/2),200))
        if scores[3] in scores:
            topScore4 = SubHeader(f"4. {scores[3][1]} ({scores[3][0]})")
            screen.blit(topScore4.surface, (240-(topScore4.size[0]/2),250))
        if scores[4] in scores:
            topScore5 = SubHeader(f"5. {scores[4][1]} ({scores[4][0]})")
            screen.blit(topScore5.surface, (240-(topScore5.size[0]/2),300))
        if scores[5] in scores:
            topScore6 = SubHeader(f"6. {scores[5][1]} ({scores[5][0]})")
            screen.blit(topScore6.surface, (560-(topScore6.size[0]/2),100))
        if scores[6] in scores:
            topScore7 = SubHeader(f"7. {scores[6][1]} ({scores[6][0]})")
            screen.blit(topScore7.surface, (560-(topScore7.size[0]/2),150))
        if scores[7] in scores:
            topScore8 = SubHeader(f"8. {scores[7][1]} ({scores[7][0]})")
            screen.blit(topScore8.surface, (560-(topScore8.size[0]/2),200))
        if scores[8] in scores:
            topScore9 = SubHeader(f"9. {scores[8][1]} ({scores[8][0]})")
            screen.blit(topScore9.surface, (560-(topScore9.size[0]/2),250))
        if scores[9] in scores:
            topScore10 = SubHeader(f"10. {scores[9][1]} ({scores[9][0]})")
            screen.blit(topScore10.surface, (560-(topScore10.size[0]/2),300))
    except:
        print("Game lacks top scores")
    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.display.quit()
                py.quit()
                exit()
            if event.type == py.MOUSEBUTTONDOWN:
                clickPos = py.mouse.get_pos()
                if backButtonBox.collidepoint(clickPos) == True:
                    userNames.clear()
                    screen.fill("Black")
                    mainMenu()
                    break
        screen.blit(backButton.surface, backPos)
        screen.blit(highScoreTitle.surface, scoreTitlePos)
        backButtonBox = py.Rect((backPos), (backButton.size))
        py.display.update()
        time.tick(60)

def loadMusic():
    py.mixer.music.load("music/slow-2021-10-19_-_Funny_Bit_-_www.FesliyanStudios.com.mp3")
    py.mixer.music.set_volume(0.1)
    py.mixer.music.play(-1)

def stopMusic():
    py.mixer.music.stop()

def playClick():
    py.mixer.Sound.play(clickSound)

def changeBox(boxNum, pointerIndex, maskBoxDefArray, x, y):
    if boxNum == 0:
        #py.transform.scale(maskBoxDefArray[pointerIndex] ,(maskBoxDefArray[pointerIndex].get_width(), maskBoxDefArray[pointerIndex].get_height()))
        screen.blit(maskBoxDefArray[pointerIndex], (x+66*pointerIndex, y))
    elif boxNum == 1:
        #py.transform.scale(maskBoxDefArray[pointerIndex], (0,0))
        screen.blit(pointer, (x+66*pointerIndex, y))
        
def placeCounter(curPlayer, counter, pointerIndex):
    global p1TotalCount
    global p2TotalCount
    global currentWinnerCount
    index = 0
    c = 0
    win = False
    while c != 5:
        if coinArray[pointerIndex][index] == 0:
            c = 5
        if c != 5:
            index += 1
            c += 1
        elif c == 5:
            c = 5
    if curPlayer == 0:
        if coinArray[pointerIndex][5] == 0:
            p1TotalCount -= 1
            screen.blit(counter, (176.5+65.5*pointerIndex, 346-58.5*index))
            playClick()
            coinArray[pointerIndex][index] += 1
            winState = winCheck(win, coinArray, 1)
            if winState == True:
                currentWinnerCount = p1TotalCount
                for x in range(width):
                    for y in range(height):
                        coinArray[x][y] = 0
                return True
    elif curPlayer == 1:
        if coinArray[pointerIndex][5] == 0:
            p2TotalCount -= 1
            screen.blit(counter, (176.5+65.5*pointerIndex, 346-58.5*index))
            playClick()
            coinArray[pointerIndex][index] += 2
            winState = winCheck(win, coinArray, 2)
            if winState == True:
                currentWinnerCount = p2TotalCount
                for x in range(width):
                    for y in range(height):
                        coinArray[x][y] = 0
                return True
    
def winCheck(win, coinArray, curPlayer):
    count = 0
    for y in range(height):
        for x in range(width):
            if coinArray[x][y] == curPlayer:
                count += 1
                if count >= 4:
                    #print("1")
                    #print(coinArray)
                    win = True
                    return win
            else:
                count = 0
    count = 0
    for x in range(width):
        for y in range(height):
            if coinArray[x][y] == curPlayer:
                count += 1
                if count >=4:
                    #print("2")
                    #print(coinArray)
                    win = True
                    return win
            else:
                count = 0          
    count = 0
    for x in range(width):
        for y in range(height):
            xIndex = x
            yIndex = y
            while xIndex < width and yIndex < height:
                if coinArray[xIndex][yIndex] == curPlayer:
                    count += 1
                    if count >= 4:
                        #print("3")
                        #print(coinArray)
                        win = True
                        return win
                else:
                    count = 0
                xIndex += 1
                yIndex += 1
    count = 0
    for x in range(width-1,0,-1):
        for y in range(height):
            xIndex = x
            yIndex = y
            while xIndex < width and yIndex < height:
                if coinArray[xIndex][yIndex] == curPlayer:
                    count += 1
                    if count >= 4:
                        #print('4')
                        #print(coinArray)
                        win = True
                        return win
                else:
                    count = 0
                xIndex -= 1
                yIndex += 1

def displayWinName(curPlayer):
    winText = Header(f"Player {curPlayer} Wins!")
    #winText size: 288,45
    screen.blit(winText.surface,(256,5))

loadMusic()
mainMenu()