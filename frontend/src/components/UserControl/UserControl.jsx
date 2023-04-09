import React, { useState } from "react";
import './UserControl.css';
import UserControlDefault from "./UserControlDefault";
import UserControlDetails from "./UserControlDetails";

const UserControl = ({
    isRequestGenerated, setIsRequestGenerated, requestBody, setRequestBody, responseBody, setResponseBody
}) => {
    if (!isRequestGenerated) {
        return (
            <UserControlDefault
                setIsRequestGenerated={setIsRequestGenerated}
                setRequestBody={setRequestBody}
                requestBody={requestBody}
            />
        )
    } else {
        return (
            <UserControlDetails
                setIsRequestGenerated={setIsRequestGenerated}
                setRequestBody={setRequestBody}
                responseBody={responseBody}
                setResponseBody={setResponseBody}
            />
        )
    }
}

export default UserControl;