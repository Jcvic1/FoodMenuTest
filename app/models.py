from app.database import Base
from sqlalchemy import Column, String, Numeric, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String, index=True) 

    submenus = relationship("SubMenu", back_populates="menu", cascade="all, delete", passive_deletes=True)


class SubMenu(Base):
    __tablename__ = 'submenus'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String, index=True) 
    menu_id = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'))

    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu', cascade="all, delete", passive_deletes=True)


class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String, index=True) 
    price = Column(Numeric(5, 2))
    submenu_id = Column(Integer, ForeignKey('submenus.id', ondelete='CASCADE'))

    submenu = relationship('SubMenu', back_populates='dishes')
