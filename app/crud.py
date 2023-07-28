from typing import Optional, Type
from sqlalchemy.orm import Session
from fastapi import HTTPException


class CRUD:
    def __init__(self, item_class_menu: Optional[type] = None, item_class_submenu: Optional[type] = None, item_class_dish: Optional[type] = None):
        self.item_class_menu = item_class_menu
        self.item_class_submenu = item_class_submenu
        self.item_class_dish = item_class_dish

    def create_item(self, db: Session, item_schema: Type, menu_id: int = None, submenu_id: int = None):

        # Dishes

        if menu_id is not None and submenu_id is not None:

            item_query = db.query(self.item_class_menu).filter(
                self.item_class_menu.id == menu_id).first()
            if not item_query:
                raise HTTPException(status_code=404, detail="menu not found")
            else:
                item_query = db.query(self.item_class_submenu).filter(
                    self.item_class_submenu.id == submenu_id).first()
                if not item_query:
                    raise HTTPException(
                        status_code=404, detail="submenu not found")
                else:
                    db_item = self.item_class_dish(
                        **item_schema.dict(), submenu_id=submenu_id)

                    db.add(db_item)
                    db.commit()
                    db.refresh(db_item)
                    return db_item

        # Submenu

        elif menu_id is not None and submenu_id is None:

            item_query = db.query(self.item_class_menu).filter(
                self.item_class_menu.id == menu_id).first()
            if not item_query:
                raise HTTPException(status_code=404, detail="menu not found")
            else:
                db_item = self.item_class_submenu(
                    **item_schema.dict(), menu_id=menu_id)
                db.add(db_item)
                db.commit()
                db.refresh(db_item)
                return db_item

        # Menu

        elif menu_id is None and submenu_id is None:

            db_item = self.item_class_menu(**item_schema.dict())
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return db_item

    def read_item(self, db: Session, item_id: int, item: str, menu_id: int = None, submenu_id: int = None):
        if item == 'menu':
            item_query = db.query(self.item_class_menu).filter(
                self.item_class_menu.id == item_id).first()
            if not item_query:
                raise HTTPException(status_code=404, detail="menu not found")
            return item_query
        elif item == 'submenu':
            item_query = db.query(self.item_class_menu).filter(
                self.item_class_menu.id == menu_id).first()
            if not item_query:
                raise HTTPException(status_code=404, detail="menu not found")
            else:
                item_query = db.query(self.item_class_submenu).filter(
                    self.item_class_submenu.id == item_id).first()
                if not item_query:
                    raise HTTPException(
                        status_code=404, detail="submenu not found")
                return item_query
        elif item == 'dish':
            item_query = db.query(self.item_class_menu).filter(
                self.item_class_menu.id == menu_id).first()
            if not item_query:
                raise HTTPException(status_code=404, detail="menu not found")
            else:
                item_query = db.query(self.item_class_submenu).filter(
                    self.item_class_submenu.id == submenu_id).first()
                if not item_query:
                    raise HTTPException(
                        status_code=404, detail="submenu not found")
                else:
                    item_query = db.query(self.item_class_dish).filter(
                        self.item_class_dish.id == item_id).first()
                    if not item_query:
                        raise HTTPException(
                            status_code=404, detail="dish not found")
                    return item_query

    # For current test

    def read_items(self, db: Session, item: str, limit: int = 20, page: int = 1, search: Optional[str] = None):
        skip = (page - 1) * limit

        if item == 'menu':
            return db.query(self.item_class_menu).filter(self.item_class_menu.title.contains(search)).limit(limit).offset(skip).all()
        elif item == 'submenu':
            return db.query(self.item_class_submenu).filter(self.item_class_submenu.title.contains(search)).limit(limit).offset(skip).all()
        elif item == 'dish':
            return db.query(self.item_class_dish).filter(self.item_class_dish.title.contains(search)).limit(limit).offset(skip).all()

    # For validation preferably

    # def read_items(self, db: Session, item: str, limit: int = 20, page: int = 1, search: Optional[str] = None, menu_id: int = None, submenu_id: int = None):
    #     skip = (page - 1) * limit

    #     if item == 'menu':
    #         return db.query(self.item_class_menu).filter(self.item_class_menu.title.contains(search)).limit(limit).offset(skip).all()
    #     elif item == 'submenu':
    #         item_query = db.query(self.item_class_menu).filter(
    #             self.item_class_menu.id == menu_id).first()
    #         if not item_query:
    #             raise HTTPException(status_code=404, detail="menu not found")
    #         else:
    #             return db.query(self.item_class_submenu).filter(self.item_class_submenu.title.contains(search)).limit(limit).offset(skip).all()
    #     elif item == 'dish':
    #         item_query = db.query(self.item_class_menu).filter(
    #             self.item_class_menu.id == menu_id).first()
    #         if not item_query:
    #             raise HTTPException(status_code=404, detail="menu not found")
    #         else:
    #             item_query = db.query(self.item_class_submenu).filter(
    #                 self.item_class_submenu.id == submenu_id).first()
    #             if not item_query:
    #                 raise HTTPException(
    #                     status_code=404, detail="submenu not found")
    #             else:
    #                 return db.query(self.item_class_dish).filter(self.item_class_dish.title.contains(search)).limit(limit).offset(skip).all()
        
    def update_item(self, db: Session, item_schema: Type, item_id: int, item: str, menu_id: int = None, submenu_id: int = None):

        if item == 'menu':
            item_query = db.query(self.item_class_menu).filter(
                self.item_class_menu.id == item_id)
            db_item = item_query.first()
            if not db_item:
                raise HTTPException(status_code=404, detail="menu not found")
            update_data = item_schema.dict(exclude_unset=True)
            item_query.filter(self.item_class_menu.id == item_id).update(
                update_data, synchronize_session=False)
        elif item == 'submenu':
            item_query = db.query(self.item_class_menu).filter(
                self.item_class_menu.id == menu_id).first()
            if not item_query:
                raise HTTPException(status_code=404, detail="menu not found")
            else:
                item_query = db.query(self.item_class_submenu).filter(
                    self.item_class_submenu.id == item_id)
                db_item = item_query.first()
                if not db_item:
                    raise HTTPException(
                        status_code=404, detail="submenu not found")
                update_data = item_schema.dict(exclude_unset=True)
                item_query.filter(self.item_class_submenu.id == item_id).update(
                    update_data, synchronize_session=False)
        elif item == 'dish':
            item_query = db.query(self.item_class_menu).filter(
                self.item_class_menu.id == menu_id).first()
            if not item_query:
                raise HTTPException(status_code=404, detail="menu not found")
            else:
                item_query = db.query(self.item_class_submenu).filter(
                    self.item_class_submenu.id == submenu_id).first()
                if not item_query:
                    raise HTTPException(
                        status_code=404, detail="submenu not found")
                else:
                    item_query = db.query(self.item_class_dish).filter(
                        self.item_class_dish.id == item_id)
                    db_item = item_query.first()
                    if not db_item:
                        raise HTTPException(
                            status_code=404, detail="dish not found")
                    update_data = item_schema.dict(exclude_unset=True)
                    item_query.filter(self.item_class_dish.id == item_id).update(
                        update_data, synchronize_session=False)

        db.commit()
        db.refresh(db_item)
        return db_item

    def delete_item(self, db: Session, item_id: int, item: str, menu_id: int = None, submenu_id: int = None):
        if item == 'menu':
            item_query = db.query(self.item_class_menu).filter(
                self.item_class_menu.id == item_id).first()
            if not item_query:
                raise HTTPException(status_code=404, detail="menu not found")
            db.query(self.item_class_menu).filter(
                self.item_class_menu.id == item_id).delete(synchronize_session=False)
        elif item == 'submenu':
            item_query = db.query(self.item_class_menu).filter(
                self.item_class_menu.id == menu_id).first()
            if not item_query:
                raise HTTPException(status_code=404, detail="menu not found")
            else:
                item_query = db.query(self.item_class_submenu).filter(
                    self.item_class_submenu.id == item_id).first()
                if not item_query:
                    raise HTTPException(
                        status_code=404, detail="submenu not found")
                db.query(self.item_class_submenu).filter(
                    self.item_class_submenu.id == item_id).delete(synchronize_session=False)
        elif item == 'dish':
            item_query = db.query(self.item_class_menu).filter(
                self.item_class_menu.id == menu_id).first()
            if not item_query:
                raise HTTPException(status_code=404, detail="menu not found")
            else:
                item_query = db.query(self.item_class_submenu).filter(
                    self.item_class_submenu.id == submenu_id).first()
                if not item_query:
                    raise HTTPException(
                        status_code=404, detail="submenu not found")
                else:
                    item_query = db.query(self.item_class_dish).filter(
                        self.item_class_dish.id == item_id).first()
                    if not item_query:
                        raise HTTPException(
                            status_code=404, detail="dish not found")
                    db.query(self.item_class_dish).filter(
                        self.item_class_dish.id == item_id).delete(synchronize_session=False)

        db.commit()
 