import random, pygame, sys, os, multiprocessing

def getPath(file, join="/"):
    return os.path.dirname(os.path.abspath(__file__)) + join + file

def centerCoordinate(start, dimensions):
    return int(start + dimensions/2)

#I obtained these coordinates with Wall Maker.py
wallList = [[1, 374, 149, 625], [147, 548, 280, 114], [147, 662, 107, 330], [253, 975, 341, 23], [323, 750, 273, 228], [501, 400, 97, 348], [225, 375, 152, 89], [375, 398, 131, 66], [550, 398, 5, 4], [553, 2, 45, 397], [1, 290, 49, 84], [1, 240, 558, 46], [453, 285, 105, 57]]

characterXY = [279, 900] #put starting coordinates here
characterDirections = 0 #None, Left, Up, Right, Down
recentDirection = 3
playerWalkTimer = 0

nonPlayerCharacterXY = [514, 365] #put starting coordinates here
NPCWalkTimer = 0

gameStage = 0
cameraY = 400

def wallProximity(returnIndex):

    returnList = [False, False, False, False] #Subjective to player: Left, Up, Right, Down

    for wall in wallList:
        #pygame.draw.rect(WIN, (255, 0, 0), (wall[0], wall[1] - cameraY, wall[2], wall[3]), 0)
        if abs(centerCoordinate(wall[0], wall[2]) - centerCoordinate(characterXY[0], characterPNG.get_width())) <= (wall[2] + characterPNG.get_width())/2:
            if abs(centerCoordinate(wall[1], wall[3]) - centerCoordinate(characterXY[1], characterPNG.get_height())) <= wall[3]/2:
                if centerCoordinate(characterXY[0], characterPNG.get_width()) - centerCoordinate(wall[0], wall[2]) >= 0:
                    returnList[0] = True
                if centerCoordinate(characterXY[0], characterPNG.get_width()) - centerCoordinate(wall[0], wall[2]) < 0:
                    returnList[2] = True
        if abs(centerCoordinate(wall[1], wall[3]) - centerCoordinate(characterXY[1], characterPNG.get_height())) <= (wall[3] + characterPNG.get_height())/2:
            if abs(centerCoordinate(wall[0], wall[2]) - centerCoordinate(characterXY[0], characterPNG.get_width())) <= wall[2]/2:
                if centerCoordinate(characterXY[1], characterPNG.get_height()) - centerCoordinate(wall[1], wall[3]) >= 0:
                    returnList[1] = True
                if centerCoordinate(characterXY[1], characterPNG.get_height()) - centerCoordinate(wall[1], wall[3]) < 0:
                    returnList[3] = True

    return returnList[returnIndex]

def cameraPanUpdate(): #Pans the camera relative to the player's y position
    global cameraY
    if centerCoordinate(characterXY[1], characterPNG.get_height()) >= windowY/2 and centerCoordinate(characterXY[1], characterPNG.get_height()) < gameMapPNG.get_height() - (windowY/2):
        cameraY = centerCoordinate(characterXY[1], characterPNG.get_height()) - (windowY/2)
    elif centerCoordinate(characterXY[1], characterPNG.get_height()) <= (windowY/2):
        cameraY = 0
    elif centerCoordinate(characterXY[1], characterPNG.get_height()) >= gameMapPNG.get_height() - (windowY/2):
        cameraY = gameMapPNG.get_height() - windowY

