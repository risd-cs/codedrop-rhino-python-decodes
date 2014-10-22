import rhinoscriptsyntax as rs
import math, pickle


def convertRhinoPointToSimpleList (pointList, surface):
    simplePointList = []
    for pt in pointList:
        UV = rs.SurfaceClosestPoint(surface,pt)
        coord = (UV[0], UV[1])
        simplePointList.append(coord)
    return simplePointList

def cleanList (messyList):
    clean = []
    for item in messyList:
        if type(item) is list:
            for subitem in item:
                if subitem and subitem!=[]:
                    clean.append(subitem)
        else:
            clean.append(item)
    return clean
        

def sameLine (line1, line2):
    start1, end1, start2, end2 = rs.CurveStartPoint(line1), rs.CurveEndPoint(line1), rs.CurveStartPoint(line2), rs.CurveEndPoint(line2)
    d1 = math.sqrt((start1[0]-start2[0])**2+(start1[1]-start2[1])**2)
    d2 = math.sqrt((end1[0]-end2[0])**2+(end1[1]-end2[1])**2)
    d3 = math.sqrt((start1[0]-end2[0])**2+(start1[1]-end2[1])**2)
    d4 = math.sqrt((end1[0]-start2[0])**2+(end1[1]-start2[1])**2)
    #print (d1,d2,d3,d4)
    if (d1<.1 and d2<.1) or (d3<.1 and d4<.1):
        return True
    return False

def arePolysTouching(poly1, poly2):
    #print(poly1, poly2)
    if poly1 == None or poly2==None:
        return False
    
    planeSrf1 = rs.AddPlaneSurface(rs.PlaneFitFromPoints(rs.CurvePoints(poly1)),10,10)
    planeSrf2 = rs.AddPlaneSurface(rs.PlaneFitFromPoints(rs.CurvePoints(poly2)),10,10)
    if rs.SurfaceNormal(planeSrf1,(0,0)) != rs.SurfaceNormal(planeSrf2,(0,0)):
        rs.DeleteObjects([planeSrf1,planeSrf2])
        return False
    rs.DeleteObjects([planeSrf1,planeSrf2])
    intersections = rs.CurveCurveIntersection(poly1, poly2)
    if intersections:
        for inter in intersections:
            if inter[0]==2:
                return True
    return False
    
def mergePolys(poly1, poly2):
    if poly1 == None or poly2==None:
        return False
    segments1 = rs.ExplodeCurves(poly1)
    segments2 = rs.ExplodeCurves(poly2)
    
    nonOverlappingSegs = []
    
    for seg in segments1:
        dup = False
        for seg2 in segments2:
            if sameLine(seg, seg2):
                #print 'found a same'
                dup = True
                segments2.remove(seg2)
                break
        if not dup:
            nonOverlappingSegs.append(seg)

    result = rs.JoinCurves(nonOverlappingSegs+segments2)[0]
    
    rs.DeleteObjects(segments1)
    rs.DeleteObjects(segments2)
    return result


