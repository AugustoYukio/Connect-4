import React from "react";
import './Button.css';

export default ({ text, type, margin, color = 'none', ...props }) => {
    return (
        <button className={`btn-${color} Button ${margin}`} type={type} { ...props }>
            {text}
        </button>
    )
}