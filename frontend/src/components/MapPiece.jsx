import React, { Component } from "react";
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { PLYLoader } from 'three/addons/loaders/PLYLoader.js';

class MapPiece extends Component {
    /**
     * TO DO: any required arguments to be passed can be done via props here
     * remove the sample props when implementing
     */

    // constructor(props) {
    //     super(props);
    //     this.state = {
    //         sample: props.sample,
    //     };
    // }

	componentDidMount() {
		const width = this.mount.clientWidth;
		const height = this.mount.clientHeight;

		this.scene = new THREE.Scene();
		this.scene.add(new THREE.AxesHelper(5))

		// --- Renderer
		this.renderer = new THREE.WebGLRenderer()
		// this.renderer.outputEncoding = THREE.sRGBEncoding
		// this.renderer.setSize(window.innerWidth, window.innerHeight)
		this.renderer.setClearColor(0xffffff)
		// this.renderer.setSize(height, width);
		this.mount.appendChild(this.renderer.domElement);

		// --- Camera
		// manages the camera position
		this.camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
		this.camera.position.z = 10;
		this.camera.position.y = 10;
		// this.camera.position.z = 40

		// --- Camera controls
		// manages the 3D movement
		this.controls = new OrbitControls(this.camera, this.renderer.domElement)
		this.controls.enableDamping = true

		// --- Lights
		this.light = new THREE.SpotLight()
		this.light.position.set(20, 20, 20)
		this.scene.add(this.light)

		// --- Creating our own object
		this.material = new THREE.MeshPhysicalMaterial({
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

		this.loader = new PLYLoader()
		this.loader.load(
			'../assets/test.ply',
			function (geometry) {
				geometry.computeVertexNormals()
				this.mesh = new THREE.Mesh(geometry, this.material)
				this.mesh.rotateX(-Math.PI / 2)
				this.scene.add(this.mesh)
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
            this.camera.aspect = window.innerWidth / window.innerHeight
            this.camera.updateProjectionMatrix()
            this.renderer.setSize(window.innerWidth, window.innerHeight)
        }

		this.renderScene()
		this.start();
	}

	start = () => {
		if (!this.frameId) {
			this.frameId = requestAnimationFrame(this.animate);}
	};

	stop = () => {
	cancelAnimationFrame(this.frameId);
	};

	animate = () => {
		//Animate Models Here
		//ReDraw Scene with Camera and Scene Object
		this.renderScene();
		this.controls.update();
		this.frameId = window.requestAnimationFrame(this.animate);
		//stats.update()
	};

	renderScene = () => {
		if (this.renderer) this.renderer.render(this.scene, this.camera);
	};

	render() {
		return (
			<div style={{ width: "800px", height: "800px" }} ref={mount => { this.mount = mount }} >
				Hello World
			</div>
		)
	}
}

export default MapPiece;