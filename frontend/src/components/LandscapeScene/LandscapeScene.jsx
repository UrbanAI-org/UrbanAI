import React, { useState, useRef, useEffect } from "react";
import Region from "./Region";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import DatGui, { DatNumber } from "react-dat-gui";
import "react-dat-gui/dist/index.css";
import "./LandscapeScene.css";
import * as THREE from 'three';

const LandscapeScene = ({ responseBody }) => {
  // const [position, setPosition] = useState({ x: 54622.674343846564, y: -45736.43317283617, z: 274.990234375, rotationX: 0, rotationY: 0, rotationZ: 0 });
  const [position, setPosition] = useState({ x: 0, y: 0, z: 0, rotationX: 0, rotationY: 0, rotationZ: 0 });
  const [lookAt, setLookAt] = useState([0, 0, 0]);

  const orbitControlsRef = useRef();
  // useEffect((responseBody) => {
  //   if (responseBody !== null) {
      
  //   }

  // }, [responseBody])

  if (responseBody === null) {
    return (
      <Canvas className="landscape-scene">
      </Canvas>
    );
  } else {
    // ***********************************************
    // TODO: 
    // setPosition({
    //   x : 54622.674343846564,
    //   y : -45736.43317283617,
    //   z : 274.990234375,
    //   rotationX: 0, 
    //   rotationY: 0, 
    //   rotationZ: 0
    // });
    // setLookAt([54622.674343846564, -45736.43317283617, 274.990234375])
    // ***********************************************
    console.log(position)
    console.log(lookAt)
    return (
        <Canvas className="landscape-scene">
          {/* <DatGui data={position} onUpdate={setPosition} >
          <DatNumber path="x" label="X" min={-300} max={300} step={0.1} />
          <DatNumber path="y" label="Y" min={-300} max={300} step={0.1} />
          <DatNumber path="z" label="Z" min={-300} max={300} step={0.1} />
          <DatNumber path="rotationX" label="Rotation X" min={-Math.PI} max={Math.PI} step={0.01} />
          <DatNumber path="rotationY" label="Rotation Y" min={-Math.PI} max={Math.PI} step={0.01} />
          <DatNumber path="rotationZ" label="Rotation Z" min={-Math.PI} max={Math.PI} step={0.01} />
          </DatGui> */}
          <Region position={position} setLookAt={setLookAt}/>
          <OrbitControls ref={orbitControlsRef} target={new THREE.Vector3(lookAt[0], lookAt[1], lookAt[2])} />
        </Canvas>
    );
  }
};

export default LandscapeScene;