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

// Custom fragment shader
const fragmentShader = `
  varying vec3 vPosition;
  uniform float minHeight;
  uniform float maxHeight;

  void main() {
    // Calculate normalized height value (0 to 1)
    float height = (vPosition.y - minHeight) / (maxHeight - minHeight);
    // Use height value to interpolate gradient color
    vec3 color = mix(vec3(1.0, 0.0, 0.0), vec3(0.0, 1.0, 0.0), height);
    gl_FragColor = vec4(color, 1.0);
  }
`;

const Region = ({ position, setLookAt, url }) => {
  const [geo, setGeo] = useState(null);
  const [minHeight, setMinHeight] = useState(Number.POSITIVE_INFINITY);
  const [maxHeight, setMaxHeight] = useState(Number.NEGATIVE_INFINITY);
  const camera = useThree((state) => state.camera); // Access camera object

  // Create a ref to store the mesh material
  const materialRef = useRef();

  useEffect(() => {
    const loader = new PLYLoader();
    loader.load(
      url,
      function (geometry) {
        setLookAt([
          geometry.boundingSphere.center.y,
          geometry.boundingSphere.center.x,
          geometry.boundingSphere.center.z
        ]);

        setGeo(geometry);

        // Set far property of the camera
        camera.far = 1000000; // Set a large value for far property
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
    const positions = geo.attributes.position.array;
    let min = Number.POSITIVE_INFINITY;
    let max = Number.NEGATIVE_INFINITY;
    for (let i = 1; i < positions.length; i += 3) {
      const height = positions[i];
      min = Math.min(min, height);
      max = Math.max(max, height);
    }

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
      geometry={geo}
      onCreated={(mesh) => {
        // Store the material in the ref
        materialRef.current = mesh.material;
      }}
    >
      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        wireframe={true}
        uniforms={{
          minHeight: { value: minHeight },
          maxHeight: { value: maxHeight },
        }}
      />
    </mesh>
  );
};

export default Region;