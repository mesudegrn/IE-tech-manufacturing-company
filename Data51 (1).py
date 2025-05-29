# Write your group number here: Case Study 2 - 51 #

numComp = 5
numPlant = 3
numPeriod = 2
components = ["Aluminum", "CarbonFiber", "Manual", "Control", "Sensor"]
plants = ["Istanbul", "Ankara", "Izmir"]
periods = [1, 2]

laborData = [[1, 1.5, 1.5, 3, 4], [3.5, 3.5, 4.5, 4.5, 5], [3, 3.5, 4, 4.5, 5.5]]
labor = {}
for i in range(numComp):
    for k in range(numPlant):
        labor[(components[i], plants[k])] = laborData[k][i]

laborAvailability = [12000, 15000, 22000]
laborAv={}
for k in range(numPlant):
    laborAv[(plants[k])] = laborAvailability[k]
packingData = [[4, 4, 5, 6, 6], [7, 7, 8, 9, 7], [7.5, 7.5, 8.5, 8.5, 8]]
packing={}
for i in range(numComp):
    for k in range(numPlant):
        packing[(components[i], plants[k])] = packingData[k][i]
packingAvailability = [20000, 40000, 35000]
packingAv={}
for k in range(numPlant):
    packingAv[(plants[k])] = packingAvailability[k]
assemblyData = [65, 60, 65]
assembly={}
for k in range(numPlant):
    assembly[(plants[k])] = assemblyData[k]
assemblyAvailability = [5500, 5000, 6000]
assemblyAv={}
for k in range(numPlant):
    assemblyAv[(plants[k])] = assemblyAvailability[k]
minDemandComponents = [[0, 100, 200, 30, 100], [0, 100, 200, 30, 100], [0, 50, 100, 15, 100]]
minDemands={}
for i in range(numComp):
    for k in range(numPlant):
        minDemands[(components[i], plants[k])] = minDemandComponents[k][i]
maxDemandComponents = [[2000, 2000, 2000, 2000, 2000], [2000, 2000, 2000, 2000, 2000], [2000, 2000, 2000, 2000, 2000]]
maxDemands={}
for i in range(numComp):
    for k in range(numPlant):
        maxDemands[(components[i], plants[k])] = maxDemandComponents[k][i]
minDemandRoboticKit = [0, 0, 0]
minDemandsRobo={}
for k in range(numPlant):
    minDemandsRobo[(plants[k])] = minDemandRoboticKit[k]
maxDemandRoboticKit = [200, 200, 200]
maxDemandsRobo={}
for k in range(numPlant):
    maxDemandsRobo[(plants[k])] = maxDemandRoboticKit[k]
productionCostComponents = [[6, 19, 4, 10, 26], [5, 18, 5, 11, 24], [7, 20, 5, 12, 27],]
prodComps={}
for i in range(numComp):
    for k in range(numPlant):
        prodComps[(components[i], plants[k])] = productionCostComponents[k][i]
productionCostRoboticKits = [178, 175, 180]
prodRobo={}
for k in range(numPlant):
    prodRobo[(plants[k])] = productionCostRoboticKits[k]
sellingPriceComponents = [[10, 25, 8, 18, 40], [10, 25, 8, 18, 40], [12, 30, 10, 22, 45]]
priceComps={}
for i in range(numComp):
    for k in range(numPlant):
        priceComps[(components[i], plants[k])] = sellingPriceComponents[k][i]
sellingPriceRoboticKits = [290, 290, 310]
priceRobo={}
for k in range(numPlant):
    priceRobo[(plants[k])] = sellingPriceRoboticKits[k]
req = [13, 13, 10, 3, 3]
reqs={}
for i in range(numComp):
    reqs[(components[i])] = req[i]

