import os.path
import os
import time


# Shift F10 to run, 2xShift to search

def SetBaseVariables(): # this is used to make sure all global variables have been declared
    # variables to know if the files has been found in the system
    global oldFileFound

    oldFileFound = False

    # world variables that are mostly constant across the whole program
    global paintAreaPerLitre  # m2 per liter
    global paintSizes # the size of the paint cam
    global paintPrices  # price for 5 liters in GBP
    global paintName  # name of the paint used for this program
    global paintColor  # color of the paint
    global paintFinish  # finish of the paint, like eggshell or silk or matt
    global paintChoice # the choice of paint from the menu provided

    paintName = "Dulux"
    paintPrices = "16/18/22"
    paintColor = "White"
    paintFinish = "Matt"
    paintAreaPerLitre = 13
    paintSizes = "2.5/5/10"
    paintChoice = 1


    # variables needed to do the math of the walls and the paint needed for it
    global info_walls  # num of walls needed to be painted
    global info_wallMeasurements  # measurements of the walls that are going to be painted
    global info_lastInputWall  # if the client puts a value wrong in the wall measurements section, they can continue
    global info_exceptions # num of chunks in the walls that don't need to be painted
    global info_exceptionMeasurements # measurements of the chunks of wall that don't need painting
    global info_lastInputException # if the client puts a value wrong in the exceptions section, they can continue
    global info_coats # number of coats used per each wall

    info_walls = 0
    info_wallMeasurements = []
    info_lastInputWall = 1
    info_exceptions = 0
    info_exceptionMeasurements = []
    info_lastInputException = 1
    info_coats = 0

    global info_primerSize # the size of the primer can
    global info_primerAreaPerLitre # the coverage area that a primer can get with 1 litre
    global info_primerPrice # the price of primer per can

    info_primerPrice = 10
    info_primerAreaPerLitre = 10
    info_primerSize = "2.5"

    if os.path.exists("primerData.csv"):
        primerCSV = True

    if primerCSV:
        fileContent = open("primerData.csv",'r').read()
        fileContent = fileContent.split(',')
        info_primerPrice = fileContent[3]
        info_primerAreaPerLitre = fileContent[1]
        info_primerPrice = fileContent[2]

    return True

def Main():
    os.system('cls')
    createdBaseVariables = SetBaseVariables()
    # print welcome to the program
    print("Hello and welcome to your personal wall painting calculator!")
    # if there is an old file attached to this program, tell the program that it is available, otherwise tell it to
    # not try anything
    oldFileFound = False

    if os.path.exists("oldCalculation.txt"):
        oldFileFound = True

    MainMenu(oldFileFound);

### MAIN MENU ###-------------------------------------------------------------------------------------------------------

def MainMenu(oldFileFound):
    # print the needed menu items, and also print view last file if the client wants to see it
    print("1. Create new calculation")
    if oldFileFound: print("2. View old calculation")
    valid = False
    while not valid:
        try:
            menuChoice = int(input("Please select which option you would like "))
            if menuChoice == 1 or menuChoice == 2: valid = True
        except ValueError: print("Sorry, that is not a valid option, please try again")

    match menuChoice:
        case 1:
            print("Proceeding to new calculation menu")
            InformationWallNumberGathering()
        case 2:
            print("Sure, I will load up your previous session right away")
            LoadLastFile()

### READ FILE ###-------------------------------------------------------------------------------------------------------

def LoadLastFile():
    # open the file and split it all by lines
    file = open("oldCalculation.txt",'r')
    fileContent = file.read()
    lineSplitContents = fileContent.split("\n")
    PrintFileContent(lineSplitContents)

