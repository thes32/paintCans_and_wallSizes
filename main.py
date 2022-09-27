import os.path

# Shift F10 to run, 2xShift to search

def SetBaseVariables(): # this is used to make sure all global variables have been declared
    # variables to know if the files has been found in the system
    global oldFileFound

    oldFileFound = False

    # world variables that are mostly constant across the whole program
    global paintAreaPerLitre  # m2 per liter
    global paintPrice  # price for 5 liters in GBP
    global paintName  # name of the paint used for this program
    global paintColor  # color of the paint
    global paintFinish  # finish of the paint, like eggshell or silk or matt

    paintName = "Dulux"
    paintPrice = 30
    paintColor = "White"
    paintFinish = "Eggshell"
    paintAreaPerLitre = 10

    # variables needed to do the math of the walls and the paint needed for it
    global info_walls  # num of walls needed to be painted
    global info_wallMeasurements  # measurements of the walls that are going to be painted
    global info_lastInputWall  # if the client puts a value wrong in the wall measurements section, they can continue
    global info_exceptions # num of chunks in the walls that don't need to be painted
    global info_exceptionMeasurements # measurements of the chunks of wall that don't need painting
    global info_lastInputException # if the client puts a value wrong in the exceptions section, they can continue

    info_walls = 0
    info_wallMeasurements = []
    info_lastInputWall = 1
    info_exceptions = 0
    info_exceptionMeasurements = []
    info_lastInputException = 1
    return True

def Main():
    createdBaseVariables = SetBaseVariables()
    # print welcome to the program
    print("Hello and welcome to your personal wall painting calculator!")
    # if there is an old file attached to this program, tell the program that it is available, otherwise tell it to
    # not try anything
    oldFileFound = False

    if os.path.exists("oldCalculation.txt"):
        oldFileFound = True

    MainMenu(oldFileFound);

### MAIN MENU ###

def MainMenu(oldFileFound):
    # print the needed menu items, and also print view last file if the client wants to see it
    print("1. Create new calculation")
    if oldFileFound: print("2. View old calculation")
    menuChoice = int(input("Please select which option you would like"))

    match menuChoice:
        case 1:
            print("Proceeding to new calculation menu")
            InformationWallNumberGathering()
        case 2:
            print("Sure, I will load up your previous session right away")
            LoadLastFile()
        case _:
            print("I'm sorry, that is not an option, please try again")

### READ FILE ###

def LoadLastFile():
    # open the file and split it all by lines
    file = open("oldCalculation.txt",'r')
    fileContent = file.read()
    lineSplitContents = fileContent.split("\n")
    PrintFileContent(lineSplitContents)

def PrintFileContent(content):
    # needed variables to print the final document
    customerName = "blank"
    numOfWalls = 0
    wallMeasurements = []
    numOfExceptions = 0
    exceptionsMeasurements = []
    numOfPaintCans = []

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
                currentLine = "exceptions"
            case "PaintNeeded":
                currentLine = "paints"
            case _:
                match currentLine:
                    case "walls":
                        wallMeasurements.append([lineContent[1],lineContent[2]])
                    case "exceptions":
                        exceptionsMeasurements.append([lineContent[1],lineContent[2]])
                    case "paints":
                        numOfPaintCans.append([lineContent[0], lineContent[1],lineContent[2]])

    # use functions to calculate the wall area and the chunks of wall to take out
    totalAreaOfWalls = areaOfWall(wallMeasurements)
    totalAreaOfException = areaOfExceptions(exceptionsMeasurements)
    # take the chunks out of the wall area and have the final wall area needing painting
    totalPaintableArea = totalAreaOfWalls - totalAreaOfException

    # print some structured stuff to show the client their last data
    print()
    print(f"Hello, {customerName}")
    print(f"Per you last calculation, you had {numOfWalls} walls with a total area of {totalPaintableArea} m2")
    print(f"For this area, you will need {(totalPaintableArea / paintAreaPerLitre) * 1.1} litres of paint")
    print(f"You will need this amount of paint for this project")

    # for each paintcan needed for the project, print new line with the number, the size and the total price
    for i in numOfPaintCans:
        if int(i[1]) > 0:
            print(f"- {i[1]} {i[0]} can for a price of £{int(i[2])} per can, or £{int(i[1]) * int(i[2])} total")

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

