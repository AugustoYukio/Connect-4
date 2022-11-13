import React from "react";
import './Shop.css'

import CardShop from "../../components/CardShop/CardShop";"../../components/CardShop/CardShop";

export default () => {
    const itens = [
        {
          "id": 1,
          "name": "Padrão",
          "image_url": "teste.jpeg",
          "price": 9.99,
          "status": "default"
        },
        {
          "id": 2,
          "name": "Universo",
          "image_url": "teste.jpeg",
          "price": 19.99,
          "status": "available"
        },
        {
          "id": 3,
          "name": "Doces",
          "image_url": "teste.jpeg",
          "price": 20.99,
          "status": "unavailable"
        }
      ]

    return (
        <div className="Shop">
            <h1 className="ShopTitle">Loja</h1>
            <hr />
            <div className="ShopItemContainer row">
                {itens.map(item => {
                    return <CardShop key={item.id} item={item} />
                })}
            </div>
        </div>
    )
}