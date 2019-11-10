"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
 
From:
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
 
Explanation video: http://youtu.be/QplXBw_NK5Y
 
Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/
 
"""
 
import pygame
 
# Global constants
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW=(255, 255, 0)
MAGENTA = (255, 0, 175)
BROWN = (190, 90, 0)
 
# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

 
class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """
 
    # -- Methods
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None

        self.timeStop = False

 
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                
        block_hit_list = pygame.sprite.spritecollide(self, self.level.brick_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right
                
        block_hit_list = pygame.sprite.spritecollide(self, self.level.item_brick_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        block_hit_list = pygame.sprite.spritecollide(self, self.level.pipe_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        if self.level.pipeFound == False:
            platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            for platform in platform_hit_list:
     
                # Reset our position based on the top/bottom of the object.
                if self.change_y > 0:
                    self.rect.bottom = platform.rect.top
                elif self.change_y < 0:
                    self.rect.top = platform.rect.bottom
     
                # Stop our vertical movement
                self.change_y = 0

            #block hitting
            block_hit_list = pygame.sprite.spritecollide(self, self.level.brick_list, False)
            for block in block_hit_list:
     
                # Reset our position based on the top/bottom of the object.
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom - 1
                    block_hit_list = pygame.sprite.spritecollide(self, self.level.brick_list, True)
                    
     
                # Stop our vertical movement
                self.change_y = 0

            #item block hitting
            item_block_hit_list = pygame.sprite.spritecollide(self, self.level.item_brick_list, False)
            for block in item_block_hit_list:
     
                # Reset our position based on the top/bottom of the object.
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom
                    block.hit += 1
                    block.image.fill(RED)
                    
                self.change_y = 0

            pipe_hit_list = pygame.sprite.spritecollide(self, self.level.pipe_list, False)
            for pipe in pipe_hit_list:
                if self.change_y > 0:
                    self.rect.bottom = pipe.rect.top
                elif self.change_y < 0:
                    self.rect.top = pipe.rect.bottom
                    
     
                # Stop our vertical movement
                self.change_y = 0

            item_hit_list = pygame.sprite.spritecollide(self, self.level.item_list, True)
        #effect
 
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.level.pipeFound == False:
            if self.change_y == 0:
                self.change_y = 1
            else:
                self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        brick_hit_list = pygame.sprite.spritecollide(self, self.level.brick_list, False)
        item_brick_hit_list = pygame.sprite.spritecollide(self, self.level.item_brick_list, False)
        pipe_hit_list = pygame.sprite.spritecollide(self, self.level.pipe_list, False)
        self.rect.y -= 2
         
        # If it is ok to jump, set our speed upwards
        if len(item_brick_hit_list) > 0 or len(brick_hit_list) > 0 or len(pipe_hit_list) > 0 or len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def enterPipe(self, direction):
        if direction == 'down':
            self.rect.y += 2
            pipe_hit_list = pygame.sprite.spritecollide(self, self.level.pipe_list, False)
            self.rect.y -= 2
            if len(pipe_hit_list) > 0:
                self.level.pipeFound = True
            else:
                self.level.pipeFound = False
                
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0


class Item(pygame.sprite.Sprite):

    def __init__(self, item, in_block):

        super().__init__()
        
        self.image = pygame.Surface([40, 40])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.change_x = 0
        self.change_y = 0

        self.in_block = in_block
        self.anim_f = 0
        self.hit = False
        
        self.level = None

        if item == 1:
            self.id = 1
        if item == 2:
            self.id = 2

 
    def update(self):
        """ Move the item. """

        #Gravity (and by extension, movement) only works if self.in_block is False.
        #These if statements animate the item coming out of the block and sets self.in_block to false
        if self.hit == True and self.anim_f < 40:
            self.rect.y -= 1
            self.anim_f += 1
        elif self.anim_f == 40:
            self.in_block = False
            self.change_x = 3
            self.anim_f += 1

        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.change_x = -self.change_x
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.change_x = -self.change_x
                self.rect.left = block.rect.right
                
        block_hit_list = pygame.sprite.spritecollide(self, self.level.brick_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
                self.change_x = -self.change_x
            elif self.change_x < 0:
                self.rect.left = block.rect.right
                self.change_x = -self.change_x
                
        block_hit_list = pygame.sprite.spritecollide(self, self.level.item_brick_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
                self.change_x = -self.change_x
            elif self.change_x < 0:
                self.rect.left = block.rect.right
                self.change_x = -self.change_x

        pipe_hit_list = pygame.sprite.spritecollide(self, self.level.pipe_list, False)
        for pipe in pipe_hit_list:
            if self.change_x > 0:
                self.rect.right = pipe.rect.left
                self.change_x = -self.change_x
            elif self.change_x < 0:
                self.rect.left = pipe.rect.right
                self.change_x = -self.change_x

        
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for platform in platform_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = platform.rect.top
 
            # Stop our vertical movement
            self.change_y = 0


        #block hitting
        block_hit_list = pygame.sprite.spritecollide(self, self.level.brick_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
 
            # Stop our vertical movement
            self.change_y = 0

        item_block_hit_list = pygame.sprite.spritecollide(self, self.level.item_brick_list, False)
        for block in item_block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top

            self.change_y = 0

        pipe_hit_list = pygame.sprite.spritecollide(self, self.level.pipe_list, False)
        for pipe in pipe_hit_list:

            if self.change_y > 0:
                self.rect.bottom = pipe.rect.top

            self.change_y = 0
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        #this only works if the item is out of the block(meaning self.in_block is False)
        if self.in_block == False:
            if self.change_y == 0:
                self.change_y = 1
            else:
                self.change_y += .35
        #else:
            
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
        
 
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(MAGENTA)
 
        self.rect = self.image.get_rect()


class Pipe(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = pygame.Surface([80, 100])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()


class Coin(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = pygame.Surface([30, 50])
        self.image.fill(YELLOW)

        self.rect = self.image.get_rect()


class Brick(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = pygame.Surface([40, 40])
        self.image.fill(BROWN)

        self.rect = self.image.get_rect()


class ItemBrick(pygame.sprite.Sprite):

    def __init__(self, x, y, item):

        super().__init__()

        self.image = pygame.Surface([40, 40])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.hit = 0
        self.level = None
        
        item.rect.x = self.rect.x
        item.rect.y = self.rect.y

    def update(self):

        #if hit by player from the bottom, self.hit will equal 1, making item.hit True
        #This sets off a one time chain of events in the item class
        item_hit_list = pygame.sprite.spritecollide(self, self.level.item_list, False)
        for item in item_hit_list:
            if self.hit >= 1:
                item.hit = True
                self.hit = 2

 
 
class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.pipe_list = pygame.sprite.Group()
        self.coin_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.brick_list = pygame.sprite.Group()
        self.item_brick_list = pygame.sprite.Group()
        self.item_list = pygame.sprite.Group()
        self.player = player
 
        # How far this world has been scrolled left/right
        self.world_shift = 0

        self.pipeFound = False
        self.pipeEntering = False

        #score from various things (ex. collecting coins)
        self.score = 0
 
    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.pipe_list.update()
        self.enemy_list.update()
        self.coin_list.update()
        self.brick_list.update()
        self.item_brick_list.update()
        self.item_list.update()

        coin_hit_list = pygame.sprite.spritecollide(self.player, self.coin_list, True)
        if coin_hit_list:
            self.score += 1
        
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.fill(BLUE)
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.pipe_list.draw(screen)
        self.enemy_list.draw(screen)
        self.coin_list.draw(screen)
        self.item_list.draw(screen)
        self.brick_list.draw(screen)
        self.item_brick_list.draw(screen)
 
    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """
 
        # Keep track of the shift amount
        self.world_shift += shift_x
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for coin in self.coin_list:
            coin.rect.x += shift_x

        for brick in self.brick_list:
            brick.rect.x += shift_x

        for itemBrick in self.item_brick_list:
            itemBrick.rect.x += shift_x

        for item in self.item_list:
            item.rect.x += shift_x

        for pipe in self.pipe_list:
            pipe.rect.x += shift_x
 
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -10000
 
        # Array with width, height, x, and y of platform
        platformMap = [[210, 70, 500, 500],
                       [210, 70, 800, 400],
                       [210, 70, 1000, 500],
                       [210, 70, 1120, 280],
                       [20, 70, 300, 600],
                       [20, 70, 700, 650]
                       ]
 
        # Go through the array above and add platforms
        for platform in platformMap:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        #
        coinMap = [[530, 400],
                   [600, 400],
                   [935, 40]
                   ]

        for coin in coinMap:
            collect = Coin()
            collect.rect.x = coin[0]
            collect.rect.y = coin[1]
            collect.player = self.player
            self.coin_list.add(collect)

        #
        brickMap = [[530, 300],
                    [480, 300],
                    [930, 130]
                    ]

        for brick in brickMap:
            block = Brick()
            block.rect.x = brick[0]
            block.rect.y = brick[1]
            block.player = self.player
            self.brick_list.add(block)

        #items     item(id, in_block)
        mushroom01 = Item(1, True)
        self.item_list.add(mushroom01)
        mushroom01.change_x = 0
        
        mushroom02 = Item(2, True)
        self.item_list.add(mushroom02)
        mushroom02.change_x = 0
        
        #
        itemBrickMap = [[1000, 230, mushroom01],
                        [1300, 100, mushroom02]
                        ]

        for brick in itemBrickMap:
            brah = ItemBrick(brick[0], brick[1], brick[2])
            brah.player = self.player
            self.item_brick_list.add(brah)

        #
        pipeMap = [[1600, 660]
                   ]

        for pipe in pipeMap:
            entrance = Pipe()
            entrance.rect.x = pipe[0]
            entrance.rect.y = pipe[1]
            entrance.player = self.player
            self.pipe_list.add(entrance)


 
# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -1000
 
        # Array with type of platform, and x, y location of the platform.
        level = [[210, 30, 450, 570],
                 [210, 30, 850, 420],
                 [210, 30, 1000, 520],
                 [210, 30, 1120, 280],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 
 
def main():
    """ Main Program """
    pygame.init()
    pygame.mixer.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Basically Super Mario Bros")
 
    # Create the player
    player = Player()
 
    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    for items in level_list[current_level_no].item_list:
        items.level = current_level

    for item_block in level_list[current_level_no].item_brick_list:
        item_block.level = current_level
 
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    player.anim_f = 0
    active_sprite_list.add(player)

    timeStop = False
    
    #music
    #pygame.mixer.music.load('overworld.mp3')
    #pygame.mixer.music.play(-1, 0)
    
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.mixer.music.stop()
                pygame.mixer.stop()
 
            if event.type == pygame.KEYDOWN:
                if timeStop == False:
                    if event.key == pygame.K_LEFT:
                        player.go_left()
                    if event.key == pygame.K_RIGHT:
                        player.go_right()
                    if event.key == pygame.K_UP:
                        player.jump()
                    if event.key == pygame.K_DOWN:
                        player.enterPipe('down')
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
 
        # Update the player.
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()

        # player entering pipe animation
        if level_list[current_level_no].pipeFound == True:
            pipe_hit_list = pygame.sprite.spritecollide(player, level_list[current_level_no].pipe_list, False)
            for pipe in pipe_hit_list:
                pipeCenter = pipe.rect.x + ((pipe.rect.right - pipe.rect.left) / 2) - ((player.rect.right - player.rect.left) / 2)
                if player.rect.x != pipeCenter:
                    if (pipeCenter - player.rect.x) < 0:
                        player.rect.x -= 1
                    elif (pipeCenter - player.rect.x) > 0:
                        player.rect.x += 1
               # else:
                #    level_list[current_level_no].pipeEntering = True



        if player.anim_f < 60 and level_list[current_level_no].pipeFound == True :
            player.rect.y += 1
            player.anim_f += 1
            timeStop = True
            level_list[current_level_no].pipeFound = True
        elif player.anim_f == 60:
            player.anim_f = 0
            timeStop = False
            level_list[current_level_no].pipeFound = False
            #level_list[current_level_no].pipeEntering = False
            player.rect.y -= 100
 
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)
 
        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
 
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
 
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

if __name__ == "__main__":
    main()
