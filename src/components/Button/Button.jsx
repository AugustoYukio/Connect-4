import React from "react";
import './Button.css';

export default ({ text, type, margin, color = 'none', ...props }) => {
    return (
        <button className="Button" type={type}>
            {text}
        </button>
    )
}