def PrintFileContent(content):
    global paintChoice

    # needed variables to print the final document
    customerName = "blank"
    numOfWalls = 0
    wallMeasurements = []
    numOfExceptions = 0
    exceptionsMeasurements = []
    numOfPaintCans = []
    numOfCoats = 0
    primerNeeded = 0

    # variables used for internal tracking and finding the information in the file being read
    currentLine = "blank"

    # for loop to go through each line and extract the variables based on a match statement and known words in the file
    for lineNum, i in enumerate(content):
        #print(lineNum)
        lineContent = i.split(',')
        lineHeader = str(lineContent[0])

        #match case used for
        match lineHeader:
            case "ClientName":
                customerName = lineContent[1]
            case "Walls":
                numOfWalls = int(lineContent[1])
                currentLine = "walls"
            case "Exceptions":
                numOfExceptions = int(lineContent[1])
                if numOfExceptions > 0 : currentLine = "exceptions"
            case "PaintNeeded":
                currentLine = "paints"
            case "PrimerNeeded":
                primerNeeded = lineContent[1]
                currentLine = "primer"
            case "CoatsNeeded":
                numOfCoats = int(lineContent[1])
                currentLine = "coats"
            case "TotalCost":
                costForProj = lineContent[1]
            case _:
                match currentLine:
                    case "walls":
                        wallMeasurements.append([lineContent[1],lineContent[2]])
                    case "exceptions":
                        exceptionsMeasurements.append([lineContent[1],lineContent[2]])
                    case "paints":
                        numOfPaintCans.append([lineContent[0], lineContent[1]])

    # use functions to calculate the wall area and the chunks of wall to take out
    totalAreaOfWalls = areaOfWall(wallMeasurements)
    totalAreaOfException = areaOfExceptions(exceptionsMeasurements)
    # take the chunks out of the wall area and have the final wall area needing painting
    totalPaintableArea = totalAreaOfWalls - totalAreaOfException

    # print some structured stuff to show the client their last data
    os.system('cls')
    print()
    print(f"Hello, {customerName}")
    print(f"Per you last calculation, you had {numOfWalls} walls with a total area of {totalPaintableArea} m2")

    #if multiple cans, use plural
    if int(primerNeeded) > 1: cans = "cans"
    else: cans = "can"

    #print primer needed
    print(f"You will need {primerNeeded} x {info_primerSize} litre {cans} of primer")
    print(f"You will also need this amount of paint for this project")

    # for each can of paint needed for the project, print new line with the number, the size and the total price
    totalPrice = 0
    for i in numOfPaintCans:
        if int(i[1]) > 0:
            if int(i[1]) > 1: cans = "cans"
            else: cans = "can"

            print(f"- {i[1]} x {i[0]} litre {cans}")


    #print final price of project
    print(f"In total, this project will cost £{costForProj}")

def areaOfWall(wallMeasurements): # this is used to return the area of the walls that need painting
    totalArea = 0
    for i in wallMeasurements:
        totalArea += float(i[0]) * float(i[1])
    return totalArea

def areaOfExceptions(exceptionMeasurements): # this is used to return the area of the walls that don't need painting
    totalArea = 0
    for i in exceptionMeasurements:
        totalArea += float(i[0]) * float(i[1])
    return totalArea

### GET INFORMATION ON THE WALLS ###------------------------------------------------------------------------------------

def InformationWallNumberGathering(): # get how many walls the use wants to paint
    print()
    global info_walls

    valid = False
    while not valid: # way of making sure that the thing going forward is definitely going to run

        try:
            info_walls = int(input("How many walls do you want to pain? "))
            if info_walls > 0: valid = True

        except ValueError: # if they don't use a whole number, tell them and start this function again
            print("I'm sorry, that was not a whole number, please try again")

    InformationWallMeasurementsGathering()

