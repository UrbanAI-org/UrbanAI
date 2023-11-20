import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';

const ThreeScene = () => {
  const sceneRef = useRef();
  const cameraRef = useRef();
  const rendererRef = useRef();

  useEffect(() => {
    // Set up the scene
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();

    // Set up camera position
    camera.position.z = 5;

    // Set up renderer size
    renderer.setSize(window.innerWidth, window.innerHeight);

    // Append renderer to the DOM
    sceneRef.current.appendChild(renderer.domElement);

    // Array of geometries and materials
    const geometries = [
      new THREE.BoxGeometry(),
      new THREE.SphereGeometry(),
      new THREE.CylinderGeometry(),
    ];

    const materials = [
      new THREE.MeshBasicMaterial({ color: 0x00ff00 }),
      new THREE.MeshBasicMaterial({ color: 0xff0000 }),
      new THREE.MeshBasicMaterial({ color: 0x0000ff }),
    ];

    // Create and add meshes to the scene using a loop
    const meshes = [];
    for (let i = 0; i < geometries.length; i++) {
      const mesh = new THREE.Mesh(geometries[i], materials[i]);
      mesh.position.x = i * 3; // Adjust the spacing between geometries
      meshes.push(mesh);
      scene.add(mesh);
    }

    // Animation function
    const animate = () => {
      requestAnimationFrame(animate);

      // Rotate all meshes
      meshes.forEach((mesh) => {
        mesh.rotation.x += 0.01;
        mesh.rotation.y += 0.01;
      });

      // Render the scene
      renderer.render(scene, camera);
    };

    // Call the animate function
    animate();

    // Cleanup on component unmount
    return () => {
      scene.dispose();
      camera.dispose();
      renderer.dispose();
    };
  }, []);

  return <div ref={sceneRef} />;
};

export default ThreeScene;
