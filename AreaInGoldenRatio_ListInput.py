# calculates length and width of a rectangle in the golden ratio, based on the given area, input as list

import math

area = IN[0] #input has to be a list

# convert inputlist to float
area_fl = []
for i in range(len(area)):
	result_a = float(area[i])
	area_fl.append(result_a)

# calculate golden angle
phi = (1+math.sqrt(5))/2

# calculate width
width_out = []
for f in area_fl:
	width = math.sqrt(f*(1/phi))
	width_out.append(width)
width_r = ['%.1f' % elem for elem in width_out] #round to 1 decimal

# calculate length
length_out = []
for a,w in zip(area_fl,width_out):
	length = a/w
	length_out.append(length)
length_r = ['%.1f' % elem for elem in length_out] #round to 1 decimal

OUT = [length_r, width_r]
