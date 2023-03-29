import React from "react";
import MapPiece from "./MapPiece";
import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import '../App.css';

const LandscapeScene = () => {
	/**
	 * TO DO: create requests for map pieces here
	 */

	async function fetchMeshes() {
		try {
			const response = await fetch("http://localhost:9999/query/mesh", {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					polygon: [
						[-33.005, 151.0056],
						[-33.021, 151.078],
						[-33.037, 151.384],
					]
				})
			})

			if (!response.ok) {
				throw new Error(`Error has occurred: ${response.status}`);
			} else {
				console.log(response)
				response.json().then((meshes) => {
                    console.log(meshes)
                }).catch((error) => {
                    console.log("Promise rejected");
                })
			}
		} catch(e) {
			console.log("Network error occured");
		}
	}

	fetchMeshes();

	return (
		<Canvas className="landscape-scene">
			<MapPiece position={[-0.75, -0.75, 0]} />
			<OrbitControls />
		</Canvas>
	)
}

export default LandscapeScene;