#Penguin.py
import random
class Penguin:

    attributes = ['damage', 'defence', 'speed']
    
    # health, damage, speed, defence, attribute, level, affection
    # max affection is 10 and is used to determine extra exp
    # Exp needed increases by the square of level
    def __innit__(self) :
        self.health = random.randint(5,10)
        self.damage = random.randint(1,3)
        self.speed = random.randint(1,3)
        self.attribute = Penguin.attributes[random.randint(0,2)] #random attribute
        self.level = 1
        self.affection = 10
        self.exp = 0

        #increase stats depending on attribute
        if self.attribute == 'damage':
            self.damage+=1
        elif self.attribute == 'defence':
            self.defence+=1
        else :
            self.speed+=1
    
    # Returns the penguins stats as a string
    def displayStats(self) :
        out = f'Level: {self.level}\nExp: {self.exp}/{self.level**2}\nHealth: {self.health}\n'
        out += f'Damage: {self.damage}\nDefence: {self.defence}\nSpeed: {self.speed}\n'
        out += f'Affection: {self.affection}/10\n'
        out += f'Attribute: {self.attribute.capitalize()}'
        return out
    
    # Pet the penguin to increase affection by 1
    def pet(self) :
        self.affection+=1
        if self.affection == 10 :
            return f'✨ 🐧 You pet your penguin 🐧 ✨ (Affection + 1 (MAX): {self.affection}/10)'
        elif self.affection >= 11 :
            self.affection = 10
            return f'✨ 🐧 You pet your penguin 🐧 ✨ (Affection + 0 (MAX): {self.affection}/10)'
        return f'✨ 🐧 You pet your penguin 🐧 ✨ (Affection + 1 : {self.affection}/10)'
    
    # Hug your penguin to increase affection by 2
    def hug(self) :
        self.affection+=2
        if self.affection < 5:
            return f'Your penguin backs away (Affection too low: {self.affection}/10)'
        elif self.affection == 10 :
            return f'✨ 🐧 You hug your penguin 🐧 ✨ (Affection + 2 (MAX): {self.affection}/10)'
        elif self.affection == 11 :
            self.affection = 10
            return f'✨ 🐧 You hug your penguin 🐧 ✨ (Affection + 1 (MAX): {self.affection}/10)'
        elif self.affection >= 12 :
            self.affection = 10
            return f'✨ 🐧 You hug your penguin 🐧 ✨ (Affection + 0 (MAX): {self.affection}/10)'
        return f'✨ 🐧 Your penguin has been pet 🐧 ✨ (Affection + 2 : {self.affection}/10)'