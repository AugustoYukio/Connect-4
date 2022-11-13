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

    function showChipCreateBox() {
        Swal.fire({
            title: 'Criar Peça',
            html:
            '<input id="id" type="hidden">' +
            '<input id="name" class="swal2-input" placeholder="Nome">' +
            '<input id="image-file" type="file" accept="image/*" style="margin-top: 20px;"/>',
            focusConfirm: false,
            preConfirm: async () => {
                if (document.getElementById('name').value && document.getElementById('image-file').files[0]) {
                    chipCreate();
                }else{
                    Swal.showValidationMessage('Existe algum campo incompleto')
                }
            }
        })
    }
    
    async function chipCreate() {
        const name = document.getElementById("name").value;
        //const url = await uploadFile();
        const url = createGuid();
        let xhttp = new XMLHttpRequest();
        xhttp.open("POST", "http://127.0.0.1:5000/chip/", false);
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.setRequestHeader("Authorization", "Bearer " + cookies.token);
        xhttp.send(JSON.stringify({ "name": name, "url": url}));
        if(xhttp.status == 201){
            Swal.fire('Peça criada com sucesso!','','success').then((result) => {
                if (result.isConfirmed || result.isDismissed) {
                    window.location.reload();
                }
            });
        }
    }

    //Função de criação de Guid apenas para ter uma string única nos temas/imagens dos cadastros criados enquanto não tiver upload
    function createGuid()  
    {  
       return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {  
          var r = Math.random()*16|0, v = c === 'x' ? r : (r&0x3|0x8);  
          return v.toString(16);  
       });  
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
                            onClick={()=>showChipCreateBox()}>
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