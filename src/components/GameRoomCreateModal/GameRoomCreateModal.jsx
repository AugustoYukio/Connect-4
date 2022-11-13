import React, { useState } from "react";
import './GameRoomCreateModal.css'

import 'react-responsive-modal/styles.css';
import { Modal } from 'react-responsive-modal';

import Button from "../Button/Button";
import Input from "../Input/Input";

export default props => {
    const [room, setRoom] = useState("")

    const onCreateGame = () => {
        // Aqui entra a lógica para criar uma sala
        console.log("Criando sala...")
    }

    return (
        <Modal classNames="GameRoomCreateModal" center {...props}>
            <div className="CustomModalHeader">
                <h4>Criar Sala</h4>
            </div>
            <hr />
            <div className="CustomModalBody">
                <Input label="Nome da Sala" inputName="lobbyName" value={room} onChange={e => setRoom(e.target.value)} />
            </div>
            <hr />
            <div className="CustomModalFooter">
                <Button onClick={onCreateGame} color="success" margin="mr-3" text="Criar" />
                <Button onClick={props.onClose} color="secondary" text="Cancelar" />
            </div>
        </Modal>
    )
}