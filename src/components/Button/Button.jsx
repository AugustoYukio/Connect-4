import React from "react";
import './Button.css';

export default ({ text, type }) => {
    return (
        <button className="Button" type={type}>
            {text}
        </button>
    )
}