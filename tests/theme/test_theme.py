import json
import logging
from flask import url_for, current_app

logging.basicConfig(level=logging.NOTSET)


def test_rota_errada_retorna_404(client):
    assert client.get(r'/url_nao_existente').status_code == 404


def test_cria_novo_tema(client, unauthenticated_headers, theme_db):
    # garante que o tema seja novo, apagando-o se já existir
    username = 'm1ayc.ol'
    user = theme_db.query.filter_by(username=username).first()
    if user is not None:
        client.application.db.session.delete(user)
        client.application.db.session.commit()

    payload = json.dumps({
        "username": username,
        "principal_email": "may3con@gmail.com",
        "secondary_email": "mayc3on@uol.com.br",
        "first_name": "Mafycon",
        "last_name": "da Silvfa",
        "password": "#$@$#a1!@#3$%34*__s23da4sd6a1!@#sASDd6gdfm<M5as4d89a",
        "default_theme": 1,
        "active": True,
        "avatar_url": "https://cdn.pixabay.com/photo/2021/06/07/13/46/user-6318008_960_720.png"
    })

    result = client.post(url_for('bp_theme.register', _external=True), headers=unauthenticated_headers, data=payload)
    assert result.status_code == 201


def test_deve_falhar_por_falta_de_username(client, unauthenticated_headers):
    payload = json.dumps({
        "principal_email": "may3con@gmail.com",
        "secondary_email": "mayc3on@uol.com.br",
        "first_name": "Mafycon",
        "last_name": "da Silvfa",
        "password": "#$@$#a1!@#3$%34*__s23da4sd6a1!@#sASDd6gdfm<M5as4d89a",
        "default_theme": 0,
        "active": True,
        "avatar_url": "https://cdn.pixabay.com/photo/2021/06/07/13/46/user-6318008_960_720.png"
    })

    result = client.post(url_for('bp_theme.register', _external=True), headers=unauthenticated_headers, data=payload)
    assert result.status_code == 301


def test_deve_falhar_por_erro_no_db_constraint_unique(client, unauthenticated_headers):
    payload = {
        "username": "m1ayc.ol",
        "principal_email": "may3con@gmail.com",
        "secondary_email": "mayc3on@uol.com.br",
        "first_name": "Mafycon",
        "last_name": "da Silvfa",
        "password": "#$@$#a1!@#3$%34*__s23da4sd6a1!@#sASDd6gdfm<M5as4d89a",
        "default_theme": 1,
        "active": True,
        "avatar_url": "https://cdn.pixabay.com/photo/2021/06/07/13/46/user-6318008_960_720.png"
    }
    # import ipdb;ipdb.set_trace()

    result = client.post(url_for('bp_theme.register', _external=True), headers=unauthenticated_headers, data=payload)
    logging.info(result.json)
    # print(result.json)
    assert result.status_code == 500
    assert result.json.get('message') == 'Fail Creation'


def test_deve_retornar_token_valido(client, user_db, unauthenticated_headers):
    # test_cria_novo_usuario(client, models)
    payload = json.dumps({
        "username": "m1ayc.ol",
        "password": "#$@$#a1!@#3$%34*__s23da4sd6a1!@#sASDd6gdfm<M5as4d89a",
    })

    result = client.post(url_for('bp_user.login', _external=True), headers=unauthenticated_headers, data=payload)
    logging.info(result.json.get('message'))
    assert result.json.get('message') == r'success'
    assert result.json.get('token') is not None
    assert result.json.get('refresh_token') is not None
    assert result.status_code == 200
