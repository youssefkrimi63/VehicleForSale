from flask_app import app
from flask import render_template,redirect,request, session , flash
from flask_app.models.order_model import Order
from flask_app.models.user_model import User

@app.route('/orders/new')
def order_form():
    if 'user_id' not in session:#if he has not an id redirect to the register page
        return redirect('/')
    return render_template('create_order.html')

@app.route('/orders/create', methods=['post'])
def create_order():
    if not Order.validate_order(request.form):
        return redirect('/orders/new')
    order_data={
        **request.form,
        'user_id': session['user_id']
    }
    Order.save_order(order_data)
    return redirect('/dashboard')









@app.route('/creations/<int:id>')
def show_order(id):
    if 'user_id' not in session:#if he has not an id redirect to the register page
        return redirect('/')
    order=order.get_by_id_order({'id':id})
    user = User.get_by_id({'id':session['user_id']})
    return render_template('show_order.html',order=order,user=user)


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
































@app.route('/orders/delete/<int:id>', methods=['post'])
def delete(id):
    Order.delete_order({'id':id})
    return redirect('/dashboard')





