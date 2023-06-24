import React, {useState, useEffect} from "react";
import NavBar from "../components/NavBar";
import '../components/styles/Contributions.css'


/**
 * Use this opportunity to play with react
 * - Insertion of clickable option followed by a 'next' person option
 */

// Returns or renders some jsx. Functional component.

// const Person = (props) => {
//     return (
//         // Wrap in react fragment
//         <>
//         <h2>Name: {props.name}</h2>
//         <h3>Last Name: {props.lastName}</h3>
//         <h3>Degree: {props.degree}</h3>
//         </>
//     )
// }


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
    useEffect(() => {
        document.title = "UNSW VIP Project - Urban Topological Visulisation Tool"
    }, []);

    return (
        <div>
            <NavBar/>
            <div>
                <div class="container-wrapper">
                    <div class="card-container">
                        <img class="round" src="https://media.licdn.com/dms/image/D4D03AQFfGCnwEtJCEA/profile-displayphoto-shrink_400_400/0/1664584850736?e=1692835200&v=beta&t=LH0_1bHBwGOLP_JWYdjNijHJ6nw8VxrTn4COGyrJMYw" alt="user" width="170px" height="170px"/>
                        <h3>Alice Wan</h3>
                        <h5>Computer Science</h5>
                        <div class="buttons">
                            <button class="primary">
                                &nbsp;&nbsp;Email&nbsp;&nbsp;
                            </button>
                            <button class="primary ghost">
                                <a class="linkedin_a" href = "https://www.linkedin.com/in/alice-wan-42936921b/">LinkedIn</a>
                            </button>
                        </div>
                        <div class="skills">
                            <hr color="#54a3e4" size="0.5px"></hr>
                            <h4>Skills</h4>
                            <ul>
                                <li>Front End Development</li>
                                <li>HTML</li>
                                <li>CSS</li>
                                <li>JavaScript</li>
                                <li>React</li>
                            </ul>
                        </div>
                    </div>
                    <div class="card-container">
                        <img class="round" src="https://media.licdn.com/dms/image/D5603AQGGbWRebhEbtA/profile-displayphoto-shrink_400_400/0/1675696985424?e=1692835200&v=beta&t=InsBGWaFbY5sn-pLIutaVa9N_T2Gp7UQLAHGKcwr2JM" alt="user" width="170px" height="170px"/>
                        <h3>Bob He</h3>
                        <h5>Econonmics/Computer Science</h5> 
                        <div class="buttons">
                            <button class="primary">
                                <a class="email_a" href = "mailto: bobhe2002@gmail.com">Send Email</a>
                            </button>
                            <button class="primary ghost">
                                <a class="linkedin_a" href = "https://www.linkedin.com/in/bob-he-94a66920b/">LinkedIn</a>
                            </button>
                        </div>
                        
                        <div class="skills">
                            <hr color="#54a3e4" size="0.5px"></hr>
                            <h4>Skills</h4>
                            <ul>
                                <li>SQL</li>
                                <li>HTML</li>
                                <li>CSS</li>
                                <li>JavaScript</li>
                                <li>React</li>
                                <li>Web service development</li>
                            </ul>
                        </div>
                    </div>
                    <div class="card-container">
                        <img class="round" src="https://media.licdn.com/dms/image/D5603AQGHWM4za9OvVg/profile-displayphoto-shrink_400_400/0/1683079869781?e=1692835200&v=beta&t=1t3r7Jul3K7tgixiUcMCLtONApIxHY7AYExCXf-jT98" alt="user" width="170px" height="170px"/>
                        <h3>Hongyi Zheng</h3>
                        <h5>Commerce/Computer Science</h5>
                        <div class="buttons">
                            <button class="primary">
                                <a class="email_a" href = "mailto: jenniferzheng1023@gmail.com">Send Email</a>
                            </button>
                            <button class="primary ghost">
                                <a class="linkedin_a" href = "https://www.linkedin.com/in/hongyi-zheng-57544a216/">LinkedIn</a>
                            </button>
                        </div>
                        <div class="skills">
                            <hr color="#54a3e4" size="0.5px"></hr>
                            <h4>Skills</h4>
                            <ul>
                                <li>Python</li>
                                <li>HTML</li>
                                <li>CSS</li>
                                <li>JavaScript</li>
                                <li>React</li>
                                <li>RDBMS</li>
                            </ul>
                        </div>
                    </div>
                    <div class="card-container">
                        <img class="round" src="https://media.licdn.com/dms/image/D5603AQGYOTaE9GahTQ/profile-displayphoto-shrink_400_400/0/1678084950110?e=1692835200&v=beta&t=jMEseCWR88n05ANAp1wDUjrBnTeZMXDELt8VPlh-5U0" alt="user" width="170px" height="170px"/>
                        <h3>Riley Liu</h3>
                        <h5>Commerce/Computer Science</h5>
                        <div class="buttons">
                            <button class="primary">
                                &nbsp;&nbsp;Email&nbsp;&nbsp;
                            </button>
                            <button class="primary ghost">
                                <a class="linkedin_a" href = "https://www.linkedin.com/in/rileyliu/">LinkedIn</a>
                            </button>
                        </div>
                        <div class="skills">
                            <hr color="#54a3e4" size="0.5px"></hr>
                            <h4>Skills</h4>
                            <ul>
                                <li>SQL</li>
                                <li>JavaScript</li>
                                <li>TypeScript</li>
                                <li>Java</li>
                            </ul>
                        </div>
                    </div>
                    <div class="card-container">
                        <img class="round" src="https://media.licdn.com/dms/image/C4D03AQGKBwnOti63ow/profile-displayphoto-shrink_400_400/0/1624784626611?e=1692835200&v=beta&t=ovqdbUpc3wlDMO3e7QB_nCXiAqpsgjj1XQ5K87pcOr4" alt="user" width="170px" height="170px"/>
                        <h3>Shilong Li</h3>
                        <h5>Commerce/Computer Science</h5>
                        <div class="buttons">
                            <button class="primary">
                                <a class="email_a" href = "mailto: li77534479@gmail.com">Send Email</a>
                            </button>
                            <button class="primary ghost">
                                <a class="linkedin_a" href = "https://www.linkedin.com/in/shilong-li-69aa4b215/">LinkedIn</a>
                            </button>
                        </div>
                        <div class="skills">
                            <hr color="#54a3e4" size="0.5px"></hr>
                            <h4>Skills</h4>
                            <ul>
                                <li>Back End Development</li>
                                <li>Python development</li>
                                <li>React</li>
                                <li>Database</li>
                            </ul>
                        </div>
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