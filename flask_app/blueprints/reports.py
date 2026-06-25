from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import func, extract
from datetime import date, timedelta
from app import db
from models import Transaction, Category

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')


@reports_bp.route('/')
@login_required
def index():
    today = date.today()
    period = request.args.get('period', 'month')

    if period == 'week':
        start_date = today - timedelta(days=today.weekday())
    elif period == 'month':
        start_date = today.replace(day=1)
    elif period == 'year':
        start_date = today.replace(month=1, day=1)
    else:
        start_date = today.replace(day=1)

    # Income vs Expense totals
    income_total = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == 'income',
        Transaction.date >= start_date
    ).scalar() or 0

    expense_total = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == 'expense',
        Transaction.date >= start_date
    ).scalar() or 0

    # Category breakdown for expenses
    expense_by_category = db.session.query(
        Category.name, Category.color, func.sum(Transaction.amount)
    ).join(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == 'expense',
        Transaction.date >= start_date
    ).group_by(Category.id).order_by(func.sum(Transaction.amount).desc()).all()

    # Category breakdown for income
    income_by_category = db.session.query(
        Category.name, Category.color, func.sum(Transaction.amount)
    ).join(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == 'income',
        Transaction.date >= start_date
    ).group_by(Category.id).order_by(func.sum(Transaction.amount).desc()).all()

    # Daily trend
    daily_trend = db.session.query(
        Transaction.date,
        Transaction.transaction_type,
        func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= start_date
    ).group_by(Transaction.date, Transaction.transaction_type)\
     .order_by(Transaction.date).all()

    # Process daily trend data
    trend_dates = []
    trend_income = []
    trend_expense = []
    date_data = {}

    for d, t_type, amount in daily_trend:
        date_str = d.strftime('%b %d')
        if date_str not in date_data:
            date_data[date_str] = {'income': 0, 'expense': 0}
        date_data[date_str][t_type] = float(amount)

    for date_str, values in date_data.items():
        trend_dates.append(date_str)
        trend_income.append(values['income'])
        trend_expense.append(values['expense'])

    # Top expenses
    top_expenses = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == 'expense',
        Transaction.date >= start_date
    ).order_by(Transaction.amount.desc()).limit(5).all()

    return render_template('reports/index.html',
                           period=period,
                           income_total=income_total,
                           expense_total=expense_total,
                           expense_by_category=expense_by_category,
                           income_by_category=income_by_category,
                           trend_dates=trend_dates,
                           trend_income=trend_income,
                           trend_expense=trend_expense,
                           top_expenses=top_expenses)
