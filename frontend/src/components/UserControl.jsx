import React, { useState } from "react";
import './styles/UserControl.css'

const UserControl = () => {
    const [lat, setLat] = useState(0);
    const [long, setLong] = useState(0);

    const defultUserMsg = "Enter and latitude and longitude value";
    const [userMsg, setUserMsg] = useState(defultUserMsg);

	async function fetchMeshes(latitude, longitude) {
		try {
			const response = await fetch("http://localhost:9999/query/mesh", {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					polygon: [
                        [-33.005, 151.0056],
						// [latitude, longitude]
					]
				})
			})

			if (!response.ok) {
				throw new Error(`Error has occurred: ${response.status}`);
			} else {
				response.json().then((meshes) => {
                    console.log(meshes.urls)
                    window.open(meshes.urls)
                }).catch((error) => {
                    console.log("Promise rejected");
                })
			}
		} catch(e) {
			console.log("Network error occured");
		}
	}
    async function downloadMesh(event) {
        event.preventDefault();

        if (lat < -90 || lat > 90) {
            setUserMsg("decimals must range from -90 to 90 for latitude and -180 to 180 for longitude");
            return;
        } else if (long < -180 || long > 180) {
            setUserMsg("decimals must range from -90 to 90 for latitude and -180 to 180 for longitude");
            return;
        }

        setUserMsg("getting meshes...");
        fetchMeshes(lat, long)
        setUserMsg(defultUserMsg);
    }

    return (
        <div className="panel-control">
            <div className="user-control">
                <p>{userMsg}</p>
                <form onSubmit={downloadMesh}>
                    <input
                        placeholder="latitude"
                        onChange={(e) => setLat(e.target.value)}
                        type="decimal"
                        className="input-field"
                    />
                    <input
                        placeholder="longitude"
                        onChange={(e) => setLong(e.target.value)}
                        type="decimal"
                        className="input-field"
                    />
                    <input
                        type="submit"
                        value="Download"
                        className="download-button"
                    />
                </form>
            </div>
            <div className="panel-info">
                <p>Current latitude: {lat}</p>
                <p>Current longitude: {long}</p>
            </div>
        </div>
    )
}

export default UserControl;