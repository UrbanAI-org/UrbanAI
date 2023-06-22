import React, { useEffect, useRef } from 'react';
import "./LandscapeScene.css";
function DrawableMap() {
    const mapRef = useRef(null);
    const coordinatesRef = useRef(null);
    let map;
    // useEffect(() => {
    //     if (mapRef.current != null) {
    //         initMap();
    //     }
    //   }, []);
    window.initMap = initMap
    
    function initMap() {
        console.log("LOAD MAP")
        map = new window.google.maps.Map(mapRef.current, {
            center: { lat: -33.917, lng: 151.230 },
            zoom: 15,
          });
        var rectangle;
        var markers = [];
        var bounds = new window.google.maps.LatLngBounds();
        var coordinatesDiv = document.getElementById('coordinates');
        map.addListener('mousemove', function(event) {
            coordinatesDiv.textContent = 'Latitude: ' + event.latLng.lat().toFixed(6) + ', Longitude: ' + event.latLng.lng().toFixed(6);
        });
        map.addListener('click', function(event) {
            if (markers.length >= 2) {
              // Remove previous markers and rectangle
                markers.forEach(function(marker) {
                    marker.setMap(null);
              });
              markers = [];
              if (rectangle) {
                rectangle.setMap(null);
              }
              bounds = new window.google.maps.LatLngBounds();
            }
            var marker = new window.google.maps.Marker({
              position: event.latLng,
              map: map,
              draggable: true
            });
            markers.push(marker);
            bounds.extend(event.latLng);
            if (markers.length === 2) {
                var ne = bounds.getNorthEast();
                var sw = bounds.getSouthWest();
                var lngDiff = ne.lng() - sw.lng();
                var latDiff = ne.lat() - sw.lat();
                if (lngDiff > 0.5 || latDiff > 0.5) {
                  alert('Rectangle exceeds the maximum length limit of 0.5');
                } else {
                    rectangle = new window.google.maps.Rectangle({
                        bounds: bounds,
                        editable: true,
                        draggable: true,
                        map: map
                    });
                }
              
                markers.forEach(function(marker) {
                    marker.setMap(null);
                });
            }
        });
        rectangle.setMap(map);
        // listen to changes
        ["bounds_changed", "dragstart", "drag", "dragend"].forEach((eventName) => {
            rectangle.addListener(eventName, () => {
            console.log({ bounds: rectangle.getBounds(), eventName });
            });
        });
    }


    return (
        
        <div className="landscape-scene">
            <script
                src={`https://maps.googleapis.com/maps/api/js?key=AIzaSyAW4Q2lrdkVvpHEwEplkAYXbNLc5SG9SlQ&callback=initMap`}
                // src={`https://maps.googleapis.com/maps/api/js?key=KEY_KEY_KEY&callback=initMap`}
                async
            ></script>
            <div ref={mapRef} id="map"> </div>
            <div ref={coordinatesRef}></div>
            
        </div>
    );
}
export default DrawableMap;