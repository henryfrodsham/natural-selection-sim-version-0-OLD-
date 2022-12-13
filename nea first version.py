import pygame
import sys
import random

pygame.init()
surface = pygame.display.set_mode((800, 600))
font = pygame.font.Font('freesansbold.ttf', 12)

GREY = (128,128,128)
BLACK = (20,20,20)

FoodRegister = []
SpeciesRegister = []

def IsPrime(arg): # this checks for prime numbers
    for i in range(2,int(arg**0.5)+1):
        if arg%i==0:
            return False
    return True

def InHitboxRect(X,Y,posX,posY,sizeX,sizeY):
    if posX > X and posX < (X + sizeX): #checks for allignment on the X axis
        if posY > Y and posY < (Y + sizeY): #checks for allignment on the Y axis
            return True

class button:
   
    def  __init__(self,size,position,color,pressedcolor,hoveredcolor,text,textcolor):
        self.size = size
        self.position = position
        self.color = color
        self.pressedcolor = pressedcolor
        self.hoveredcolor = hoveredcolor
        self.text = text
        self.textcolor = textcolor
       
    def DrawButton(self,mousestate,mousepos):
        if mousestate == 0 and InHitboxRect(self.position[0],self.position[1],mousepos[0],mousepos[1],self.size[0],self.size[1]): #hovered but not clicked
            pygame.draw.rect(surface, self.hoveredcolor, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])) #this is the hovered state of the button
            text = font.render(self.text, True, self.textcolor, self.hoveredcolor)
           
        elif mousestate == 1 and InHitboxRect(self.position[0],self.position[1],mousepos[0],mousepos[1],self.size[0],self.size[1]): #pressed
            pygame.draw.rect(surface, self.pressedcolor, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])) #pressed state
            return True
       
        else:
            pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])) #this is the static state of the button
            text = font.render(self.text, True, self.textcolor, self.color)
           
        surface.blit(text,((self.position[0] + (self.size[0] * 0.2)),(self.position[1] + (self.size[1] * 0.4))))
       
    def Output(self):
        print(self.size,self.position,self.color,self.pressedcolor,self.hoveredcolor,self.text,self.textcolor)
       
class Species:
   
    def  __init__(self, name, color, charcolor, size, charsize, position, genes):
        self.name = name
        self.color = color
        self.charcolor = charcolor
        self.size = size
        self.charsize = charsize
        self.position = position
        self.genes = genes
       
    def DrawSprite(self):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1]))
        factor = 0
       
        for Pointer in range((len(self.genes) // 2) - 2):
            Horizontal = (self.position[0] + self.size[0])
            Down = (self.position[1] + self.size[1])
            X = (Horizontal - self.genes[factor])
            Y = (Down - self.genes[factor + 1])
            A = (Horizontal - self.genes[factor+2])
            B = (Down - self.genes[factor+3])
           
            if self.genes[factor] % 2 == 0: #even check
                pygame.draw.circle(surface, self.charcolor[Pointer],(X,Y),self.charsize[Pointer])
            elif IsPrime(self.genes[factor]):
                pygame.draw.line(surface,self.charcolor[Pointer],(X,Y),(A,B))
            else:
                 pygame.draw.rect(surface, self.charcolor[Pointer], pygame.Rect(X,Y,self.charsize[Pointer],self.charsize[Pointer]))
                 
            factor += 2
           
    def Output(self):
        print(self.name,self.color,self.charcolor,self.size,self.charsize,self.position,self.genes)
       
class Food:
    def __init__(self,position,color,size,dotsize):
        self.position = position
        self.color = color
        self.size = size
        self.dotsize = dotsize
       
    def DrawFoodObject(self):
        pygame.draw.circle(surface, self.color,(self.position[0],self.position[1]),self.size)
        pygame.draw.circle(surface, BLACK,(self.position[0],self.position[1]),self.dotsize)
       
    def Output(self):
        print(self.position,self.color,self.size,self.dotsize)
   
def InitiateSpeciesObject():
    name = ""
    genes = []
    charcolor = []
    charsize = []
    color = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
    size = (random.randint(35,65),random.randint(35,65))
    position = (random.randint(100,700),random.randint(100,500))
   
    for i in range(random.randint(1,8)):
        for o in range(random.randint(1,3)): #this generates alien like names
            name += chr(random.randint(65,122))
        name += "-"
       
    for i in range(random.randint(6,24)): #genetic code generator, codes for the appearance
        X = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
        genes.append(random.randint(1,size[0]))
        genes.append(random.randint(1,size[1]))
        charcolor.append(X)
        charsize.append(random.randint(1,4))
       
    SpeciesRegister.append(Species(name,color,charcolor,size,charsize,position,genes))

def CreateFoodObject():
    position = (random.randint(50,750),random.randint(50,550))
    color = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
    size = random.randint(1,6)
    dotsize = random.randint(0,(size // 2))
    FoodRegister.append(Food(position,color,size,dotsize))
   
def DrawObjects():
    for i in range(len(FoodRegister)):
        FoodRegister[i].DrawFoodObject()
       
    for i in range(len(SpeciesRegister)):
        SpeciesRegister[i].DrawSprite()
       
InitiateSpeciesObject()
CreateFoodObject()
SpawnFood = button((50,30),(0,0),(40,40,40),(200,0,0),(100,0,0),"FOOD",(0,0,200))
pygame.mouse.set_visible(False)

while True:
    mousepos = pygame.mouse.get_pos()
    mousestate = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys. exit()
    surface.fill(GREY)
    DrawObjects()
    if (SpawnFood.DrawButton(mousestate[0],mousepos)):
        CreateFoodObject()
    pygame.display.flip()