def makeTree(polygons):
    plane = rs.PlaneFitFromPoints(rs.CurvePoints(polygons[0]))
    planeSrf = rs.AddPlaneSurface(plane, 1,1)
    planeNormal = rs.SurfaceNormal(planeSrf,(0,0))
    pointAboveSurface  = rs.VectorAdd(rs.EvaluateSurface(planeSrf, 0,0), planeNormal)
    pointBelowSurface = rs.VectorAdd(rs.EvaluateSurface(planeSrf, 0,0), rs.VectorScale(planeNormal,-1))
    polysOnPositiveSide = []
    polysOnNegativeSide = []
    polysInPlane = [polygons[0]]
    
    
    rs.ObjectLayer(polygons[0], "Layer 01")
    
    polygons = polygons[1:]
    
    for polygon in polygons:
        segments = rs.ExplodeCurves(rs.CopyObject(polygon))
        
        
        
        center = rs.CurveAreaCentroid(polygon)
    
        for seg in segments:
            countOverlaps = 0
            countPoints = 0
            crossPoints = []
            crossPointParams = []
            intersect = rs.PlaneCurveIntersection(plane,seg)
            if intersect:
                
                
                for intersectionEvent in intersect:
                    if intersectionEvent[0]==2:
                        countOverlaps+=1
                    else:
                        #rs.AddPoint(intersectionEvent[1])
                        countPoints+=1
                        crossPoints.append(intersectionEvent[1])
                        crossPointParams.append(intersectionEvent[5])
                break
        #print (countOverlaps, countPoints)
        
        if len(crossPoints) > 1:
            tempPointObjects = rs.AddPoints(crossPoints)
        if countOverlaps>=3: #we have a plane in plane. 
            polysInPlane.append(polygon)
            
        elif countPoints>=2 and countOverlaps==0: #we have a genuine crossover intersect. a healthy intersect. not touching, actually crossing. what a pain rhino!
            
            cuttingLine = rs.AddLine(crossPoints[0], crossPoints[1])
            cuttingLine2 = rs.CopyObject(cuttingLine, (1,1,1))
            cuttingSurface = rs.AddLoftSrf([cuttingLine, cuttingLine2])
            srf = rs.AddPlanarSrf(polygon)
            splitResult = rs.SplitBrep(srf, cuttingSurface, True)
            #print (srf, cuttingSurface)
            #print splitResult
            
            if splitResult == None:
                centroid = rs.CurveAreaCentroid(polygon)
                print centroid[0]
                closestPoint  = rs.PlaneClosestPoint(plane,centroid[0])
                vectorToCentroid = rs.VectorCreate(centroid[0], closestPoint)
                angle1 = rs.VectorAngle( vectorToCentroid, planeNormal)
                if angle1<1:
                    polysOnPositiveSide.append(polygon)
                else:
                    polysOnNegativeSide.append(polygon)
                
            
                
                rs.DeleteObjects([cuttingSurface, cuttingLine, srf, cuttingLine2])
            else:
                newPoly1 = rs.DuplicateSurfaceBorder(splitResult[0])
                newPoly2 = rs.DuplicateSurfaceBorder(splitResult[1])
                
                centroid = rs.CurveAreaCentroid(newPoly1)[0]
                closestPoint  = rs.PlaneClosestPoint(plane,centroid)
                
                vectorToCentroid = rs.VectorCreate(centroid, closestPoint)
                
                angle1 = rs.VectorAngle( vectorToCentroid, planeNormal)
                
                if angle1<1:
                    polysOnPositiveSide.append(newPoly1)
                    polysOnNegativeSide.append(newPoly2)
                else:
                    polysOnPositiveSide.append(newPoly2)
                    polysOnNegativeSide.append(newPoly1)
            
                rs.DeleteObject(polygon)
            
                rs.DeleteObjects(splitResult)
                rs.DeleteObjects([cuttingSurface, cuttingLine, srf, cuttingLine2])
           
            
            
            
            #splitCurve = rs.SplitCurve(polygon, crossPointParams[0])
            
        
        
        #at this point all special cases taken care of -- polys in plane and polys intersecting plane
        
        elif rs.Distance(pointAboveSurface,center)<rs.Distance(pointBelowSurface, center):
            polysOnPositiveSide.append(polygon)
        else:
            polysOnNegativeSide.append(polygon)
        if len(crossPoints) > 1:
            rs.DeleteObjects(tempPointObjects)
        rs.DeleteObjects(segments)
        
        #at this point all the polys are partioned into lists
        
    if len(polysOnNegativeSide)>0:
        polysOnNegativeSide = makeTree(polysOnNegativeSide)
    if len(polysOnPositiveSide)>0:
        polysOnPositiveSide = makeTree(polysOnPositiveSide)
            
        
    rs.DeleteObject(planeSrf)
    return [polysInPlane, polysOnPositiveSide, polysOnNegativeSide]
        


