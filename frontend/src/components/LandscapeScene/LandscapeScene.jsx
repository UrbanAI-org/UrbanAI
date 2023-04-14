import React from "react";
import Region from "./Region";
import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import './LandscapeScene.css'

const LandscapeScene = ({responseBody}) => {
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