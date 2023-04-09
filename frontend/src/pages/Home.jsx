import React, { useState, useEffect } from "react";
import NavBar from "../components/NavBar";
import '../App.css';

import LandscapeScene from "../components/LandscapeScene";
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

	async function fetchMeshes() {
		try {
			const response = await fetch("http://localhost:9999/PUT_REQUEST_HERE", {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(requestBody)
			})

			if (!response.ok) {
				throw new Error(`Error has occurred: ${response.status}`);
			} else {
				response.json().then((repsonseValues) => {
                    console.log(repsonseValues);
                }).catch((error) => {
                    console.log("Promise rejected");
                })
			}
		} catch(e) {
			console.log("Network error occured");
		}
	}

    useEffect(() => {
        if (isRequestGenerated) {
            // handle fetching request
            setResponseBody(
                {
                    download_link: "oiwefoi",
                    mesh: "",
                    details: "",
                }
            )
        } else {
            setResponseBody(null)
        }


    }, [isRequestGenerated])

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