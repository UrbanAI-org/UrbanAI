import React from "react";
import { RectAreaLightUniformsLib } from "three-stdlib";
import './UserControl.css';

const PolygonForm = ({polygonItems, setPolygonItems}) => {
    const handleAddPolygonItem = (event) => {
        event.preventDefault();

        const lat = event.target.elements.latitude.value;
        const long = event.target.elements.longitude.value;
        let validDist = true;
        const regex = /^-?\d*\.?\d*$/;

        if (!regex.test(lat) || !regex.test(long)) {
            alert("decimals must range from -90 to 90 for latitude and -180 to 180 for longitude");
            return;
        }

        if (lat < -90 || lat > 90) {
            alert("decimals must range from -90 to 90 for latitude and -180 to 180 for longitude");
            return;
        } else if (long < -180 || long > 180) {
            alert("decimals must range from -90 to 90 for latitude and -180 to 180 for longitude");
            return;
        }


        polygonItems.forEach((item) => {
            const latitude = item.latitude;
            const longitude = item.longitude;
            // const distance = sqrt(latitude^2 + longitude^2);
            if (latitude - lat > 1 || lat - latitude > 1) {
                alert("Please ensure that latitude difference does not exceed 1");
                validDist = false;
                return;
            } else if (longitude - long > 1 || long - longitude > 1) {
                alert("TPlease ensure that longitude difference does not exceed 1");
                validDist = false;
                return;
            }
        });
        if (!validDist) {
            return;
        }

        setPolygonItems((prevPolygonItems) => [
            ...prevPolygonItems,
            { latitude: parseFloat(lat), longitude: parseFloat(long) }
        ])
    }

    return (
        <div>
            <form onSubmit={handleAddPolygonItem}>
                <input
                    placeholder="latitude"
                    name="latitude"
                    type="text"
                    className="poly-input-field"
                />
                <input
                    placeholder="longitude"
                    name="longitude"
                    type="text"
                    className="poly-input-field"
                />
                <input
                    type="submit"
                    value="Add"
                    className="add-button"
                />
            </form>
        </div>
    )
}

export default PolygonForm;
