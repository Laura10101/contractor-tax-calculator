from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from .models import *
from .services import *
from .views import *
import pytest

client = APIClient()
url = '/api/jurisdictions/'


@pytest.mark.django_db
def test_post_valid_jurisdiction():
    name = 'United Kingdom'

    body = {
        'name': name
    }
    response = client.post(url, body, format='json')
    assert response.status_code == 200
    id = response.data['id']

    assert id is not None

    jurisdiction = Jurisdiction.objects.get(pk=id)
    assert jurisdiction.name == name


@pytest.mark.django_db
def test_post_jurisdiction_with_null_name(rf):
    name = None
    body = {
        'name': name
    }
    response = client.post(url, body, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_jurisdiction_with_integer_name(rf):
    name = 1
    body = {
        'name': name
    }
    response = client.post(url, body, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_jurisdiction_with_short_name(rf):
    name = 'A'
    body = {
        'name': name
    }
    response = client.post(url, body, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_jurisdiction_with_long_name(rf):
    name = '012345678901234567890123456789012345678901234567890123456789'
    body = {
        'name': name
    }
    response = client.post(url, body, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_duplicate_jurisdiction(rf):
    name = 'United Kingdom'
    body = {
        'name': name
    }
    response = client.post(url, body, format='json')
    assert response.status_code == 200

    response = client.post(url, body, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_jurisdiction_with_no_ids():
    request_url = url + '?ids='
    response = client.delete(request_url)
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_jurisdiction_with_string_id():
    ids = ['A']

    request_url = url + '?ids=' + ','.join([str(id) for id in ids])
    response = client.delete(request_url)
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_jurisdiction_with_incorrect_ids_formatting():
    ids = [1, 2, 3, 4]

    request_url = url + '?ids=' + ';'.join([str(id) for id in ids])
    response = client.delete(request_url)
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_jurisdiction():
    name = 'My Test Jurisdiction'
    id = create_jurisdiction(name)
    jurisdiction = Jurisdiction.objects.get(pk=id)
    assert jurisdiction.name == name
    ids = [id]

    request_url = url + '?ids=' + ','.join([str(id) for id in ids])
    response = client.delete(request_url)
    assert response.status_code == 200

    assert Jurisdiction.objects.filter(pk__in=ids).count() == 0


@pytest.mark.django_db
def test_get_empty_jurisdictions_list(rf):
    response = client.get(url)
    jurisdictions = response.data['jurisdictions']
    assert len(jurisdictions) == 0


@pytest.mark.django_db
def test_get_list_with_single_jurisdiction(rf):
    name = 'My Test Jurisdiction'
    id = create_jurisdiction(name)
    response = client.get(url)
    jurisdictions = response.data['jurisdictions']
    assert len(jurisdictions) == 1
    assert jurisdictions[0]['name'] == name
    assert jurisdictions[0]['id'] == id


@pytest.mark.django_db
def test_get_list_with_multiple_jurisdictions(rf):
    names = ['USA', 'United Kingdom', 'Thailand', 'Dubai', 'Hong Kong']
    jurisdiction_ids = {}
    for name in names:
        jurisdiction_ids[name] = create_jurisdiction(name)

    response = client.get(url)
    print(response.data)
    jurisdictions = response.data['jurisdictions']

    assert len(jurisdictions) == len(names)
    for jurisdiction in jurisdictions:
        print(jurisdiction)
        assert jurisdiction['name'] in names
        assert jurisdiction['id'] == jurisdiction_ids[jurisdiction['name']]
