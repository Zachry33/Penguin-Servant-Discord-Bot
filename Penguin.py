#Penguin.py
import random
class Penguin:

    attributes = ['health', 'damage', 'defence', 'speed']
    
    # health, damage, speed, defence, attribute, level, affection
    # max affection is 10 and is used to determine extra exp
    # Exp needed increases by the square of level
    # 5% chance for a shiny
    def __innit__(self) :
        self.health = random.randint(8,20)
        self.damage = random.randint(1,6)
        self.speed = random.randint(1,10)
        self.defence = random.randint(1,10)
        self.attribute = Penguin.attributes[random.randint(0,3)] #random attribute
        self.level = 1
        self.affection = 10
        self.exp = 0

        #increase stats depending on attribute
        if self.attribute == 'damage':
            self.damage+=1
        elif self.attribute == 'defence':
            self.defence+=1
        elif self.attribute == 'health' :
            self.health +=1
        else :
            self.speed+=1

        # Determine if it is a shiny
        if random.randint(1,20) == 1:
            self.shiny = True
        else :
            self.shiny = False

        self.tempHealth = self.health
    
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
        if self.shiny == True:
            if self.affection == 10 :
                return f'✨ 🐧 You pet your penguin 🐧 ✨ (Affection + 1 (MAX): {self.affection}/10)'
            elif self.affection >= 11 :
                self.affection = 10
                return f'✨ 🐧 You pet your penguin 🐧 ✨ (Affection + 0 (MAX): {self.affection}/10)'
            return f'✨ 🐧 You pet your penguin 🐧 ✨ (Affection + 1 : {self.affection}/10)'
        else :
            if self.affection == 10 :
                return f'🐧 You pet your penguin 🐧 (Affection + 1 (MAX): {self.affection}/10)'
            elif self.affection >= 11 :
                self.affection = 10
                return f'🐧 You pet your penguin 🐧 (Affection + 0 (MAX): {self.affection}/10)'
            return f'🐧 You pet your penguin 🐧 (Affection + 1 : {self.affection}/10)'
    
    # Hug your penguin to increase affection by 2
    def hug(self) :
        self.affection+=2
        if self.shiney == True:
            if self.affection < 5:
                self.affection-=2
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
        else:
            if self.affection < 5:
                self.affection-=2
                return f'Your penguin backs away (Affection too low: {self.affection}/10)'
            elif self.affection == 10 :
                return f'🐧 You hug your penguin 🐧 (Affection + 2 (MAX): {self.affection}/10)'
            elif self.affection == 11 :
                self.affection = 10
                return f'🐧 You hug your penguin 🐧 (Affection + 1 (MAX): {self.affection}/10)'
            elif self.affection >= 12 :
                self.affection = 10
                return f'🐧 You hug your penguin 🐧 (Affection + 0 (MAX): {self.affection}/10)'
            return f'🐧 Your penguin has been pet 🐧 (Affection + 2 : {self.affection}/10)'
    
    #TODO add a way to identify which stats have leveled up
    # When a penguin levels up it will upgrade stats
    # Each stat has a 50% chance to increase with the attribute geting an addtional chance
    def levelUp(self) :
        if self.exp >= self.level**2:
            self.level += 1
            self.exp = 0
            roll = random.randint(1,2)
            if roll == 2:
                self.health += 1
            roll = random.randint(1,2)
            if roll == 2:
                self.damage +=1
            roll = random.randint(1,2)
            if roll == 2:
                self.speed +=1
            roll = random.randint(1,2)
            if roll == 2:
                self.defence +=1

            roll = random.randint(1,2)
            if self.attribute == 'damage' and roll == 2:
                self.damage+=1
            elif self.attribute == 'defence' and roll == 2:
                self.defence+=1
            elif self.attribute == 'speed' and roll == 2:
                self.speed+=1
            elif self.attribute == 'health' and roll == 2:
                self.speed+=1
            
    # Method to calculate damage the attacker Penguin to deal to the opponent Penguin
    def attack(self, opponent) :
        attTokens = self.attack
        defTokens = opponent.defence
        damBlocked = 0

        for i in range(defTokens):
            roll = random.randint(0,i)
            if roll == 0:
                damBlocked += 1
            
        attTokens -= damBlocked
        return attTokens
        
        
                