class Character:
    def move(): #this function moves the character depending on the arrow keys and character speed
        if characterDirections == 1 and wallProximity(0) == False:
            characterXY[0] -= 2
        elif characterDirections == 3 and wallProximity(2) == False:
            characterXY[0] += 2
        elif characterDirections == 2 and wallProximity(1) == False:
            characterXY[1] -= 2
        elif characterDirections == 4 and wallProximity(3) == False:
            characterXY[1] += 2
        WIN.blit(characterPNG, (characterXY[0], characterXY[1] - cameraY))

    def animation(): #this function initializes the sprites walk animation
        global recentDirection, playerWalkTimer, characterPNG

        if characterDirections == 1:
            recentDirection = 1
            playerWalkTimer += 1
        elif characterDirections == 3:
            recentDirection = 2
            playerWalkTimer += 1
        elif characterDirections == 2:
            recentDirection = 3
            playerWalkTimer += 1
        elif characterDirections == 4:
            recentDirection = 0
            playerWalkTimer += 1
        elif characterDirections == 0:
            playerWalkTimer = 0

        if playerWalkTimer == 61:
            playerWalkTimer = 1
        

        if playerWalkTimer >= 1 and playerWalkTimer <= 20:
            characterPNG = characterSpritesPNG.subsurface((characterSpritesList[recentDirection][1], characterSpritesList[4][recentDirection], 17, 26))
        elif playerWalkTimer >= 31 and playerWalkTimer <= 50:
            characterPNG = characterSpritesPNG.subsurface((characterSpritesList[recentDirection][3], characterSpritesList[4][recentDirection], 17, 26))
        elif (playerWalkTimer >= 21 and playerWalkTimer <=30) or (playerWalkTimer >= 51 and playerWalkTimer <= 60): 
            characterPNG = characterSpritesPNG.subsurface((characterSpritesList[recentDirection][2], characterSpritesList[4][recentDirection], 17, 26))
        elif playerWalkTimer == 0:
            characterPNG = characterSpritesPNG.subsurface((characterSpritesList[recentDirection][0], characterSpritesList[4][recentDirection], 17, 26))

class NonPlayerCharacter:

    def detectPlayer(): #Detects if the player walks nearby the NPC
        detectedPlayer = False
        if abs(centerCoordinate(nonPlayerCharacterXY[0], nonPlayerCharacterPNG.get_width()) - centerCoordinate(characterXY[0], characterPNG.get_width())) <= 60:
            if abs(centerCoordinate(nonPlayerCharacterXY[1], nonPlayerCharacterPNG.get_height()) - centerCoordinate(characterXY[1], characterPNG.get_height())) < nonPlayerCharacterPNG.get_height() + 16:
                detectedPlayer = True
        return detectedPlayer

    def walkToPlayer(): 
        global nonPlayerCharacterPNG, NPCWalkTimer, gameStage, characterDirections
        characterDirections = 0
        characterPNG = characterSpritesPNG.subsurface((characterSpritesList[2][1], characterSpritesList[4][2], 17, 26))

        if abs(centerCoordinate(nonPlayerCharacterXY[0], nonPlayerCharacterPNG.get_width()) - centerCoordinate(characterXY[0], characterPNG.get_width())) >= (nonPlayerCharacterPNG.get_width() + characterPNG.get_width())/2 + 8:

            nonPlayerCharacterXY[0] -= 1
            NPCWalkTimer += 1 
        else:
            if gameStage == 0:
                gameStage = 1
            
        if NPCWalkTimer >= 1 and NPCWalkTimer <= 20:
            nonPlayerCharacterPNG = nonPlayerCharacterSpritesPNG.subsurface((0, 0, 16, 19))
        elif NPCWalkTimer >= 31 and NPCWalkTimer <= 50:
            nonPlayerCharacterPNG = nonPlayerCharacterSpritesPNG.subsurface((48, 0, 16, 19))
        elif (NPCWalkTimer >= 21 and NPCWalkTimer <=30) or (NPCWalkTimer >= 51 and NPCWalkTimer <= 60): 
            nonPlayerCharacterPNG = nonPlayerCharacterSpritesPNG.subsurface((24, 0, 16, 19))
        elif NPCWalkTimer == 0:
            nonPlayerCharacterPNG = nonPlayerCharacterSpritesPNG.subsurface((24, 0, 16, 19))

