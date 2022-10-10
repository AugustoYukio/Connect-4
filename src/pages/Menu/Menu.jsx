import React from "react";
import "./Menu.css"

import GameMenu from "../../components/GameMenu/GameMenu";
import GameMenuOption from "../../components/GameMenuOption/GameMenuOption";
import { Link, useRouteMatch } from "react-router-dom";

export default () => {
    const { path, url } = useRouteMatch();

    return (
        <div className="Menu">
            <h1 className="MenuTitle my-5">Connect 4</h1>
            <GameMenu>
                <GameMenuOption urlTo={`${path}game`} label="Jogar" />
                <GameMenuOption urlTo={`${path}admin`} label="Painel de Administrador" />
                <GameMenuOption isButton label="Sair" />
            </GameMenu>
        </div>
    )
}