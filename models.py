# models.py
# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *
import colormodel



# PRIMARY RULE: Models are not allowed to access anything except the module constants.py.
# If you need extra information from Play, then it should be a parameter in your method, 
# and Play should pass it as a argument when it calls the method.


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    
    # INITIALIZER TO CREATE A NEW PADDLE
    def __init__(self):
        """
        Creates the Paddle for the game to use
        """
        GRectangle.__init__(self,x = GAME_WIDTH/2,y = PADDLE_OFFSET + PADDLE_HEIGHT/2,width = PADDLE_WIDTH,height = PADDLE_HEIGHT)
        self.fillcolor = colormodel.BLACK
    
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    def paddleCollide(self,ball):
        """
        Tests whether the paddle collides with the ball
        
        Returns true if collision happens between ball and paddle and false otherwise
        
        Parameter ball: the ball to be tested for collision with the paddle
        Precondition ball: ball is of type Ball from class model
        """
        assert isinstance (ball, Ball)
        
        if (self.contains(ball.x + BALL_DIAMETER/2,ball.y - BALL_DIAMETER/2)):
            return True
        if (self.contains(ball.x - BALL_DIAMETER/2,ball.y - BALL_DIAMETER/2)):
            return True
        return False
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Brick(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball.  You may wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    
    
    # INITIALIZER TO CREATE A BRICK
    def __init__(self,x,y,width,height,c):
        """
        Creates the brick to be placed into the list of bricks in play.
        
        Parameter x: the x coordinate of the center of the brick
        Precondition: x is a number of type int or float
        
        Parameter y: the y coordinate of the center of the brick
        Precondition: y is a number of type of int or float
        
        Parameter width: the width of each brick
        Precondition: width is a number of type int or float
        
        Parameter height: the height of each brick
        Precondition: height is a number of type int or float
        
        Parameter c: the color of the brick
        Precondition: c is a color of type colormodel.RGB
        """
        assert type(x) == int or type(x) == float
        assert type(y) == int or type(y) == float
        assert type(width) == int or type(width) == float
        assert type(height) == int or type(height) == float
        assert isinstance(c, colormodel.RGB)
        
        GRectangle.__init__(self,x = x,y = y,width = width,height = height, fillcolor = c)
    
    
    # METHOD TO CHECK FOR COLLISION
    def brickCollide(self,ball):
        """
        Tests for a collision between the ball and brick. It checks every side of the
        brick for collision.
        
        Returns true if there is a collision and false otherwise
        
        Parameter ball: the ball to test for collision between the brick and ball
        Precondition: ball is an instance of type Ball from models
        """
        assert isinstance (ball,Ball)
        
        if (self.contains(ball.x + BALL_DIAMETER/2,ball.y + BALL_DIAMETER/2)):
            return True
        if (self.contains(ball.x - BALL_DIAMETER/2,ball.y + BALL_DIAMETER/2)):
            return True
        if (self.contains(ball.x + BALL_DIAMETER/2,ball.x - BALL_DIAMETER/2)):
            return True
        if (self.contains(ball.x - BALL_DIAMETER/2,ball.x - BALL_DIAMETER/2)):
            return True
        return False
        
    
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getvx(self):
        """
        Returns the velocity of the ball in the x-direction
        """
        return self._vx
    def getvy(self):
        """
        Returns the velocity of the ball in the y-direction
        """
        return self._vy
    def setvx(self,velocity):
        """
        Sets the velocity of the ball in the x-direction
        
        Parameter velocity: the new velocity of the ball in the x-direction
        Precondition: velocity is a number of either type float or int
        """
        assert type(velocity) == int or type(velocity) == float

        self._vx = velocity
    def setvy(self, velocity):
        """
        Sets the velocity of the ball in the y-direction
        
        Parameter velocity: the new velocity of the ball in the y-direction
        Precondition: velocity is a number of either type float or int
        """
        assert type(velocity) == int or type(velocity) == float
        
        self._vy = velocity

    

    
    

    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self):
        """
        Creates the Ball for the game to use and it is given random velocities in the x direction.
        It is given the velocity of -5 in the y-direction
        """
        
        GEllipse.__init__(self,x = GAME_WIDTH/2, y = BALL_Y, width = BALL_DIAMETER,height = BALL_DIAMETER, fillcolor = colormodel.BLACK)
        self._vx = random.uniform(1.0,5.0) 
        self._vx = self._vx * random.choice([-1, 1])
        self._vy = -5
    
    
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
        
    
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY





    # IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE