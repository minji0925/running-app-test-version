import json, requests
from flask import Flask, jsonify, request, render_template
import googlemaps
import random

app = Flask(__name__)

# Initialize the Google Maps client
gmaps = googlemaps.Client(key="")

'''@app.route('/location', methods=['POST'])
def get_places():
    data = request.get_json(force=True, silent=True)
    lat = data.get('lat')
    lng = data.get('lng')

    if lat is None or lng is None:
        return jsonify({'error': 'Latitude and Longitude are required'}), 400

    print(f"Received location: Latitude={lat}, Longitude={lng}")
    # Fetch query parameters
    #lat = float(request.args.get('lat', 37.7749))
    #lng = float(request.args.get('lng', -122.4194))
    #radius = int(request.args.get('radius', 2000))

    # Search for parks
    places = gmaps.places_nearby(
        location=(lat, lng),
        radius = 2000,
        #radius=radius,
        type="park"
    )

    # Return places as JSON
    return jsonify(places["results"])
    #return jsonify({'message': 'Location received', 'lat': lat, 'lng': lng})

@app.route('/')
def index():
   return render_template('index.html')
'''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['search']
    #results = gmaps.places(query = search_query)
    place = gmaps.geocode(search_query) #language='ko'
    print(place)
    print('\n\n\n')
    place_lat = place[0]['geometry']['location']['lat']
    place_lng = place[0]['geometry']['location']['lng']

    weather_url = 'https://api.openweathermap.org/data/2.5/weather?lat={place_lat}&lon={place_lng}&APPID={1840e8b185e853cff41a492988daafc4}'
    weather_data = requests.get(weather_url).json()

    print(weather_data)
    print('\n\n\n')
    '''places = [
                {
                    'name': place.get('name'),
                    'address': place.get('formatted_address'),
                }
                for place in results.get('results', [])
            ]
'''
    search_types = ["park", "trail", "hiking", "tourist_attraction"]
    keyword_types = ["running path", "scenic view"]

    combined_results = []

    for place_type in search_types:
        places1 = gmaps.places_nearby(
            location=(place_lat, place_lng),
            radius=2000,
            type=place_type
        )
        combined_results.extend(places1.get('results', []))

    for place_keyword in keyword_types:
        places2 = gmaps.places_nearby(
            location=(place_lat, place_lng),
            radius=2000,
            keyword=place_keyword
        )
        combined_results.extend(places2.get('results', []))


    '''places_park = gmaps.places_nearby(
        location=(place_lat, place_lng),
        radius = 2000,
        type="point_of_interest"
    )'''

    places = [
                {
                    'name': p.get('name'),
                    'address': p.get('vicinity'),
                    'lat': p['geometry']['location']['lat'],
                    'lng': p['geometry']['location']['lng'],
                    'place_id': p['place_id']
                }
                for p in combined_results#.get('results', [])
            ]
    
    print(places)
            
    directions = []
    random_waypoints = []

    for i in range(0,10):
        if len(places) > 3:
            random_samples = random.sample(places, 3)
            random_waypoints = ['place_id:' + p['place_id'] for p in random_samples]
        else:
            # Use all places if there are fewer than 3
            random_samples = places
            random_waypoints = ['place_id:' + p['place_id'] for p in random_samples]

        '''for waypoint in random_waypoints:
            print(f"Waypoint: {waypoint}")'''

        directions.append(gmaps.directions(
            origin='place_id:' + place[0]['place_id'],
            destination='place_id:' + place[0]['place_id'],
            waypoints=random_waypoints,  # Add POIs as waypoints
            mode="walking",  # Or "bicycling" for faster routes
            optimize_waypoints=True
        ))

    #print(directions[0])
    #print(random_waypoints)

    response = gmaps.directions(
        origin='place_id:ChIJA_ClgTSkfDURMVF9TcMKCOg',
        destination='place_id:ChIJEaGUTSKkfDURrXN-knNmA2Y',
        waypoints=['place_id:ChIJK_b0UX2jfDURmkYPvmWYm90'],
        mode="walking",
        optimize_waypoints=True
    )
    print(response)

    print('\n\nhello world')


    try:
        response = gmaps.directions(
            origin='37.49391831970851,127.0625864197085',
            destination='37.4952673,127.0639354',
            mode="walking",
            optimize_waypoints=True
        )
        print(response)
    except Exception as e:
        print(f"Error: {e}")

    print('\n\nabc')
    place_details = gmaps.place(place_id='ChIJNaoEOCukfDURd3wWss7E6xo')
    place_details2 = gmaps.place(place_id='ChIJEaGUTSKkfDURrXN-knNmA2Y')
    print(place_details)
    print(place_details2)

    #print(places)
    return render_template('results.html', places=places, query=search_query, lat=place_lat, lng=place_lng)

if __name__ == '__main__':
    app.run(debug=True)


