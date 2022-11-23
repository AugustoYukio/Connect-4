import React from "react";
import "./Menu.css"

import GameMenu from "../../components/GameMenu/GameMenu";
import GameMenuOption from "../../components/GameMenuOption/GameMenuOption";
import User from "../../components/User/User";
import { useRouteMatch } from "react-router-dom";
import { useCookies } from "react-cookie";

export default ({showAdm, ...props}) => {
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
    return (
        <div className="Menu">
            <User user={getUserName()} />
            <h1 className="MenuTitle my-5">Connect 4</h1>
            <GameMenu>
                <GameMenuOption urlTo={`${path}gamelist`} label="Jogar" />
                <GameMenuOption urlTo={`${path}shop`} label="Loja" />
                <GameMenuOption urlTo={`${path}admin`} label="Painel de Administrador" show={showAdm}/>
                <GameMenuOption isButton label="Sair" />
            </GameMenu>
        </div>
    )
}