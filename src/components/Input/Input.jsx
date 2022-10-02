import React from "react";
import './Input.css';

export default ({ inputType = "text", inputName, inputPlaceholder = "", label }) => {
    return (
        <div className="input-group mb-3">
            <label className="input-group-text" htmlFor={inputName}>{label}</label>
            <input className="form-control" id={inputName} name={inputName} type={inputType} placeholder={inputPlaceholder} />
        </div>
    )
}