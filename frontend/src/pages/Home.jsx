import React, { useState, useEffect } from "react";
import NavBar from "../components/NavBar";
import '../App.css';

import LandscapeScene from "../components/LandscapeScene/LandscapeScene";
import UserControl from "../components/UserControl/UserControl";

const Home = () => {
    const [isRequestGenerated, setIsRequestGenerated] = useState(false);
    const [requestBody, setRequestBody] = useState(
        {
            type: "",
            data: {}
        }
    );
    const [responseBody, setResponseBody] = useState(null);

    const fetchMeshes = async () => {
        try {
          const response = await fetch("http://localhost:9999/v1/api/region/mesh", {
            method: 'POST',
            mode: "cors",
            headers: { 'Content-Type': 'text/plain' },
            body: JSON.stringify(requestBody)
          });

          if (!response.ok) {
            throw new Error(`Error has occurred: ${response.status}`);
          } else {
            response.json().then((values) => {
                console.log(values)
                setResponseBody({
                    download_link: values.download,
                    mesh: values.mesh
                });
            }).catch((error) => {
                console.log("Promise rejected");
            })
          }
        } catch(e) {
          console.log("Network error occurred");
        }
      };


    useEffect(() => {
        const fetchData = async () => {
          if (isRequestGenerated) {
            fetchMeshes()
          }
        };
        fetchData();
      }, [isRequestGenerated]);
    
    useEffect(() => {
      document.title = "UNSW VIP Project - Urban Topological Visulisation Tool"
    }, []);
    
    return (
        <div className="home">
            <NavBar />
            <div className="landscape-container">
                <UserControl
                    isRequestGenerated={isRequestGenerated}
                    setIsRequestGenerated={setIsRequestGenerated}
                    requestBody={requestBody}
                    setRequestBody={setRequestBody}
                    responseBody={responseBody}
                    setResponseBody={setResponseBody}
                />
                <LandscapeScene responseBody={responseBody}/>
            </div>
        </div>
    )
}

export default Home;