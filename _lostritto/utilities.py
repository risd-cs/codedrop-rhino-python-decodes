import rhinoscriptsyntax as rs
import math

def sameLine (line1, line2):
    start1, end1, start2, end2 = rs.CurveStartPoint(line1), rs.CurveEndPoint(line1), rs.CurveStartPoint(line2), rs.CurveEndPoint(line2)
    d1 = math.sqrt((start1[0]-start2[0])**2+(start1[1]-start2[1])**2)
    d2 = math.sqrt((end1[0]-end2[0])**2+(end1[1]-end2[1])**2)
    d3 = math.sqrt((start1[0]-end2[0])**2+(start1[1]-end2[1])**2)
    d4 = math.sqrt((end1[0]-start2[0])**2+(end1[1]-start2[1])**2)
    print (d1,d2,d3,d4)
    if (d1<.1 and d2<.1) or (d3<.1 and d4<.1):
        return True
    return False
    
def arePolysTouching(poly1, poly2):
    if poly1 == None or poly2==None:
        return False
    intersections = rs.CurveCurveIntersection(poly1, poly2)
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
                print 'found a same'
                dup = True
                segments2.remove(seg2)
                break
        if not dup:
            nonOverlappingSegs.append(seg)

    result = rs.JoinCurves(nonOverlappingSegs+segments2)
    rs.DeleteObjects(segments1)
    rs.DeleteObjects(segments2)
    return result

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
        


a = [1,2,2,3,[4,5,6],[],7,[9,8],0,0]
print cleanList(a)