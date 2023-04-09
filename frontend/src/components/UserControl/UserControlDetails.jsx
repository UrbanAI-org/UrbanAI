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

    return (
        <div className="panel-control">
            <div className="panel-info">
                Hello
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