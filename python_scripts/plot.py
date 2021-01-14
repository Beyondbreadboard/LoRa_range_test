import gmplot
from csv import reader
import haversine as hs

'''
alert('Lat: ' + event.latLng.lat() + ' Lng: ' + event.latLng.lng()); // JS for adding latlon on click
'''
def map_values(rssi):
    old_max=-48
    old_min=-110
    new_max=10
    new_min = 0
    new_val = ((rssi - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min
    return new_val
    #return ((rssi*30/110))

    
apikey = "AIzaSyAv9ZSZ4O9nIlAyV8i95uabV5eEFc6dfBo" # (your API key here)
map_styles= [
 {
  "featureType": "all",
  "elementType": "labels",
  "stylers": [
      { "visibility": "off" }
    ]

}
]
gateway_loc =(17.0705735,79.26204)
weight= []
gps_scooter = []
gps_lora = []
gps_scooter = []

gmap = gmplot.GoogleMapPlotter(gateway_loc[0],gateway_loc[1], 16,map_type = "roadmap",map_styles= map_styles,apikey=apikey)

with open('lora_nlg13-01-2021.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    header = next(csv_reader)
    # Check file as empty
    if header != None:
        # Iterate over each row after the header in the csv
        for row in csv_reader:
            gps_lora.append([float(row[0]),float(row[1])])# row variable is a list that represents a row in csv
            weight.append(map_values(float(row[5])))


#print(gps_lora)

attractions = zip(*gps_lora)
gmap.scatter(
    *attractions,
    s=7,
    marker = False,
    color="red"
)
attractions = zip(*gps_lora)
gmap.heatmap(
    *attractions,
    radius=30,
    dissipating =True,
    weights=weight,
    gradient=[(255, 0, 0, 0), (100, 100, 0, 0.9), (0, 255, 0, 1)]
)
with open('lora_nlg_from_phone13-01-2021_copy.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    header = next(csv_reader)
    # Check file as empty
    if header != None:
        # Iterate over each row after the header in the csv
        for row in csv_reader:
            gps_scooter.append([float(row[0]),float(row[1])])# row variable is a list that represents a row in csv
            

path = zip(*gps_scooter)
gmap.enable_marker_dropping('orange', draggable=True)
gmap.marker(17.0705735,79.26204,title='LoRaWAN_Gateway_865-867',precision=6, label='LoRaWAN_Gateway_865-867',color='black')
gmap.plot(*path, edge_width=4, color='blue')

print(hs.haversine(gateway_loc,gps_lora[100]))
#print(weight)



gmap.draw('map.html')
