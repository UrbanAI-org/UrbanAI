import React from "react";
import './UserControl.css';

const PolygonForm = ({polygonItems, setPolygonItems}) => {
    const handleAddPolygonItem = (event) => {
        event.preventDefault();

        const lat = event.target.elements.latitude.value;
        const long = event.target.elements.longitude.value;
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
