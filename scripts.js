/*let map;

      async function initMap() {
        // Load the library using importLibrary
        const { Map } = await google.maps.importLibrary("maps");

        map = new Map(document.getElementById("map"), {
          center: { lat: -34.397, lng: 150.644 },
          zoom: 8,
        });
      }

      // Load the Maps API script
      (async () => {
        const script = document.createElement("script");
        script.src = "https://maps.googleapis.com/maps/api/js?key=/////&v=weekly";
        script.async = true;
        script.defer = true;
        script.onload = initMap; // Initialize the map after script loads
        document.head.appendChild(script);
      })();*/
let map;

function initMap() {
  // Initialize the map
  const {Map} =  google.maps.importLibrary("maps");
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 37.7749, lng: -122.4194 }, // San Francisco
    zoom: 14,
  });

  // Create a PlacesService instance
  const service = new google.maps.places.PlacesService(map);

  // Define search parameters
  const request = {
    location: { lat: 37.7749, lng: -122.4194 },
    radius: 2000, // 2 km radius
    type: "park", // Search for parks
  };

  // Perform a nearby search
  service.nearbySearch(request, (results, status) => {
    if (status === google.maps.places.PlacesServiceStatus.OK) {
      results.forEach((place) => {
        console.log(`Place: ${place.name}, Address: ${place.vicinity}`);

        // Add markers to the map
        new google.maps.Marker({
          position: place.geometry.location,
          map: map,
          title: place.name,
        });
      });
    }
  });
}

window.onload = initMap;