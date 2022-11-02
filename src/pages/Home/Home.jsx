import React from "react";
import './Home.css';
import Game from "../Game/Game"
import Menu from "../Menu/Menu"
import Admin from "../Admin/Admin"
import User from "../../components/User/User";
import { Route, useRouteMatch } from 'react-router-dom';
import Shop from "../Shop/Shop";

export default () => {
    const { path, url } = useRouteMatch();

    return (
        <div className="Home">
            <User user="Thiago" />
            <Route exact path={`${path}/`}>
                <Menu />
            </Route>
            <Route path={`${path}/game`}>
                <Game />
            </Route>
            <Route path={`${path}/shop`}>
                <Shop />
            </Route>
            <Route path={`${path}/admin`}>
                <Admin />
            </Route>
        </div>
    )
}