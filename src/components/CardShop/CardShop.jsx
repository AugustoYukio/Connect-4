import React, { useState } from "react";
import "./CardShop.css"

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCartShopping } from '@fortawesome/free-solid-svg-icons'

import CustomModal from "../CustomModal/CustomModal";
import Message from "../Message/Message";

export default ({ item, ...props }) => {
    const [open, setOpen] = useState(false);
    const [showMsg, setShowMsg] = useState(false);
    const isAvaiable = item.status == "available"

    const onOpen = () => setOpen(true);
    const onClose = () => setOpen(false);

    const onPurchase = () => {
        // TODO: Adicionar aqui função para API para realizar compra de tema
        setShowMsg(true)
        console.log("Comprou item: " + item.name)
        onClose()
    }

    return (
        <div className="CardShop card">
            { showMsg && (
                <Message msgTitle="Compra realizada" msgInfo='Transação realizada com sucesso!' onClose={() => setShowMsg(false)} />
            ) }
            <CustomModal open={open} onClose={onClose} onPurchase={onPurchase} onCancel={onClose} itemName={item.name} itemPrice={item.price} />
            <img className="card-img-top" src={require(`../../upload/${item.image_url}`)} alt={item.name} {...props} />
            <div className="CardShopBody card-body">
                <div className="CardShopDesc">
                    { isAvaiable ? (
                        <>
                            <div className="CardShopDetails">
                                <h4 className="CardShopTitle">{item.name}</h4>
                                <p className="CardShopPrice">R$ {item.price}</p>
                            </div>
                            <button className="CardShopBuyButton" onClick={onOpen}>
                                <FontAwesomeIcon icon={faCartShopping} />
                            </button>
                        </>
                    ) : (
                        <h4 className="CardShopTitle">Já obtido</h4>
                    ) }
                    
                </div>
            </div>
        </div>
    )
}