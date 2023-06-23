import React, { useState, useEffect } from "react";
import NavBar from "../components/NavBar";
import '../App.css';

import LandscapeScene from "../components/LandscapeScene/LandscapeScene";
import UserControl from "../components/UserControl/UserControl";
import Loading from "../components/LandscapeScene/Loading";
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
    // const []
    const fetchMeshes = async () => {
        try {
            // setLoading(true)
            setWaitingResponse(true)
            const response = await fetch("http://localhost:9999/v1/api/region/mesh", {
            method: 'POST',
            mode: "cors",
            headers: { 'Content-Type': 'text/plain' },
            body: JSON.stringify(requestBody)
          });

          if (!response.ok) {
            response.json().then((values) => {
              alert(values.message)
            })
            setWaitingResponse(false)
            setLoading(false)
            throw new Error(`Error has occurred: ${response.status}`);
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
                {isWaitingResponse && <Loading word={"Generating ..."}/> }
                {isLoading && <Loading word={"Loading ..."}/>}
                <LandscapeScene responseBody={responseBody} setLoading={setLoading}/>
            </div>
        </div>
    )
}

export default Home;