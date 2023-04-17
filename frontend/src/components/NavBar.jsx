import React, {useEffect, useState} from "react";
import './styles/NavBar.css'
import { useNavigate, Link } from "react-router-dom";
import bugImage from './assets/bug.jpeg';


const NavBar = () => {
    
    const [path, setPath] = useState('');
    const nav = useNavigate();

    useEffect(() => {
        nav(path)
    }, [path]);

    return (
        <div className="NavBar">
            <header onClick={() => {setPath('/')}}>Home</header>
            <header onClick={() => {setPath('/about')}}>About</header>
            <header onClick={() => {setPath('/contributions')}}>Contributions</header>
            <header onClick={() => {setPath('/UserGuid')}}>How To Use</header>

            <a href="https://docs.google.com/forms/d/e/1FAIpQLSeDCRgAMDRd8n3Bz68ILfMUSrYcpRR4zKRpurCH_jJVqunqXw/viewform">
                <img src={bugImage} alt="Random Image"/>
            </a>

        </div>
    )
}

export default NavBar;