import React from "react";
import { Link, useHistory } from "react-router-dom";
import "./TopNavBar.css";

export default ({urlToTema, labelTema, urlToPeca, labelPeca, urlToTabuleiro, labelTabuleiro, ...props}) => {
    let history = useHistory();
    return (
        <div className="topnav">
            <nav className="topnav">
                <Link to={urlToPeca}>{labelPeca}</Link>
                <Link to={urlToTabuleiro}>{labelTabuleiro}</Link>
                <Link to={urlToTema}>{labelTema}</Link>
                <button className="topnav" onClick={()=>history.push('/home')}>Menu</button> 
            </nav>
        </div>
    )
}