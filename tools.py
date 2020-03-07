from math import sqrt

def distance(c1,c2):
    x=abs(c1[0]-c2[0])**2
    y=abs(c1[1]-c2[1])**2
    return sqrt(x+y)


