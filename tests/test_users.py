from http import HTTPStatus

from fast_zero.security import create_access_token


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_username_that_already_exists(client, user):
    response_new_user = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response_new_user.status_code == HTTPStatus.CONFLICT
    assert response_new_user.json() == {'detail': 'Username already exists'}


def test_create_email_that_already_exists(client, user):
    response_new_user = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': user.email,
            'password': 'testtest',
        },
    )

    assert response_new_user.status_code == HTTPStatus.CONFLICT
    assert response_new_user.json() == {'detail': 'Email already exists'}


def test_read_users(client, token):
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'Teste',
                'email': 'teste@test.com',
            },
        ],
    }


def test_read_unique_user(client, user, token):
    response = client.get(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_read_unique_user_not_found(client, token):
    response = client.get(
        '/users/0', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': user.id,
    }


def test_update_integrity_error(client, user, token):
    # Criando um registro para "fausto"
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Alterando o user.name das fixture para fausto
    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or Email already exists'
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_get_current_user_not_found(client):
    data = {'no-email': 'test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_does_not_exist(client):
    data = {'sub': 'teste@test.com'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
