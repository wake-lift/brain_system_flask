import random

from flask import abort, flash, render_template, request, send_file, session
import pandas as pd
from sqlalchemy import and_

from . import app, session_factory, simple_captcha
from .forms import FeedbackForm, QuestionForm, QuestionAddForm
from .models import BoughtInProduct, Feedback, Question
from .services import get_initial_queryset


@app.route('/')
def index_view():
    return render_template('common_pages/main.html')


@app.route('/legal/')
def legal_view():
    return render_template('common_pages/legal.html')


@app.route('/feedback/', methods=['GET', 'POST'])
def feedback_view():
    form = FeedbackForm()
    captcha = simple_captcha.create()
    context = {'form': form, 'captcha': captcha}
    if request.method == 'POST':
        if form.validate_on_submit():
            c_hash = request.form.get('captcha-hash')
            c_text = request.form.get('captcha-text')
            if simple_captcha.verify(c_text, c_hash):
                feedback = Feedback(
                    name=form.name.data,
                    email=form.email.data,
                    feedback_text=form.feedback_text.data
                )
                with session_factory() as sf:
                    sf.add(feedback)
                    sf.commit()
                context['form_saved'] = True
            else:
                flash('Введенные символы не совпадают с изображением')
    else:
        context['form_saved'] = False
    return render_template('common_pages/feedback.html', **context)


@app.route('/brain_system/operating-principle/')
def operating():
    return render_template('brain_system/operating_principle.html')


@app.route('/brain_system/electric-schematics/')
def circuit():
    return render_template('brain_system/circuit.html')


@app.route('/brain_system/pcb/')
def pcb():
    return render_template('brain_system/pcb.html')


@app.route('/brain_system/printed-parts/')
def printed():
    return render_template('brain_system/printed_parts.html')


@app.route('/brain_system/bought-in-products/')
def bought():
    with session_factory() as sf:
        product_list = sf.query(BoughtInProduct).all()
    return render_template(
        'brain_system/bought_in_products.html',
        product_list=product_list
    )


@app.route('/brain_system/export_model_to_ods/')
def export_model_to_ods():
    with session_factory() as sf:
        products = sf.query(BoughtInProduct).all()
    if not products:
        abort(500)
    products_list = []
    for product in products:
        product_dict = {
            'Название': product.name,
            'Входит в состав': product.a_part_of.name,
            'Кол-во': product.quantity,
            'Тип': product.product_type,
            'Ссылки': '\n'.join(_.link for _ in product.link_for_product),
            'Комментарий': product.comment
        }
        products_list.append(product_dict)
    df = pd.DataFrame(products_list)
    file_path = app.config['UPLOAD_DIR'] + '/brain_system_BOM.ods'
    with pd.ExcelWriter(file_path, engine='odf') as doc:
        df.to_excel(doc, sheet_name='Bought-in poducts')
    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        abort(500)


@app.route('/brain_system/firmware/')
def firmware():
    return render_template('brain_system/firmware.html')


@app.route('/questions/', methods=['GET', 'POST'])
def questions():
    form = QuestionForm()
    context = {'form': form}
    if request.method == 'POST':
        """Обработка запроса при отправке пользователем заполненной формы."""
        form = QuestionForm()
        if form.validate_on_submit():
            with session_factory() as sf:
                if form.search_pattern.data:
                    questions = sf.query(Question).filter(and_(
                        Question.question.contains(form.search_pattern.data),
                        Question.question_type == form.question_type.data,
                        Question.condemned == 0,
                        Question.is_published == 1,
                    )
                    ).all()
                else:
                    questions = get_initial_queryset(
                        form.question_type.data
                    )
            questions_quantity = min(
                form.questions_quantity.data,
                len(questions)
            )
            questions = random.choices(questions, k=questions_quantity)
            context['questions'] = questions
    return render_template('questions/questions.html', **context)


@app.route('/questions/add/', methods=['GET', 'POST'])
def add_question():
    form = QuestionAddForm()
    captcha = simple_captcha.create()
    context = {'form': form, 'captcha': captcha}
    if request.method == 'POST':
        if form.validate_on_submit():
            c_hash = request.form.get('captcha-hash')
            c_text = request.form.get('captcha-text')
            if simple_captcha.verify(c_text, c_hash):
                question = Question(
                    package=form.package.data,
                    tour=form.tour.data,
                    number=form.number.data,
                    question_type=form.question_type.data,
                    question=form.question.data,
                    answer=form.answer.data,
                    pass_criteria=form.pass_criteria.data,
                    authors=form.authors.data,
                    sources=form.sources.data,
                    comments=form.comments.data,
                )
                with session_factory() as sf:
                    sf.add(question)
                    sf.commit()
                context['form_saved'] = True
            else:
                flash('Введенные символы не совпадают с изображением')
    else:
        context['form_saved'] = False
    return render_template('questions/add_question.html', **context)


@app.route('/questions/telegram-bot/')
def tg_bot():
    return render_template('questions/tg_bot.html')


@app.route('/api/v1/info/')
def api_info():
    return 'api_info'
