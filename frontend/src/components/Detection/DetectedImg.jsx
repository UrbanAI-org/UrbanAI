import React, { useState, useEffect, useRef } from "react";
import * as THREE from 'three';
import { PLYLoader, OBJLoader } from 'three-stdlib';
// import { PLYLoader, OBJLoader, MTLLoader } from 'three-stdlib';
// import { useLoader } from '@react-three/fiber';
// import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
const DetectedImg = (data) => {
    const [geo, setGeo] = useState(null);
    const {
        building,
        road,
        tree,
        size,
        download
    } = data;
    const [treeData, setTreeData] = useState(null);
    // API request to get the response body for vectary OBJ 
    useEffect(() => {
        // const loader = new OBJLoader();
        // loader.load(
        //     "http://localhost:9999/v1/download?types=trees&id=class10",
        // //   "class10.obj",
        // function (geometry) {
        //     setGeo(geometry);
        // },
        // // called when loading is in progresses
        // function ( xhr ) {
        //     console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );
        // },
        // // called when loading has errors
        // function ( error ) {
        //     console.log( 'An error happened' );
        // }
        // )
        
        const handleLoad = async () => {
            const response = await fetch('http://localhost:9999/v1/download?types=trees&id=class10', {
                method: 'GET',
            })
            const data = await response.json();
            if (data.error) {
                alert(data.error);
            } else {
                console.log(data);
            }
        }
        handleLoad();
    }, [])
    const orbitControlsRef = useRef();

    return (
        <>
        <p>Hello</p>
        </>
    )
}

export default DetectedImg;
