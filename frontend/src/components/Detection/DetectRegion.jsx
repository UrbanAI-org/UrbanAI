import React, { useState, useEffect, useRef, Suspense, useFrame } from 'react';
import * as THREE from 'three';
import { PLYLoader, OBJLoader } from 'three-stdlib';
import { useLoader } from '@react-three/fiber';
// import { OBJLoader } from 'three/addons/loaders/OBJLoader';

import { useThree, Canvas } from '@react-three/fiber';
// import { Group } from 'three';
// Custom vertex shader
// const 

const DetectRegion = ({ position, setLookAt, responseBody, isframe }) => {
  const [geo, setGeo] = useState(null);
  const [minHeight, setMinHeight] = useState(Number.POSITIVE_INFINITY);
  const [maxHeight, setMaxHeight] = useState(Number.NEGATIVE_INFINITY);
  const [center, setCenter] = useState([0, 0, 0]);
  const [meshs,setMeshs] = useState([])
  const camera = useThree((state) => state.camera); // Access camera object
  // Create a ref to store the mesh material
  const materialRef = useRef();
  const geoRef = useRef();
//   const frame = isframe === 'Yes' ? true : false;
const [my_responseBody, setmy_responseBody] = useState(

{
    tree : {
        num_trees: 23,
        trees: [
            {
                seq_number: 0,
                position: {
                    x: 20,
                    y: 20,
                },
                size: {
                    width: 48,
                    height: 44,
                }
            },
            {
                seq_number: 1,
                position: {
                    x: 0,
                    y: 0,
                },
                size: {
                    width: 25,
                    height: 20,
                }
            }
        ]
    }
}
)
console.log(my_responseBody);

   let target_size = [25, 25]
   const scale_geo = (geometry, target_size) => {
        console.log("scale")
        console.log(geometry)
        geometry.computeBoundingBox();
        let min = geometry.boundingBox.min;
        let max = geometry.boundingBox.max;
        let size = [max.x - min.x, max.y - min.y, max.z - min.z]
        let scale_1 = target_size[0] / size[0]
        let scale_2 = target_size[1] / size[1]
        let scale_3 = (scale_1 + scale_2) / 2
        geometry.scale(scale_1, scale_2, scale_3);
        return geometry;
   }

//    for (let index = 0; index < responseBody.tree.num_trees; index++) {
//         const element = responseBody.tree.trees[index];
//         let position = [element.position.x, element.position.y]
//         let size =  [element.size.width, element.size.height]
//         let new_clone = geo.clone()
//         new_clone = scale_geo(new_clone, size)
//         // setMeshs((meshs) => (...meshs, {geometry: new_clone, position: position}))
    
//    }

   
const [response, setResponse] = useState([])
useEffect(() => {
    console.log("use effect")
    if (geo !== null) {
        console.log(geo.clone())
        setResponse(getAnimalsContent(my_responseBody.tree.trees, geo))

    }
}, [geo])

useEffect(() => {
    const load_geo = () => {
        const loader = new PLYLoader();
        loader.load(
          "tree_1.ply",
          function (geometry) {
              console.log(geometry);
            geometry.computeBoundingBox();
            let min = geometry.boundingBox.min;
            let max = geometry.boundingBox.max;
            let size = [max.x - min.x, max.y - min.y, max.z - min.z]
            let scale_1 = target_size[0] / size[0]
            let scale_2 = target_size[1] / size[1]
            let scale_3 = (scale_1 + scale_2) / 2
            geometry.scale(scale_1, scale_2, scale_3);
            console.log(geometry)
            geometry.clone()
            setLookAt([
                0,0,0
            ]);
            setGeo(geometry);
            geometry.copy()
            geoRef.current = geometry.clone()
            console.log("ref clone")
            console.log(geoRef.current.clone())
          },
          function (xhr) {
            console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
          },
          function (error) {
            console.log("An error happened");
            console.log(error);
          }
        );
        // console.log(
        //     "aaaaaaaaaaaaaaaaaa"
        // )
        // console.log(geoRef.current)

    
    }
    // let geometry = 
    load_geo()
    
    // setResponse(getAnimalsContent(my_responseBody.tree.trees))

    
  }, [my_responseBody]);
  

  // Update the uniform values in the material
  useEffect(() => {
    if (materialRef.current) {
      materialRef.current.uniforms.minHeight.value = minHeight;
      materialRef.current.uniforms.maxHeight.value = maxHeight;
    }
  }, [minHeight, maxHeight]);
//   console.log("before return")
    // load_geo()
    // console.log("after return")
    // console.log(geoRef.current.clone())
    const getAnimalsContent = (element, geo) => {
        console.log(element)
        let content = [];
        for (let item of element) {
            let temp = geo.clone()
            console.log("temp")
            console.log(temp)
          content.push(<mesh>
            position={[item.position.x, item.position.y, 0]}
            geometry={scale_geo(temp, [item.size.width, item.size.height])}
            key = {temp.id}
        </mesh>);
        }
        return content;
    };
    
  return (
      <group>
        {/* {response} */}
        {/* {getAnimalsContent(my_responseBody.tree.trees)} */}
    {/* <mesh
      position={[0, 0, 0]}
      geometry={geo}
      >
    </mesh>
    <mesh
      position={[5,0, 0]}
      geometry={geo}
      >
    </mesh> */}
        {/* { my_responseBody.tree.trees.map((element, index) => (
            <mesh>
                position={[element.position.x, element.position.y, 0]}
                geometry={scale_geo(geoRef.current.clone(), [element.size.width, element.size.height])}
            </mesh>
        )) } */}

    </group>
    

    
      
  );
};

export default DetectRegion;