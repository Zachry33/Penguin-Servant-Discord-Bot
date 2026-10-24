#Penguin.py
import random
class Penguin:

    stats = ['health', 'damage', 'defence', 'speed']
    # Stats a penguin can have as its attribute
    attributes = ['damage', 'defence', 'speed']
    # Amount each stat increases by when it grows for balance reasons
    growth = {'health': 3, 'damage': 1, 'defence': 2, 'speed': 1}

    # health, damage, speed, defence, attribute, level, affection
    # max affection is 10 and is used to determine extra exp
    # Exp needed increases by the square of level
    # 5% chance for a shiny
    def __init__(self) :
        self.health = random.randint(8,20)
        self.damage = random.randint(3,6)
        self.speed = random.randint(1,10)
        self.defence = random.randint(1,10)
        self.attribute = random.choice(Penguin.attributes) #random attribute
        self.level = 1
        self.affection = 0
        self.exp = 0

        # Increase stats depending on attribute
        setattr(self, self.attribute, getattr(self, self.attribute) + Penguin.growth[self.attribute])

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
        if self.shiny == True:
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
            return f'✨ 🐧 You hug your penguin 🐧 ✨ (Affection + 2 (MAX): {self.affection}/10)'
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
            return f'🐧 You hug your penguin 🐧 (Affection + 2 (MAX): {self.affection}/10)'
    
    # When a penguin levels up it will upgrade stats
    # Each stat has a 50% chance to increase by its growth amount with the attribute getting an addtional chance
    # Total tracks how much each stat has leveled up for output message
    def levelUp(self) :
        if self.exp >= self.level**2:
            self.level += 1
            self.exp = 0
            total = {}
            for stat in Penguin.stats:
                total[stat] = 0

            # Normal level up attempts for each stat
            for stat in Penguin.stats:
                if random.randint(1,2) == 2:
                    total[stat] += Penguin.growth[stat]
            
            # Extra level up attempt for the attribute
            if random.randint(1,2) == 2:
                total[self.attribute] += Penguin.growth[self.attribute]

            # Set damage, defence, health and speed to their new values
            for stat in Penguin.stats:
                setattr(self, stat, getattr(self, stat) + total[stat])

            return f'LEVEL UP:\n\tHealth: {self.health - total["health"]} --> {self.health} (+{total["health"]})\n\tDamage: {self.damage - total["damage"]} --> {self.damage} (+{total["damage"]})\n\tSpeed: {self.speed - total["speed"]} --> {self.speed} (+{total["speed"]})\n\tDefence: {self.defence - total["defence"]} --> {self.defence} (+{total["defence"]})'
            
    # Method to calculate damage the attacker Penguin to deal to the opponent Penguin
    def attack(self, opponent) :
        attTokens = self.damage
        defTokens = opponent.defence
        damBlocked = 0

        if (defTokens <= 0) :
            return attTokens

        for i in range(defTokens):
            roll = random.randint(0,1)
            if roll == 0:
                damBlocked += 1
            
        attTokens = max(0,attTokens - damBlocked)
        return attTokens
        
        
                


