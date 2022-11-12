import React from "react";
import { Link, useHistory } from "react-router-dom";
import "./TopNavBar.css";

export default ({urlToTema, labelTema, urlToPeca, labelPeca, urlToTabuleiro, labelTabuleiro, ...props}) => {
    let history = useHistory();
    return (
        <div className="topnav">
            <nav className="topnav">
                <button className="topnav" onClick={()=>history.push('/home')}><img className="topNavImg" src={require("../../res/img/spinningchip.gif")} /></button> 
                <Link to={urlToTema}>{labelTema}</Link>
                <Link to={urlToPeca}>{labelPeca}</Link>
                <Link to={urlToTabuleiro}>{labelTabuleiro}</Link>
            </nav>
        </div>
    )
}