class Pokemon:
    def __init__(self, name, level, totalHP, currentHP, element, attacksList, attacksDamage, attacksCritical):
        self.name = name
        self.level = level
        self.element = element
        self.totalHP = totalHP
        self.currentHP = currentHP
        self.attacksList = attacksList
        self.attacksDamage = attacksDamage
        self.attacksCritical = attacksCritical
    
    def damageMultiplier(whichType, whichMove, side): #Multiplies the damage of a damage move based on stats defined in __init__
        if side == "player":
            if whichType == "element":
                return elementsEffective[currentPlayerPokemon.element][currentComputerPokemon.element]
            elif whichType == "critical":
                if currentPlayerPokemon.attacksCritical[whichMove] >= random.randint(1, 10):
                    return 2
                else:
                    return 1
        elif side == "computer":
            if whichType == "element":
                return elementsEffective[currentComputerPokemon.element][currentPlayerPokemon.element]
            elif whichType == "critical":
                if currentComputerPokemon.attacksCritical[whichMove] >= random.randint(1, 10):
                    return 2
                else:
                    return 1
            
    def attack(whichPokemon, whichMove, side):
        elementMultiplier = Pokemon.damageMultiplier("element", whichMove, side)
        criticalMultiplier = Pokemon.damageMultiplier("critical", whichMove, side)

        if side == "player":
            currentComputerPokemon.currentHP -= currentPlayerPokemon.attacksDamage[whichMove] * elementMultiplier * criticalMultiplier
        elif side == "computer":
            currentPlayerPokemon.currentHP -= currentComputerPokemon.attacksDamage[whichMove] * elementMultiplier * criticalMultiplier
        
        return [elementMultiplier, criticalMultiplier]

    def checkHealth(): #Checks if pokemon has fainted, or if the game is over
        global currentPlayerPokemon, currentComputerPokemon, gameStage
        if currentPlayerPokemon.currentHP < 0 and len(playerPokemonList) == 2:
            currentPlayerPokemon.currentHP = 0
            playerPokemonList.remove(currentPlayerPokemon)
            gameStage = 6
        
        elif currentPlayerPokemon.currentHP < 0 and len(playerPokemonList) == 1:
            currentPlayerPokemon.currentHP = 0
            #lose screen
            gameStage = 17
        if currentComputerPokemon.currentHP < 0 and len(computerPokemonList) == 2:
            currentComputerPokemon.currentHP = 0
            computerPokemonList.remove(currentComputerPokemon)
            currentComputerPokemon = computerPokemonList[0]
            gameStage = 10

        elif currentComputerPokemon.currentHP < 0 and len(computerPokemonList) == 1:
            currentComputerPokemon.currentHP = 0
            #victory screen
            gameStage = 18

    def healthBar(pokemon, posX, posY): #blits a healthbar to the screen, that changes colour based on how much health the pokemon has

        if round((pokemon.currentHP/pokemon.totalHP) * 200) >= 100:
            HPColor = (18, 222, 21)
        elif round((pokemon.currentHP/pokemon.totalHP) * 200) < 100 and round((pokemon.currentHP/pokemon.totalHP) * 200) >= 25:
            HPColor = (207, 134, 17)
        elif round((pokemon.currentHP/pokemon.totalHP) * 200) < 25:
            HPColor = (207, 17, 17)
        pygame.draw.rect(WIN, HPColor, (posX, posY, round((pokemon.currentHP/pokemon.totalHP) * 200), 18))
        pygame.draw.rect(WIN, BLACK, (posX, posY, 200, 18), 7)

    def displayPokemon(whichPokemon, side):
        if side == "player":
            WIN.blit(playerPokemonImagesList[pokemonList.index(whichPokemon)], (50, 300))
        elif side == "computer":
            WIN.blit(computerPokemonImagesList[pokemonList.index(whichPokemon)], (350, 0))

