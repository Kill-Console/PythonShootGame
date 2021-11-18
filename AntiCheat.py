from random import *

class AntiCheatValue:
    keyList = []
    valueList = []
    previousValueList = []
    changedValue = 0
    
    def __init__(self):
        value = 0
        for i in range(3):
            self.keyList.append(randint(-2147483646, 2147483646))
        for i in range(len(self.keyList)):
            self.valueList.append(value ^ self.keyList[i])
            self.previousValueList.append(value ^ self.keyList[i])
        self.changedValue = 0
            
    def __init__(self, value):
        for i in range(3):
            self.keyList.append(randint(-2147483646, 2147483646))
        for i in range(len(self.keyList)):
            self.valueList.append(value ^ self.keyList[i])
            self.previousValueList.append(value ^ self.keyList[i])
        self.changedValue = 0
    
    def decode(key, value):
        return key ^ value
    
    def encode(key, value):
        return key ^ value
    
    def encodedValue(self):
        if not self.check(): return
        value = self.decode(self.keyList[0], self.valueList[0])
    
    def check(self):
        value = self.decode(self.keyList[0], self.valueList[0])
        for i in range(1, len(self.keyList)):
            if value != self.decode(self.keyList[i], self.valueList[i]):
                return False
        previousValue = self.decode(self.keyList[0], self.previousValueList[0])
        for i in range(1, len(self.keyList)):
            if previousValue != self.decode(self.keyList[i], self.previousValueList[i]):
                return False
        return value - previousValue == self.changedValue
    
    def add(self, value):
        if not self.check(): return
        for i in range(len(self.keyList)):
            self.previousValueList[i] = self.valueList[i]
        self.changedValue = value
        value += self.encodedValue()
        for i in range(len(self.keyList)):
            self.valueList[i] = self.encode(self.keyList[i], value)