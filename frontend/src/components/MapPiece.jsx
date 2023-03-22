import React, { useRef, useState, useEffect } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three';
// // import { OrbitControls } from '@react-three/drei'
import { PLYLoader } from 'three-stdlib'

const MapPiece = ({ position }) => {
  const [geo, setGeo] = useState(new THREE.BoxGeometry());

  useEffect(() => {
    const loader = new PLYLoader();
    loader.load(
      "test.ply",
      function (geometry) {
        /**
         * TO DO: fix "rotating" issue
         */
        setGeo(geometry);
      },
      // called when loading is in progress
      function (xhr) {
        console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
      },
      // called when loading has errors
      function (error) {
        console.log("An error happened");
        console.log(error);
      }
    );
  }, []);

  const ref = useRef()
  useFrame((_, delta) => {
    ref.current.rotation.x += delta
    ref.current.rotation.y += 0.5 * delta
  })

  return (
    <mesh
      position={position}
      ref={ref}
      geometry={geo}>
      <meshBasicMaterial color={'lime'} wireframe />
    </mesh>
  )
}

export default MapPiece;