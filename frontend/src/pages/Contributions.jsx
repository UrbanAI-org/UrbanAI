import React, {useState, useEffect} from "react";
import NavBar from "../components/NavBar";

/**
 * Use this opportunity to play with react
 * - Insertion of clickable option followed by a 'next' person option
 * - drop down bar contains more information of each person 
 */



// Returns or renders some jsx. Functional component.

const Person = (props) => {
    return (
        // Wrap in react fragment
        <>
        <h1>Name: {props.name}</h1>
        <h2>Last Name: {props.lastName}</h2>
        <h2>Age: {props.age}</h2>
        <h2>Degree: {props.degree}</h2>
        </>
    )
}

// Props -> arguments to pass into react components.

const Contributions = () => {

    // This is a hook. Only change this using its setter
    const [counter, setCounter] = useState(0);

    // Initially set at 100 and does not change.
    useEffect(() => {
        alert("You've changed the counter to " + counter)
    }, [counter]);

    return (
        <div className="Contributions">

            <NavBar />

            <h1>Contributions</h1>
            <div>
            The following individualss have contributed towards this project:
            <Person name = 'Bob' lastName = 'He' age = '20' degree = 'Econometrics'/>

            {/* Illustration on how states work. */}

            <button onClick={() => setCounter((prevCount) => prevCount - 1)}>-</button>
            <h1>{counter}</h1>
            <button onClick={() => setCounter((prevCount) => prevCount + 1)}>+</button>
            </div>

            

        </div>

    )
}


export default Contributions;