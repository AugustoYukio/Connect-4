import React from "react";
import './Button.css';

export default ({ text, type, margin, color = 'none', reverseColors, buttonDisabled, ...props }) => {
    return (
        <button 
            className={`btn-${color} Button ${margin} ${reverseColors ? 'reverseColors' : ''} ${buttonDisabled ? 'ButtonDisabled' : ''}`} 
            type={type} 
            disabled={buttonDisabled}
            { ...props }>
            {text}
        </button>
    )
}