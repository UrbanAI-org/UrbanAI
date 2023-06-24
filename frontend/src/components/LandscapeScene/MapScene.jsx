import React, { useEffect, useRef, useState } from 'react';
import "./LandscapeScene.css";
import {reactLocalStorage} from 'reactjs-localstorage';

function DrawableMap({isMapJsLoaded, setMapJsLoaded}) {
    const boundsRef = useRef(null);
    const rectangleBoundsDivRef = useRef(null);
    let map;
    
    window.initMap = initMap
    var coordinatesDiv = document.getElementById('coordinates');
    rectangleBoundsDivRef.current = document.getElementById('rectangle_bounds');
    function displayBoxCoord(bounds, div) {
        if ( bounds != null && !bounds.isEmpty()) {
            div.style.display = 'block';
            div.innerHTML = 'North East corner: <br>' + 'Latitude: ' +  bounds.getNorthEast().lat().toFixed(6) + ', Longitude: ' + bounds.getNorthEast().lng().toFixed(6) + '<br>';
            div.innerHTML += 'South West corner: <br>' + 'Latitude: ' +  bounds.getSouthWest().lat().toFixed(6) + ', Longitude: ' + bounds.getSouthWest().lng().toFixed(6) + '<br>';
        } else {
            div.style.display = 'none';
        }
    }
    
    function initMap() {
        console.log("LOAD MAP")
        map = new window.google.maps.Map(document.getElementById("map"), {
            center: { lat: -33.917, lng: 151.230 },
            zoom: 15,
        });
        var rectangle;
        var markers = [];
        var bounds = new window.google.maps.LatLngBounds();
        var previousBounds = bounds; 
        map.addListener('mousemove', function(event) {
            coordinatesDiv.textContent = 'Latitude: ' + event.latLng.lat().toFixed(6) + ', Longitude: ' + event.latLng.lng().toFixed(6);
            // console.log(boundsRef.current)
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
              boundsRef.current = bounds
              displayBoxCoord(null, rectangleBoundsDivRef.current)
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
                console.log(ne,sw,lngDiff, latDiff)
                if (lngDiff > 0.12 || latDiff > 0.12) {
                  alert('Rectangle exceeds the maximum length limit of 0.12 arc');
                } else {
                    rectangle = new window.google.maps.Rectangle({
                        bounds: bounds,
                        editable: true,
                        draggable: true,
                        map: map
                    });
                    reactLocalStorage.setObject("PolygonItems", [
                        {latitude: ne.lat().toFixed(6), longitude: ne.lng().toFixed(6)},
                        {latitude: sw.lat().toFixed(6), longitude: sw.lng().toFixed(6)},
                    ])
                    previousBounds = rectangle.getBounds()
                    displayBoxCoord(rectangle.getBounds(), rectangleBoundsDivRef.current)
                    window.google.maps.event.addListener(rectangle, 'bounds_changed', function() {
                        var bounds = rectangle.getBounds()
                        var ne = bounds.getNorthEast();
                        var sw = bounds.getSouthWest();
                        var lngDiff = ne.lng() - sw.lng();
                        var latDiff = ne.lat() - sw.lat();
                        console.log(ne,sw,lngDiff, latDiff)
                        if (lngDiff > 0.12 || latDiff > 0.12) {
                            alert('Rectangle exceeds the maximum length limit of 0.12 arc');
                            rectangle.setBounds(previousBounds);
                        } else {
                            previousBounds = bounds
                            displayBoxCoord(rectangle.getBounds(), rectangleBoundsDivRef.current);
                            reactLocalStorage.setObject("PolygonItems", [
                                {latitude: bounds.getNorthEast().lat().toFixed(6), longitude: bounds.getNorthEast().lng().toFixed(6)},
                                {latitude: bounds.getSouthWest().lat().toFixed(6), longitude: bounds.getSouthWest().lng().toFixed(6)},
                            ])
                        }
                        
                      });
                
                }
              
                markers.forEach(function(marker) {
                    marker.setMap(null);
                });
                // rectangle.setMap(map);
            }
        });
        // listen to changes
        // ["bounds_changed", "dragstart", "drag", "dragend"].forEach((eventName) => {
        //     rectangle.addListener(eventName, () => {
        //     console.log({ bounds: rectangle.getBounds(), eventName });
        //     });
        // });
    }
    useEffect(() => {
        if (!isMapJsLoaded) {

            const script = document.createElement('script');
            script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAW4Q2lrdkVvpHEwEplkAYXbNLc5SG9SlQ&callback=initMap'; // Replace with your desired script URL
            script.async = true;
            console.log("LOAD GOOGLE MAP JS")
            document.body.appendChild(script);
            setMapJsLoaded(true)
            return () => {
                document.body.removeChild(script);
            };
        } else {
            console.log("Init Map")
            initMap()
        }
      }, []);
    
      return (
        <div className="landscape-scene">
            {/* Your application content */}
            <div id="map"> </div>
        </div>
      );
    
    // return (
        
    //     <div className="landscape-scene">
    //         <script
    //             src={`https://maps.googleapis.com/maps/api/js?key=AIzaSyAW4Q2lrdkVvpHEwEplkAYXbNLc5SG9SlQ&callback=initMap`}
    //             // src={`https://maps.googleapis.com/maps/api/js?key=KEY_KEY_KEY&callback=initMap`}
    //             async
    //         ></script>
    //         <div ref={mapRef} id="map"> </div>
    //         <div ref={coordinatesRef}></div>
            
    //     </div>
    // );
}
export default DrawableMap;