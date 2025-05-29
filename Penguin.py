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
        if self.attribute is 'damage':
            self.damage+=1
        elif self.attribute is 'defence':
            self.defence+=1
        else :
            self.speed+=1
    
    # returns the penguins stats as a string
    def displayStats(self) :
        out = f'Level: {self.level}\nExp: {self.exp}/{self.level**2}\nHealth: {self.health}\n'
        out += f'Damage: {self.damage}\nDefence: {self.defence}\nSpeed: {self.speed}\n'
        out += f'Affection: {self.affection}/10\n'
        out += f'Attribute: {self.attribute.capitalize()}'
        return out
    
    # pet the penguin to increase affection by 1
    def pet(self) :
        self.affection+=1
        if self.affection == 10 :
            self.affection = 10
            return f'✨ 🐧 Your penguin has been pet 🐧 ✨ (Affection +1 (MAX): {self.affection}/10)'
        elif self.affection > 10 :
            return f'✨ 🐧 Your penguin has been pet 🐧 ✨ (Affection +0 (MAX): {self.affection}/10)'
        return f'✨ 🐧 Your penguin has been pet 🐧 ✨ (Affection +1 : {self.affection}/10)'
        