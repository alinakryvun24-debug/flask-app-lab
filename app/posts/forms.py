from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    BooleanField,
    DateTimeLocalField,
    SelectField,
    SubmitField
)
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField(
        'Заголовок',
        validators=[
            DataRequired(message='Введіть заголовок.'),
            Length(max=150, message='Максимум 150 символів.')
        ]
    )

    content = TextAreaField(
        'Текст поста',
        validators=[
            DataRequired(message='Введіть текст поста.')
        ]
    )

    enabled = BooleanField(
        'Активний пост',
        default=True
    )

    publish_date = DateTimeLocalField(
        'Дата та час публікації (UTC)',
        format='%Y-%m-%dT%H:%M',
        default=datetime.utcnow,
        validators=[
            DataRequired(message='Вкажіть дату та час.')
        ]
    )

    category = SelectField(
        'Категорія',
        choices=[
            ('news', 'Новини'),
            ('publication', 'Публікація'),
            ('tech', 'Технології'),
            ('other', 'Інше')
        ],
        default='other',
        validators=[DataRequired()]
    )

    submit = SubmitField('Зберегти')


class DeletePostForm(FlaskForm):
    submit = SubmitField('Видалити')