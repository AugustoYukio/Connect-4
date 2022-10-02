import React from "react";
import './Message.css';

/*
    Tipos de mensagem: success, danger, warning, info
*/ 

export default ({ msgType = 'success', msgTitle = '', msgInfo = '', ...props }) => {
    return (
        <div className={`Message alert alert-${msgType} alert-dismissible fade show`} role="alert">
            <h4 className="MessageTitle alert-heading">{msgTitle}</h4>
            <hr />
            <p className="MessageInfo">{msgInfo}</p>
            <button type="button" className="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
    )
}