class NPC:
    def computerMove(): #Decides if the computer should fight or swap pokemon
        if (len(computerPokemonList) == 2) and (currentComputerPokemon.currentHP/currentComputerPokemon.totalHP <= 0.25) and (currentComputerPokemon.currentHP > 0):
            totalPokemonHP = [0, 0]
            for x in computerPokemonList:
                totalPokemonHP[0] += x.currentHP
                totalPokemonHP[1] += x.totalHP

            if (totalPokemonHP[0]/totalPokemonHP[1] > 0.25):
                return "swap"
            else:
                return "fight"
        else:
            return "fight"
    def chooseMove():
        return random.randint(0, 1)
    
class TextBox: #This class blits all the textboxes
    def create(Text1, Text2, selection):
        global selectable
        enterable = True
        outputText1 = gameFont.render(Text1, 1, BLACK)
        outputText2 = gameFont.render(Text2, 1, BLACK)
        WIN.blit(textBoxPNG, (100, windowY-textBoxPNG.get_height()))
        WIN.blit(outputText1, (132, windowY-textBoxPNG.get_height() + 24))
        WIN.blit(outputText2, (132, windowY-textBoxPNG.get_height() + 80))
        WIN.blit(enterIconPNG, (455, windowY-textBoxPNG.get_height() + 81))

        if selection == 1:
            selectable = True
            WIN.blit(selectTrianglePNG, (116, windowY-textBoxPNG.get_height() + 24))
        elif selection == 2:
            selectable = True
            WIN.blit(selectTrianglePNG, (116, windowY-textBoxPNG.get_height() + 80))
    def inGameTextBox(whichPokemon, side):
        pokemonName = gameFont.render((whichPokemon.name[whichPokemon.level]).upper(), 1, BLACK)
        pokemonLevel = gameFontSmall.render("L:" + str(whichPokemon.level + 1), 1, BLACK)
        healthPoints = gameFontSmall.render("HP: " + str(whichPokemon.currentHP) + "/" + str(whichPokemon.totalHP), 1, BLACK)
        if side == "player":
            textBoxCoordinates = [370, 326]
            WIN.blit(healthPoints, (textBoxCoordinates[0] + 5, textBoxCoordinates[1] + 110))
        elif side == "computer":
            textBoxCoordinates = [10, 10]
            WIN.blit(healthPoints, (textBoxCoordinates[0] + 5, textBoxCoordinates[1] + 110))
        pygame.draw.rect(WIN, BLACK, (textBoxCoordinates[0], textBoxCoordinates[1], 220, 140), 6)
        WIN.blit(pokemonName, (textBoxCoordinates[0] + 5, textBoxCoordinates[1] + 5))
        WIN.blit(pokemonLevel, (textBoxCoordinates[0] + 60, textBoxCoordinates[1] + 35)) #change these if see fit
        Pokemon.healthBar(whichPokemon, textBoxCoordinates[0] + 10, textBoxCoordinates[1] + 61)
            
levelMultiplier = [1, 1.25, 1.5]

elementsList = ["Normal", "Fire", "Water", "Grass", "Electric"]
elementsEffective = [[1, 1, 1, 1, 1], [1, 0.5, 0.5, 2, 1], [1, 2, 0.5, 0.5, 1], [1, 0.5, 2, 0.5, 1], [1, 1, 2, 0.5, 0.5]]

#defining each pokemon as an object

bulbasaur = Pokemon(["Bulbasaur", "Ivysaur", "Venusaur"], random.randint(0, 2), 350, 350, 3, ["tackle", "vine whip"], [40, 45], [2, 5])
charmander = Pokemon(["Charmander", "Charmeleon", "Charizard"], random.randint(0, 2), 320, 320, 1, ["scratch", "fire fang"], [35, 50], [4, 2])
squirtle = Pokemon(["Squirtle", "Wartortle", "Blastoise"], random.randint(0, 2), 420, 420, 2, ["tackle", "water pulse"], [40, 75], [2, 4])
pidgey = Pokemon(["Pidgey", "Pidgeotto", "Pidgeot"], random.randint(0, 2), 280, 280, 0, ["tackle", "quick attack"], [40, 40,], [2, 8])
pikachu = Pokemon(["Pikachu", "Raichu"], random.randint(0, 1), 320, 320, 4, ["quick attack", "electro ball"], [40, 65], [2, 8])