def InformationWallMeasurementsGathering(): # for each wall that they want painting, ask the width and height
    print()
    global info_lastInputWall # global variable
    tempStart = info_lastInputWall # allow user to continue where they left off, instead of starting from 0

    for i in range(tempStart,info_walls+1):

        valid1 = False # way of making sure that the thing going forward is definitely going to run
        while not valid1:
            try:
                tempWallWidth = float(input(f"What is the width (meters) of the {i} wall you want to paint? "))
                if tempWallWidth > 0: valid1 = True

            except ValueError: # if input is not float, tell user to use a float
                print("I'm sorry, that is not a valid decimal number, please start again")


        valid2 = False # way of making sure that the thing going forward is definitely going to run
        while not valid2:
            try:
                tempWallHeight = float(input(f"What is the height (meters) of the {i} wall you want to paint? "))
                if tempWallHeight > 0: valid2 = True

            except ValueError: # if input is not float, tell user to use a float
                print("I'm sorry, that is not a valid decimal number, please start again")


        if valid1 and valid2:
            info_lastInputWall += 1
            info_wallMeasurements.append([tempWallWidth, tempWallHeight]) # add measurements to list of wall measurements
            if info_walls == 1: break

    InformationExceptionNumberGathering()


### GET INFORMATION ON THE SECTIONS TO CUT OUT ###----------------------------------------------------------------------

def InformationExceptionNumberGathering():
    print()
    global info_exceptions # global variable

    valid = False
    while not valid: # way of making sure that the thing going forward is definitely going to run

        try:
            info_exceptions = int(input(f"How many sections in those walls don't need painting (doors, windows, power outlets) "))
            if info_exceptions >= 0: valid = True; break

        except ValueError: # if it's not given an int, error out and restart function
            print(f"That is not a valid option, please use a number")

    if info_exceptions == 0: CoatsOfPaint()
    else: InformationExceptionMeasurementGathering()
    # go to next part of code

def InformationExceptionMeasurementGathering():
    print()
    global info_lastInputException  # global variable
    tempStart = info_lastInputException  # allow user to continue where they left off, instead of starting from 0

    for i in range(tempStart, info_walls + 1):
        valid1 = False
        while not valid1:  # way of making sure that the thing going forward is definitely going to run

            try:
                tempExceptionWidth = float(input(f"What is the width (meters) of the {i} section you don't need to paint? "))
                if tempExceptionWidth > 0: valid1 = True

            except ValueError:  # if input is not float, tell user to use a float
                print("I'm sorry, that is not a valid decimal number, please start again")

        valid2 = False
        while not valid2:

            try:
                tempExceptionHeight = float(input(f"What is the height (meters) of the {i} section you don't need to paint? "))
                if tempExceptionHeight > 0: valid2 = True

            except ValueError:  # if input is not float, tell user to use a float
                print("I'm sorry, that is not a valid decimal number, please start again")

        info_lastInputException += 1
        info_wallMeasurements.append([tempExceptionWidth, tempExceptionHeight]) # add measurements to list of wall measurements
        if info_exceptions == 1: break


    CoatsOfPaint()

def CheckIfAreaIsBigger():

    return False

### GET PAINT INFORMATION ###-------------------------------------------------------------------------------------------

def CoatsOfPaint(): # ask the client how many coats of paint they want to put into this
    print()
    global info_coats

    try:
        userAnswer = int(input("How many coats of paint would you like to apply for the walls? (2 coats is recommended) "))
    except ValueError: # if int not provided, give feedback and ask again
        print("I'm sorry, please use a whole number")
        CoatsOfPaint()
    info_coats = userAnswer
    InformationPaintGathering()

def InformationPaintGathering():
    print()
    # ask user for input regarding their knowledge of the
    userAnswer = str(input("Do you know which kind of paint you want to use (yes or no)? ")).lower()

    match userAnswer: # switch statement used for input of the customer
        case "yes":
            print("Ok, taking you to the next screen")
            InformationPaintDetailsGathering()
        case "no":
            print("Ok, showing you the results for your search")
            PaintRelatedMaths()
        case _:
            print("I'm sorry, I didn't quite understand that, please try again (yes or no answers)")
            InformationPaintGathering()

