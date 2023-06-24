import React, {useEffect} from "react";
import NavBar from "../components/NavBar";
import '../components/styles/UserGuide.css'
const UserGuide = () => {
    useEffect(() => {
        document.title = "UNSW VIP Project - Urban Topological Visulisation Tool"
      }, []);

    return (
        <div>
            <NavBar />
        <div className="UserGuide">

            {/* <nav className="user-guide-nav">
            <ul>
                <li><a href="#current-capabilities">Current capabilities</a></li>
                <li><a href="#getting-started">Getting Started</a></li>
                <li><a href="#polygon-mesh-type">Polygon Mesh Type</a></li>
                <li><a href="#circle-mesh-type">Centre Point Square Mesh Type</a></li>
                <li><a href="#viewing-the-mesh">Using the App</a></li>
                <li><a href="#faq">FAQ</a></li>
            </ul>
            </nav> */}
            
            <br></br><br></br>
            <div className="user-guide-content">
            <h1>User Guide & FAQ</h1>

            <details>
                <summary>Current Restrictions</summary>
                <section id="current-capabilities">
                    <h3>Current capabilities of the mesh generator</h3>
                    <ul>
                        {/* <li>The mesh generation area only support </li> */}
                        <li>The generated area should not greater than 11km * 11km</li>
                        <li>The input maximum and minimum longitude (or latitude) difference should not greater than 0.12</li>
                        <li>The input latitude should be less than -32 and greater than -35</li>
                        <li>The input longitude should be less than 152 and greater than 148</li>
                    </ul>
                </section>
            </details>

            <details>
                <summary>Getting Started</summary>
                <section id="getting-started">
                    <h3>There are three ways to generate meshes on the Home page:</h3>
                    <ul> 
                        <li>Polygon shape</li>
                        <ol> 
                            <li>User can entering the mesh's corner coordinates (latitude and longitude) at input box</li>
                            <li>User must input at least 2 pairs of latitude and longitude</li>
                            <li>The generated grid area will be enclosed by the largest longitude and latitude and the smallest longitude and latitude</li>
                        </ol>
                        <li>Circle</li>
                        <ol>
                            <li>User needs to enter centre Point Square shape and the radius of the shape</li>
                        </ol>
                        <li>Select from Map</li>
                        <ol>
                            <li>Click on the map to select the coordinates</li>
                            <li>Click on the "Generate" button to generate the mesh</li>
                        </ol>
                    </ul>
                    <b><p>*Please enter the longitude and latitude coordinate as decimals!</p></b>
                    <b><p>*You can download the generated mesh as a ply file.</p></b>
                </section>
            </details>

            <details>
                <summary>Polygon Mesh Type</summary>
                <section id="polygon-mesh-type">
                    <h3>Selecting the Polygon Mesh Type</h3>
                    <ul>
                        <li>The polygon mesh type allows you to enter multiple coordinates, of (latitude, longitude).</li>
                        <li>Please enter and add at least three pairs of coordinates such that it will form a triangle.</li>
                        <li>The mesh generated will have each of these coordinates as their corners.</li>
                    </ul>
                </section>
            </details>

            <details>
                <summary>Centre Point Square Mesh Type</summary>
                <section id="circle-mesh-type">
                    <h3>Selecting the Centre Point Square Mesh Type</h3>
                    <ul>
                        <li>The Centre Point Square mesh type will take the centre coordinate of the mesh.</li>
                        <li>Please specify a radius in which would generate around the centre coordinate, which forms a square.</li>
                    </ul>
                </section>
            </details>

            <details>
                <summary>Map Mesh Type</summary>
                <section id="map-mash-type">
                   <h3>Selecting the mesh coordinates from map</h3>
                   <ul>
                        <li>The map mesh type allows you to select the coordinates from the map.</li>
                        <li>Click on the map to select the coordinates.</li>
                        <li>And you will find the exactly longitude and latitude for the position of your mouse.</li>
                   </ul>
                </section>
            </details>

            <details>
                <summary>Tips of view the generated mesh</summary>
                <section id="viewing-the-mesh">
                    <h3>Here are some tips for viewing the mesh and using the slider:</h3>
                    <ul>
                        <li>Make sure the coordinates you entered are correct</li>
                        <li>Rotate the mesh by either using the slider(at the top right corner) or by dragging</li>
                        <li>Move the mesh by holding down control (windows) or command (macbook) buttons</li>
                        <li>Zoom in and out by scrolling up and down</li>
                        <li>Change the wireless or not by choosing the type at the top right</li>
                    </ul>
                </section>
            </details>

            <details>
                <summary>Frequently Asked Questions</summary>
                <section id="faq">
                    <h3>What if I found a bug?</h3>
                    <p>If you found a bug, please report it by clicking on the bug button on the top right corner.</p>
                    <h3>How do I contact support?</h3>
                    <p>You can contact support by clicking on the bug button and by submitting a query.</p>
                </section>
            </details>
            </div>

            </div>
        </div>
        );
    }

export default UserGuide;