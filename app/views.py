import logging
from pathlib import Path

from flask import render_template, request, flash, redirect, url_for
from app import app
from app.forms import ContactForm


# Налаштування запису повідомлень у файл
log_file = Path(__file__).resolve().parent.parent / 'contact_messages.log'

contact_logger = logging.getLogger('contact_messages')
contact_logger.setLevel(logging.INFO)

if not contact_logger.handlers:
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    )
    contact_logger.addHandler(file_handler)


@app.route('/')
@app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')


@app.route('/contact', methods=['GET', 'POST'])
@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():
        contact_logger.info(
    "Ім'я: %s | Email: %s | Телефон: %s | Тема: %s | Повідомлення: %s",
    form.name.data,
    form.email.data,
    form.phone.data,
    form.subject.data,
    form.message.data
)

        flash('Ваше повідомлення успішно надіслано!', 'success')
        return redirect(url_for('contacts'))

    if request.method == 'POST':
        flash('Не вдалося надіслати повідомлення. Перевірте правильність заповнення форми.', 'danger')

    return render_template(
        'contacts.html',
        title='Контакти',
        form=form
    )


@app.route('/homepage')
def home():
    agent = request.user_agent
    return render_template('homepage.html', title='Головна', agent=agent)