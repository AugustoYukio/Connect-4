import React from "react";
import './Tema.css'

export default () => {
/*
    function showCreateChip(){
        Swal.fire({
            title: 'Criar Peça',
            html:
            '<p>Peça1</p>' +
            '<input id="id" type="hidden">' +
            '<input id="name" class="swal2-input" placeholder="Nome">' +
            '<input id="image-file" type="file" accept="image/*" style="margin-top: 20px;"/>' +
            '<p style="margin-top: 50px;" >Piece2</p>' +
            '<input id="id2" type="hidden">' +
            '<input id="name2" class="swal2-input" placeholder="Nome">' +
            '<input id="image-file2" type="file" accept="image/*" style="margin-top: 20px;"/>',
            focusConfirm: false,
            preConfirm: async () => {
                if (document.getElementById('name').value && document.getElementById('image-file').files[0] && document.getElementById('name2').value && document.getElementById('image-file2').files[0]) {
                    chipCreate();
                }
                else{
                    Swal.showValidationMessage('Algum campo incompleto')
                }
            }
        })
    }
    
    async function chipCreate() {
        const name = document.getElementById("name").value;
        const url = await uploadFile("image-file");
        const name2 = document.getElementById("name2").value;
        const url2 = await uploadFile("image-file2");
        let response = await fetch("http://localhost:5000/pieces", {
            method: "POST",
            headers:{
                "Content-Type": "application/json;charset=UTF-8"
            },
            body: JSON.stringify({ "name": name, "url": url})
        });
        response = await response.json();
        let response2 = await fetch("http://localhost:5000/pieces", {
            method: "POST",
            headers:{
                "Content-Type": "application/json;charset=UTF-8"
            },
            body: JSON.stringify({ "name": name2, "url": url2})
        });
        response2 = await response2.json();
        showBoardCreateBox(response["id"], response2["id"]);
    }
    function showBoardCreateBox(id, id2){
        Swal.fire({
            title: 'Criar Tabuleiro',
            html:
            '<input id="id" type="hidden">' +
            '<input id="name" class="swal2-input" placeholder="Nome">' +
            '<input id="image-file" type="file" accept="image/*" style="margin-top: 20px;"/>',
            focusConfirm: false,
            preConfirm: async () => {
                if (document.getElementById('name').value && document.getElementById('image-file').files[0]) {
                    boardCreate(id, id2);
                }else{
                    Swal.showValidationMessage('Algum campo incompleto')
                }
            }
        })
    }
    
    async function boardCreate(id, id2) {
        const name = document.getElementById("name").value;
        const url = await uploadFile("image-file");
        const xhttp = new XMLHttpRequest();
        xhttp.open("POST", "http://localhost:5000/boards");
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.send(JSON.stringify({ "name": name, "url": url}));
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        const objects = JSON.parse(this.responseText);
        Swal.fire(objects['message']);
        showThemeCreateAllBox(id, id2, objects["id"]);
        }
        };
    }
    
    function showThemeCreateAllBox(piece1_id, piece2_id, board_id) {
        Swal.fire({
            title: 'Criar Tema',
            html:
            '<input id="id" type="hidden">' +
            '<input id="name" class="swal2-input" placeholder="Nome">' +
            '<input id="price" type="number" step="0.01" class="swal2-input" placeholder="Preço">' +
            '<input id="piece1_id" type="number" class="swal2-input" value="'+piece1_id+'" readonly>' +
            '<input id="piece2_id" type="number" class="swal2-input" value="'+piece2_id+'" readonly>' +
            '<input id="board_id" type="number" class="swal2-input" value="'+board_id+'" readonly>',
            focusConfirm: false,
            preConfirm: async () => {
                if (!document.getElementById('name').value || !document.getElementById('price').value){
                    Swal.showValidationMessage('Algum campo incompleto')
                }else{
                    themeCreate();
                }
            }
        })
    }
    
    function showThemeCreateBox() {
        Swal.fire({
            title: 'Criar Tema',
            html:
            '<input id="id" type="hidden">' +
            '<input id="name" class="swal2-input" placeholder="Nome">' +
            '<input id="price" type="number" step="0.01" class="swal2-input" placeholder="Preço">' +
            '<input id="piece1_id" type="number" min="0" step="1" class="swal2-input" placeholder="Peça1_id">' +
            '<input id="piece2_id" type="number" min="0" step="1" class="swal2-input" placeholder="Peça2_id">' +
            '<input id="board_id" type="number" min="0" step="1" class="swal2-input" placeholder="Tabuleiro_id">',
            focusConfirm: false,
            preConfirm: async () => {
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
                    themeCreate();
                }
            }
        })
    }
    
    async function themeCreate() {
        const name = document.getElementById("name").value;
        var price = document.getElementById("price").value;
        const piece1_id = document.getElementById("piece1_id").value;
        const piece2_id = document.getElementById("piece2_id").value;
        const board_id = document.getElementById("board_id").value;
        price = Number(price).toFixed(2);
        const xhttp = new XMLHttpRequest();
        xhttp.open("POST", "http://localhost:5000/themes");
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.send(JSON.stringify({ "name": name, "price": price, "piece1_id": piece1_id, "piece2_id": piece2_id, "board_id": board_id}));
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        const objects = JSON.parse(this.responseText);
        Swal.fire(objects['message']);
        loadTable();
        }
        };
    }
    
    function showThemeEditBox(id) {
        console.log(id);
        const xhttp = new XMLHttpRequest();
        xhttp.open("GET", "http://localhost:5000/themes/"+id);
        xhttp.send();
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
            loadTable();
            }
        };
    }
    
    function themeDelete(id) {
        const xhttp = new XMLHttpRequest();
        xhttp.open("DELETE", "http://localhost:5000/themes/"+id);
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.send(JSON.stringify({ 
            "id": id
        }));
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
            const objects = JSON.parse(this.responseText);
            Swal.fire(objects['message']);
            loadTable();
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
    
    function uploadFile(id) {
        return new Promise((resolve, rejected) => {
            var files = document.getElementById(id).files;
            if(files.length > 0 ){
            var formData = new FormData();
            formData.append("file", files[0]);
            var xhttp = new XMLHttpRequest();
            // Set POST method and ajax file path
            xhttp.open("POST", "http://localhost/backoffice/ajaxfile.php", true);
            xhttp.setRequestHeader('Access-Control-Allow-Origin', '*');
            xhttp.setRequestHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
            xhttp.setRequestHeader('Access-Control-Allow-Headers', 'Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers');
            // call on request changes state
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var response = this.responseText;
                    resolve(response);
                }
            };
            // Send request with data
            xhttp.send(formData);
            }
        })
    }
*/
    return (
        <div className="Tema">
                <div class="TemaContainer">
                    <div class="d-flex bd-highlight mb-3">
                        <div class="me-auto p-2 bd-highlight"><h2>Temas</h2></div>
                        <div class="p-2 bd-highlight">
                            <button
                            type="button"
                            class="btn btn-primary big-screen-button"
                            id="create"
                            onclick="{showThemeCreateBox()}"
                            >
                            Criar
                            </button>
                            <button
                            type="button"
                            class="btn btn-primary big-screen-button"
                            id="create"
                            onclick="{showCreateChip()}"
                            >
                            Criar Tudo
                            </button>
                        </div>
                    </div>

                    <div class="table-responsive">
                        <table class="table">
                            <thead>
                                <tr>
                                <th scope="col">#</th>
                                <th scope="col">Nome</th>
                                <th scope="col">Preço</th>
                                <th scope="col">Peça1</th>
                                <th scope="col">Peça2</th>
                                <th scope="col">Tabuleiro</th>
                                <th scope="col">Ações</th>
                                </tr>
                            </thead>
                            <tbody id="mytable">
                                <tr>
                                <th scope="row" colspan="5">Carregando...</th>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
        </div>
    )
}