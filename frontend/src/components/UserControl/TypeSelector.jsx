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
            <h3>Select Mesh Type</h3>
            {/* <labeL>Select mesh type</labeL> */}
            <select value={requestBody.type} onChange={handleOptionChange} className="type-selector">
                <option></option>
                <option value="polygon">polygon</option>
                <option value="circle">circle</option>
                <option value="map">map</option>
            </select>
        </div>

    )
}

export default TypeSelector;