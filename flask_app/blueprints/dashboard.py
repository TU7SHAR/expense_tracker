from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import date, timedelta
from app import db
from models import Transaction, Category

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    today = date.today()
    first_day_of_month = today.replace(day=1)

    # Monthly totals
    monthly_income = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == 'income',
        Transaction.date >= first_day_of_month
    ).scalar() or 0

    monthly_expenses = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == 'expense',
        Transaction.date >= first_day_of_month
    ).scalar() or 0

    balance = monthly_income - monthly_expenses

    # Total all-time
    total_income = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == 'income'
    ).scalar() or 0

    total_expenses = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == 'expense'
    ).scalar() or 0

    total_balance = total_income - total_expenses

    # Recent transactions
    recent_transactions = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.date.desc(), Transaction.created_at.desc())\
        .limit(5).all()

    # Expense breakdown by category (this month)
    category_breakdown = db.session.query(
        Category.name, Category.color, func.sum(Transaction.amount)
    ).join(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == 'expense',
        Transaction.date >= first_day_of_month
    ).group_by(Category.id).all()

    # Daily spending for last 7 days
    week_ago = today - timedelta(days=6)
    daily_spending = db.session.query(
        Transaction.date, func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == 'expense',
        Transaction.date >= week_ago
    ).group_by(Transaction.date).order_by(Transaction.date).all()

    # Fill in missing days
    daily_data = {}
    for i in range(7):
        d = week_ago + timedelta(days=i)
        daily_data[d.strftime('%a')] = 0
    for d, amount in daily_spending:
        daily_data[d.strftime('%a')] = float(amount)

    return render_template('dashboard/index.html',
                           monthly_income=monthly_income,
                           monthly_expenses=monthly_expenses,
                           balance=balance,
                           total_balance=total_balance,
                           recent_transactions=recent_transactions,
                           category_breakdown=category_breakdown,
                           daily_labels=list(daily_data.keys()),
                           daily_values=list(daily_data.values()))