pokemonList = [bulbasaur, charmander, squirtle, pidgey, pikachu]

#Multiplying the stats of each pokemon depending on its level

for i in pokemonList:
    i.totalHP = round(i.totalHP * levelMultiplier[i.level])
    i.currentHP = i.totalHP
    for x in range(2):
        i.attacksDamage[x] = round(i.attacksDamage[x] * levelMultiplier[i.level])

sampledPokemonList = random.sample(pokemonList, 4)
playerPokemonList = sampledPokemonList[:2]
computerPokemonList = sampledPokemonList[2:]

selectItem = 1

currentComputerPokemon = computerPokemonList[random.randint(0, 1)]

pygame.init()

FPS = 60
fpsClock = pygame.time.Clock()

windowX, windowY = 600, 600

WIN = pygame.display.set_mode((windowX, windowY))

cameraY = 400 #replace this with 400 if need be

pygame.display.set_caption("Pokemon Time")

characterSpritesPNG = pygame.image.load(getPath("Character Sprites.png"))
characterSpritesList = [[0, 32, 64, 96], [0, 32, 64, 96], [0, 32, 64, 96], [0, 32, 64, 96], [0, 33, 65, 96]]
characterPNG = characterSpritesPNG.subsurface((0, 0, 17, 26))

nonPlayerCharacterSpritesPNG = pygame.image.load(getPath("NPC Sprites.png"))
nonPlayerCharacterPNG = nonPlayerCharacterSpritesPNG.subsurface((24, 0, 16, 19))
NPCName = "RANCHER"

gameMapPNG = pygame.image.load(getPath("Game Map.png"))
croppedGameMapPNG = gameMapPNG.subsurface((0, cameraY, windowX, windowY))

textBoxPNG = pygame.image.load(getPath("Text Box.png"))
enterIconPNG = pygame.image.load(getPath("Enter Icon.png"))
selectTrianglePNG = pygame.image.load(getPath("Select Triangle.png"))
gameFont = pygame.font.SysFont("PKMN RBYGSC", 10)
gameFontSmall = pygame.font.SysFont("PKMN RBYGSC", 8)

pygame.mixer.music.load(getPath("Pallet Town.mp3"))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops = -1)

BLACK = (0, 0, 0)
GRAY = list(BLACK)

pokeBallPNG = pygame.image.load(getPath("Pokeball.png"))
pokeballX = -200 #up to 800

NPCTrainerPNG = pygame.image.load(getPath("NPC Trainer.png"))

pokemonImagesPNG = pygame.image.load(getPath("Pokemon Images.png"))
pokemonImagesCoordinatesList = [[0, 0], [174, 0], [348, 0], [174, 58], [0, 116]]

bulbasaurPNG = pokemonImagesPNG.subsurface(pokemonImagesCoordinatesList[0][0] + (bulbasaur.level * 58), pokemonImagesCoordinatesList[0][1], 58, 58)
charmanderPNG = pokemonImagesPNG.subsurface(pokemonImagesCoordinatesList[1][0] + (charmander.level * 58), pokemonImagesCoordinatesList[1][1], 58, 58)
squirtlePNG = pokemonImagesPNG.subsurface(pokemonImagesCoordinatesList[2][0] + (squirtle.level * 58), pokemonImagesCoordinatesList[2][1], 58, 58)
pidgeyPNG = pokemonImagesPNG.subsurface(pokemonImagesCoordinatesList[3][0] + (pidgey.level * 58), pokemonImagesCoordinatesList[3][1], 58, 58)
pikachuPNG = pokemonImagesPNG.subsurface(pokemonImagesCoordinatesList[4][0] + (pikachu.level * 58), pokemonImagesCoordinatesList[4][1], 58, 58)

