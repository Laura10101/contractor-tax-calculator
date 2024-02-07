from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import *
from .services import *
import pytest


@pytest.mark.django_db
def test_create_valid_jurisdiction():
    name = 'United Kingdom'
    id = create_jurisdiction(name=name)
    assert id is not None

    jurisdiction = Jurisdiction.objects.get(pk=id)
    assert jurisdiction.name == name


@pytest.mark.django_db
def test_create_jurisdiction_with_null_name():
    name = None
    with pytest.raises(ValidationError):
        id = create_jurisdiction(name=name)


@pytest.mark.django_db
def test_create_jurisdiction_with_integer_name():
    name = 1
    with pytest.raises(ValidationError):
        id = create_jurisdiction(name=name)


@pytest.mark.django_db
def test_create_jurisdiction_with_short_name():
    name = 'A'
    with pytest.raises(ValidationError):
        id = create_jurisdiction(name=name)


@pytest.mark.django_db
def test_create_jurisdiction_with_long_name():
    name = '012345678901234567890123456789012345678901234567890123456789'
    with pytest.raises(ValidationError):
        id = create_jurisdiction(name=name)


@pytest.mark.django_db
def test_create_duplicate_jurisdiction():
    name = 'United Kingdom'
    id = create_jurisdiction(name=name)
    with pytest.raises(ValidationError):
        id = create_jurisdiction(name=name)


@pytest.mark.django_db
def test_delete_jurisdiction_with_null_dictionary():
    ids = None
    with pytest.raises(TypeError):
        delete_jurisdictions_by_id(ids)


@pytest.mark.django_db
def test_delete_jurisdiction_with_empty_list():
    ids = []
    delete_jurisdictions_by_id(ids)
    assert Jurisdiction.objects.filter(pk__in=ids).count() == 0


@pytest.mark.django_db
def test_delete_jurisdiction_with_non_existent_id():
    ids = [47, 372]
    delete_jurisdictions_by_id(ids)
    assert Jurisdiction.objects.filter(pk__in=ids).count() == 0


@pytest.mark.django_db
def test_delete_valid_jurisdiction():
    name = 'My Test Jurisdiction'
    id = create_jurisdiction(name)
    jurisdiction = Jurisdiction.objects.get(pk=id)
    assert jurisdiction.name == name
    ids = [id]
    delete_jurisdictions_by_id(ids)
    assert Jurisdiction.objects.filter(pk__in=ids).count() == 0


@pytest.mark.django_db
def test_retrieve_empty_jurisdictions_list():
    jurisdictions = get_all_jurisdictions()
    assert jurisdictions.count() == 0


@pytest.mark.django_db
def test_retrieve_list_with_single_jurisdiction():
    name = 'My Test Jurisdiction'
    id = create_jurisdiction(name)
    jurisdictions = get_all_jurisdictions()
    assert jurisdictions.count() == 1
    assert jurisdictions.first().name == name
    assert jurisdictions.first().pk == id


@pytest.mark.django_db
def test_retrieve_list_with_multiple_jurisdictions():
    names = ['USA', 'United Kingdom', 'Thailand', 'Dubai', 'Hong Kong']
    jurisdiction_ids = {}
    for name in names:
        jurisdiction_ids[name] = create_jurisdiction(name)

    jurisdictions = get_all_jurisdictions()
    assert jurisdictions.count() == len(names)
    for jurisdiction in jurisdictions:
        assert jurisdiction.name in names
        assert jurisdiction.pk == jurisdiction_ids[jurisdiction.name]
