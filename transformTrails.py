import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)
import numpy as np
import sys

if __name__ == '__main__':
    df = pd.read_csv("alltrails.csv")
    # print (df["_geoloc"])
    featureSet = {}
    activitySet = {}
    updatedLines = []

    rowCount = 0
    for i, data in df.iterrows():
        if rowCount == 0 or rowCount == 1 or rowCount == 2:
            rowCount +=1
            continue
        features = data["features"]
        features = features.split(",")
        activities = data["activities"]
        activities = activities.split(",")

        for feature in features:
            feature = feature.strip(" ,\'\"[]")
            if feature == '':
                continue
            if feature in featureSet:
                featureSet[feature] += 1
            else:
                featureSet[feature] = 1
        
        for activity in activities:
            activity = activity.strip(" ,\'\"[]")
            if feature == '':
                continue
            if activity in activitySet:
                activitySet[activity] += 1
            else:
                activitySet[activity] = 1
    
    binnedDf = pd.read_csv("trails_binned6_with_visitors.csv")
    rowCount = 0
    visitorSet = {}
    for i, data in binnedDf.iterrows():
        if i == 0:
            continue
        visitors = data["visitors"]
        if data["area_name"] in visitorSet:
            continue
        else:
            visitorSet[data["area_name"]] = visitors
    visitorSet['Clayton Co International Park, Jonesboro GA'] = 100000
    visitorSet['Fort Hunt National Park'] = 100000
    visitorSet['Wolf Trap National Park for the Performing Arts'] = 100000

    # print(visitorSet)


    # first 3 lines
    header = []
    restrictions = []
    fileReader = open("alltrails.csv", 'r')
    firstLine = fileReader.readline().strip("\n")
    firstLine = firstLine.split(",")
    secondLine = fileReader.readline().strip("\n")
    secondLine = secondLine.split(",")
    for idx, var in enumerate(firstLine):
        if var == "_geoloc":
            header.append("latitude")
            header.append("longitude")
            restrictions.append("0")
            restrictions.append("0")
            continue
        if var == "features":
            for count, val in enumerate(featureSet):
                header.append(val)
                restrictions.append("2")
            continue
        if var == "activities":
            for count, val in enumerate(activitySet):
                header.append(val)
                restrictions.append("2")
            continue
        header.append(var)
        restrictions.append("-1")
    header.append("visitors")
    restrictions.append("0")
    # print(len(restrictions))
    updatedLines.append(header)
    updatedLines.append(restrictions)
    thirdLine = fileReader.readline().strip("\n")
    updatedLines.append(thirdLine)

    rowCount = 0
    for i, data in df.iterrows():
        if rowCount == 0 or rowCount == 1 or rowCount == 2:
            rowCount +=1
            continue
        newLine = []
        newLine.append(data["trail_id"])
        name = data["name"].replace(',', '')
        newLine.append(name)
        newLine.append(data["area_name"])
        newLine.append(data["city_name"])
        newLine.append(data["state_name"])
        newLine.append(data["country_name"])
        # geoloc
        geoloc = data["_geoloc"].split(",")
        lat = geoloc[0]
        lon = geoloc[1]
        lat = lat.strip(" ,\'\"[]{}lat:")
        lon = lon.strip(" ,\'\"[]{}lng:")
        newLine.append(lat)
        newLine.append(lon)

        # newLine.append(data["popularity"])
        popularity = float(data["popularity"])
        if(popularity < 4.231):
            popBin = "unpopular"
        if(popularity >= 4.231 and popularity < 8.462):
            popBin = "less popular"
        if(popularity >= 8.462 and popularity < 12.693):
            popBin = "mid popular"
        if(popularity >= 12.693 and popularity < 16.925):
            popBin = "more popular"
        if(popularity >= 16.925 and popularity < 25.387):
            popBin = "very popular"
        if(popularity >= 25.387):
            popBin = "extremely popular"
        newLine.append(popBin)

        newLine.append(data["length"])
        newLine.append(data["elevation_gain"])
        newLine.append(data["difficulty_rating"])
        newLine.append(data["route_type"])
        # if data["route_type"] != "out and back" and data["route_type"] != "loop" and data["route_type"] != "point to point":
        #     print(data["route_type"])
        newLine.append(data["visitor_usage"])
        newLine.append(data["avg_rating"])
        newLine.append(data["num_reviews"])
        # features
        features = data["features"]
        features = features.split(",")
        activities = data["activities"]
        activities = activities.split(",")
        for count, val in enumerate(featureSet):
            myFeatures = []
            for feature in features:
                feature = feature.strip(" ,\'\"[]")
                myFeatures.append(feature)
            if val in myFeatures:
                newLine.append(1)
            else:
                newLine.append(0)

        # activities
        for count, val in enumerate(activitySet):
            myActivities = []
            for activity in activities:
                activity = activity.strip(" ,\'\"[]")
                myActivities.append(activity)
            if val in myActivities:
                newLine.append(1)
            else:
                newLine.append(0)

        newLine.append(data["units"])

        # visitors
        newLine.append(visitorSet[data["area_name"]])
        updatedLines.append(newLine)
    # print(updatedLines)

    with open ('newTrails.csv', 'w') as f:
        for line in updatedLines:
            for var in line:
                f.write(str(var))
                f.write(',')
            f.write('\n')

