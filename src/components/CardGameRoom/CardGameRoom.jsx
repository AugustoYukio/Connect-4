import React from "react";
import './CardGameRoom.css';

import Button from "../Button/Button";

export default ({ lobbyName = "Connect4 #1", playerCount, ...props }) => {
    const maxPlayerCount = 2;

    const onJoinGame = () => {
        // Adicionar aqui lógica para entrar em um jogo
        console.log("Entrando em sala...")
    }

    return (
        <div className="CardGameRoom">
            <div className="GameRoomName">
                <p className="GameRoomInfoLabel">Nome da Sala</p>
                <h4 className="GameRoomTitle">{lobbyName}</h4>
            </div>
            <div className="GameRoomPlayers">
                <p className="GameRoomInfoLabel">Nº de Jogadores</p>
                <p className="GameRoomPlayerCount">{playerCount ? playerCount : 0}/{maxPlayerCount}</p>
            </div>
            <Button text="Entrar" onClick={onJoinGame} buttonDisabled={maxPlayerCount <= playerCount} />
        </div>
    )
}