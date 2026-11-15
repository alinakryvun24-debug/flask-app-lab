from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp


class ContactForm(FlaskForm):
    name = StringField(
        "Ім'я",
        validators=[
            DataRequired(message="Введіть ім'я."),
            Length(min=4, max=10, message="Ім'я має містити від 4 до 10 символів.")
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Введіть email."),
            Email(message="Введіть коректну email-адресу.")
        ]
    )

    phone = StringField(
        "Телефон",
        validators=[
            DataRequired(message="Введіть номер телефону."),
            Regexp(
                r'^\+380\d{9}$',
                message="Формат телефону: +380XXXXXXXXX"
            )
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
            Length(max=500, message="Повідомлення не може перевищувати 500 символів.")
        ]
    )

    submit = SubmitField("Надіслати")