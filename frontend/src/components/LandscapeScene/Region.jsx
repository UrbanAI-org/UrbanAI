import React, { useState, useEffect } from 'react'
import * as THREE from 'three';
import { PLYLoader } from 'three-stdlib'

const Region = ({ position }) => {
  const [geo, setGeo] = useState(new THREE.BoxGeometry());

  const attr = geo.attributes;
  useEffect(() => {
    const loader = new PLYLoader();
    loader.load(
      "test.ply",
      function (geometry) {
        console.log(geometry)
        console.log(geometry.boundingSphere.center)
        console.log(geometry.attributes.position.array)
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

  return (
    <mesh
      position={position}
      // ref={ref}
      geometry={geo}>
      <meshBasicMaterial color={'lime'} wireframe />
    </mesh>
  )
}

export default Region;