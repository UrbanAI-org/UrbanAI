import React, { useState } from "react";
import './UserControl.css';
import TypeSelector from "./TypeSelector";
import PolygonForm from "./PolygonForm";

const UserControlDefault = ({setIsRequestGenerated, requestBody, setRequestBody, isMap, setIsMap }) => {
    const [polygonItems, setPolygonItems] = useState([]);

    const polygonItemsDisplay = () => {
        let display_str = ""
        for (let i = 0; i < polygonItems.length; i++) {
            display_str += `lat: ${polygonItems[i].latitude}, long: ${polygonItems[i].longitude}<br />`
        }
        return <div dangerouslySetInnerHTML={{ __html: display_str }} />;
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
        const regex = /^-?\d*\.?\d*$/;

        if (!regex.test(radius) || !regex.test(lat) || !regex.test(long)) {
            alert("Please ensure radius is an integer/decimal within the range of [0, inf], latitude  must range from -90 to 90 and longitude must range from -180 to 180");
            return;
        }
        if (radius < 0) {
            alert("Please ensure radius is an integer/decimal within the range of [0, inf], latitude  must range from -90 to 90 and longitude must range from -180 to 180");
            return;
        }
        if (lat < -90 || lat > 90) {
            alert("Please ensure radius is an integer/decimal within the range of [0, inf], latitude  must range from -90 to 90 and longitude must range from -180 to 180");
            return;
        } else if (long < -180 || long > 180) {
            alert("Please ensure radius is an integer/decimal within the range of [0, inf], latitude  must range from -90 to 90 and longitude must range from -180 to 180");
            return;
        }
        setRequestBody(
            {
                type: "circle",
                data: {
                    latitude: lat,
                    longitude: long,
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
        setIsMap(false)
        return (
            <div className="panel-control">
                <TypeSelector requestBody={requestBody} setRequestBody={setRequestBody}/>
                <div className="panel-info" style={{fontSize:"1.5vh"}}>
                    <p>Please input at least two pairs of (lat, long)</p>
                </div>
                <div className="user-control">
                    <PolygonForm polygonItems={polygonItems} setPolygonItems={setPolygonItems}/>
                    <form onSubmit={handleInputsSubmit}>
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
        setIsMap(false)

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
                            className="poly-input-field"
                        />
                        <input
                            placeholder="longitude"
                            name="longitude"
                            type="text"
                            className="poly-input-field"
                        />
                        <input
                            placeholder="radius"
                            name="radius"
                            type="text"
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
    } else if (requestBody.type === "map") {
        setIsMap(true)
        return (
            <div className="panel-control">
                <TypeSelector requestBody={requestBody} setRequestBody={setRequestBody}/>
                <div className="panel-info">
                    <p>Please select the area you want in the map</p>
                </div>
                <div className="user-control">
                    <form onSubmit={handleInputsSubmit}>
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