import React from "react";
import './UserControl.css';

const UserControlDetails = ({setIsRequestGenerated, setRequestBody, responseBody}) => {
    const handleRestart = (event) => {
        event.preventDefault();

        setRequestBody(
            {
                type: "",
                data: {}
            }
        )

        setIsRequestGenerated(false);
    }

    const downloadUrl = "random"

    return (
        <div className="panel-control">
            <div className="panel-info">
                <p>Some details go heres</p>
            </div>
            <div style={{ padding: "5px" }}>
                <a href={downloadUrl} target="_blank" download style={{ color: 'blue' }}>Click here to download .ply</a>
            </div>
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