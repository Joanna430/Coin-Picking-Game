import random

class World:
    def __init__(self, width, height, coin_probability):
        """
        Set up world as a 2D-matrix of the given dimensions. Location coordinates are numbered 0... width-1 and 0... height-1.
        Each location either contains a coin or not, and is initialized to have a coin with the given probability.
        The world at first has no people. The world does not keep track of the people's locations, however, the people do themselves.
        Multiple people can be in the same location. Assume that width and height are positive integers and that coin_probability is in the range [0,1].
        """       
        self.width = width
        self.height = height
        self.people = set()  # Initially no people
        
        a_list = []
        for num in range(self.width):
            b_list = []
            for num in range(self.height):
                prob = random.random()
                if prob < coin_probability:
                    b_list.append(1)
                else:
                    b_list.append(0)
            a_list.append(b_list)
        self.coins = a_list 
        
    def add_person(self, person):
        """
        Adds the given person (object) to the world's people.
        """
        (self.people).add(person)       
        
    def get_people(self):
        """
        Returns a new set of the people in the world.
        """     
        return set(self.people)
            
    def get_dimensions(self):
        """
        Returns the width and height of the world.
        """     
        return (self.width, self.height)

    def pickup_coin(self, x, y):
        """
        If a coin is at location (x,y), it removes it from the location.
        It returns the number of coins that were there.     
        Assume location (x,y) is within the world boundary.
        """
        if self.coins[x][y] == 1:
            self.coins[x][y] = 0
            return 1
        else:
            return self.coins[x][y]

    
class Person:
    def __init__(self, name, x, y, coins, world):
        """
        Initializes a person with the given name, number of coins, and world.
        Initializes a person to have the given location (x,y) in the given world, except that if those coordinates are outside the bounds of the world,
        then the nearest location inside the bounds is used.
        It adds the person to the world, and uses the check_location method to look for coins or people at the initial location.
        """       
        self.name = name
        self.coins = coins
        self.world = world

        self.x = x
        self.y = y
        if x > self.world.width - 1:
            self.x = self.world.width - 1
        elif x < 0:
            self.x = 0
        if y > self.world.height -1:
            self.y = self.world.height -1
        elif y < 0:
            self.y = 0
        self.world.add_person(self)
        self.check_location()
        
    def get_name(self):
        """
        Returns the person's name.
        """       
        return self.name
        
    def get_coordinates(self):
        """
        Returns the person's (x,y) location.
        """    
        return (self.x, self.y)
        
    def get_coins(self):
        """
        Returns how many coins the person has.
        """  
        return (self.coins)
        
    def lose_coins(self):
        """
        Changes the person's number of coins to zero. Returns the number of coins the person had.
        """
        a_copy = self.coins
        self.coins = 0
        return a_copy
        
    def check_location(self):
        """
        If a coin is at the person's new location, the person picks it up and keeps it.
        If other people are already there, this person steals all their coins.       
        This method should only be called by other Person methods, after moving.
        """       
        if self.world.pickup_coin(self.x,self.y) == 1:
            self.coins += 1
        else:
            people = self.world.get_people()
            for person in people:
                if person.get_coordinates() == self.get_coordinates():
                    other = person.lose_coins()
                    self.coins += int(other)       
            
        return self.coins             
        
    def north(self):
        """
        If not already at the north world boundary, moves the person north one location and uses the check_location to look for coins or people at the location.
        """
        if self.y < self.world.height - 1:
            self.y += 1
        self.check_location()
        
    def south(self):
        """
        If not already at the south world boundary, moves the person south one location and uses the check_location method to look for coins or people at the location.
        """
        if self.y > 0:
            self.y -= 1
        self.check_location()
        
    def east(self):
        """
        If not already at the east world boundary, moves the person east one location and uses the check_location method to look for coins or people at the location.
        """
        if self.x < self.world.width - 1:
            self.x += 1
        self.check_location()
        
    def west(self):
        """
        If not already at the west world boundary, moves the person west one location and uses the check_location method to look for coins or people at the location.
        """
        if self.x > 0:
            self.x -= 1
        self.check_location()

        
        
print "=World test 1 ================================"    
nocoins_world = World(6, 5, 0)
john = Person("John", -1, -10, 2, nocoins_world)
sarah = Person("Sarah", 8, 6, 4, nocoins_world)
print john.get_name(), "is at", john.get_coordinates(), "-- should be at (0, 0)."
print sarah.get_name(), "is at", sarah.get_coordinates(), "-- should be at (5, 4)."
sarah.north() # Run into north boundary.
print sarah.get_name(), "is at", sarah.get_coordinates(), "-- should be at (5, 4)."
sarah.east()  # Run into east boundary.
print sarah.get_name(), "is at", sarah.get_coordinates(), "-- should be at (5, 4)."
print sarah.get_name(), "has", sarah.get_coins(), "coins -- should be 4." 
ryan = Person("Ryan", 5, 2, 1, nocoins_world)
print ryan.get_name(), "has", ryan.get_coins(), "coins -- should be 1."
ryan.north()  
print ryan.get_name(), "has", ryan.get_coins(), "coins -- should be 1."
ryan.north()  # Run into Sarah.
print ryan.get_name(), "has", ryan.get_coins(), "coins -- should be 5." #%%%
print sarah.get_name(), "has", sarah.get_coins(), "coins -- should be 0."
print ryan.get_name(), "is at", ryan.get_coordinates(), "-- should be at (5, 4)."
john.west()  # Run into west boundary.
print john.get_name(), "is at", john.get_coordinates(), "-- should be at (0, 0)."
john.south() # Run into south boundary.
print john.get_name(), "is at", john.get_coordinates(), "-- should be at (0, 0)."

print "=World test 2================================"
allcoins_world = World(10, 5, 1)
tanya = Person("Tanya", 2, 0, 2, allcoins_world)
print tanya.get_name(), "has", tanya.get_coins(), "coins -- should be 3."
caleb = Person("Caleb", 2, -5, 1, allcoins_world)
print caleb.get_name(), "is at", caleb.get_coordinates(), "-- should be at (2, 0)."
print tanya.get_name(), "has", tanya.get_coins(), "coins -- should be 0."
print caleb.get_name(), "has", caleb.get_coins(), "coins -- should be 4."
bailey = Person("Bailey", -3, 0, 1, allcoins_world)
print bailey.get_name(), "is at", bailey.get_coordinates(), "-- should be at (0, 0)."
print bailey.get_name(), "has", bailey.get_coins(), "coins -- should be 2."
bailey.east()
print bailey.get_name(), "has", bailey.get_coins(), "coins -- should be 3."
bailey.east()
print bailey.get_name(), "is at", bailey.get_coordinates(), "-- should be at (2, 0)."
print bailey.get_name(), "has", bailey.get_coins(), "coins -- should be 7."
print tanya.get_name(), "has", tanya.get_coins(), "coins -- should be 0."
print caleb.get_name(), "has", caleb.get_coins(), "coins -- should be 0."
