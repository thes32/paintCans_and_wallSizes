import unittest
from main import MainMenu
from inputMocker import set_keyboard_input, get_display_output

def test1():
    set_keyboard_input(["1"])

    MainMenu(True)

    output = get_display_output()

    assert output == ["1. Create new calculation",
                      "2. View old calculation",
                      "Please select which option you would like ",
                      "Proceeding to new calculation menu"]

def test2():
    set_keyboard_input(["2"])

    MainMenu(True)

    output = get_display_output()

    assert output == ["1. Create new calculation",
                      "2. View old calculation",
                      "Please select which option you would like ",
                      "Sure, I will load up your previous session right away"]

def test3():
    set_keyboard_input(["m","1"])

    MainMenu(True)

    output = get_display_output()

    assert output == ["1. Create new calculation",
                      "2. View old calculation",
                      "Please select which option you would like ",
                      "Sorry, that is not a valid option, please try again",
                      "Please select which option you would like ",
                      "Proceeding to new calculation menu"]

if __name__ == "__main__":
    test1()
    test2()
    test3()