computerBulbasaurPNG = pygame.transform.rotozoom(bulbasaurPNG, 0, 3)
computerCharmanderPNG = pygame.transform.rotozoom(charmanderPNG, 0, 3)
computerSquirtlePNG = pygame.transform.rotozoom(squirtlePNG, 0, 3)
computerPidgeyPNG = pygame.transform.rotozoom(pidgeyPNG, 0, 3)
computerPikachuPNG = pygame.transform.rotozoom(pikachuPNG, 0, 3)

computerPokemonImagesList = [computerBulbasaurPNG, computerCharmanderPNG, computerSquirtlePNG, computerPidgeyPNG, computerPikachuPNG]

playerBulbasaurPNG = pygame.transform.flip(computerBulbasaurPNG, True, False)
playerCharmanderPNG = pygame.transform.flip(computerCharmanderPNG, True, False)
playerSquirtlePNG = pygame.transform.flip(computerSquirtlePNG, True, False)
playerPidgeyPNG = pygame.transform.flip(computerPidgeyPNG, True, False)
playerPikachuPNG = pygame.transform.flip(computerPikachuPNG, True, False)

playerPokemonImagesList = [playerBulbasaurPNG, playerCharmanderPNG, playerSquirtlePNG, playerPidgeyPNG, playerPikachuPNG]

firstMove = True
secondMove = True
gameUI = False
viewSwap = False

