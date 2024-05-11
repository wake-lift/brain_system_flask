from flask_wtf import FlaskForm
from wtforms import EmailField, IntegerField, RadioField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional
from wtforms.widgets import Select


class FeedbackForm(FlaskForm):
    name = StringField(
        label='Ваше имя',
        validators=[DataRequired(message='Имя - обязательное поле'),
                    Length(1, 128)],
    )
    email = EmailField(
        label='Если вы хотите, чтобы вам ответили - заполните это поле',
        validators=[Email(message=('Введите валидный адрес e-mail или'
                                   ' оставьте поле пустым')),
                    Optional()],
    )
    feedback_text = TextAreaField(
        label='Текст обратной связи',
        validators=[DataRequired(message=('Текст обратной связи'
                                          ' - обязательное поле')),
                    Length(1, 5000)],
    )
    submit = SubmitField(label='Отправить')


class QuestionForm(FlaskForm):
    CHOICES = [
        ('Ч', 'Что-Где-Когда'),
        ('Б', 'Брейн-ринг'),
        ('Я', 'Своя игра'),
    ]
    question_type = RadioField(
        label='Тип вопроса:',
        choices=CHOICES,
        default='Ч',
    )
    search_pattern = StringField(
        label='Поиск по тексту вопроса:',
        description='Не менее трех символов',
        validators=[Length(min=3), Optional()],
    )
    questions_quantity = IntegerField(
        label='Количество вопросов (не более 100):',
        description='не более 100',
        default=10,
        validators=[DataRequired(message='Обязательное поле'),
                    NumberRange(min=1, max=100)],
    )
    # questions_displayed_on_page = IntegerField(
    #     label='Вопросов на странице',
    #     description='не более 36',
    #     default=5,
    #     validators=[NumberRange(min=1, max=36), Optional()],
    # )
    submit = SubmitField(label='Отправить')


class QuestionAddForm(FlaskForm):
    QUESTION_TYPE_CHOICES = [
        ('Б', 'Брейн-ринг'),
        ('ДБ', 'Брейн-ринг (детский)'),
        ('И', 'Вопросы из интернета'),
        ('Л', 'Бескрылка'),
        ('Ч', 'Что-где-когда'),
        ('ЧБ', 'Что-где-когда (тренировки)'),
        ('ЧД', 'Что-где-когда (детский)'),
        ('Э', 'Эрудитка'),
        ('Я', 'Своя игра'),
    ]
    package = StringField(
        label='Название пакета',
        description='Максимальная длина - 256 символов',
        validators=[Length(max=256), Optional()],
    )
    tour = StringField(
        label='Название тура',
        description='Максимальная длина - 256 символов',
        validators=[Length(max=256), Optional()],
    )
    number = IntegerField(
        label='Номер вопроса в пакете',
        validators=[NumberRange(min=1), Optional()],
    )
    question_type = SelectField(
        label='Тип вопроса',
        choices=QUESTION_TYPE_CHOICES,
        default='Ч',
        widget=Select(multiple=True),
    )
    question = TextAreaField(
        label='* Текст вопроса',
        validators=[DataRequired(
            message=('Текст вопроса - обязательное поле')
        ),],
    )
    answer = TextAreaField(
        label='* Ответ на вопрос',
        validators=[DataRequired(
            message=('Ответ на вопрос - обязательное поле')
        ),],
    )
    pass_criteria = TextAreaField(
        label='Критерий правильности ответа',
        validators=[Optional(),],
    )
    authors = TextAreaField(
        label='Автор(ы) вопроса',
        validators=[Optional(),],
    )
    sources = TextAreaField(
        label='Источники',
        validators=[Optional(),],
    )
    comments = TextAreaField(
        label='Комментарий к ответу',
        validators=[Optional(),],
    )
    submit = SubmitField(label='Отправить')
