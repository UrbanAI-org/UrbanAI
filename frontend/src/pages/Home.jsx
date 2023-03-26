import React from "react";
import NavBar from "../components/NavBar";
import '../App.css';

import LandscapeScene from "../components/LandscapeScene";
const Home = () => {
    return (
        <div className="home">
            <NavBar />
            <div className="landscape-container">
                <LandscapeScene />
            </div>
        </div>
    )
}

export default Home;