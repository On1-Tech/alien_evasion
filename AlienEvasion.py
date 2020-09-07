# Importing modules for cross platform compatability
import sys, pygame, random, math, pickle #Add import module for random, maths, pickle
from pygame.locals import *

# Initialisation of Variables
GAME_NAME = "Alien Evasion"
NEBULA = "Nebula.jpg"
MONSTER = "monster.png"
SPACESHIP = "spaceship.png"
#MUSIC = "Left_Behind.mp3"
#WHOOSH = "Whoosh.wav"
#DEAD = "Ending.wav"
global DIFFICULTY
DIFFICULTY = 1 # 3 Diffculty Settings

# initialsing Scoring
global SCORE
global HIGHSCORE
HIGHSCORE = 0
SCORE = 0
# Saving and retrieving high score using Pickle
try:
    with open('score.dat', 'rb') as file:
        HIGHSCORE = pickle.load(file)
except:
    SCORE = 0

print ("High score: %d" % HIGHSCORE) # Print high score



#Define Frame Rate
FRAME_RATE = 60

# Settting up colours
BLACK =(0,0,0)
WHITE =(255,255,255)
PURPLE = (147,112,219)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Setting up screen dimensions & Borders
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
BORDER_WIDTH = 5
BORDER_HEIGHT = 5

# Background Image and Music
background = pygame.image.load(NEBULA)
backgroundRect = background.get_rect()
#pygame.mixer.init()
##pygame.mixer.pre_init(44100, 16, 2, 4096)

##pygame.mixer.music.load(MUSIC)
##pygame.mixer.music.set_volume(0.5) # Volume between 0 and 1.
##pygame.mixer.music.play(-1) # Loops the music continuously.

# Additional Sounds
##enemy_destroyed = pygame.mixer.Sound(WHOOSH)
##game_over = pygame.mixer.Sound(DEAD)



#============================================================================
# CLASS FOR THE WALLS

# Creating walls for the game using Sprites
class Walls(pygame.sprite.Sprite):
    def __init__(self, x, y, WIDTH, HEIGHT):
        # Call the parent's constructor
        super().__init__()

        # Make white walls
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill(WHITE)

        # Use the top left corner the place to pass in the location
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

#============================================================================
# CLASS FOR BULLETS
class Shooting(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Bullet size, colour and object
        self.image = pygame.Surface([4, 4])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()

        # Create floating point values for bullet position based on player object position
        self.floating_point_x = player.rect.x # player x position
        self.floating_point_y = player.rect.y # player y position
 
        # Calculate the angle between player position and mouse position
        x_diff = x - player.rect.x # player x position
        y_diff = y  - player.rect.y # player y position
        angle = math.atan2(y_diff, x_diff); # angle calculation
 
        # Using angle taken from mouse position, calculate components of bullet direction of travel
        speed = 4
        self.change_x = math.cos(angle) * speed # Magnitude bullet x direction
        self.change_y = math.sin(angle) * speed # Magnitude bullet y direction
 
    def update(self):
        # Update for bullet direction
        # The floating values for x and y position of bullet
        self.floating_point_x += self.change_x
        self.floating_point_y += self.change_y
 
        # Convert the bullet position to an integer value for quicker processing than using floating point
        self.rect.x = int(self.floating_point_x)
        self.rect.y = int(self.floating_point_y)

        # Remove bullets that go off the screen 
        if self.floating_point_x < (0+BORDER_WIDTH) or self.floating_point_x > (SCREEN_WIDTH-BORDER_WIDTH) \
           or self.floating_point_y < (0+BORDER_HEIGHT) or self.floating_point_y > (SCREEN_HEIGHT-BORDER_HEIGHT):
            self.kill()
            
#============================================================================
# CLASS FOR ENEMIES
class Enemy(pygame.sprite.Sprite):

    # Constructor Function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Setting up image for enemies        
        self.image = pygame.image.load(MONSTER)
        self.image.set_colorkey((WHITE))
        self.size = self.image.get_size()
        # resize the image
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*0.05),\
                                                         int(self.size[1]*0.05)))
        
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.x = self.rect.x
        self.y = self.rect.y
        self.rect.center = (self.rect.x,self.rect.y)

    def update(self):  # Enemies to follow player            
        if self.x > player.rect.x:
            self.x -= 1
            self.rect.center = (self.x, self.y)
        elif self.x < player.rect.x:
            self.x += 1
            self.rect.center = (self.x, self.y)
            
        if self.y > player.rect.y:
            self.y -= 1
            self.rect.center = (self.x, self.y)
        elif self.y < player.rect.y:
            self.y += 1
            self.rect.center = (self.x, self.y)
        

#============================================================================
# CLASS FOR THE PLAYER

class Player(pygame.sprite.Sprite):
    
    # Constructor Function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.walls = None


        # Set up image for player object
        self.image = pygame.image.load(SPACESHIP)
        self.image.set_colorkey((WHITE))
        # return a width and height of an image
        self.size = self.image.get_size()
        # resize the image
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*0.08),\
                                                         int(self.size[1]*0.08)))
        
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.rect.center = (self.rect.x,self.rect.y)


