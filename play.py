# play.py
# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getTries(self):
        """
        Returns the number of tries left as type string
        """
        return str(self._tries)
    
    def getWin(self):
        """
        Returns True if there are no bricks left
        """
        if (len(self._bricks) == 0):
            return True
        else:
            return False
        
    
    


    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """
        Creates the bricks and the paddle for the game. Also sets the number of tries the player
        has. The ball is created later when it is 'served'.
        """
        self._paddle = Paddle()
        self._bricks = []
        xCoord = BRICK_SEP_H/2 + BRICK_WIDTH/2
        for x in range(BRICK_ROWS):
            for y in range(BRICKS_IN_ROW):
                yCoord = GAME_HEIGHT - BRICK_Y_OFFSET - BRICK_HEIGHT/2 - (y * (BRICK_SEP_V + BRICK_HEIGHT))
                self._bricks.append(Brick(xCoord,yCoord,BRICK_WIDTH,BRICK_HEIGHT, self.brickColor(y+1)))
            xCoord = BRICK_SEP_H + BRICK_WIDTH + xCoord
        self._tries = NUMBER_TURNS
        

        
    
    
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def serveBall(self):
        """
        This method is called by Breakout.py. It creates the ball for the game to use.
        """
        self._ball = Ball()
    
    def updatePaddle(self,direction):
        """
        This method moves the paddle either left or right depending on player input
        which is received from Breakout.py.
        
        Parameter direction: The direction the paddle is being directed to move in
        Precondition: direction is a string of "left" or "right".
        """
        if (direction == 'left'):
            self._paddle.x = max(self._paddle.x - 7, PADDLE_WIDTH/2)
        elif (direction == 'right'):
            self._paddle.x = min (self._paddle.x + 7, GAME_WIDTH - PADDLE_WIDTH/2)
            
            
            
    def updateBall(self):
        """
        This method utilizes the collision methods from models to adjust the velocities
        of the ball depending on wheter the ball actually collides. It also constantly
        updates the ball in the x and y direction
        """
        
        self._ball.x = self._ball.x + self._ball.getvx()
        self._ball.y = self._ball.y + self._ball.getvy()
        if (self._ball.left <= 0):
            velocity = self._ball.getvx() * -1
            self._ball.setvx(velocity)
        if (self._ball.right >= GAME_WIDTH):
            velocity = self._ball.getvx() * -1
            self._ball.setvx(velocity)
        if (self._ball.top >= GAME_HEIGHT):
            velocity = self._ball.getvy() * -1
            self._ball.setvy(velocity)
        if (self.brickCollision(self._ball)):
            velocity = self._ball.getvy() * -1
            self._ball.setvy(velocity)
        if (self.paddleCollsion(self._ball)):
            velocity = self._ball.getvy() * -1
            self._ball.setvy(velocity)
            
    
    
    
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def drawPaddle(self,view):
        """
        This function which draws the paddle is called by the draw function in
        Breakout.py
        
        Parameter view: This is the view that this function will draw to
        Precondition: view is an instance of GView
        """
        assert isinstance(view, GView)
        self._paddle.draw(view)
        
        
        
    def drawBricks(self,view):
        """
        This function which draws the bricks is called by the draw function in
        Breakout.py
        
        Parameter view: This is the view that this function will draw to
        Precondition: view is an instance of GView
        """
        assert isinstance(view, GView)
        for x in self._bricks:
            (x.draw(view))
            
            
    def drawBall(self,view):
        """
        This function which draws the ball is called by the draw function in
        Breakout.py
        
        Parameter view: This is the view that this function will draw to
        Precondition: view is an instance of GView
        """
        assert isinstance (view, GView)
        
        self._ball.draw(view)
    
    
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def brickCollision(self,ball):
        """
        This function tests collisions between the ball and the bricks. If there
        is a collsion, the brick is removed from the game.
        
        Returns true if there is a collision and false if there isn't.
        
        Parameter ball: The ball that will be tested for collision with the bricks
        Precondition: ball is an instance of the model Ball.
        """
        assert isinstance (ball,Ball)
        
        for x in range(len(self._bricks)):
            if (self._bricks[x].brickCollide(ball)):
                self._bricks.pop(x)
                return True   
        return False
    
    
    def paddleCollsion(self,ball):
        """
        This function tests collisions between the ball and the paddle.
        
        Returns true if there is a collision and false if there isn't.
        
        Parameter ball: The ball that will be tested for collision with the paddle
        Precondition: ball is an instance of the model Ball.
        """
        assert isinstance(ball,Ball)
        
        if(self._paddle.paddleCollide(ball)):
            return True
        return False
    
                
    
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE

    def checkLostBall(self):
        """
        This function tests whether the player has lost the ball. If the ball is lost,
        the player loses a try
        
        Returns true if the ball is lost and false if it isn't
        """
        if (self._ball.y < -20):
            self._tries = self._tries - 1
            return True
        else:
            return False
        
    def brickColor(self, n):
        """
        A helper function to make bricks which returns the color needed by that row of bricks
        """
        if (n % 10 == 0 or n%10 == 9):
            return colormodel.BLUE
        if (n % 10 == 2 or n% 10 == 1):
            return colormodel.RED
        elif (n % 10 <=  4):
            return colormodel.ORANGE
        elif (n % 10 <= 6):
            return colormodel.YELLOW
        elif (n % 10 <= 8):
            return colormodel.GREEN
            
    
    

    
