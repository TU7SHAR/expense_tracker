from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import Transaction, Category
from forms import TransactionForm
from datetime import date

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')


@transactions_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    filter_type = request.args.get('type', 'all')
    filter_category = request.args.get('category', 'all')
    search = request.args.get('search', '')

    query = Transaction.query.filter_by(user_id=current_user.id)

    if filter_type != 'all':
        query = query.filter_by(transaction_type=filter_type)

    if filter_category != 'all':
        query = query.filter_by(category_id=int(filter_category))

    if search:
        query = query.filter(Transaction.description.ilike(f'%{search}%'))

    transactions = query.order_by(Transaction.date.desc(), Transaction.created_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)

    categories = Category.query.order_by(Category.name).all()

    return render_template('transactions/index.html',
                           transactions=transactions,
                           categories=categories,
                           filter_type=filter_type,
                           filter_category=filter_category,
                           search=search)


@transactions_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = TransactionForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]

    if form.validate_on_submit():
        transaction = Transaction(
            amount=form.amount.data,
            description=form.description.data,
            transaction_type=form.transaction_type.data,
            date=form.date.data,
            category_id=form.category_id.data,
            user_id=current_user.id
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transactions.index'))

    return render_template('transactions/add.html', form=form, title='Add Transaction')


@transactions_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('transactions.index'))

    form = TransactionForm(obj=transaction)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]

    if form.validate_on_submit():
        transaction.amount = form.amount.data
        transaction.description = form.description.data
        transaction.transaction_type = form.transaction_type.data
        transaction.date = form.date.data
        transaction.category_id = form.category_id.data
        db.session.commit()
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('transactions.index'))

    return render_template('transactions/add.html', form=form, title='Edit Transaction')


@transactions_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('transactions.index'))

    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted.', 'success')
    return redirect(url_for('transactions.index'))
