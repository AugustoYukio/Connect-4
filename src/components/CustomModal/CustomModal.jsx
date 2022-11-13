import React, { useState } from "react";
import './CustomModal.css'

import Button from "../Button/Button"

import 'react-responsive-modal/styles.css';
import { Modal } from 'react-responsive-modal';

export default ({ itemName, itemPrice, onPurchase, onCancel, ...props }) => {
    const [cancel, setCancel] = useState(false);

    const confirmPurchase = () => {
        onPurchase();
    }

    const cancelPurchase = () => {
        onCancel();
    }

    return (
        <Modal classNames="CustomModal" center {...props}>
            <div className="CustomModalHeader">
                <h4>Comprar tema '{itemName}'?</h4>
            </div>
            <hr />
            <div className="CustomModalBody">
                <p>Tem certeza de que deseja comprar '{itemName}' no valor de R$ {itemPrice}?</p>
            </div>
            <hr />
            <div className="CustomModalFooter">
                <Button onClick={() => confirmPurchase()} color="success" margin="mr-3" text="Comprar" />
                <Button onClick={() => cancelPurchase()} color="secondary" text="Cancelar" />
            </div>
        </Modal>
    )
}