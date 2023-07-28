from fastapi.testclient import TestClient
from ..main import app
from ..database import Base, engine
from sqlalchemy.orm import sessionmaker
import pytest


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)  # Drop all existing tables before each test
Base.metadata.create_all(bind=engine)

# Use a pytest fixture to create a clean database for each test
@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)

prefix = "api/v1"


# MENU CRUD


def test_create_menu():

    menu_data = {
        "title": "Sample Menu",
        "description": "Menu Description"
    }
    response = client.post(f"{prefix}/menus/", json=menu_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Sample Menu"
    assert "id" in response.json()



def test_read_menus():
   
    menu_data = {
        "title": "Sample Menu 2",
        "description": "Menu Description 2"
    }
    response = client.post(f"{prefix}/menus/", json=menu_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Sample Menu 2"
    assert "id" in response.json()

    response = client.get(f"{prefix}/menus/")
    assert response.status_code == 200
    menus_list = response.json()
    assert isinstance(menus_list, list)


    titles = [menu["title"] for menu in menus_list]
   
    expected_titles = ["Sample Menu", "Sample Menu 2"]
    assert titles == expected_titles



def test_read_menu():
    menu_id = 1
    
    response = client.get(f"{prefix}/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Sample Menu"




def test_update_menu():
    menu_data = {
        "title": "Sample Menu 1 Updated",
        "description": "Menu Description"
    }

    menu_id = 1

    response = client.patch(f"{prefix}/menus/{menu_id}", json=menu_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Sample Menu 1 Updated"
    assert "id" in response.json()



def test_delete_menu():
    menu_id = 2

    response = client.delete(f"{prefix}/menus/{menu_id}")

    
    response = client.get(f"{prefix}/menus/{menu_id}")
    assert response.status_code == 404

    menu_data = {
        "title": "Sample Menu 2",
        "description": "Menu Description 2"
    }
    response = client.post(f"{prefix}/menus/", json=menu_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Sample Menu 2"
    assert "id" in response.json()


# SUBMENU CRUD


def test_create_submenu():

    submenu_data = {
        "title": "Sample Submenu",
        "description": "Submenu Description"
    }
    menu_id = 3

    response = client.post(f"{prefix}/menus/{menu_id}/submenus", json=submenu_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Sample Submenu"
    assert "id" in response.json()



def test_read_submenus():
   
    menu_id = 3

    submenu_data = {
        "title": "Sample Submenu 2",
        "description": "Submenu Description 2"
    }
    response = client.post(f"{prefix}/menus/{menu_id}/submenus", json=submenu_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Sample Submenu 2"
    assert "id" in response.json()

    response = client.get(f"{prefix}/menus/{menu_id}/submenus")
    assert response.status_code == 200
    submenus_list = response.json()
    assert isinstance(submenus_list, list)


    titles = [submenu["title"] for submenu in submenus_list]
   
    expected_titles = ["Sample Submenu", "Sample Submenu 2"]
    assert titles == expected_titles



def test_read_submenu():
    menu_id = 3
    submenu_id = 1
    
    response = client.get(f"{prefix}/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Sample Submenu"




def test_update_submenu():
    submenu_data = {
        "title": "Sample Submenu 1 Updated",
        "description": "Submenu Description"
    }

    menu_id = 3
    submenu_id = 1

    response = client.patch(f"{prefix}/menus/{menu_id}/submenus/{submenu_id}", json=submenu_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Sample Submenu 1 Updated"
    assert "id" in response.json()



def test_delete_submenu():
    menu_id = 3
    submenu_id = 2

    response = client.delete(f"{prefix}/menus/{menu_id}/submenus/{submenu_id}")

    
    response = client.get(f"{prefix}/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 404


    submenu_data = {
        "title": "Sample Submenu 2",
        "description": "Submenu Description 2"
    }
    response = client.post(f"{prefix}/menus/{menu_id}/submenus", json=submenu_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Sample Submenu 2"
    assert "id" in response.json()



# DISH CRUD


def test_create_dish():

    menu_id = 3
    submenu_id = 3

    dish_data = {
        "title": "Dish",
        "description": "Dish Description",
        "price": "20.70"
    }
    response = client.post(f"{prefix}/menus/{menu_id}/submenus/{submenu_id}/dishes", json=dish_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Dish"
    assert "id" in response.json()



def test_read_dishes():

    menu_id = 3
    submenu_id = 3
   
    dish_data = {
        "title": "Dish 2",
        "description": "Dish Description 2",
        "price": "2.50"
    }
    response = client.post(f"{prefix}/menus/{menu_id}/submenus/{submenu_id}/dishes", json=dish_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Dish 2"
    assert "id" in response.json()

    response = client.get(f"{prefix}/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.status_code == 200
    dishes_list = response.json()
    assert isinstance(dishes_list, list)


    titles = [menu["title"] for menu in dishes_list]
   
    expected_titles = ["Dish", "Dish 2"]
    assert titles == expected_titles



def test_read_dish():

    menu_id = 3
    submenu_id = 3
    dish_id = 1
    
    response = client.get(f"{prefix}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Dish"




def test_update_dish():
    dish_data = {
        "title": "Dish 1 Updated",
        "description": "Dish Description",
        "price": "15.70"
    }

    menu_id = 3
    submenu_id = 3
    dish_id = 1

    response = client.patch(f"{prefix}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", json=dish_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Dish 1 Updated"
    assert "id" in response.json()



def test_delete_dish():

    menu_id = 3
    submenu_id = 3
    dish_id = 2

    response = client.delete(f"{prefix}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")

    
    response = client.get(f"{prefix}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 404

    dish_data = {
        "title": "Dish 2",
        "description": "Dish Description 2",
        "price": "2.50"
    }
    response = client.post(f"{prefix}/menus/{menu_id}/submenus/{submenu_id}/dishes", json=dish_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Dish 2"
    assert "id" in response.json()





# SUBMENU COUNT


def test_count_submenus():
   
    menu_id = 3

    response = client.get(f"{prefix}/menus/{menu_id}")
    assert response.status_code == 200

    menu = response.json()

    submenu_count = len(menu["submenus"])

    assert submenu_count == 2



# DISH COUNT



def test_count_dishes():

    menu_id = 3
    submenu_id = 3

    dish_data = {
        "title": "Dish 3",
        "description": "Dish Description 3",
        "price": "12.50"
    }
    response = client.post(f"{prefix}/menus/{menu_id}/submenus/{submenu_id}/dishes", json=dish_data)
   
    response = client.get(f"{prefix}/menus/{menu_id}")
    assert response.status_code == 200

    menu = response.json()

    dish_count = sum(len(submenu["dishes"]) for submenu in menu["submenus"])

    assert dish_count == 3