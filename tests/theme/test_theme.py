import json
import logging
from flask import url_for, current_app

logging.basicConfig(level=logging.NOTSET)


def test_rota_errada_retorna_404(client):
    assert client.get(r'/url_nao_existente').status_code == 404


def test_cria_novo_tema(client, unauthenticated_headers, theme_db):
    payload = json.dumps(
        {
            "name": 'pokemón',
            "price": 0,
            "chip1_id": 2,
            "chip2_id": 1,
            "board_id": 1
        }
    )

    result = client.post(url_for('bp_theme.create', _external=True), headers=unauthenticated_headers, data=payload)
    assert result.status_code == 201


def test_deve_falhar_por_falta_de_name(client, unauthenticated_headers):
    payload = json.dumps(
        {
            "name": 'pokemón',
            "price": 0,
            "chip1_id": 2,
            "chip2_id": 1,
            "board_id": 1
        }
    )
    result = client.post(url_for('bp_theme.create', _external=True), headers=unauthenticated_headers, data=payload)
    assert result.status_code == 301


def test_deve_falhar_por_erro_no_db_constraint_unique(client, unauthenticated_headers):
    payload = json.dumps(
        {
            "name": 'pokemón',
            "price": 0,
            "chip1_id": 2,
            "chip2_id": 1,
            "board_id": 1
        }
    )
    # import ipdb;ipdb.set_trace()

    result = client.post(url_for('bp_theme.create', _external=True), headers=unauthenticated_headers, data=payload)
    logging.info(result.json)
    # print(result.json)
    assert result.status_code == 500
    assert result.json.get('message') == 'Fail Creation'

