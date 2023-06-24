import React from "react";
import './UserControl.css';

const UserControlDetails = ({setIsRequestGenerated, setRequestBody, responseBody, setResponseBody}) => {
    const handleRestart = (event) => {
        event.preventDefault();

        setRequestBody(
            {
                type: "",
                data: {}
            }
        )

        setIsRequestGenerated(false);
        setResponseBody(null);
    }

    const downloadURL = "http://13.210.146.135:5000" + responseBody.download_link;
    return (
        <div className="panel-control">
            <div className="panel-info">
                <p>Some details go heres</p>
            </div>
            <div style={{ padding: "5px" }}>
                <a href={downloadURL} target="_blank" download style={{ color: 'blue' }}>Click here to download .ply</a>
            </div>
            {/* <p>{responseBody.download_link}</p> */}
            <div className="user-control">
                <form onSubmit={handleRestart}>
                    <input
                        type="submit"
                        value="Restart"
                        className="generate-button"
                    />
                </form>
            </div>
        </div>
    )
}

export default UserControlDetails;