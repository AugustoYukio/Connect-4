import React from "react";
import './Peca.css'

export default () => {
    return (
      <div className="Peca">
              <div class="PecaContainer">
                  <div class="d-flex bd-highlight mb-3">
                      <div class="me-auto p-2 bd-highlight"><h2>Peça</h2></div>
                      <div class="p-2 bd-highlight">
                          <button
                            type="button"
                            class="btn btn-primary big-screen-button"
                            id="create"
                            onclick="showChipCreateBox()">
                            Criar
                          </button>
                      </div>
                  </div>

                  <div class="table-responsive">
                      <table class="table">
                          <thead>
                              <tr>
                              <th scope="col">#</th>
                              <th scope="col">Nome</th>
                              <th scope="col">URL</th>
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