import React from "react";
import './Home.css';
import Game from "../Game/Game"
import Menu from "../Menu/Menu"
import Admin from "../Admin/Admin"
import { Route, useRouteMatch } from 'react-router-dom';
import { useCookies } from "react-cookie";

export default () => {
    const { path, url } = useRouteMatch();
    const [cookies] = useCookies();
    
    function getPainelAdm () {
        var base64Url = cookies.token.split('.')[1];
        var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        
        var parsedJSON = JSON.parse(jsonPayload)
        return !parsedJSON.is_admin; /*Inverte o valor de admin para que o atributo hidden fique false*/ 
    };

    return (
        <div className="Home">
            <Route exact path={`${path}/`}>
                <Menu showAdm={getPainelAdm()} />
            </Route>
            <Route path={`${path}/game`}>
                <Game />
            </Route>
            <Route path={`${path}/admin`}>
                <Admin />
            </Route>
        </div>
    )
}