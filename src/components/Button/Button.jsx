import React from "react";
import './Button.css';

import { useHistory } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faHouse } from '@fortawesome/free-solid-svg-icons'

export default ({ text, type, margin, color = 'none', reverseColors, buttonDisabled, home, ...props }) => {
    const history = useHistory();

    return (
        <button 
            className={`
                btn-${color} 
                Button ${margin} 
                ${reverseColors ? 'reverseColors' : ''} 
                ${buttonDisabled ? 'ButtonDisabled' : ''}
                ${home ? 'ButtonHome' : ''}`
            } 
            type={type} 
            disabled={buttonDisabled}
            onClick={home ? (() => history.push('/home')) : props.onClick}
            { ...props }>
            {home ? (<FontAwesomeIcon icon={ faHouse } />) : text}
        </button>
    )
}