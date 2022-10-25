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

    return (
        <div className="Home">
            <User user={cookies.userName} />
            <Route exact path={`${path}/`}>
                <Menu />
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