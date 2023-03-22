import React from "react";
import MapPiece from "./MapPiece";
import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import '../App.css';

const LandscapeScene = () => {
	/**
	 * TO DO: create requests for map pieces here
	 */

	return (
		<Canvas className="landscape-scene">
			<MapPiece position={[-0.75, -0.75, 0]} />
			<OrbitControls />
		</Canvas>
	)
}

export default LandscapeScene;