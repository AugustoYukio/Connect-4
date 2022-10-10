import React from "react";
import { Link } from "react-router-dom";

import "./GameMenuOption.css";

export default ({ isButton = false, urlTo, label, onLogout, ...props }) => {
    return (
        <div className="GameMenuOptionWrapper">
            <img className="GameMenuOptionImg mr-3" src={require("../../res/img/spinningchip.gif")} />
            {
                isButton ?
                <button className="GameMenuOption my-2" onClick={onLogout}>{label}</button> :
                <Link className="GameMenuOption my-2" to={urlTo}>{label}</Link>
            }
        </div>
    )
}