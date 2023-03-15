import React from "react";
import NavBar from "../components/NavBar";
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { PLYLoader } from 'three/addons/loaders/PLYLoader.js';

const Home = () => {
    const scene = new THREE.Scene()
    scene.add(new THREE.AxesHelper(5))

    const light = new THREE.SpotLight()
    light.position.set(20, 20, 20)
    scene.add(light)

    const camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    )

    camera.position.z = 40

    const renderer = new THREE.WebGLRenderer()
    renderer.outputEncoding = THREE.sRGBEncoding
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)
    renderer.setClearColor(0xffffff)

    const controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true
    const material = new THREE.MeshPhysicalMaterial({
        color: 0x00ffff,
        //envMap: envTexture,
        metalness: 0,
        roughness: 0,
        transparent: true,
        transmission: 1.0,
        side: THREE.DoubleSide,
        clearcoat: 1.0,
        clearcoatRoughness: 0.25
    })

    const loader = new PLYLoader()
    loader.load(
        '../assets/test.ply',
        function (geometry) {
            geometry.computeVertexNormals()
            const mesh = new THREE.Mesh(geometry, material)
            mesh.rotateX(-Math.PI / 2)
            scene.add(mesh)
        },
        (xhr) => {
            console.log((xhr.loaded / xhr.total) * 100 + '% loaded')
        },
        (error) => {
            console.log(error)
        }
    )

    window.addEventListener('resize', onWindowResize, false)
    function onWindowResize() {
        camera.aspect = window.innerWidth / window.innerHeight
        camera.updateProjectionMatrix()
        renderer.setSize(window.innerWidth, window.innerHeight)
        render()
    }

    //const stats = Stats()
    //document.body.appendChild(stats.dom)

    function animate() {
        requestAnimationFrame(animate)

        controls.update()

        render()

        //stats.update()
    }

    function render() {

        renderer.render(scene, camera)
    }

    animate()

    return (
        <div>
            <NavBar />
            Home Page
            <div>
                {scene}
            </div>
        </div>
    )
}

export default Home;