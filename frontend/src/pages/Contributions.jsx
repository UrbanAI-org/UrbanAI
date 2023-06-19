import React, {useState, useEffect} from "react";
import NavBar from "../components/NavBar";
import '../components/styles/Contributions.css'


/**
 * Use this opportunity to play with react
 * - Insertion of clickable option followed by a 'next' person option
 */

// Returns or renders some jsx. Functional component.

const Person = (props) => {
    return (
        // Wrap in react fragment
        <>
        <h2>Name: {props.name}</h2>
        <h3>Last Name: {props.lastName}</h3>
        <h3>Degree: {props.degree}</h3>
        </>
    )
}


const Contributions = () => {

    // // This is a hook. Only change this using its setter
    // const [clickText, setclickText] = useState(0)

    // const peopleName = [
    // <Person name = 'Bob' lastName = 'He' degree = 'Econonmics/Computer Science'/> ,
    // <Person name = 'Hongyi' lastName = 'Zheng' degree = 'Commerce/Computer Science'/>,
    // <Person name = 'Alice' lastName = 'Wan' degree = 'Computer Science'/>,
    // <Person name = 'Shilong' lastName = 'Li' degree = 'Commerce/Computer Science'/>,
    // <Person name = 'Riley' lastName = 'Liu' degree = 'Commerce/Computer Science'/>,
    // ]

    return (
        <div>
            <NavBar/>
        <div>

        <div class="card-container">
            <span class="pro">PRO</span>
            <img class="round" src="https://randomuser.me/api/portraits/women/79.jpg" alt="user" />
            <h3>Ricky Park</h3>
            <h6>New York</h6>
            <p>User interface designer and <br/> front-end developer</p>
            <div class="buttons">
                <button class="primary">
                    Message
                </button>
                <button class="primary ghost">
                    Following
                </button>
            </div>
        </div>
            </div>
        </div>

    );
}


// Props -> arguments to pass into react components.

// const Contributions = () => {


//     const [clickText, setclickText] = useState(Person)

//     // This is a hook. Only change this using its setter
//     const [counter, setCounter] = useState(0);

//     // Initially set at 100 and does not change.
//     useEffect(() => {
//         alert("You've changed the counter to " + counter)
//     }, [counter]);

//     return (
//         <div className="Contributions">

//             <NavBar />

//             <h1>Contributions</h1>
//             <div>
//             The following individuals have contributed towards this project:
//             <Person name = 'Bob' lastName = 'He' age = '20' degree = 'Econometrics'/>

//             {/* Illustration on how states work. */}

//             <button onClick={() => setCounter((prevCount) => prevCount - 1)}>-</button>
//             <h1>{counter}</h1>
//             <button onClick={() => setCounter((prevCount) => prevCount + 1)}>+</button>
//             </div>

//         </div>

//     )
// }


export default Contributions;