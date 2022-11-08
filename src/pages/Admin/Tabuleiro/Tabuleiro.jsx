import React from "react";
import './Tabuleiro.css'
import { useCookies } from "react-cookie";
import Swal from 'sweetalert2'
import AdminTable from '../../../components/AdminTable/AdminTable'

export default () => {
    const [cookies] = useCookies();
    var boardsArray = new Array();

    function loadTable() {
        let xhttp = new XMLHttpRequest();
        xhttp.open("GET", "http://127.0.0.1:5000/board/", false);
        xhttp.setRequestHeader("Authorization", "Bearer " + cookies.token);
        xhttp.send();
        if(xhttp.status == 200){
            var response = JSON.parse(xhttp.responseText);
            boardsArray = response.items;
        }   
    }

    return (
      <div className="Tabuleiro">
              <div className="TabuleiroContainer">
                  <div className="d-flex bd-highlight mb-3">
                      <div className="me-auto p-2 bd-highlight"><h2>Tabuleiro</h2></div>
                      <div className="p-2 bd-highlight">
                          <button
                          type="button"
                          className="btn btn-primary big-screen-button"
                          id="create"
                          onClick="showBoardCreateBox()">
                          Criar
                          </button>
                      </div>
                  </div>

                  <div className="table-responsive">
                      <table className="table">
                          <thead>
                              <tr>
                              <th scope="col">#</th>
                              <th scope="col">Nome</th>
                              <th scope="col">URL</th>
                              <th scope="col">Ações</th>
                              </tr>
                          </thead>
                          <tbody id="mytable" onLoad={loadTable()}>
                            {boardsArray.map(board=>{
                                return(<AdminTable key={board['id']} tipoTable="Tabuleiro" idTabuleiro={board['id']} nomeTabuleiro={board['name']} urlTabuleiro={board['url']}/>)
                                })}
                          </tbody>
                      </table>
                  </div>
              </div>        
      </div>
    )
}