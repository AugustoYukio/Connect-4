import React from "react";
import "./GameMenu.css";

export default (props) => {
    return ( 
        <div className="GameMenu">
            <nav className="GameMenuNav">
                {props.children}
            </nav>
        </div>
    );
}