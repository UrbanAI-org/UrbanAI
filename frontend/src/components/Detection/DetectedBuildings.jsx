import React, { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';
import { useFrame } from 'react-three-fiber';
import { Canvas, Mesh } from "@react-three/fiber";

const ThreeScene = () => {
  const cameraRef = useRef();
  const rendererRef = useRef();
  const [meshes,setMeshs] = useState([])
  useEffect(() => {
    // Set up the scene
   
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();

    // Set up camera position
    camera.position.z = 5;

    

    // Array of geometries and materials
    const geometry = new THREE.BoxGeometry();

    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });

    // Create and add meshes to the scene using a loop
    
    for (let i = 0; i < 3; i++) {
      const mesh = new THREE.Mesh(geometry, material);
      mesh.position.x = i * 3; // Adjust the spacing between geometries
      setMeshs((meshes)=>[...meshes, mesh])
    }
    // Animation function
    // const animate = () => {
    //   // requestAnimationFrame(animate);

      // Rotate all meshes
      useFrame(() => {
        meshes.forEach((mesh) => {
          mesh.rotation.x += 0.01;
          mesh.rotation.y += 0.01;
        });
      });

  
  }, []);
  console.log(meshes)
  return (
    <>
    {meshes.map((mesh, index) => (
      <mesh
        key={index}
        position={[mesh.position.x, mesh.position.y, mesh.position.z]}
        scale={[mesh.scale.x, mesh.scale.y, mesh.scale.z]}
        rotation={[mesh.rotation.x, mesh.rotation.y, mesh.rotation.z]}
      >
        <boxGeometry args={[1, 1, 1]} />
        <meshBasicMaterial color={0x00ff00} />
      </mesh>
    ))}
  </>
  );
};

export default ThreeScene;
