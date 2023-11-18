import React, { useState, useEffect } from "react";
import NavBar from "../components/NavBar";
import '../components/styles/Detection.css';
// -33.916276, 151.227973
const TreeBuildingDetection = () => {
	const [longLat, setLogLat] = useState({
		latitude: '',
		longitude: '',
	})

	const handleInputChange = (e) => {
		const {name, value} = e.target;
		setLogLat((prevLongLat) => ({
			...prevLongLat,
			[name]: parseFloat(value),
		}))
	}

	const handleSubmit = async () => {
		const inputData = {data: [longLat]};
		const response = await fetch('http://localhost:9999/v1/api/region/detect', {
			method: 'POST',
			body: JSON.stringify(inputData),
			headers: {
				'Content-type': 'application/json',
			}
		})
		const data = await response.json();
		if (data.error) {
			alert(data.error);
		} else {
			console.log(data);
		}
	}
	return (
		<>
		<NavBar />
		<h2>Please Enter a Latitude and Longitude</h2><br/>
		<h2>Latitude</h2>
		<input
			type = "text"
			name = "latitude"
			value = {longLat.latitude}
			onChange = {handleInputChange}
		/>
		<br/>
		<h2>Longitude</h2>
		<input
			type = "text"
			name = "longitude"
			value = {longLat.longitude}
			onChange = {handleInputChange}
		/>
		<br/>
		<button onClick={handleSubmit}>Submit</button>
		</>
	)
}

export default TreeBuildingDetection;
