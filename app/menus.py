
from typing import List
from app import schemas
from app import models
from app.crud import CRUD
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from app.database import get_db



router = APIRouter()




menu_crud = CRUD(item_class_menu=models.Menu, item_class_submenu=models.SubMenu, item_class_dish=models.Dish)


# MENU


@router.post('/menus/', status_code=201, response_model=schemas.Menu)
async def create_menu(item_schema:schemas.MenuCreate, db: Session = Depends(get_db)):
    new_menu = menu_crud.create_item(db=db, item_schema=item_schema)
    return new_menu

@router.get('/menus/', response_model=List[schemas.MenuReponse])
async def read_menus(db: Session = Depends(get_db),  limit: int = 10, page: int = 1, search: str = ''):
    item = 'menu'
    menus = menu_crud.read_items(db=db, limit=limit, page=page, search=search, item=item)
    for menu in menus:
        menu.submenus_count = len(menu.submenus)
        menu.dishes_count = sum(len(submenu.dishes) for submenu in menu.submenus)
    return menus

@router.get('/menus/{menu_id}', response_model=schemas.MenuReponse)
async def read_menu(menu_id: int, db: Session = Depends(get_db)):
    item = 'menu'
    menu = menu_crud.read_item(db=db, item_id=menu_id, item=item)
    
    menu.submenus_count = len(menu.submenus)
    menu.dishes_count = sum(len(submenu.dishes) for submenu in menu.submenus)

    return menu


@router.patch('/menus/{menu_id}', response_model=schemas.Menu)
async def update_menu(menu_id: int, item_schema:schemas.MenuUpdate, db: Session = Depends(get_db)):
    item = 'menu'
    updated_menu = menu_crud.update_item(db=db, item_schema=item_schema, item_id=menu_id, item=item)
    return updated_menu


@router.delete('/menus/{menu_id}')
async def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    item = 'menu'
    return menu_crud.delete_item(db=db, item_id=menu_id, item=item)



# SUBMENU



@router.post('/menus/{menu_id}/submenus', status_code=201, response_model=schemas.SubMenu)
async def create_submenu(menu_id: int, item_schema:schemas.SubMenuCreate, db: Session = Depends(get_db)):
    new_submenu = menu_crud.create_item(db=db, item_schema=item_schema, menu_id=menu_id)
    return new_submenu

@router.get('/menus/{menu_id}/submenus', response_model=List[schemas.SubMenuReponse])
async def read_submenus(db: Session = Depends(get_db),  limit: int = 10, page: int = 1, search: str = ''):
    item = 'submenu'
    submenus = menu_crud.read_items(db=db, limit=limit, page=page, search=search, item=item)
    for submenu in submenus:
        submenu.dishes_count = len(submenu.dishes)
    return submenus

# For validation preferably

# @router.get('/menus/{menu_id}/submenus', response_model=List[schemas.SubMenuReponse])
# async def read_submenus(menu_id: int, db: Session = Depends(get_db),  limit: int = 10, page: int = 1, search: str = ''):
#     item = 'submenu'
#     submenus = menu_crud.read_items(db=db, menu_id=menu_id, limit=limit, page=page, search=search, item=item)
#     for submenu in submenus:
#         submenu.dishes_count = len(submenu.dishes)
#     return submenus

@router.get('/menus/{menu_id}/submenus/{submenu_id}', response_model=schemas.SubMenuReponse)
async def read_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    item = 'submenu'
    submenu = menu_crud.read_item(db=db, menu_id=menu_id, item_id=submenu_id, item=item)
    submenu.dishes_count = len(submenu.dishes)
    return submenu


@router.patch('/menus/{menu_id}/submenus/{submenu_id}', response_model=schemas.SubMenu)
async def update_submenu(menu_id: int, submenu_id: int, item_schema:schemas.SubMenuUpdate, db: Session = Depends(get_db)):
    item = 'submenu'
    updated_menu = menu_crud.update_item(db=db, item_schema=item_schema, menu_id=menu_id, item_id=submenu_id,  item=item)
    return updated_menu


@router.delete('/menus/{menu_id}/submenus/{submenu_id}')
async def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    item = 'submenu'
    return menu_crud.delete_item(db=db, menu_id=menu_id, item_id=submenu_id, item=item)



# DISH



@router.post('/menus/{menu_id}/submenus/{submenu_id}/dishes/', status_code=201, response_model=schemas.Dish)
async def create_dish(menu_id: int, submenu_id: int, item_schema:schemas.DishCreate, db: Session = Depends(get_db)):
    new_dish = menu_crud.create_item(db=db, item_schema=item_schema, menu_id=menu_id, submenu_id=submenu_id)
    return new_dish

@router.get('/menus/{menu_id}/submenus/{submenu_id}/dishes/', response_model=List[schemas.Dish])
async def read_dishes(db: Session = Depends(get_db),  limit: int = 10, page: int = 1, search: str = ''):
    item = 'dish'
    dishes = menu_crud.read_items(db=db, limit=limit, page=page, search=search, item=item)
    return dishes
 
# For validation preferably

# @router.get('/menus/{menu_id}/submenus/{submenu_id}/dishes/', response_model=List[schemas.Dish])
# async def read_dishes(menu_id: int, submenu_id: int, db: Session = Depends(get_db),  limit: int = 10, page: int = 1, search: str = ''):
#     item = 'dish'
#     dishes = menu_crud.read_items(db=db, menu_id=menu_id, submenu_id=submenu_id, limit=limit, page=page, search=search, item=item)
#     return dishes

@router.get('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=schemas.Dish)
async def read_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    item = 'dish'
    dish = menu_crud.read_item(db=db, item_id=dish_id, submenu_id=submenu_id, menu_id=menu_id, item=item)
    return dish


@router.patch('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=schemas.Dish)
async def update_dish(menu_id: int, submenu_id: int, dish_id: int, item_schema:schemas.DishUpdate, db: Session = Depends(get_db)):
    item = 'dish'
    updated_dish = menu_crud.update_item(db=db, item_id=dish_id, submenu_id=submenu_id, menu_id=menu_id, item_schema=item_schema, item=item)
    return updated_dish



@router.delete('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    item = 'dish'
    return menu_crud.delete_item(db=db, item_id=dish_id, submenu_id=submenu_id, menu_id=menu_id, item=item)



