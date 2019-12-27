#calculates length and width of a rectangle in the golden ratio, based on the given area

import math

area = IN[0]

#calculate golden angle
phi = (1+math.sqrt(5))/2

#calculate width and length
width = math.sqrt(area*(1/phi))
length = area/width

#output as a list, rounded to 1 decimal 
OUT = [round(length,1), round(width,1)]
