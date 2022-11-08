import React from "react";
import './Peca.css'
import { useCookies } from "react-cookie";
import Swal from 'sweetalert2'
import AdminTable from '../../../components/AdminTable/AdminTable'

export default () => {
    const [cookies] = useCookies();
    var chipsArray = new Array();

    function loadTable() {
        let xhttp = new XMLHttpRequest();
        xhttp.open("GET", "http://127.0.0.1:5000/chip/", false);
        xhttp.setRequestHeader("Authorization", "Bearer " + cookies.token);
        xhttp.send();
        if(xhttp.status == 200){
            var response = JSON.parse(xhttp.responseText);
            chipsArray = response.items;
        }   
    }

    return (
      <div className="Peca">
              <div className="PecaContainer">
                  <div className="d-flex bd-highlight mb-3">
                      <div className="me-auto p-2 bd-highlight"><h2>Peça</h2></div>
                      <div className="p-2 bd-highlight">
                          <button
                            type="button"
                            className="btn btn-primary big-screen-button"
                            id="create"
                            onClick="showChipCreateBox()">
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
                            {chipsArray.map(chip=>{
                                return(<AdminTable key={chip['id']} tipoTable="Peça" idPeca={chip['id']} nomePeca={chip['name']} urlPeca={chip['url']}/>)
                                })}
                          </tbody>
                      </table>
                  </div>
              </div>
      </div>
    )
}