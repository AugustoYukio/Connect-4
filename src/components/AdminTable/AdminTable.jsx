import React from "react";
import "./AdminTable.css"
import Swal from 'sweetalert2'
import { useCookies } from "react-cookie";

export default ({ tipoTable, idTema, nomeTema, precoTema, urlPeca1, nomePeca1, urlPeca2, nomePeca2, idTabuleiro, urlTabuleiro, nomeTabuleiro, idPeca, nomePeca, urlPeca, ...props }) => {
    
    const [cookies] = useCookies();
    
    function showThemeEditBox(id) {
        let xhttp = new XMLHttpRequest();
        xhttp.open("GET", "http://127.0.0.1:5000/theme/"+id, false);
        xhttp.setRequestHeader("Authorization", "Bearer " + cookies.token);
        xhttp.send();
        if(xhttp.status == 200){
            const theme = JSON.parse(xhttp.responseText);
            Swal.fire({
                title: 'Editar Tema',
                html:
                '<input id="id" type="hidden" value='+theme['id']+'>' +
                '<input id="name" class="swal2-input" placeholder="Nome" value="'+theme['name']+'">' +
                '<input id="price" type="number" step="0.01" class="swal2-input" placeholder="Preço" value="'+theme['price']+'">' +
                '<input id="piece1_id" type="number" min="0" step="1" class="swal2-input" placeholder="Peça1_id" value="'+theme['piece1_id']+'">' +
                '<input id="piece2_id" type="number" min="0" step="1" class="swal2-input" placeholder="Peça2_id" value="'+theme['piece2_id']+'">' +
                '<input id="board_id" type="number" min="0" step="1" class="swal2-input" placeholder="Tabuleiro_id" value="'+theme['board_id']+'">',
                focusConfirm: false,
                preConfirm: () => {
                    if (!document.getElementById('name').value || !document.getElementById('price').value || !document.getElementById('piece1_id').value || !document.getElementById('piece2_id').value || !document.getElementById('board_id').value){
                        Swal.showValidationMessage('Existe algum campo incompleto')
                    }
                    else if (document.getElementById('piece1_id').value == document.getElementById('piece2_id').value) {
                        Swal.showValidationMessage('Peça1 e 2 não podem ter o mesmo valor')
                    }
                    else if (!Number.isInteger(Number(document.getElementById('piece1_id').value)) || !Number.isInteger(Number(document.getElementById('piece2_id').value))) {
                        Swal.showValidationMessage('ID Peça1 e 2 deve ser um número inteiro')
                    }
                    else if (!Number.isInteger(Number(document.getElementById('board_id').value))) {
                        Swal.showValidationMessage('ID Boad deve ser um número inteiro')
                    }else{
                        themeEdit();
                    }
                }
            })
        }   
    }
       
    async function themeEdit() {
        const id = document.getElementById("id").value;
        const name = document.getElementById("name").value;
        var price = document.getElementById("price").value;
        const piece1_id = document.getElementById("piece1_id").value;
        const piece2_id = document.getElementById("piece2_id").value;
        const board_id = document.getElementById("board_id").value;
        price = Number(price).toFixed(2);
        let xhttp = new XMLHttpRequest();
        xhttp.open("PUT", "http://127.0.0.1:5000/theme/", false);
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.setRequestHeader("Authorization", "Bearer " + cookies.token);
        xhttp.send(JSON.stringify({ "id": id, "name": name, "price": price, "chip1Id": piece1_id, "chip2Id": piece2_id, "boardId": board_id}));
        if(xhttp.status == 202){
            Swal.fire('Tema editado com sucesso!','','success').then((result) => {
                if (result.isConfirmed || result.isDismissed) {
                    window.location.reload();
                }
              });
        };
    }

    function showChipEditBox(id) {
        let xhttp = new XMLHttpRequest();
        xhttp.open("GET", "http://127.0.0.1:5000/chip/"+id, false);
        xhttp.setRequestHeader("Authorization", "Bearer " + cookies.token);
        xhttp.send();
        if(xhttp.status == 200){
            const chip = JSON.parse(xhttp.responseText);
            Swal.fire({
                title: 'Editar Peça',
                html:
                '<input id="id" type="hidden" value='+chip['id']+'>' +
                '<input id="url" type="hidden" value="'+chip['url']+'">' +
                '<input id="name" class="swal2-input" placeholder="Nome" value="'+chip['name']+'">' +
                '<input id="image-file" type="file" accept="image/*" style="margin-top: 20px;"/>',
                focusConfirm: false,
                preConfirm: () => {
                chipEdit();
                }
            })
        };
    }
      
    async function chipEdit() {
        const id = document.getElementById("id").value;
        const name = document.getElementById("name").value;
        var url = document.getElementById("url").value;
        /*
        if(document.getElementById('image-file').files[0]){
            url = await uploadFile();
        }
        */
        let xhttp = new XMLHttpRequest();
        xhttp.open("PUT", "http://127.0.0.1:5000/chip/", false);
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.setRequestHeader("Authorization", "Bearer " + cookies.token);
        xhttp.send(JSON.stringify({ "id": id, "name": name, "url": url}));
        if(xhttp.status == 202){
            Swal.fire('Peça editada com sucesso!','','success').then((result) => {
                if (result.isConfirmed || result.isDismissed) {
                    window.location.reload();
                }
              });
        };
    }

    function showBoardEditBox(id) {
        let xhttp = new XMLHttpRequest();
        xhttp.open("GET", "http://127.0.0.1:5000/board/"+id, false);
        xhttp.setRequestHeader("Authorization", "Bearer " + cookies.token);
        xhttp.send();
        if(xhttp.status == 200){
            const board = JSON.parse(xhttp.responseText);;
            Swal.fire({
                title: 'Editar Tabuleiro',
                html:
                '<input id="id" type="hidden" value='+board['id']+'>' +
                '<input id="url" type="hidden" value="'+board['url']+'">' +
                '<input id="name" class="swal2-input" placeholder="Nome" value="'+board['name']+'">' +
                '<input id="image-file" type="file" accept="image/*" style="margin-top: 20px;"/>',
                focusConfirm: false,
                preConfirm: () => {
                boardEdit();
                }
            })
        };
    }
        
    async function boardEdit() {
        const id = document.getElementById("id").value;
        const name = document.getElementById("name").value;
        var url = document.getElementById("url").value;
        /*
        if(document.getElementById('image-file').files[0]){
            url = await uploadFile();
        }
        */
        let xhttp = new XMLHttpRequest();
        xhttp.open("PUT", "http://127.0.0.1:5000/board/", false);
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.setRequestHeader("Authorization", "Bearer " + cookies.token);
        xhttp.send(JSON.stringify({ "id": id, "name": name, "url": url}));
        if(xhttp.status == 202){
            Swal.fire('Tabuleiro editado com sucesso!','','success').then((result) => {
                if (result.isConfirmed || result.isDismissed) {
                    window.location.reload();
                }
              });
        };
    }
    
    
    function confirmDelete(id, tipo){
        var complemento = "";
        var param = "";
        switch (tipo) {
            case "Tema":
                complemento = "esse tema";
                param = "theme";
                break;
            case "Peça":
                complemento = "essa peça";
                param = "chip";
                break;
            case "Tabuleiro":
                complemento = "esse tabuleiro";
                param = "board";
                break;
        }
        Swal.fire({
            title: `Tem certeza que deseja deletar ${complemento}?`,
            text: "Essa ação é irreversível!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Deletar!'
            }).then((result) => {
            if (result.isConfirmed) {
                doDelete(id, param)
            }
        })
    }

    function doDelete(id, param){
        let xhttp = new XMLHttpRequest();
        xhttp.open("DELETE", `http://127.0.0.1:5000/${param}/`+id, false);
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.setRequestHeader("Authorization", "Bearer " + cookies.token);
        xhttp.send();
        if(xhttp.status == 202){
            Swal.fire('Deletado com sucesso!','','success').then((result) => {
                if (result.isConfirmed || result.isDismissed) {
                    window.location.reload();
                }
              });
        };
    }

    switch(tipoTable){
        case 'Tema':
            return (
                <tr>
                    <td>{idTema}</td>
                    <td>{nomeTema}</td>
                    <td>{Number(precoTema).toFixed(2)}</td>
                    <td><a href={`upload/${urlPeca1}`} target="_blank" rel="noopener noreferrer">{nomePeca1}</a></td>
                    <td><a href={`upload/${urlPeca2}`} target="_blank" rel="noopener noreferrer">{nomePeca2}</a></td>                  
                    <td><a href={`upload/${urlTabuleiro}`} target="_blank" rel="noopener noreferrer">{nomeTabuleiro}</a></td>
                    <td>
                        <button type="button" className="btn btn-outline-secondary" onClick={()=>showThemeEditBox(idTema)}>Edit</button>
                        <button type="button" className="btn btn-outline-danger" onClick={()=>confirmDelete(idTema, tipoTable)}>Del</button>
                    </td>
                </tr>
            );
        case 'Peça': 
            return (
                <tr>
                    <td>{idPeca}</td>
                    <td>{nomePeca}</td>
                    <td><a href={`upload/${urlPeca}`} target="_blank" rel="noopener noreferrer">Link</a></td>
                    <td>
                        <button type="button" className="btn btn-outline-secondary" onClick={()=>showChipEditBox(idPeca)}>Edit</button>
                        <button type="button" className="btn btn-outline-danger" onClick={()=>confirmDelete(idPeca, tipoTable)}>Del</button>
                    </td>
                </tr>
            );
        case 'Tabuleiro':
            return (
                <tr>
                    <td>{idTabuleiro}</td>
                    <td>{nomeTabuleiro}</td>
                    <td><a href={`upload/${urlTabuleiro}`} target="_blank" rel="noopener noreferrer">Link</a></td>
                    <td>
                        <button type="button" className="btn btn-outline-secondary" onClick={()=>showBoardEditBox(idTabuleiro)}>Edit</button>
                        <button type="button" className="btn btn-outline-danger" onClick={()=>confirmDelete(idTabuleiro, tipoTable)}>Del</button>
                    </td>
                </tr>
            )
    }
}