#===================================================================================================================================================> 
    def changespeed(self, x, y):
       # Editing player movement
        self.change_x += x
        self.change_y += y


        
#===================================================================================================================================================<
    def update(self):
        """ Update the player position. """
        # Move left/right
        self.rect.x += self.change_x
 
        # Did this update cause us to hit a wall?
        wall_hit_list = pygame.sprite.spritecollide(self, self.walls, False) # False set here so blocks aren't deleted
        for wall_hit in wall_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = wall_hit.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = wall_hit.rect.right

        # Move up/down
        self.rect.y += self.change_y

 
        # Check and see if we hit anything
        wall_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for wall_hit in wall_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = wall_hit.rect.top
            else:
                self.rect.top = wall_hit.rect.bottom

#============================================================================
                
# Initialise Pygame
pygame.init()

#================================================================================
#Start Menu Class - Where Difficulty is selected

class GameMenu():
    def __init__(self, screen, items, bg_color=(BLACK), font=None, font_size=30,
                    font_color=(WHITE)):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
 
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
 
        self.items = items
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
 
        self.items = []
        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)
 
            width = label.get_rect().width
            height = label.get_rect().height
 
            posx = (self.scr_width / 2) - (width / 2)
            # t_h: total height of text block
            t_h = len(items) * height
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)
 
            self.items.append([item, label, (width, height), (posx, posy)])
 
    def run(self):
        global DIFFICULTY
        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
 
            # Redraw the background
            self.screen.fill(self.bg_color)

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()


            # Set mouse positions for clicking on difficulty
            if 165+315 > mouse[0] > 165 and 165+15 > mouse[1] > 165 \
               and click[0] == 1:              
                DIFFICULTY = 9
                mainloop = False
                
            elif 150+335 > mouse[0] > 150 and 230+15 > mouse[1] > 230 \
                 and click[0] == 1:               
                DIFFICULTY = 5
                mainloop = False
                
            elif 163+312 > mouse[0] > 163 and 295+15 > mouse[1] > 295 \
                 and click[0] == 1:
                DIFFICULTY = 3
                mainloop = False

            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))
                
 
            pygame.display.flip()
 
 
if __name__ == "__main__":
    # Creating the screen
    screen = pygame.display.set_mode((640, 480))
 
    menu_items = ('ALIEN EVASION','','','','Click here for easy mode','','','Click here for medium mode','','','Click here for hard mode','','','','')
 
    pygame.display.set_caption('Game Menu')
    gm = GameMenu(screen, menu_items)
    gm.run()

#=====================================================================================================
# Create the Screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
#screen = pygame.display.set_mode((1366,768),pygame.FULLSCREEN)

# Title of Window
pygame.display.set_caption(GAME_NAME)

# List to hold the sprites 
all_sprite_list = pygame.sprite.Group()

# Making the walls (X_pos, Y_pos, WIDTH, HEIGHT)
wall_list = pygame.sprite.Group()

# Left Border
wall = Walls(0, 0, BORDER_WIDTH, SCREEN_HEIGHT)
wall_list.add(wall)
all_sprite_list.add(wall)

# Top Border
wall = Walls(0, 0, SCREEN_WIDTH, BORDER_HEIGHT)
wall_list.add(wall)
all_sprite_list.add(wall)

# Right Border
wall = Walls((SCREEN_WIDTH-BORDER_WIDTH), 0, BORDER_WIDTH, SCREEN_HEIGHT)
wall_list.add(wall)
all_sprite_list.add(wall)

# Bottom Border
wall = Walls(0, (SCREEN_HEIGHT-BORDER_HEIGHT), SCREEN_WIDTH, BORDER_HEIGHT)
wall_list.add(wall)
all_sprite_list.add(wall)