def traverseTree(tree, viewerPosition):
    global renderQueue
    
    if tree == []:
        return
    
    plane = rs.PlaneFitFromPoints(rs.CurvePoints(tree[0][0]))
    planeSrf = rs.AddPlaneSurface(plane, 1,1)
    planeNormal = rs.SurfaceNormal(planeSrf,(0,0))
    closestPoint  = rs.PlaneClosestPoint(plane,viewerPosition)
    vectorToViewer = rs.VectorCreate(viewerPosition, closestPoint)
    angle1 = rs.VectorAngle( vectorToViewer, planeNormal)
    if angle1<1: #ON THE POSITIVE SIDE
        traverseTree(tree[2], viewerPosition)
        renderQueue.extend(tree[0])
        traverseTree(tree[1], viewerPosition)
    else:
        traverseTree(tree[1], viewerPosition)
        renderQueue.extend(tree[0])
        traverseTree(tree[2], viewerPosition)
        
    rs.DeleteObjects([planeSrf])


def render(queue, picturePlane, viewPoint, viewDirection):
    pictureSurface = rs.AddPlaneSurface(picturePlane,10000,10000)
    rs.ExtendSurface(pictureSurface, (0,10),10000)
    rs.ExtendSurface(pictureSurface, (10,0),10000)
    
    rs.MoveObject(pictureSurface, rs.VectorScale(rs.VectorUnitize(viewDirection),10))
    
    filteredQueue = []
    
    queue = cleanList(queue)
    
    #filter to check touching
    w=0
    while w < (len(queue)-1):
        
        if arePolysTouching(queue[w], queue[w+1]):
            filteredQueue.append(mergePolys(queue[w], queue[w+1]))
            w+=2
        else:
            filteredQueue.append(queue[w])
            w+=1
    if w == len(queue)-1:
        filteredQueue.append(queue[w])
        
        
        
        
    curvesProjectedOnPicture = []
    solids = []
    surfacesInPicturePlane = []
    curvePointsInPP=[]
    distancesFromPP = []
    for poly in filteredQueue:
 
        extruded = rs.ExtrudeCurvePoint(poly, viewPoint)
        areaCenter=rs.CurveAreaCentroid(poly)[0]
        distancesFromPP.append(rs.Distance(areaCenter,viewPoint))
        rs.CapPlanarHoles(extruded)
        
        solids.append(extruded)
        intersections = rs.IntersectBreps(extruded, pictureSurface)
        surfacesInPicturePlane.append(rs.AddPlanarSrf(intersections[0]))
        curvePointsInPP.append(convertRhinoPointToSimpleList(rs.CurvePoints(intersections[0]),pictureSurface))
    rs.DeleteObjects(solids)

    count = 0
    
    f = open('./data.pkl', 'wb')
    fsimple = open('./simple.txt', 'w')
    print 'picklethisobject:'
    print (zip(curvePointsInPP,distancesFromPP))
    pickle.dump(zip(curvePointsInPP,distancesFromPP),f ,-1)
    fsimple.write(str(zip(curvePointsInPP,distancesFromPP)))
    fsimple.close()
    f.close()
    
    
    for srf in surfacesInPicturePlane:
        layer = rs.AddLayer(str(count).zfill(2) )
        rs.ObjectLayer(srf,layer)
        rs.MoveObject(srf, rs.VectorScale(rs.VectorUnitize(viewDirection),-.2*count))
        count+=1
        

    

sceneCurves = rs.ObjectsByType(4)

closedPlanarCurves = []

count = 0

for c in sceneCurves:
    if rs.ObjectLayer(c) == 'non-printing':
        continue
    if not rs.IsCurveClosed(c):
        print 'found an open curve. this is probably unexpected. script will ignore it'
    else:
        if not rs.IsCurvePlanar(c):
            print 'found a non-planar cuve. this is probably unexpected. script will ignore it'
        else:
            closedPlanarCurves.append(c)
        


renderQueue = []
tree = makeTree(closedPlanarCurves)

currentView = rs.CurrentView()
viewPoint = rs.ViewCamera ( currentView)
viewTarget = rs.ViewTarget(currentView)
viewDirection = rs.VectorScale(rs.VectorCreate(viewTarget, viewPoint),10)
viewUpVector = rs.ViewCameraUp(currentView)
picturePlane = rs.PlaneFromNormal(viewPoint, viewDirection)

traverseTree(tree, viewPoint)

render(renderQueue, picturePlane,viewPoint,viewDirection)
#print tree
