import React, { useState, useEffect } from "react";
import NavBar from "../components/NavBar";
import '../App.css';

import LandscapeScene from "../components/LandscapeScene/LandscapeScene";
import UserControl from "../components/UserControl/UserControl";
import Loading from "../components/LandscapeScene/Loading";
import DrawableMap from "../components/LandscapeScene/MapScene";
import uploardImage from "../components/Detection/uploardImage";
const Home = () => {
    const [isRequestGenerated, setIsRequestGenerated] = useState(false);
    const [requestBody, setRequestBody] = useState(
        {
            type: "",
            data: {}
        }
    );
    const [responseBody, setResponseBody] = useState(null);
    const [isWaitingResponse, setWaitingResponse] = useState(false);
    const [isLoading, setLoading] = useState(false);
    const [isDisplayingMap, setIsDisplayingMap] = useState(false)
    const [isMapJsLoaded, setMapJsLoaded] = useState(false)
    const [isPredict, setIsPredict] = useState(false);
    // const []
    const fetchMeshes = async () => {
        try {
            // setLoading(true)
            console.log(requestBody)
            setWaitingResponse(true)

            const response = await fetch("http://13.210.146.135:5000/v1/api/region/mesh", {
            // const response = await fetch("http://127.0.0.1:9999/v1/api/region/mesh", {
            method: 'POST',
            mode: "cors",
            headers: { 'Content-Type': 'text/plain' },
            body: JSON.stringify(requestBody)
          });
          
          if (!response.ok) {
            response.json().then((values) => {
              alert(values.message)
            setIsDisplayingMap(true)

            })
            setWaitingResponse(false)
            setLoading(false)
            throw new Error(`Error has occurred: ${response.status}`);
            // setIsRequestGenerated(false)
          } else {
            setWaitingResponse(false)
            setLoading(true)
            response.json().then((values) => {
                console.log(values)
                setResponseBody({
                    download_link: values.download,
                    // mesh: values.mesh
                });
            }).catch((error) => {
                setWaitingResponse(false)
                setLoading(false)
                alert("Promise rejected")

                console.log("Promise rejected");
            })
          }
        } catch(e) {
          console.log("Network error occurred");
          setWaitingResponse(false)
          setLoading(false)
            setIsRequestGenerated(false)
            // alert("Network error occurred")
        }
      };

      // function initMap() {

      // }
    useEffect(() => {
        setIsDisplayingMap(false)
        const fetchData = async () => {
          if (isRequestGenerated) {
            fetchMeshes()
          }
        };
        console.log(isDisplayingMap)
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
                    // isPredict = {isPredict}
                    requestBody={requestBody}
                    setRequestBody={setRequestBody}
                    responseBody={responseBody}
                    setResponseBody={setResponseBody}
                    isMap = {isDisplayingMap}
                    setIsMap = {setIsDisplayingMap}
                    isPredict={isPredict}
                />
                {isWaitingResponse && <Loading word={"Generating ..."}/> }
                {isLoading && <Loading word={"Loading ..."}/>}
                {isDisplayingMap && !isRequestGenerated && <DrawableMap isMapJsLoaded={isMapJsLoaded} setMapJsLoaded={setMapJsLoaded}/> }
                {(!isDisplayingMap || responseBody || !isPredict) && <uploardImage/>}
                {(!isDisplayingMap || responseBody || isPredict) && <LandscapeScene responseBody={responseBody} setLoading={setLoading}/>}
            </div>
        </div>
    )
}

export default Home;