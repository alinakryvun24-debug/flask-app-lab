
from flask import render_template, abort, redirect, url_for, flash
from pathlib import Path
from datetime import datetime
from uuid import uuid4

from . import products_bp
from .database import products_table
from .forms import ProductForm, DeleteProductForm


UPLOAD_FOLDER = Path(__file__).resolve().parent / 'static' / 'uploads'
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


@products_bp.route('/')
def list_products():
    products = products_table.all()

    return render_template(
        'products/products.html',
        products=products
    )


@products_bp.route('/<int:product_id>')
def product_detail(product_id):
    product = products_table.get(
        lambda p: p['id'] == product_id
    )

    if product is None:
        abort(404)

    return render_template(
        'products/detail_product.html',
        product=product,
        delete_form=DeleteProductForm()
    )


@products_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()

    if form.validate_on_submit():
        products = products_table.all()
        product_id = max(
            (product['id'] for product in products),
            default=0
        ) + 1

        image_path = ''

        if form.image.data:
            image = form.image.data
            extension = Path(image.filename).suffix.lower()
            filename = f'{uuid4().hex}{extension}'

            image.save(UPLOAD_FOLDER / filename)
            image_path = f'uploads/{filename}'

        product = {
            'id': product_id,
            'name': form.name.data,
            'content': form.content.data,
            'price': float(form.price.data),
            'category': form.category.data,
            'quantity': form.quantity.data,
            'image': image_path,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        products_table.insert(product)

        flash('Товар успішно додано!', 'success')
        return redirect(url_for('products.list_products'))

    return render_template(
        'products/add_product.html',
        form=form
    )


@products_bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    product = products_table.get(
        lambda p: p['id'] == product_id
    )

    if product is None:
        abort(404)

    form = ProductForm(data=product)

    if form.validate_on_submit():
        image_path = product.get('image', '')

        if form.image.data:
            image = form.image.data
            extension = Path(image.filename).suffix.lower()
            filename = f'{uuid4().hex}{extension}'

            image.save(UPLOAD_FOLDER / filename)
            image_path = f'uploads/{filename}'

        products_table.update(
            {
                'name': form.name.data,
                'content': form.content.data,
                'price': float(form.price.data),
                'category': form.category.data,
                'quantity': form.quantity.data,
                'image': image_path
            },
            lambda p: p['id'] == product_id
        )

        flash('Товар успішно оновлено!', 'success')

        return redirect(
            url_for('products.product_detail', product_id=product_id)
        )

    return render_template(
        'products/edit_product.html',
        form=form,
        product=product
    )

@products_bp.route('/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    product = products_table.get(
        lambda p: p['id'] == product_id
    )

    if product is None:
        abort(404)

    form = DeleteProductForm()

    if form.validate_on_submit():
        products_table.remove(
            lambda p: p['id'] == product_id
        )

        flash('Товар успішно видалено!', 'success')
        return redirect(url_for('products.list_products'))

    abort(400)