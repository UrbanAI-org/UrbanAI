import React, { useState } from "react";
import './UserControl.css';
import TypeSelector from "./TypeSelector";
import PolygonForm from "./PolygonForm";

const UserControlDefault = ({setIsRequestGenerated, requestBody, setRequestBody}) => {
    const [polygonItems, setPolygonItems] = useState([]);

    const polygonItemsDisplay = () => {
        let display_str = ""
        for (let i = 0; i < polygonItems.length; i++) {
            display_str += `lat: ${polygonItems[i].lat}, long: ${polygonItems[i].long}\n`
        }
        return display_str
    }

    const handleInputsSubmit = (event) => {
        event.preventDefault();

        if (requestBody.type === "polygon") {
            handlePolygon();
        } else if (requestBody.type === "circle") {
            handleCircle(
                event.target.radius.value,
                event.target.latitude.value,
                event.target.longitude.value
            );
        }
    }

    function handlePolygon() {
        if (polygonItems.length < 2) {
            alert("Please input at least 2 pairs of latitude and longitude");
            return
        }
        setRequestBody(
            {
                type: "polygon",
                data: polygonItems
            }
        )
        setPolygonItems([]);
        setIsRequestGenerated(true);
    }

    function handleCircle(radius, lat, long) {
        if (radius < 0) {
            alert("Please ensure radius is an integer/decimal within the range of [0, inf]");
            return;
        }
        if (lat < -90 || lat > 90) {
            alert("decimals must range from -90 to 90 for latitude and -180 to 180 for longitude");
            return;
        } else if (long < -180 || long > 180) {
            alert("decimals must range from -90 to 90 for latitude and -180 to 180 for longitude");
            return;
        }
        setRequestBody(
            {
                type: "circle",
                data: {
                    lat: lat,
                    long: long,
                    radius: radius
                }
            }
        )
        setIsRequestGenerated(true);
    }

    if (requestBody.type === "") {
        return (
            <div className="panel-control">
                <TypeSelector requestBody={requestBody} setRequestBody={setRequestBody}/>
            </div>
        )
    } else if (requestBody.type === "polygon") {
        return (
            <div className="panel-control">
                <TypeSelector requestBody={requestBody} setRequestBody={setRequestBody}/>
                <div className="panel-info" style={{fontSize:"1.5vh"}}>
                    <p>Please input at least two pairs of (lat, long)</p>
                </div>
                <div className="user-control">
                    <form onSubmit={handleInputsSubmit}>
                        <PolygonForm polygonItems={polygonItems} setPolygonItems={setPolygonItems}/>
                        <input
                            type="submit"
                            value="Generate"
                            className="generate-button"
                        />
                    </form>
                </div>
                <div>
                    <p>current pairs:</p>
                    <p style={{fontSize:"1.5vh"}}>{polygonItemsDisplay()}</p>
                </div>
            </div>
        )
    } else if (requestBody.type === "circle") {
        return (
            <div className="panel-control">
                <TypeSelector requestBody={requestBody} setRequestBody={setRequestBody}/>
                <div className="panel-info">
                    <p>Please input radius</p>
                </div>
                <div className="user-control">
                    <form onSubmit={handleInputsSubmit}>
                        <input
                            placeholder="latitude"
                            name="latitude"
                            type="decimal"
                            className="poly-input-field"
                        />
                        <input
                            placeholder="longitude"
                            name="longitude"
                            type="decimal"
                            className="poly-input-field"
                        />
                        <input
                            placeholder="radius"
                            name="radius"
                            type="decimal"
                            className="input-field"
                            style={{width: "15vh"}}
                        />
                        <input
                            type="submit"
                            value="Generate"
                            className="generate-button"
                        />
                    </form>
                </div>
            </div>
        )
    }

}

export default UserControlDefault;