# Create the player object
player = Player(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
player.walls = wall_list

# Create the shooting/ bullet list
bullet_list = pygame.sprite.Group()

# Create the Enemy object
enemy = Enemy(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
enemy.walls = wall_list
enemy_list = pygame.sprite.Group() # List of each enemy in the game
enemy_list.add(enemy)

all_sprite_list.add(player, enemy)

clock = pygame.time.Clock()

done = False # Loop until user specifies true in pygame.QUIT()


while not done:

    pygame.font.init()
    font = pygame.font.Font(None, 30)
    text = font.render("Score: " + str(SCORE), 1, WHITE)
    textrect = text.get_rect()
    textrect.left, textrect.top = 15, 15
    screen.blit(text, textrect)
    pygame.display.flip()

    font = pygame.font.Font(None, 30)
    text1 = font.render("High Score: " + str(HIGHSCORE), 1, WHITE)
    textrect = text.get_rect()
    textrect.left, textrect.top = 15, 40
    screen.blit(text1, textrect)
    pygame.display.flip()
 
    for event in pygame.event.get():
        # Closing the game
        if event.type == pygame.QUIT:
            done = True

        # Movement of the player using either arrow keys or WASD    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord("a"):
                player.changespeed(-3, 0)                
            elif event.key == pygame.K_RIGHT or event.key == ord("d"):
                player.changespeed(3, 0)
            elif event.key == pygame.K_UP or event.key == ord("w"):
                player.changespeed(0, -3)
            elif event.key == pygame.K_DOWN or event.key == ord("s"):
                player.changespeed(0, 3)         
                
 
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord("a"):
                player.changespeed(3, 0)       
            elif event.key == pygame.K_RIGHT or event.key == ord("d"):
                player.changespeed(-3, 0)
            elif event.key == pygame.K_UP or event.key == ord("w"):
                player.changespeed(0, 3)
            elif event.key == pygame.K_DOWN or event.key == ord("s"):
                player.changespeed(0, -3)
                

        # Shooting Direction
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            x = mpos[0]
            y = mpos[1]
            
            
            # Fire a bullet if the user clicks the mouse button
            bullet = Shooting(x, y)
            # Set the bullet so it is where the player is
            bullet.rect.x = player.rect.x
            bullet.rect.y = player.rect.y
            # Add the bullet to the lists
            all_sprite_list.add(bullet)
            bullet_list.add(bullet)
            
    # Create the Enemy object at a random point in each corner of screen
    
    if pygame.time.get_ticks()%(2*DIFFICULTY)==0:
        ii = random.randint(1,4)
        if ii == 1:
            enemy = Enemy(random.randint(BORDER_WIDTH, (SCREEN_WIDTH/10+BORDER_WIDTH)), random.randint(BORDER_HEIGHT, (SCREEN_HEIGHT/10+BORDER_HEIGHT)))
        elif ii == 2:
            enemy = Enemy(random.randint((SCREEN_WIDTH-(SCREEN_WIDTH/10+BORDER_WIDTH)), SCREEN_WIDTH-BORDER_WIDTH), random.randint(BORDER_HEIGHT, (SCREEN_HEIGHT/10+BORDER_HEIGHT)))
        elif ii == 3:
            enemy = Enemy(random.randint(BORDER_WIDTH, (SCREEN_WIDTH/10+BORDER_WIDTH)), random.randint((SCREEN_HEIGHT-(SCREEN_HEIGHT/10+BORDER_HEIGHT)), (SCREEN_HEIGHT-BORDER_HEIGHT)))
        elif ii == 4:
            enemy = Enemy(random.randint((SCREEN_WIDTH-(SCREEN_WIDTH/10+BORDER_WIDTH)),SCREEN_WIDTH-BORDER_WIDTH), random.randint((SCREEN_HEIGHT-(SCREEN_HEIGHT/10+BORDER_HEIGHT)), (SCREEN_HEIGHT-BORDER_HEIGHT)))
        # Add enemies to sprite list
        all_sprite_list.add(enemy)
        enemy_list.add(enemy)

    
    all_sprite_list.update()
    #Add score for each second running of game
    multiplier=1
    if pygame.time.get_ticks()%999999999==0:
        multiplier*10
    SCORE +=1*multiplier
   # Calculate mechanics for each bullet
    for bullet in bullet_list:
 
        # See an enemy is hit
        enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)
        enemy_destroyed.play() # However still plays if bullet misses and hits wall
 
        # For each block hit, remove the bullet and add to the score
        for block in enemy_hit_list:
            bullet_list.remove(bullet)
            all_sprite_list.remove(bullet)
            SCORE += 50
            #print(score)
 
        # Remove the bullet if it flies up off the screen
        if bullet.rect.y < 0 or bullet.rect.y > SCREEN_HEIGHT or bullet.rect.x < 0 or bullet.rect.x > SCREEN_WIDTH:
            bullet_list.remove(bullet)
            all_sprite_list.remove(bullet)
            
    # Checks if the player has been hit by an enemy =========================================================================================< Add score to high score if greater. 
    player_hit = pygame.sprite.spritecollide(player, enemy_list, False)
    if len(player_hit) > 0:
        if (SCORE > HIGHSCORE):
            with open('score.dat', 'wb') as file:
                pickle.dump(SCORE, file)
            
        if __name__ == "__main__":
        # Creating the screen
                screen = pygame.display.set_mode((640, 480))
                game_over.play()
                menu_items = ("GAME OVER!", "Your Score:", str(SCORE),'','Click here to close','','Highscore:',str(HIGHSCORE))
    
                pygame.display.set_caption('Game Over Screen')
                gm = GameMenu(screen, menu_items)
                gm.run()
                break
            
    all_sprite_list.update()

    screen.blit(background, backgroundRect) # For background to not interfere with sprites
    
    all_sprite_list.draw(screen)
 
    pygame.display.flip()

    clock.tick(FRAME_RATE)

pygame.quit()
