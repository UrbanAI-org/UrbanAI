import React, { useState } from "react";
import Region from "./Region";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import DatGui, { DatNumber } from "react-dat-gui";
import "react-dat-gui/dist/index.css";
import "./LandscapeScene.css";

const LandscapeScene = ({ responseBody }) => {
  const [position, setPosition] = useState([0, 0, 0]);

  if (responseBody === null) {
    return (
      <Canvas className="landscape-scene">
        {/*...your existing code*/}
      </Canvas>
    );
  } else {
    return (
      <div className="landscape-scene">
        <DatGui data={position} onUpdate={setPosition}>
          <DatNumber path="0" label="X" min={-100} max={100} step={0.1} />
          <DatNumber path="1" label="Y" min={-100} max={100} step={0.1} />
          <DatNumber path="2" label="Z" min={-100} max={100} step={0.1} />
        </DatGui>
        <Canvas >
          <Region position={position} />
          <OrbitControls />
        </Canvas>
      </div>
    );
  }
};

export default LandscapeScene;




// import React from "react";
// import Region from "./Region";
// import { Canvas } from '@react-three/fiber'
// import { OrbitControls } from '@react-three/drei'
// import './LandscapeScene.css';

// const LandscapeScene = ({responseBody}) => {
// 	if (responseBody === null) {
// 		return(
// 			<Canvas className="landscape-scene">
// 			</Canvas>
// 		)
// 	} else {
// 		return (
// 			<Canvas className="landscape-scene">
// 				<Region position={[0, 0 , 0]} />
// 				<mesh>
// 					<planeBufferGeometry attach="geometry" args={[25, 15]} />
// 					<meshPhongMaterial attach="material" color="green" />
// 				 </mesh>
// 				<OrbitControls />
// 			</Canvas>
// 		)
// 	}
// }

// export default LandscapeScene;