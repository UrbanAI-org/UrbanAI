import React from "react";
import NavBar from "../components/NavBar";
import '../components/styles/UserGuide.css'
const UserGuide = () => {

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

            <div className="user-guide-content">

            <section id="current-capabilities">
                <h2>Current capabilities of the mesh generator</h2>
                <h3>The latitude values can only take in between <u>-33 to -34</u></h3>
                <h3>The longitude values can only take in between <u>151 to 152</u></h3>
            </section>


            <section id="getting-started">
                <h2>Getting Started</h2>
                <p>There are two ways to generate meshes on the Home page:</p>
                <ul>
                    <li>Polygon shape - by entering the mesh's corner coordinates, </li>
                    <li>Centre Point Square shape- enter the mesh's centre coordinate and a given radius</li>
                </ul>
                <p>Please enter the longitude and latitude coordinate as decimals!</p>
                <p>You can download the generated mesh as a ply file.</p>
            </section>

            <section id="polygon-mesh-type">
                <h2>Selecting the Polygon Mesh Type</h2>
                <p>The polygon mesh type allows you to enter multiple coordinates, of (latitude, longitude).</p>
                <p>Please enter and add at least three pairs of coordinates such that it will form a triangle.</p>
                <p>The mesh generated will have each of these coordinates as their corners.</p>
            </section>

            <section id="circle-mesh-type">
                <h2>Selecting the Centre Point Square Mesh Type</h2>
                <p>The Centre Point Square mesh type will take the centre coordinate of the mesh.</p>
                <p>Please specify a radius in which would generate around the centre coordinate, which forms a square.</p>
            </section>

            <section id="viewing-the-mesh">
                <h2>Viewing the Mesh</h2>
                <p>Here are some tips for viewing the mesh and using the slider:</p>
                <ul>
                <li>Make sure the coordinates you entered are correct</li>
                <li>Rotate the mesh by either using the slider or by dragging</li>
                <li>Move the mesh by holding down control (windows) or command (macbook) buttons</li>
                </ul>
            </section>

            <section id="faq">
                <h2>FAQ</h2>
                <h3>What if I found a bug?</h3>
                <p>If you found a bug, please report it by clicking on the bug button on the top right corner.</p>
                <h3>How do I contact support?</h3>
                <p>You can contact support by clicking on the bug button and by submitting a query.</p>
            </section>
            </div>

            </div>
        </div>
        );
    }

export default UserGuide;