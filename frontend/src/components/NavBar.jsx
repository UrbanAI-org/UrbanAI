import React, {useEffect, useState} from "react";
import './styles/NavBar.css'
import { useNavigate } from "react-router-dom";

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
        </div>
    )
}

export default NavBar;