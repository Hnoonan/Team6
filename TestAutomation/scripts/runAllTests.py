#!/usr/bin/python
 
import subprocess   
import os.path
import sys
from importlib import import_module

def getTestCases():
    os.chdir("../testCases/")
    allFiles = os.listdir(".")
    return [TestCase(fileName) for fileName in allFiles if ".txt" in fileName]
     
def executeTest(testCase):
    importStatement = convertPathToImport(testCase.modulePath)
    sys.path.append(testCase.modulePath)
    module = __import__(importStatement, fromlist=[testCase.methodName])
    methodToTest = getattr(module, testCase.methodName.replace("()",""))
    result = methodToTest(testCase.inputValue)
    testCase.actualResult = result
    
    #actual test
    if result == testCase.expectedResult:
        testCase.testPassed = True
    return testCase

def convertPathToImport(path):
    path = path.replace("/", ".")
    path = path.replace(".py","")
    return path.split(".")[-1]

class TestCase:
    def __init__(self, fileName):
        file = open(fileName, 'r')
        fileContents = file.read().split("\n")
        self.id = fileContents[0]
        self.description = fileContents[1]
        self.modulePath = fileContents[2].strip()
        self.methodName = fileContents[3].strip()
        self.inputValue = fileContents[4]
        self.expectedResult = fileContents[5]

        self.actualResult = ""
        self.testPassed = False

        file.close()
        
    
def clearTempFolder():
    #go back a directory, remove everyting from temp,
    #if nothing is in temp, the warning is suppressed by sending it to null
    subprocess.call("rm ../temp/* 2>/dev/null", shell=True)

def main():
    clearTempFolder()
    testCases = getTestCases()
    for testCase in testCases:
        executeTest(testCase)
        if testCase.testPassed:
            print "Test case "+testCase.id+" passed!"
        else:
            print "Test case "+testCase.id+" FAILED!"
            print "\tInput: " + testCase.inputValue 
            print "\tExpected: " + testCase.expectedResult
            print "\tActual output was: "+str(testCase.actualResult) 

            
main()
