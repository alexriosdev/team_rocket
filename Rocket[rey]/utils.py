import math

class vector2:
   # note, no data member declarations needed

   # constructor
   def __init__(self, x, y):
      # unlike C/Java, no implicit "this" pointer
      # instead, reference is passed in as first argument (self in this case)
      self.x = x
      self.y = y

   # method definitions
   def x(self):
      return self.x

   def y(self):
      return self.y

   
   def add(self, other):
      v = vector2(self.x + other.x, self.y + other.y)
      return v

   def subtract(self, other):
      v = vector2(other.x - self.x, other.y - self.y)
      return v

   def scale(self, scalar):
      v = vector2(self.x * scalar, self.y * scalar)
      return v

   def magnitude(self):
      v = (self.x**2 ) + (self.y**2)
      return math.sqrt(v)

   def normalized(self):
      if self.magnitude()==0:
         return vector2(0,0)
      else:
         return vector2(self.x/self.magnitude(), self.y/self.magnitude())
   
   # overload return-this-as-string for printing
   def __str__(self):
      # format allows you to replace "{}" with variable values
      return "({}, {})".format(self.x, self.y)