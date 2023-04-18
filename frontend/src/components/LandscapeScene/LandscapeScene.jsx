import React, { useState, useRef, useEffect } from "react";
import Region from "./Region";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import "react-dat-gui/dist/index.css";
import "./LandscapeScene.css";
import * as THREE from 'three';

const LandscapeScene = ({ responseBody }) => {
  const [position, setPosition] = useState({ x: 0, y: 0, z: 0, rotationX: 0, rotationY: 0, rotationZ: 0 });
  const [lookAt, setLookAt] = useState([0, 0, 0]);

  const orbitControlsRef = useRef();

  if (responseBody === null) {
    return (
      <Canvas className="landscape-scene">
      </Canvas>
    );
  } else {
    return (
        <Canvas className="landscape-scene">
          <Region position={position} setLookAt={setLookAt} responseBody={responseBody}/>
          <OrbitControls ref={orbitControlsRef} target={new THREE.Vector3(lookAt[0], lookAt[1], lookAt[2])} />
        </Canvas>
    );
  }
};

export default LandscapeScene;