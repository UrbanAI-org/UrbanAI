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
        console.log(geometry.attributes.position.array)
        geometry.attributes.position.array.forEach((_, i) => {
          // get the height value for this vertex
          const height = geometry.attributes.position.array[i];
          // console.log(height)
          // set the color based on the height value
          const color = new THREE.Color();
          if (height < 0.5) {
            color.setRGB(1, 0, 0); // red for low values
          } else if (height < 1) {
            color.setRGB(1, 1, 0); // yellow for medium values
          } else {
            color.setRGB(0, 1, 0); // green for high values
          }

          // set the color of this vertex
          geometry.attributes.color.setXYZ(i, color.r, color.g, color.b);
        });

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

  // const ref = useRef()
  // useFrame((_, delta) => {
  //   ref.current.rotation.x += delta
  //   ref.current.rotation.y += 0.5 * delta
  // })

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