import React, { useState } from "react";
import './UserControl.css';
import TypeSelector from "./TypeSelector";

const UserControlDefault = ({setIsRequestGenerated, requestBody, setRequestBody}) => {
    // function setInputsValues(event) {
    //     event.preventDefault();

    //     if (lat < -90 || lat > 90) {
    //         setUserMsg("decimals must range from -90 to 90 for latitude and -180 to 180 for longitude");
    //         return;
    //     } else if (long < -180 || long > 180) {
    //         setUserMsg("decimals must range from -90 to 90 for latitude and -180 to 180 for longitude");
    //         return;
    //     }

    //     setRequestBody(
    //         {
    //             "isSet": true,
    //             "type": "",
    //             "data": {}
    //         }
    //     )
    // }

    const handleInputsSubmit = (event) => {
        event.preventDefault();

        if (requestBody.type === "polygon") {
            handlePolygon();
        } else if (requestBody.type === "circle") {
            handleCircle(event.target.radius.value);
        }
    }

    function handlePolygon() {
        return true;
    }

    function handleCircle(radius) {
        if (radius < 0) {
            alert("Please ensure radius is within the range of [0, inf]");
            return;
        }
        setRequestBody(
            {
                type: "circle",
                data: {
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
                <div className="panel-info">
                    <p>Please input at least two pairs of (lat, long)</p>
                </div>
                <div className="user-control">
                    <form onSubmit={handleInputsSubmit}>
                        {/* <input
                            placeholder="latitude"
                            onChange={(e) => setLat(e.target.value)}
                            type="decimal"
                            className="input-field"
                        />
                        <input
                            placeholder="longitude"
                            onChange={(e) => setLong(e.target.value)}
                            type="decimal"
                            className="input-field"
                        /> */}
                        <input
                            type="submit"
                            value="Generate"
                            className="generate-button"
                        />
                    </form>
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
                            placeholder="radius"
                            name="radius"
                            type="decimal"
                            className="input-field"
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