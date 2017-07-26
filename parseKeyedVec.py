import dbConn as db
#from lib.VectorizePlace import VectorizePlace
import codecs
import re
import numpy as np
import time
import datetime


def getCorpusPlace(cpidx, order, limit) :

    if (cpidx == None) :
        cpidxQuery = " OwnerCpIdx IS NULL "
    else :
        cpidxQuery = " OwnerCpIdx = "+ cpidx

    if (limit == None) :
        count = ""
    else :
        count = " LIMIT 0,"+str(limit)

    query  = 'SELECT p.idx, '
    query += '       p.Title '
    query += 'FROM place_info p '
    query += ' JOIN '
    query += '    (SELECT * '
    query += '     FROM place_rank '
    query += '     WHERE '+cpidxQuery+')'
    query += '     r ON p.idx=r.placeIdx '
    query += 'WHERE p.IsOpen=1'
    query += '    AND p.IsDelete=0 '
    query += '    AND p.Lat IS NOT NULL '
    query += '    AND p.Lng IS NOT NULL '
    query += '    AND p.Lat <> "" '
    query += '    AND p.Lng <> "" '
    query += '    AND p.LanguageCode = "ko" '
    query += '    AND NOT p.Lat LIKE "%,%" '
    query += '    AND NOT p.Lng LIKE "%,%" '
    query += 'ORDER BY ' + str(order)
    query += ''+ str(count)

    dbResult = db.getQuery(_query=query)
    return np.array(dbResult)


def getCorpusPlaceCategory(cpidx, categoryidx, order, limit) :

    if (cpidx == None) :
        cpidxQuery = " OwnerCpIdx IS NULL "
    else :
        cpidxQuery = " OwnerCpIdx = "+ cpidx

    if (limit == None) :
        count = ""
    else :
        count = " LIMIT 0,"+str(limit)

    query  = 'SELECT p.idx, '
    query += '       p.Title, '
    query += '       CONCAT("c", p.Category) AS category '
    query += 'FROM place_info p '
    query += 'WHERE p.IsOpen=1'
    query += '    AND p.IsDelete=0 '
    query += '    AND p.Lat IS NOT NULL '
    query += '    AND p.Lng IS NOT NULL '
    query += '    AND p.Lat <> "" '
    query += '    AND p.Lng <> "" '
    query += '    AND p.LanguageCode = "ko" '    
    query += '    AND NOT p.Lat LIKE "%,%" '
    query += '    AND NOT p.Lng LIKE "%,%" '
    query += '    AND p.Category = ' + str(categoryidx) + ' '
    query += 'ORDER BY ' + str(order)
    query += ''+ str(count)

    dbResult = db.getQuery(_query=query)
    return np.array(dbResult)

def getCorpusPlacePlan(limit) :

    if (limit == None) :
        count = ""
    else :
        count = " LIMIT 0,"+str(limit)

    query  = 'SELECT p.Title '
    query += '  FROM plan_info_day d '
    query += '  JOIN place_info p ON d.PlaceIdx = p.idx '
    query += '  WHERE d.IsDelete = 0 '
    query += '    AND d.PlaceIdx <> 0 '
    query += '    AND d.PlaceIdx <> "" '        
    query += '  ORDER BY d.PlanCode, d.DayNum '
    query += ''+ str(count)

    dbResult = db.getQuery(_query=query)
    return np.array(dbResult)


def printToFile (cpid, limit) :
    # Parse place list
    tmp = ["Lat ASC", "Lng ASC", "Rate DESC", "TotalPoints DESC"]
    tmp2 = [getCorpusPlace(cpidx=cpid, order=a, limit=limit).transpose()[1] for a in tmp]
    placeList = np.concatenate(tmp2, axis=0)

    print ("place loaded")
    # Parse categoried place list
    tmp = [getCorpusPlaceCategory(cpidx=None, categoryidx=i, order="Lat ASC", limit=limit) for i in range(1,10)]
    tmp2 = np.concatenate(tmp, axis=0).transpose()
    placeCategoryListLat = np.array([tmp2[1],tmp2[2]]).transpose()
    tmp = [getCorpusPlaceCategory(cpidx=None, categoryidx=i, order="Lng ASC", limit=limit) for i in range(1,10)]
    tmp2 = np.concatenate(tmp, axis=0).transpose()
    placeCategoryListLng = np.array([tmp2[1],tmp2[2]]).transpose()
    placeCategoryList = np.concatenate([placeCategoryListLat, placeCategoryListLng], axis=0).flatten()
    placeList = np.concatenate([placeList, placeCategoryList], axis=0)

    print ("placeCategory loaded")

    # make plan's place list corpus
    placePlanList = np.concatenate(getCorpusPlacePlan(limit), axis=0)
    placeList = np.concatenate([placeList, placePlanList], axis=0)

    print ("placePlan loaded")
    
    # make this part to 2 dimention array
    placeListLen = len(placeList)
    shapesize = 10
    placeList = placeList[0:(placeListLen-(placeListLen%shapesize))]
    placeList.shape = (int(placeListLen/shapesize), shapesize)
    placeList = placeList.tolist()

    # print(placeList)
    print("training data word count : ", len(placeList)*shapesize)
    np.save(file="tmp1", arr=placeList)


printToFile(None, None)
