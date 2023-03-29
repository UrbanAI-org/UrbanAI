import React from "react";
import NavBar from "../components/NavBar";
import '../App.css';

import LandscapeScene from "../components/LandscapeScene";
import UserControl from "../components/UserControl";

const Home = () => {
    return (
        <div className="home">
            <NavBar />
            <div className="landscape-container">
                <UserControl />
                <LandscapeScene />
            </div>
        </div>
    )
}

export default Home;