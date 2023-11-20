import React, { useState, useEffect, useRef } from "react";
import * as THREE from 'three';
import DetectRegion from "./DetectRegion";
import DetectedBuildings from "./DetectedBuildings";
import { PLYLoader, OBJLoader } from 'three-stdlib';
import { useThree } from "@react-three/fiber";
// import { PLYLoader, OBJLoader, MTLLoader } from 'three-stdlib';
// import { useLoader } from '@react-three/fiber';
// import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';
import { Canvas, Mesh } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
const DetectedImg = (data) => {
  const [position, setPosition] = useState({ x: 0, y: 0, z: 0, rotationX: 0, rotationY: 0, rotationZ: 0 });
  const [lookAt, setLookAt] = useState([0, 0, 0]);
  const [isframe, setFrame] = useState('Yes');
  const [center, setCenter] = useState([0, 0, 0]);

  const orbitControlsRef = useRef();

  // if (data === null) {
  //   return (
  //     <Canvas className="landscape-scene">

  //     </Canvas>
  //   );
  // } else {
    return (
      <div className="landscape-scene">
         
        
        <Canvas >
          {/* <axesHelper args={[10000]} /> */}
          {/* <DetectRegion position={position} setLookAt={setLookAt} responseBody={data} isframe={isframe}/>
          <DetectedBuildings position={position} setLookAt={setLookAt} responseBody={data}/>
          <OrbitControls ref={orbitControlsRef} target={new THREE.Vector3(lookAt[0], lookAt[1], lookAt[2])} /> */}
          {/* <OrbitControls ref={orbitControlsRef} target={new THREE.Vector3(0,0,0)} /> */}
        </Canvas>
      </div>
    );
  


  //   let position = [0,0,0]
  //   const [look, setLookAt] = useState([0,0,0])
  //   const [a, setLoading] = useState([])
  //   const [geo, setGeo] = useState(null);
  //   const {
  //       building,
  //       road,
  //       tree,
  //       size,
  //       download
  //   } = data;
  //   const [treeData, setTreeData] = useState(null);
  //   // API request to get the response body for vectary OBJ 
  // const [center, setCenter] = useState([0, 0, 0]);
  // const camera = useThree((state) => state.camera); // Access camera object
  // // Create a ref to store the mesh material
  // const materialRef = useRef();
  // // console.log(responseBody.download_link);
  // useEffect(() => {
  //   const loader = new OBJLoader();
  //   loader.load(
  //       "class10.obj",
  //     function (geometry) {
  //       console.log(position)
  //       setLoading(false)
  //       geometry.computeBoundingBox();
  //       setLookAt([
  //         geometry.boundingSphere.center.x,
  //         geometry.boundingSphere.center.y,
  //         geometry.boundingSphere.center.z
  //       ]);
  //       console.log(geometry);
  //       setGeo(geometry);
  //       camera.far = 1000000; // Set a large value for far property
  //       camera.position.set(geometry.boundingSphere.center.x, geometry.boundingSphere.center.y , geometry.boundingSphere.center.z + 5000);
  //       camera.updateProjectionMatrix(); // Apply changes to camera
  //     },
  //     function (xhr) {
  //       console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
  //     },
  //     function (error) {
  //       console.log("An error happened");
  //       console.log(error);
  //     }
  //   );
  // }, []);
  // Calculate min and max heights
    
    
    // useEffect(() => {
    //     const loader = new OBJLoader();
    //     loader.load(
    //         // "http://localhost:9999/v1/download?types=trees&id=class10",
    //       "class10.obj",
    //     function (geometry) {
    //         setGeo(geometry);
    //     },
    //     // called when loading is in progresses
    //     function ( xhr ) {
    //         console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );
    //     },
    //     // called when loading has errors
    //     function ( error ) {
    //         console.log( error );
    //     }
    //     )
    // }, [])
    // const orbitControlsRef = useRef();

    // return (
    //     <>
    //     <p>Hello</p>
    //     <Canvas>
    //         <mesh
    //       position={[0,0,0]}
    //       // lookAt={[position.x, position.y, position.z]}
    //       geometry={geo}
    //       onCreated={(mesh) => {
    //         // Store the material in the ref
    //         materialRef.current = mesh.material;
    //       }}
    //       // up={new THREE.Vector3(0, 0, 1)}
    //     >
    // </mesh>

    //         {/* <mesh position={[0, 0, 0]} geometry={geo}></mesh> */}
    //         <OrbitControls ref={orbitControlsRef} target={new THREE.Vector3(0, 0, 0)} />
    //     </Canvas>
    //     {/* <Mesh position={[0, 0, 0]} geometry={geo}></Mesh> */}

    //     </>
    // )
}

export default DetectedImg;
