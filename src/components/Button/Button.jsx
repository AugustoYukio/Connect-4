import React from "react";
import './Button.css';

export default ({ text, type, margin, color = 'none', reverseColors, ...props }) => {
    return (
        <button className={`btn-${color} Button ${margin} ${reverseColors ? 'reverseColors' : ''}`} type={type} { ...props }>
            {text}
        </button>
    )
}