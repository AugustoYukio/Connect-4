import React from "react";
import "./AdminTable.css"
import Swal from 'sweetalert2'
import { useCookies } from "react-cookie";

export default ({ tipoTable, idTema, nomeTema, precoTema, urlPeca1, nomePeca1, urlPeca2, nomePeca2, urlTabuleiro, nomeTabuleiro, ...props }) => {
    
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
                        Swal.showValidationMessage('Algum campo incompleto')
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
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
            const objects = JSON.parse(this.responseText);
            const theme = objects;
            console.log(theme);
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
                        Swal.showValidationMessage('Algum campo incompleto')
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
        };
    }
        
    async function themeEdit() {
        const id = document.getElementById("id").value;
        const name = document.getElementById("name").value;
        var price = document.getElementById("price").value;
        const piece1_id = document.getElementById("piece1_id").value;
        const piece2_id = document.getElementById("piece2_id").value;
        const board_id = document.getElementById("board_id").value;
        price = Number(price).toFixed(2);
        const xhttp = new XMLHttpRequest();
        xhttp.open("PUT", "http://localhost:5000/themes/"+id);
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.send(JSON.stringify({ "id": id, "name": name, "price": price, "piece1_id": piece1_id, "piece2_id": piece2_id, "board_id": board_id}));
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
            const objects = JSON.parse(this.responseText);
            Swal.fire(objects['message']);
            }
        };
    }

    function confirmDelete(id) {
        Swal.fire({
            title: 'Tem certeza que deseja apagar esse tema?',
            text: "Essa ação é irreversível!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Deletar!'
            }).then((result) => {
            if (result.isConfirmed) {
                themeDelete(id); 
            }
        })
    }
    
    function themeDelete(id) {
        console.log("APAGANDO");
        let xhttp = new XMLHttpRequest();
        xhttp.open("DELETE", "http://127.0.0.1:5000/theme/"+id, false);
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.setRequestHeader("Authorization", "Bearer " + cookies.token);
        xhttp.send();
        if(xhttp.status == 202){
            window.location.reload();
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
                        <button type="button" className="btn btn-outline-danger" onClick={()=>confirmDelete(idTema)}>Del</button>
                    </td>
                </tr>
            );
        case '': break;
    }
}