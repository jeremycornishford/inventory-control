import pytest

from inventory_control import storage

def get_config():
    """
    Create my simple localhost config
    :return:
    """

    config = {'host': 'localhost', 'user': 'wce',
              'password': 'thispasswordisobjectivelyterrible',
              'db': 'inventory_control'}
    return config


def test_integration_storage():

    engine = storage.StorageEngine(config=get_config())
    result = engine.cursor.execute("SELECT COUNT(*) FROM test")
    assert result == 1

    try:
        #engine._drop_tables()
        engine._create_tables()
        res = engine.cursor.execute("SELECT * FROM components")
        assert res == 0
        res = engine.cursor.execute("SELECT * FROM projects")
        assert res == 0
    except Exception as ex:
        print(ex)
    finally:
        engine._drop_tables()

def test_integration_component_creation():
    """
    Create a component type, get it, and delete it.
    :return:
    """

    name = 'some_name'
    engine = storage.StorageEngine(config=get_config())
    try:
        engine._create_tables()
        engine.add_component_type(type_name=name)
        result = engine.get_component_type(type_name=name)
        assert result['type'] == name
        engine.remove_component_type(type_name=name)
        result = engine.get_component_type(type_name=name)
        assert result is None
    finally:
        engine._drop_tables()


def test_project():
    """
    Create a project, delete a project, and possibly
    rank them in order

    :return:
    """
    engine = storage.StorageEngine(config=get_config())
    project_number = 1001
    try:
        engine._create_tables()
        engine.add_project(project_number=project_number)
        engine.delete_project(project_number=project_number)
    finally:
        engine._drop_tables()