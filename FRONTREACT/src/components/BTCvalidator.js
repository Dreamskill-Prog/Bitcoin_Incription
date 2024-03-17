import React from "react";

// Function to validate the
// BITCOIN Address
function isValidBTCAddress(str) {
    // Regex to check valid
    // BITCOIN Address
    let regex = new RegExp(/^(bc1|[13])[a-km-zA-HJ-NP-Z1-9]{25,34}$/);

    // if str
    // is empty return false
    if (str == null) {
        return "false";
    }

    // Return true if the str
    // matched the ReGex
    if (regex.test(str) === true) {
        return "true";
    }
    else {
        return "false";
    }
}

export default function ValidityChecker(input) {
    // const { input } = props;
    const isValidInput = isValidBTCAddress(input);
    console.log(isValidInput)

    if (isValidInput) {
        window.alert("Not a Valid BTC address!");
    }

    return (
        <div>
            {isValidInput ? ('') : (
                <span style={{ color: "red" }}>Invalid</span>
            )}
        </div>
    );
}
