from datetime import datetime
import enum

from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        SmallInteger, String, Text)

from sqlalchemy.orm import declarative_base, declared_attr, relationship


class QuestionType(enum.Enum):
    """Перечень допустимых значений типа вопроса."""
    Б = 'Брейн-ринг'
    ДБ = 'Брейн-ринг (детский)'
    И = 'Вопросы из интернета'
    Л = 'Бескрылка'
    Ч = 'Что-где-когда'
    ЧБ = 'Что-где-когда (тренировки)'
    ЧД = 'Что-где-когда (детский)'
    Э = 'Эрудитка'
    Я = 'Своя игра'


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, autoincrement=True)


Base = declarative_base(cls=PreBase)


class BoughtInProduct(Base):
    """Основная таблица покупных деталей."""
    name = Column(String(64), nullable=False)
    a_part_of_id = Column(
        Integer,
        ForeignKey('boughtinproductasapartof.id', ondelete="SET NULL"),
        nullable=True
    )
    a_part_of = relationship(
        'BoughtInProductAsAPartOf', backref='product', lazy='joined'
    )
    quantity = Column(SmallInteger, nullable=True)
    product_type = Column(String(128),  nullable=True)
    comment = Column(String(512),  nullable=True)
    link_for_product = relationship('BoughtInProductLink', lazy='joined')

    def __str__(self):
        return self.name


class BoughtInProductAsAPartOf(Base):
    """Таблица узлов, в которые входят покупные детали."""
    name = Column(String(64), nullable=False)
    product_as_a_part_of = relationship('BoughtInProduct')

    def __str__(self):
        return self.name


class BoughtInProductLink(Base):
    """Таблица ссылок на покупные детали в интернет-магазинах."""
    product_id = Column(
        Integer,
        ForeignKey('boughtinproduct.id', ondelete="CASCADE"),
        nullable=True
    )
    product = relationship('BoughtInProduct', backref='link')
    link = Column(String(300),  nullable=True)
    link_short_name = Column(String(128),  nullable=True)

    def __str__(self):
        return self.link_short_name


class Feedback(Base):
    """Таблица для сохранения данных,
    полученных через форму обратной связи."""
    name = Column(String(300),  nullable=False)
    email = Column(String(150),  nullable=True)
    feedback_text = Column(Text,  nullable=False)
    date = Column(DateTime, index=True, default=datetime.now)

    def __str__(self):
        return self.name


class Question(Base):
    """Основная таблица с вопросами."""
    package = Column(String(256), nullable=True)
    tour = Column(String(256), nullable=True)
    number = Column(SmallInteger, nullable=True)
    question_type = Column(
        Enum(QuestionType),
        default=QuestionType.Ч,
        index=True
    )
    question = Column(Text,  nullable=False)
    answer = Column(Text,  nullable=False)
    pass_criteria = Column(Text, nullable=True)
    authors = Column(Text, nullable=True)
    sources = Column(Text, nullable=True)
    comments = Column(Text, nullable=True)
    """Вопросы, которые не годятся для выдачи: содержат ссылку на изображение,
    угловые скобки, некодируемый набор символов и т.п."""
    condemned = Column(Boolean, default=False, index=True, nullable=False)
    is_published = Column(Boolean, default=False, index=True, nullable=False)

    def __str__(self):
        return f'{self.question[:75]} ...'
