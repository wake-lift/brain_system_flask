import datetime
import random

from . import session_factory
from .models import Question

MAX_SET_JEOPARDY = None
MAX_SET_BRAIN = None
MAX_SET_WWW = None
LAST_REFRESH = datetime.datetime.now()
REFRESH_INTERVAL = datetime.timedelta(hours=8)
SET_FOR_RANDOMIZING: int = 5000


def get_max_question_sets():
    """Пересчитывает количество вопросов в БД по трем категориям через
    заданный в параметре REFRESH_INTERVAL интервал времени."""
    global MAX_SET_WWW, MAX_SET_BRAIN, MAX_SET_JEOPARDY, LAST_REFRESH
    if (
        not all([MAX_SET_JEOPARDY, MAX_SET_BRAIN, MAX_SET_WWW,])
        or (datetime.datetime.now() - LAST_REFRESH > REFRESH_INTERVAL)
    ):
        with session_factory() as sf:
            MAX_SET_WWW = sf.query(Question).filter(Question.question_type == 'Ч').count()
            MAX_SET_BRAIN = sf.query(Question).filter(Question.question_type == 'Б').count()
            MAX_SET_JEOPARDY = sf.query(Question).filter(Question.question_type == 'Я').count()
        LAST_REFRESH = datetime.datetime.now()
    return {
        'Ч': MAX_SET_WWW,
        'Б': MAX_SET_BRAIN,
        'Я': MAX_SET_JEOPARDY
    }


def get_initial_queryset(question_type):
    """Формирует первоначальный список вопросов с учетом типа вопроса и
    заданного константой "SET_FOR_RANDOMIZING" размера выборки.
    Функция необходима для ускорения запросов к БД."""
    with session_factory() as sf:
        queryset = sf.query(Question).filter(
            Question.question_type == question_type,
            Question.condemned == 0,
            Question.is_published == 1
        ).all()
        start_point = random.randint(
            0,
            get_max_question_sets()[question_type] - SET_FOR_RANDOMIZING - 1
        )
    return queryset[start_point: start_point + SET_FOR_RANDOMIZING]