def InformationPaintDetailsGathering():
    global paintChoice
    os.system('cls')
    print()

    if os.path.exists("paintData.csv"):
        paintCSV = True
    else:
        print("I'm sorry, it seems that the paint table is missing. You will have to use the default paints we have available")
        time.sleep(2)
        PaintRelatedMaths()


    if paintCSV:
        fileContent = open("paintData.csv", 'r').read()
        allLines = fileContent.splitlines()
        for count, line in enumerate(allLines):
            if count==0: continue

            tempLine = line.split(',')
            print(f"{count}. Name:{tempLine[0]} Color:{tempLine[1]} Finish:{tempLine[2]} Available in {tempLine[3]} litres at prices of {tempLine[4]} respectively. It covers {tempLine[5]} m2 per litre")
            print("----------------------------------------------------------------------------------------------------")

    valid = False
    while not valid:
        try:
            userChoice = int(input("Which paint would you like to use? (insert number before paint name) "))
            if userChoice > 0 and userChoice < len(allLines): valid = True
        except ValueError:
            print("Please select a valid number in the list")

    paintChoice = userChoice

    ReadPaintDataAndContinue()

def ReadPaintDataAndContinue():
    global paintAreaPerLitre
    global paintPrices
    global paintName
    global paintColor
    global paintFinish
    global paintSizes

    paintData = ReadPaintFileDataRaw(paintChoice)
    print(paintData)
    paintName = paintData[0]
    paintColor = paintData[1]
    paintFinish = paintData[2]
    paintSizes = paintData[3]
    paintPrices = paintData[4]
    paintAreaPerLitre = int(paintData[5])

    PaintRelatedMaths()

### READ PAINT DATA FROM ANYWHERE IN THE SCRIPT ### --------------------------------------------------------------------

def ReadPaintFileDataRaw(lineToRead):
    paintCSV = False
    if os.path.exists("paintData.csv"):
        paintCSV = True

    if paintCSV:
        fileContent = open("paintData.csv", 'r').read()
        allLines = fileContent.splitlines()
        for count, line in enumerate(allLines):
            if count == lineToRead:
                return line.split(',') # only return the chosen paint color


### PRINT STUFF IN COMMAND LINE ###-------------------------------------------------------------------------------------

def PaintRelatedMaths():
    print()
    # some math about the basic stuff
    wallArea = areaOfWall(info_wallMeasurements)
    exceptionArea = areaOfExceptions(info_exceptionMeasurements)
    totalArea = wallArea - exceptionArea

    # calculate how many cans of painter are needed
    primerNeeded = round(((totalArea / 9) * 1.1), 2)
    primerCans = 1
    tempPrimer = float(primerNeeded)

    #while loop for how much primer is needed
    while tempPrimer > float(info_primerSize):
        primerCans += 1
        tempPrimer -= float(info_primerSize)

    primerPrice = int(info_primerPrice) * int(primerCans)

    #calculate the best way to have the cans arranged
    paintNeeded = round((((totalArea * info_coats) / paintAreaPerLitre) * 1.1), 2)

    totalPaintCans = []

    result = paintSizes.split('/')
    tempPaint = paintNeeded
    lowerCans = 1

    # make dict for all the paint values available for the current paint
    paintSizeDict = {key : 0 for key in result}

    # find how many small cans can be used to
    while tempPaint > 0:
        if tempPaint > float(result[0]):
            lowerCans += 1
            tempPaint -= float(result[0])
        else: break

    # go through each result again, this time with a counter
    for count, i in enumerate(result):
        if count == len(result)-1: break
        # how many small cans can go into the next tier of cans
        dividingFactor = float(result[count+1]) / float(i)
        # get the remainder and the division result
        upperCans, lowerCans = divmod(float(lowerCans), float(dividingFactor))
        # put results in the dictionary as values for each key
        paintSizeDict[i] = int(lowerCans)
        paintSizeDict[result[count+1]] = int(upperCans)

        lowerCans = upperCans

    #total price for each thing
    totalPrice = 0
    tempPrices = paintPrices.split('/')

    for count, i in enumerate(paintSizeDict.values()):
        priceForThisCan = int(tempPrices[count]) * i
        totalPrice += priceForThisCan

    ShowFinalResults(totalArea, primerNeeded, primerCans, primerPrice, paintSizeDict, paintNeeded, totalPrice)

