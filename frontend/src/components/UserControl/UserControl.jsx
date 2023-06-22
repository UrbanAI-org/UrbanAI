import React, { useState } from "react";
import './UserControl.css';
import UserControlDefault from "./UserControlDefault";
import UserControlDetails from "./UserControlDetails";

const UserControl = ({
    isRequestGenerated, setIsRequestGenerated, requestBody, setRequestBody, responseBody, setResponseBody, isMap, setIsMap 
}) => {
    if (responseBody == null) {
        return (
            <UserControlDefault
                setIsRequestGenerated={setIsRequestGenerated}
                setRequestBody={setRequestBody}
                requestBody={requestBody}
                isMap={isMap}
                setIsMap={setIsMap}
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