### GET INFORMATION ON THE WALLS ###

def InformationWallNumberGathering(): # get how many walls the use wants to paint
    print()
    global info_walls
    try:
        info_walls = int(input("How many walls do you want to pain?"))
    except ValueError: # if they dont use a whole number, tell them and start this function again
        print("I'm sorry, that was not a whole number, please try again")
        InformationWallNumberGathering()
    InformationWallMeasurementsGathering()

def InformationWallMeasurementsGathering(): # for each wall that they want painting, ask the width and height
    global info_lastInputWall # global variable
    tempStart = info_lastInputWall # allow user to continue where they left off, instead of starting from 0

    for i in range(tempStart,info_walls+1):
        try:
            tempWallWidth = float(input(f"What is the width (meters) of the {i} wall you want to paint?"))
        except ValueError: # if input is not float, tell user to use a float
            print("I'm sorry, that is not a valid decimal number, please start again")
            InformationWallMeasurementsGathering()
        try:
            tempWallHeight = float(input(f"What is the height (meters) of the {i} wall you want to paint?"))
        except ValueError: # if input is not float, tell user to use a float
            print("I'm sorry, that is not a valid decimal number, please start again")
            InformationWallMeasurementsGathering()
        info_lastInputWall += 1
        info_wallMeasurements.append([tempWallWidth, tempWallHeight]) # add measurements to list of wall measurements

    InformationExceptionNumberGathering()

### GET INFORMATION ON THE SECTIONS TO CUT OUT ###

def InformationExceptionNumberGathering():
    print()
    global info_exceptions # global variable
    try:
        info_exceptions = int(input(f"How many sections in those walls don't need painting (doors, windows, power outlets)"))
    except ValueError: # if its not given an int, error out and restart function
        print(f"That is not a valid option, please use a number")
        InformationExceptionNumberGathering()
    # go to next part of code
    InformationExceptionMeasurementGathering()

def InformationExceptionMeasurementGathering():
    global info_lastInputException  # global variable
    tempStart = info_lastInputException  # allow user to continue where they left off, instead of starting from 0

    for i in range(tempStart, info_walls + 1):
        try:
            tempExceptionWidth = float(input(f"What is the width (meters) of the {i} section you don't need to paint?"))
        except ValueError:  # if input is not float, tell user to use a float
            print("I'm sorry, that is not a valid decimal number, please start again")
            InformationWallMeasurementsGathering()
        try:
            tempExceptionHeight = float(input(f"What is the height (meters) of the {i} section you don't need to paint?"))
        except ValueError:  # if input is not float, tell user to use a float
            print("I'm sorry, that is not a valid decimal number, please start again")
            InformationWallMeasurementsGathering()
        info_lastInputException += 1
        info_wallMeasurements.append([tempExceptionWidth, tempExceptionHeight]) # add measurements to list of wall measurements

    InformationPaintGathering()

### GET PAINT INFORMATION ###

def InformationPaintGathering():
    # ask user for input regarding their knowledge of the
    userAnswer = str(input("Do you know any details about the paint you want to use, or do you want to use the default values provided by the program? (yes or no)")).lower()

    match userAnswer: # switch statement used for input of the customer
        case "yes":
            print("Ok, taking you to the next screen")
        case "no":
            print("Ok, showing you the results for your search")
            ShowFinalResults()
        case _:
            print("I'm sorry, I didn't quite understand that, please try again (yes or no answers)")

def InformationPaintDetailsGathering():
    global paintAreaPerLitre
    global paintPrice
    global paintName
    global paintColor
    global paintFinish

    print("Work in progress")


### PRINT STUFF IN COMMAND LINE ###

def ShowFinalResults():

    wallArea = areaOfWall(info_wallMeasurements)
    exceptionArea = areaOfExceptions(info_exceptionMeasurements)
    totalArea = wallArea - exceptionArea

    print()
    print(f"You need to paint {round(totalArea,2)} m2 of wall in total")
    print(f"This will require {round(((totalArea / paintAreaPerLitre) * 1.1),2)} liters of paint")


if __name__ == "__main__":
    Main();