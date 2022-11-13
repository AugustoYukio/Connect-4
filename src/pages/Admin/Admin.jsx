import React from "react";
import './Admin.css'
import { Route, useRouteMatch, Redirect  } from 'react-router-dom';
import TopNav from "../../components/TopNavBar/TopNavBar";
import Tema from './Tema/Tema'
import Peca from'./Peca/Peca'
import Tabuleiro from'./Tabuleiro/Tabuleiro'

export default () => {
  const { path, url } = useRouteMatch();
  
    return (
      <div className="Admin">
        <TopNav urlToTema={`${path}/tema`} labelTema="Tema" urlToPeca={`${path}/peca`} labelPeca="Peça" urlToTabuleiro={`${path}/tabuleiro`} labelTabuleiro="Tabuleiro"/>
        <Route path={`${path}/tema`}>
          <Tema />
        </Route>
        <Route path={`${path}/peca`}>
          <Peca />
        </Route>
        <Route path={`${path}/tabuleiro`}>
          <Tabuleiro />
        </Route>
        <Route exact path={`${path}/`}>
          <Redirect to={`${path}/tema`} />
        </Route>
      </div>
    )
}