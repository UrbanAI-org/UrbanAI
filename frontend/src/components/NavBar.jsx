import React, {useEffect, useState} from "react";
import './styles/NavBar.css'
import { useNavigate, Link } from "react-router-dom";


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

            <button>
            <Link to="https://docs.google.com/forms/d/e/1FAIpQLSeDCRgAMDRd8n3Bz68ILfMUSrYcpRR4zKRpurCH_jJVqunqXw/viewform">
            Report a bug  </Link>
            </button>         

        </div>
    )
}

export default NavBar;