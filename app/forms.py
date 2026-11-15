from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ContactForm(FlaskForm):
    name = StringField(
        "Ваше ім'я",
        validators=[
            DataRequired(message="Введіть своє ім'я."),
            Length(min=2, max=50, message="Ім'я має містити від 2 до 50 символів.")
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Введіть email."),
            Email(message="Введіть коректну email-адресу.")
        ]
    )

    subject = SelectField(
        "Тема звернення",
        choices=[
            ("question", "Запитання"),
            ("cooperation", "Співпраця"),
            ("other", "Інше")
        ],
        validators=[DataRequired(message="Оберіть тему звернення.")]
    )

    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(message="Введіть повідомлення."),
            Length(min=10, max=1000, message="Повідомлення має містити від 10 до 1000 символів.")
        ]
    )

    submit = SubmitField("Надіслати")