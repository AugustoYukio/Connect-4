import React from "react";
import "./User.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUser } from '@fortawesome/free-solid-svg-icons'

export default ({ user, rank, ...props }) => {
    return (
        <div className="User">
            <div className="UserIconContainer">
                <FontAwesomeIcon icon={faUser} />
            </div>
            <div className="UserInfo ml-3">
                <p className="UserName mb-1">Usuário: {user}</p>
                <p className="UserRank mb-0">Rank: #{rank ? rank : "-"}</p>
            </div>
        </div>
    )
}