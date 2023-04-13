import React from "react";
import './UserControl.css';

const PolygonForm = ({polygonItems, setPolygonItems}) => {
    const handleAddPolygonItem = (event) => {
        console.log("here");
        event.preventDefault();
        console.log(event.target.lattitude.value);

        const lat = event.target.lattitude.value;
        const long = event.target.longitude.value;

        if (lat < -90 || lat > 90) {
            alert("decimals must range from -90 to 90 for latitude and -180 to 180 for longitude");
            return;
        } else if (long < -180 || long > 180) {
            alert("decimals must range from -90 to 90 for latitude and -180 to 180 for longitude");
            return;
        }

        setPolygonItems([...polygonItems, {
            latitude: lat,
            longitude: long
        }]);
        console.log(polygonItems);
    }

    return (
        <div className>
            <form onSubmit={handleAddPolygonItem}>
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
                    type="submit"
                    value="Add"
                    className="add-button"
                />
            </form>
        </div>
    )
}

export default PolygonForm;