### SHOW THE FINAL RESULTS TO USER ###----------------------------------------------------------------------------------

def ShowFinalResults(totalArea, primerNeeded, primerCans, primerPrice, individualPaints, totalPaintNeeded, totalPrice):
    os.system('cls') # clear console for a better look

    print()
    print(f"You need to paint {round(totalArea,2)} m2 of wall in total")
    print(f"In terms of primers, you will need {primerCans} {info_primerSize} Litre cans at a price of £{primerPrice}")
    print(f"In terms of paint, you will need to cover {totalPaintNeeded}m2 in total, at a rate of {paintAreaPerLitre}m2 per litre")

    for i in individualPaints.keys():
        # if no cans used, continue
        if individualPaints[i] == 0: continue
        # if more than 1 can, use plural
        if individualPaints[i] > 1: cans = "cans"
        else: cans = "can"
        # print how many cans of each quantity
        print(f"\tYou need {individualPaints[i]} {i} litre {cans}")

    print(f"Your {paintColor} {paintFinish} paint will cost £{totalPrice} in total")

    finalCost = totalPrice+primerPrice
    print(f"Your primer and paint put together, it will cost: £{finalCost}")

    # ask user if they want to save the file
    valid = False
    while not valid:
        try:
            saveFile = input("Do you wish to save the file? (yes or no) ").lower()
            if saveFile == "yes" or saveFile == "no": valid = True
        except ValueError:
            print("Please say that again, using only yes or no as answers")

    match saveFile: # write file if user asks for it, overwriting the old one
        case "yes":
            print("SAVING FILE, PLEASE DONT TURN OFF SYSTEM")
            writeFile(individualPaints,primerCans,finalCost)
        case "no":
            print("OK, THANKS FOR USING THE PROGRAM AND HAVE A NICE DAY")

### WRITE FILES ###-----------------------------------------------------------------------------------------------------

def writeFile(individualPaints,primerCans,finalCost):
    valid = False
    while not valid:
        try:
            clientName = input("Please enter your name ")
            if ',' not in clientName: valid = True
            else: print("Please try again, without the comma (,) this time")
        except ValueError:
            print("Apologies, I didn't quite understand that, please try again")

    file = open("oldCalculation.txt",'w')
    file.write(f"ClientName,{clientName}")
    file.write("\n")
    file.write(f"Walls,{info_walls}")
    file.write("\n")
    for i in range(0,info_walls):
        currentNums = info_wallMeasurements[i]
        file.write(f"wl{i},{currentNums[0]},{currentNums[1]}")
        file.write("\n")
    file.write(f"Exceptions,{info_exceptions}")
    file.write("\n")
    if info_exceptions != 0:
        for i in range(0,info_exceptions):
            currentNums = info_exceptionMeasurements[i]
            file.write(f"ex{i},{currentNums[0]},{currentNums[1]}")
            file.write("\n")
        file.write("\n")
    file.write(f"PaintNeeded,{paintChoice}")
    file.write("\n")
    for i in individualPaints.keys():
        file.write(f"{i},{individualPaints[i]}")
        file.write("\n")
    file.write(f"PrimerNeeded,{primerCans}")
    file.write("\n")
    file.write(f"CoatNeeded,{info_coats}")
    file.write("\n")
    file.write(f"TotalCost,{finalCost}")
    file.close()


### TRIGGER PROGRAM ###-------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    Main();