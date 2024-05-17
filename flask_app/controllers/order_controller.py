from flask_app import app
from flask import render_template, redirect, request, session, flash,jsonify
from flask_app.models.order_model import Order
from flask_app.models.user_model import User

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    all_orders = Order.get_all_with_likes()
    user = User.get_by_id({'id': session['user_id']})
    return render_template('dashboard.html', user=user, all_orders=all_orders)
@app.route('/orders/new')
def order_form():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('create_order.html')

@app.route('/orders/create', methods=['POST'])
def create_order():
    if not Order.validate_order(request.form):
        return redirect('/orders/new')
    order_data = {
        **request.form,
        'user_id': session['user_id']
    }
    Order.save_order(order_data)
    return redirect('/dashboard')

@app.route('/orders/delete/<int:id>', methods=['POST'])
def delete_order(id):
    Order.delete_order(id)
    return redirect('/dashboard')

@app.route('/orders/<int:id>/like', methods=['GET', 'POST'])
def like_order(id):
    if 'user_id' not in session:
        if request.method == 'GET':
            flash('Please log in to like an order', 'error')
            return redirect('/dashboard')
        else:
            return jsonify({'error': 'Please log in to like an order'}), 401

    user_id = session['user_id']
    data = {'users_id': user_id, 'orders_id': id}

    if Order.user_has_liked(data):
        Order.remove_user_like(data)
        action = 'disliked'
    else:
        Order.add_user_like(data)
        action = 'liked'

    if request.method == 'GET':
        return redirect('/dashboard')
    else:
        likes_count = Order.get_likes_count(id)
        return jsonify({'likes_count': likes_count, 'action': action})
    



    

@app.route('/orders/<int:id>/dislike', methods=['GET', 'POST'])
def dislike_order(id):
    # This route is no longer necessary since the like_order route handles both like and dislike actions
    return redirect('/dashboard')




@app.route('/order/edit/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    if request.method == 'GET':
        order = Order.get_by_id_order({'id': order_id})  # Corrected the method call
        if not order:
            flash('Order not found', 'error')
            return redirect('/dashboard')
        return render_template('edit_order.html', order=order)
    elif request.method == 'POST':
        order = Order.get_by_id_order({'id': order_id})  # Corrected the method call
        if not order:
            flash('Order not found', 'error')
            return redirect('/dashboard')
        if not Order.validate_order(request.form):  # Changed to validate_order
            flash('Invalid form data', 'error')
            return redirect(f'/order/edit/{order_id}')
        order_data = {
            **request.form,
            'id': order_id
        }
        try:
            Order.update_order(order_data)
            flash('Order information updated successfully', 'success')
            return redirect('/dashboard')
        except Exception as e:
            flash('An error occurred while updating order information', 'error')
            return redirect(f'/order/edit/{order_id}')
        




@app.route('/show/<int:id>')
def show_order_detail(id):
    if 'user_id' not in session:
        return redirect('/')
    order = Order.get_by_id_order({'id': id})
    if not order:
        flash('Order not found', 'error')
        return redirect('/dashboard')
    user = User.get_by_id({'id': session['user_id']})
    return render_template('show_order.html', order=order, user=user)