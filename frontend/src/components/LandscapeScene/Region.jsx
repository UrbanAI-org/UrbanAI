import React, { useState, useEffect, useRef } from 'react';
import * as THREE from 'three';
import { PLYLoader } from 'three-stdlib';
import { useThree } from '@react-three/fiber';

// Custom vertex shader

const vertexShader = `
  varying vec3 vPosition;

  void main() {
    vPosition = position;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

const fragmentShader = `
  varying vec3 vPosition;
  uniform float minHeight;
  uniform float maxHeight;
  void main() {
    // Calculate normalizoi ed height value (0 to 1)
    float height = (vPosition.z - minHeight) / (maxHeight - minHeight);
    // Use height value to interpolate gradient color
    vec3 color = mix(vec3(0.0,0.0,1.0), vec3(0.0,1.0,0.0), height);
    gl_FragColor = vec4(color, 1.0);
  }
`;

const Region = ({ position, setLookAt, responseBody , isframe, setLoading}) => {
  const [geo, setGeo] = useState(null);
  const [minHeight, setMinHeight] = useState(Number.POSITIVE_INFINITY);
  const [maxHeight, setMaxHeight] = useState(Number.NEGATIVE_INFINITY);
  const [center, setCenter] = useState([0, 0, 0]);
  const camera = useThree((state) => state.camera); // Access camera object
  // Create a ref to store the mesh material
  const materialRef = useRef();
  const frame = isframe === 'Yes' ? true : false;
  // console.log(responseBody.download_link);
  useEffect(() => {
    const loader = new PLYLoader();
    loader.load(
      "http://13.210.146.135:5000" + responseBody.download_link,
      // "http://127.0.0.1:9999" + responseBody.download_link,
      // "test.ply",
      function (geometry) {
        console.log(position)
        setLoading(false)
        geometry.computeBoundingBox();
        setLookAt([
          geometry.boundingSphere.center.x,
          geometry.boundingSphere.center.y,
          geometry.boundingSphere.center.z
        ]);
        // setCenter([geometry.boundingSphere.center.x, geometry.boundingSphere.center.y, geometry.boundingSphere.center.z])
        // geometry.position.set(geometry.boundingSphere.center.x, geometry.boundingSphere.center.y, geometry.boundingSphere.center.z)
        // geometry.scene.position.sub(geometry.boundingSphere.center); // Center the geometry
        // geometry.needsUpdate = true;
        console.log(geometry);
        // geometry.up = new THREE.Vector3(1, 0, 0);
        setGeo(geometry);

        // rotate the geometry to the correct position
        // geometry.rotateX(-Math.PI / 2);
        // Set far property of the camera
        camera.far = 1000000; // Set a large value for far property
        camera.position.set(geometry.boundingSphere.center.x, geometry.boundingSphere.center.y , geometry.boundingSphere.center.z + 5000);
        camera.updateProjectionMatrix(); // Apply changes to camera
      },
      function (xhr) {
        console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
      },
      function (error) {
        console.log("An error happened");
        console.log(error);
      }
    );
  }, []);
  // Calculate min and max heights
  useEffect(() => {
    if (geo) {
      const { min, max } = calculateMinMaxHeights();
      setMinHeight(min);
      setMaxHeight(max);
    }
  }, [geo]);

  // Function to calculate min and max heights
  const calculateMinMaxHeights = () => {
    const min = geo.boundingBox.min.z;
    const max = geo.boundingBox.max.z;
    return { min, max };
  };

  // Update the uniform values in the material
  useEffect(() => {
    if (materialRef.current) {
      materialRef.current.uniforms.minHeight.value = minHeight;
      materialRef.current.uniforms.maxHeight.value = maxHeight;
    }
  }, [minHeight, maxHeight]);


  return (
    <mesh
      position={[position.x, position.y, position.z]}
      // lookAt={[position.x, position.y, position.z]}
      geometry={geo}
      onCreated={(mesh) => {
        // Store the material in the ref
        materialRef.current = mesh.material;
      }}
      // up={new THREE.Vector3(0, 0, 1)}
    >
      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        wireframe={frame}
        side={THREE.DoubleSide}
        uniforms={{
          minHeight: { value: minHeight },
          maxHeight: { value: maxHeight },
        }}
        // uniformsNeedUpdate = {true}
      />
      
    </mesh>
  );
};

export default Region;