import React from "react";
import './Home.css';
import Game from "../Game/Game"
import Menu from "../Menu/Menu"
import Admin from "../Admin/Admin"
import User from "../../components/User/User";
import { Route, useRouteMatch } from 'react-router-dom';
import { useCookies } from "react-cookie";

export default () => {
    const { path, url } = useRouteMatch();
    const [cookies] = useCookies();
    function getUserName() {
        let xhttp = new XMLHttpRequest();
        xhttp.open("GET", "http://127.0.0.1:5000/user/" + cookies.userID, false);
        xhttp.setRequestHeader("Authorization", "Bearer " + cookies.token);
        xhttp.send();

        if(xhttp.status == 200){
            var jResponse = JSON.parse(xhttp.responseText);
            return jResponse[0].username;
        }
    }
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
            <User user={getUserName()} />
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