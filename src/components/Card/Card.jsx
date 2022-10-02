import './Card.css';
import React from 'react';

/*

    Criado por: Thiago Carvalho Füllenbach  
    Data: 01/10/2022

*/

export default ({ title = "Título padrão", ...props }) => {
    return (
        <div className='Card'>
            <h2 className='CardTitle'>{title}</h2>
            <hr />
            <div className='CardContent'>{props.children}</div>
        </div>
    )
}