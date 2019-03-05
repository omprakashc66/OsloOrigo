# Author: Om Prakash Chapagain
# Date: 05.03.2019
# Python version: 3.6.6
# IDE: Visual Studio Code

# import necessary libraries/modules
import json
import requests

# request url header (converted from curl)
header = {
    'Client-Identifier': 'YourClientIdentifierKey', 
    # Please change the 'YourClientIdentifierKey' with the the identifier key of your own
}

# api endpoint (url)
apiEndPoint = "https://oslobysykkel.no/api/v1/"

# retrieve data (response in json format)
stationInOperationResponse = requests.get(apiEndPoint + 'stations', headers=header)
stationAvilabilityResponse = requests.get(apiEndPoint + 'stations/availability', headers=header)

# get the status_code of the request
isSIOR_valid = stationInOperationResponse.status_code
isSAR_valid = stationAvilabilityResponse.status_code

# Proceed if the response is successful
if isSIOR_valid == 200 & isSAR_valid == 200: # 200 = all ok

    # convert the json object to a python object (dictionary)
    stationInOperationData = stationInOperationResponse.json()
    stationAvilableData = stationAvilabilityResponse.json()

    # number of data points
    nso = len(stationInOperationData['stations']) # number of stations in operation
    nsa = len(stationAvilableData['stations']) # number of available stations

    # print all the stations in opetation if the get request is valid
    print('Station title \t\t\t Number of locks') # print the header for the table of data
    for i in range(nso):
        stationInOp = stationInOperationData['stations'][i] # retrieve info about the station in operation
        print('%25s \t %d' %(stationInOp['title'], stationInOp['number_of_locks']))

    # print available station detail if the get request is valid
    for i in range(nsa):
        stationAvil = stationAvilableData['stations'][i] # retrieve info about an available station
        
        # A querry to get the name of the station based on the station id
        stationNames = [stationInOperationData['stations'][j]['title'] \
            for j in range(nso) if stationInOperationData['stations'][j]['id'] == stationAvil['id']]
        
        # Print station name and info if the station with ID is present in the list of station in operation
        if len(stationNames) > 0:
            print('Station: %25s \t available bikes: %d \t available locks: %d' \
            %(stationNames[0], stationAvil['availability']['bikes'], stationAvil['availability']['locks']))
        else: # otherwise, print station ID and info
            print('Station: %25d \t available bikes: %d \t available locks: %d' \
            %(stationAvil['id'], stationAvil['availability']['bikes'], stationAvil['availability']['locks']))
else:
    print("Invalid request. Check the api endpoint url and/or client identifier key")