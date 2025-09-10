from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert


def test_ola_mundo_html_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/ola-mundo-html')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert (
        response.text
        == """
    <html>
        <head>
            <title>Pagina de Ola Mundo HTML</title>
        </head>
        <body>
         <h1>Olá Mundo!</h1>
        </body>
    </html>
    """
    )  # Assert
