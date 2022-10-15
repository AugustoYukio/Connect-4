import json
import logging
from flask import url_for, current_app
from sqlalchemy.sql import Select

logging.basicConfig(level=logging.NOTSET)


def test_cria_nova_chip(client, header_with_access_token, chip_db):
    payload = json.dumps({
        "name": 'Pokémon',
        "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-vi"
               "/omegaruby-alphasapphire/shiny/132.png"
    })

    result = client.post(url_for('bp_chip.create', _external=True), headers=header_with_access_token, data=payload)
    assert result.status_code == 201


def test_deve_deletar_um_chip_by_id(client, header_with_access_token, chip_db):

    first_chip = chip_db.query.first()
    if first_chip is None:
        test_cria_nova_chip(client, header_with_access_token, chip_db)
        first_chip = chip_db.query.first()
    payload = json.dumps({'id': first_chip.id})

    result = client.post(url_for('bp_chip.delete', _external=True), headers=header_with_access_token, data=payload)
    assert result.status_code == 202
    assert result.json.get('message') == 'success'


def test_atualiza_um_chip_by_id(client, header_with_access_token, chip_db):

    first_chip = chip_db.query.first()
    if first_chip is None:
        test_cria_nova_chip(client, header_with_access_token, chip_db)
        first_chip = chip_db.query.first()

    payload = json.dumps({
        "name": 'Pokémon_Blue',
        "url": "https://static.pokemonpets.com/images/monsters-images-300-300/10059-Shiny-Mega-Arcanine.webp"
    })
    result = client.post(url_for('bp_chip.update', number=first_chip.id, _external=True), headers=header_with_access_token, data=payload)
    assert result.status_code == 200
    assert result.json.get('message') == "Success Update Chip"
