import React from "react";
import './UserControl.css';

const TypeSelector = ({requestBody, setRequestBody}) => {
    const handleOptionChange = (event) => {
        setRequestBody(prevState => ({
            ...prevState,
            type: event.target.value
        }))
    }

    return (
        <div>
            <labeL>Select mesh type</labeL>
            <select value={requestBody.type} onChange={handleOptionChange} className="type-selector">
                <option></option>
                <option value="polygon">polygon</option>
                <option value="circle">circle</option>
            </select>
        </div>

    )
}

export default TypeSelector;