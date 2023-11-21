import React, { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';
import { useFrame} from 'react-three-fiber';


const ThreeScene = () => {
  const [meshes,setMeshs] = useState([])
  useEffect(() => {

    // Array of geometries and materials
    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    // Create and add meshes to the scene using a loop
    
    for (let i = 0; i < 3; i++) {
      const mesh = new THREE.Mesh(geometry, material);
      mesh.position.x = i * 3; // Adjust the spacing between geometries
      setMeshs((meshes)=>[...meshes, mesh])
    }
  }, []);

  useFrame(() => {
    meshes.forEach((mesh) => {
      mesh.rotation.x += 0.01;
      mesh.rotation.y += 0.01;
    });
  });

  console.log(meshes)

  return (
    <group>
    {meshes.length > 0 &&
      meshes.map((mesh, index) => (
        <mesh
          key={index}
          position={[mesh.position.x, mesh.position.y, mesh.position.z]}
          rotation={[mesh.rotation.x, mesh.rotation.y, mesh.rotation.z]}
          geometry={mesh.geometry}
          material={mesh.material}
        />
      ))}
  </group>
  );
};

export default ThreeScene;