while True:
    enterable = False
    selectable = False
    if gameStage <= 2:
        cameraPanUpdate()
        croppedGameMapPNG = gameMapPNG.subsurface((0, cameraY, windowX, windowY))
        WIN.blit(croppedGameMapPNG, (0, 0))
        WIN.blit(nonPlayerCharacterPNG, (nonPlayerCharacterXY[0], nonPlayerCharacterXY[1] - cameraY))
        if NonPlayerCharacter.detectPlayer() == True:
            NonPlayerCharacter.walkToPlayer()
        Character.animation()
        Character.move()
    if gameStage == 1: 
        enterable = True
        TextBox.create("Hey! You have POKEMON! Come on!", "Let's Battle 'em!", 0)
    elif gameStage == 2: #Battle sequence starts
        pygame.mixer.music.stop()
        pygame.mixer.music.load(getPath("Battle Music.mp3"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops = -1)
        if pokeballX >= -100: 
            pygame.draw.rect(WIN, GRAY, (-100,0,(pokeballX + 200),200), 0)
            pygame.draw.rect(WIN, GRAY, ((600 - (pokeballX-100)),200,(pokeballX + 100),200), 0)
            pygame.draw.rect(WIN, GRAY, (-100,400,(pokeballX + 200),200), 0)
        if pokeballX >= 800:
            if GRAY != [240, 240, 240]:
                GRAY[0] += 8
                GRAY[1] += 8
                GRAY[2] += 8
            else:
                gameStage = 3
        else:
            WIN.blit(pokeBallPNG, (pokeballX, 0))
            WIN.blit(pokeBallPNG, (600 - pokeballX, 200))
            WIN.blit(pokeBallPNG, (pokeballX, 400))
            pokeballX += 10
    
    if gameStage >= 3:
        pygame.draw.rect(WIN, GRAY, (0,0,windowX,windowY), 0)
    if gameStage == 3:
        enterable = True
        WIN.blit(NPCTrainerPNG, (380, 100))
        TextBox.create(NPCName + " wants to FIGHT!", "", 0)

    elif gameStage == 4: #States which pokemon the NPC sent out
        enterable = True
        TextBox.create(NPCName + " sent out " + currentComputerPokemon.name[currentComputerPokemon.level].upper() + "!", "", 0)
        TextBox.inGameTextBox(currentComputerPokemon, "computer")
        Pokemon.displayPokemon(currentComputerPokemon, "computer")

    elif gameStage == 5: #Player chooses which pokemon to send out
        enterable = True
        TextBox.create("Select the pokemon you want to send into", "the battlefield:", 0)
        TextBox.inGameTextBox(currentComputerPokemon, "computer")
        Pokemon.displayPokemon(currentComputerPokemon, "computer")
    elif gameStage == 6:
        enterable = True
        if len(playerPokemonList) == 2:
            TextBox.create((playerPokemonList[0].name[playerPokemonList[0].level] + "  Level: " + str(playerPokemonList[0].level + 1) + "  Type: " + elementsList[playerPokemonList[0].element] + "  HP: " + str(playerPokemonList[0].currentHP) + "/" + str(playerPokemonList[0].totalHP)), (playerPokemonList[1].name[playerPokemonList[1].level] + "  Level: " + str(playerPokemonList[1].level + 1) + "  Type: " + elementsList[playerPokemonList[1].element] + "  HP: " + str(playerPokemonList[1].currentHP) + "/" + str(playerPokemonList[1].totalHP)), selectItem)
        elif len(playerPokemonList) == 1:
            TextBox.create((playerPokemonList[0].name[playerPokemonList[0].level] + "  Level: " + str(playerPokemonList[0].level + 1) + "  Type: " + elementsList[playerPokemonList[0].element] + "  HP: " + str(playerPokemonList[0].currentHP) + "/" + str(playerPokemonList[0].totalHP)), "", 1)
        TextBox.inGameTextBox(currentComputerPokemon, "computer")
        Pokemon.displayPokemon(currentComputerPokemon, "computer")
    elif gameStage == 7:
        enterable = True
        if len(playerPokemonList) == 1:
            selectItem = 1
        currentPlayerPokemon = playerPokemonList[selectItem - 1]

        TextBox.create("Go! " + currentPlayerPokemon.name[currentPlayerPokemon.level].upper() + "!", "", 0)
        gameUI = True

    if gameUI == True:
        TextBox.inGameTextBox(currentPlayerPokemon, "player")
        TextBox.inGameTextBox(currentComputerPokemon, "computer")

        Pokemon.displayPokemon(currentPlayerPokemon, "player")
        Pokemon.displayPokemon(currentComputerPokemon, "computer")

        Pokemon.checkHealth()
    
    if gameStage == 8: #NPC Chooses a move
        enterable = True
        if firstMove == True:
            computerAttack = NPC.chooseMove()
            elementMultiplier = Pokemon.damageMultiplier("element", computerAttack, "computer")
            criticalMultiplier = Pokemon.damageMultiplier("critical", computerAttack, "computer")
            currentPlayerPokemon.currentHP -= currentComputerPokemon.attacksDamage[computerAttack] * elementMultiplier * criticalMultiplier
            firstMove = False
        TextBox.create((currentComputerPokemon.name[currentComputerPokemon.level].upper()), ("used " + (currentComputerPokemon.attacksList[computerAttack]).upper() + "!"), 0)
    elif gameStage == 9: #States the effectiveness of the attack
        enterable = True
        if elementMultiplier == 1:
            effectiveMessage = "It has MODERATE effectiveness!"
        elif elementMultiplier == 0.5:
            effectiveMessage = "It is not very effective!"
        elif elementMultiplier == 2:
            effectiveMessage = "It is SUPER-EFFECTIVE!!"
        if criticalMultiplier == 1:
            criticalMessage = ""
        elif criticalMultiplier == 2:
            criticalMessage = "It is a CRITICAL hit!"
        TextBox.create(effectiveMessage, criticalMessage, 0)
    if gameStage == 10: #The player chooses which move to go again
        enterable = True
        TextBox.create("FIGHT", "SWAP POKEMON", selectItem)
    elif gameStage == 11:
        if selectItem == 1:
            gameStage = 12
        elif selectItem == 2:
            gameStage = 6
            firstMove = True
            secondMove = True
    elif gameStage == 12: #Player attacks
        enterable = True
        TextBox.create(currentPlayerPokemon.attacksList[0].upper(), currentPlayerPokemon.attacksList[1].upper(), selectItem)
    elif gameStage == 13:
        enterable = True
        if secondMove == True:
            playerAttack = selectItem - 1
            elementMultiplier = Pokemon.damageMultiplier("element", playerAttack, "player")
            criticalMultiplier = Pokemon.damageMultiplier("critical", playerAttack, "player")
            currentComputerPokemon.currentHP -= currentPlayerPokemon.attacksDamage[playerAttack] * elementMultiplier * criticalMultiplier
            secondMove = False
        TextBox.create((currentPlayerPokemon.name[currentPlayerPokemon.level].upper()), ("used " + (currentPlayerPokemon.attacksList[playerAttack]).upper() + "!"), 0)
    elif gameStage == 14: #States the effectiveness of the attack
        enterable = True
        if elementMultiplier == 1:
            effectiveMessage = "It has MODERATE effectiveness!"
        elif elementMultiplier == 0.5:
            effectiveMessage = "It is not very effective!"
        elif elementMultiplier == 2:
            effectiveMessage = "It is SUPER-EFFECTIVE!!"
        if criticalMultiplier == 1:
            criticalMessage = ""
        elif criticalMultiplier == 2:
            criticalMessage = "It is a CRITICAL hit!"
        TextBox.create(effectiveMessage, criticalMessage, 0)
    elif gameStage == 15: #When the NPC swaps pokemon, a textbox is displayed
        if NPC.computerMove() == "swap" and viewSwap == False:
            if computerPokemonList.index(currentComputerPokemon) == 0:
                currentComputerPokemon = computerPokemonList[1]
            elif computerPokemonList.index(currentComputerPokemon) == 1:
                currentComputerPokemon = computerPokemonList[0]
            viewSwap = True
        elif viewSwap == True:
            enterable = True
            TextBox.create(NPCName + " has swapped his pokemon", "with " + currentComputerPokemon.name[currentComputerPokemon.level].upper() + "!", 0)
        elif NPC.computerMove() == "fight" and viewSwap == False:
            firstMove = True
            secondMove = True
            gameStage = 8
    elif gameStage == 16:
        viewSwap = False
        gameStage = 10
    elif gameStage == 17: #Lose screen
        WIN.blit(NPCTrainerPNG, (380, 100))
        gameUI = False
        pygame.mixer.music.stop()
        TextBox.create("Game Over!! You have been defeated by", NPCName + "! Better luck next time!", 0)
    elif gameStage == 18: #Victory screen plus victory music
        WIN.blit(NPCTrainerPNG, (380, 100))
        gameUI = False
        pygame.mixer.music.stop()
        pygame.mixer.music.load(getPath("Victory Music.mp3"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops = -1)
        TextBox.create("Game Over!! You have defeated " + NPCName + "!", currentComputerPokemon.name[currentComputerPokemon.level].upper() + " ain't gonna cut it!", 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: #these events activate player movement through the arrow keys when in game
            if gameStage == 0:
                if event.key == pygame.K_LEFT:
                    characterDirections = 1
                elif event.key == pygame.K_RIGHT:
                    characterDirections = 3
                elif event.key == pygame.K_UP:
                    characterDirections = 2
                elif event.key == pygame.K_DOWN:
                    characterDirections = 4
            if event.key == pygame.K_RETURN and enterable == True:
                gameStage += 1
            if selectable == True:
                if event.key == pygame.K_UP:
                    selectItem = 1
                elif event.key == pygame.K_DOWN:
                    selectItem = 2

        if event.type == pygame.KEYUP:
            if gameStage == 0:
                if event.key == pygame.K_LEFT and characterDirections == 1:
                    characterDirections = 0
                if event.key == pygame.K_RIGHT and characterDirections == 3:
                    characterDirections = 0
                if event.key == pygame.K_UP and characterDirections == 2:
                    characterDirections = 0
                if event.key == pygame.K_DOWN and characterDirections == 4:
                    characterDirections = 0

    pygame.display.update()
    fpsClock.tick(FPS)