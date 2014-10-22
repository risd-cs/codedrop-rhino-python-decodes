import pickle, sys,pygame, shapely, chiplotle
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely.geometry import LineString
from shapely.geometry import MultiPoint
from chiplotle import *
pygame.init()
screen = pygame.display.set_mode((500,500))

f = open('./data_a.pkl', 'rb')
hpgl_file=open('./hatch.hpgl', 'w')

data = pickle.load(f)
f.close()

def pen_plot_shape(polyBoundary, spacing=2, color=10, hatchdirection = (0,1)):
	#color controls the pattern of hatching. ranging from 0 to 20, with 0  mostly pen 1, 20 is mostly pen 2
	#doesn't yet work for diag hatching, but would be quick to implement
	stepDirection = (hatchdirection[1]*spacing, hatchdirection[0]*spacing)
	#pygame.draw.polygon(screen, (255,0,0), polyBoundary.coords, 1)
	basePt = [0,0]
	lineCount = 0
	modOperand = int(abs(color-10) + 2)
	
	if color >=10:
		domPen = 1
		weakPen = 2
	else:
		domPen = 2
		weakPen = 1
	
	while basePt[0]<500 and basePt[1]<500:
		tipPt = [basePt[0]+hatchdirection[0]*500, basePt[1]+hatchdirection[1]*500]
		guideLine = LineString([basePt,tipPt])
		intersectPoints = guideLine.intersection(polyBoundary)
		#pygame.draw.line(screen, (0,255,0), basePt, tipPt, 1)
		#print intersectPoints
		if type(intersectPoints)==MultiPoint:
			for i in range(len(intersectPoints)-1):
				if i%2==0:
					x1,x2,y1,y2 = intersectPoints[i].x,intersectPoints[i+1].x,intersectPoints[i].y, intersectPoints[i+1].y
					pygame.draw.circle(screen, (0,0,255), (x1,y1), 2,0)
					pygame.draw.circle(screen, (0,0,255), (x2,y2), 2,0)
					x1,x2,y1,y2 = x1*20,x2*20,y1*20,y2*20
					x1,x2,y1,y2 = x1-5000,x2-5000,y1-5000,y2-5000
					if lineCount%modOperand == 0:
						hpgl_file.write(hpgl.SP(weakPen).format)
					else:
						hpgl_file.write(hpgl.SP(domPen).format)
					hpgl_file.write(hpgl.PU([(x1,y1)]).format)
					hpgl_file.write(hpgl.PD([(x2,y2)]).format)
		basePt[0]+=stepDirection[0]
		basePt[1]+=stepDirection[1]
		lineCount+=1
#following commented out code used to measure extents of data
#for now, sloppy
"""
minX = 10000
maxX = -10000
minY = 10000
maxY = -10000
minD = 10000
maxD = -10000

for item in data:
	coords = item[0]
	d = item[1]
	if d<minD:
		minD = d
	if d>maxD:
		maxD=d
	for coord in coords:
		x = coord[0]
		y = coord[1]
		#print (x,y)
		if x<minX:
			minX = x
		if x>maxX:
			maxX= x
		if y<minY:
			minY = y
		if y>maxY:
			maxY= y
print (minX, maxX)
print (minY, maxY)
print (minD, maxD)
"""

shiftD = -150
scaleD = 1.5

shiftX = 3.5
shiftY = 3.5

scaleCoordsX = 70
scaleCoordsY = 70
#shift and scale data

newData = []
for item in  data:
	distance = item[1]
	coords = item[0]
	newCoords = []
	for coord in coords:
		newCoord = ((coord[1]+shiftY)*scaleCoordsY, (coord[0]+shiftX)*scaleCoordsX)
		#print newCoord
		newCoords.append(newCoord)
	newDistance = (distance + shiftD)*scaleD
	newData.append([newCoords, newDistance])
	

#print newData

go = 1
drawn=False
while go:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()

	screen.fill((255,255,255))
	shapelyPolygons=[]
	for item in newData:
		#print item[1]
		#uncomment the following line should result in a drawn scene as normal and expected as raster image given accurate BSP tree-made drawing order
		#pygame.draw.polygon(screen, (item[1], item[1],item[1]), item[0], 1)
		shapelyPolygons.append(Polygon(item[0]))

	shapelyPolygonsTrimmed = []

	for i in range(len(shapelyPolygons)):
		currentPolygon = shapelyPolygons[i]
		for j in range(i+1,len(shapelyPolygons),1):
			if not currentPolygon.is_empty:
				currentPolygon = currentPolygon.difference(shapelyPolygons[j])
		shapelyPolygonsTrimmed.append(currentPolygon)
		

	for i in range(len(shapelyPolygonsTrimmed)):
		if not shapelyPolygonsTrimmed[i].is_empty:
			if type(shapelyPolygonsTrimmed[i]) is Polygon:
				coords = list(shapelyPolygonsTrimmed[i].exterior.coords)
				color = newData[i][1]
				#print color
 				pygame.draw.polygon(screen, (color,color,color), coords, 0)
 				if not drawn:
 					
 					pen_plot_shape(shapelyPolygonsTrimmed[i].exterior, color/100.0, color/10.0)
			elif type(shapelyPolygonsTrimmed[i]) is MultiPolygon:
				for poly in shapelyPolygonsTrimmed[i].geoms:
					coords = list(poly.exterior.coords)
					color = newData[i][1]
					#print color
					
 					pygame.draw.polygon(screen, (color,color,color), coords, 0)
 					if not drawn:
 						pen_plot_shape(poly.exterior, color/100.0, color/10.0)

	if not drawn:
		hpgl_file.close()
	 	drawn = True


	pygame.display.flip()
	go =1
