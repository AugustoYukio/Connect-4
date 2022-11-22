import React, { useState } from "react";
import './GameList.css'

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowsRotate } from '@fortawesome/free-solid-svg-icons'

import Button from "../../components/Button/Button";
import CardGameRoom from "../../components/CardGameRoom/CardGameRoom";
import GameRoomCreateModal from "../../components/GameRoomCreateModal/GameRoomCreateModal";

export default () => {
    const gameListExample = [
        {
            id: 1,
            lobbyName: "Jogo do Thiago",
            playerCount: 1
        },
        {
            id: 2,
            lobbyName: "Jogo do Augustu",
            playerCount: 1
        },
        {
            id: 3,
            lobbyName: "Jogo do Pedro",
            playerCount: 1
        }
    ]

    const [open, setOpen] = useState(false);
    const [gameList, setGameList] = useState(gameListExample);

    const updateGameList = () => {
        // Simula adição de uma nova sala
        let lastId = gameList[gameList.length - 1].id;
        setGameList([
            ...gameList,
            {
                id: ++lastId,
                lobbyName: "Teste atualizar",
                playerCount: 2
            }
        ])
        console.log("Atualizando lista...")
    }

    const onOpen = () => setOpen(true);
    const onClose = () => setOpen(false);

    return (
        <div className="GameList">
            <h1 className="GameListTitle">Lista de Jogos</h1>
            <hr />
            <GameRoomCreateModal open={open} onOpen={onOpen} onClose={onClose} />
            <Button onClick={() => onOpen()} margin="mx-4 my-2" text="Criar Sala" reverseColors={true} />
            <Button onClick={updateGameList} text={<FontAwesomeIcon icon={faArrowsRotate} />} reverseColors={true} />
            <div className="GamesAvailable">
                { gameList.map(item => {
                    return <CardGameRoom key={item.id} lobbyName={item.lobbyName} playerCount={item.playerCount} />
                }) }
            </div>
            { !(gameList.length > 0) && <h2 className="GameListNoGames">Não existem jogos disponíveis no momento</h2> }
        </div>
    )
}