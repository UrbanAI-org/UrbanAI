import React from "react";
import Region from "./Region";
import { Canvas } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera } from '@react-three/drei'
import '../App.css';

const LandscapeScene = ({responseBody}) => {
	/**
	 * TO DO: create requests for map pieces here
	 */

	// async function fetchMeshes() {
	// 	try {
	// 		const response = await fetch("http://localhost:9999/v1/query/mesh", {
	// 			method: 'POST',
	// 			headers: { 'Content-Type': 'application/json' },
	// 			body: JSON.stringify({
	// 				"polygon": [
	// 					[-33.005, 151.0056],
	// 					[-33.021, 151.078],
	// 					[-33.037, 151.384],
	// 				]
	// 			})
	// 		})

	// 		if (!response.ok) {
	// 			throw new Error(`Error has occurred: ${response.status}`);
	// 		} else {
	// 			console.log(response)
	// 			response.json().then((meshes) => {
    //                 console.log(meshes)
    //             }).catch((error) => {
    //                 console.log("Promise rejected");
    //             })
	// 		}
	// 	} catch(e) {
	// 		console.log("Network error occured");
	// 	}
	// }

	// fetchMeshes();

	if (responseBody === null) {
		return(
			<Canvas className="landscape-scene">
			</Canvas>
		)
	} else {
		return (
			<Canvas className="landscape-scene">
				<Region position={[0, 0 , 0]} />
				<mesh>
					<planeBufferGeometry attach="geometry" args={[25, 15]} />
					<meshPhongMaterial attach="material" color="green" />
				 </mesh>
				<OrbitControls />
			</Canvas>
		)
	}
}

export default LandscapeScene;