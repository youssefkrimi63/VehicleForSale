from getpass import getuser
from flask_app import app
from flask import render_template,request, redirect, session,flash, url_for
from flask_app.models.user_model import User

from flask_app.models.order_model import Order
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


#=========Display Route==========
@app.route('/')
def log_reg():
    return render_template('index.html')


#===========Action Route===========
@app.route('/users/register', methods=['post'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    # data={
    #     'first_name':request.form['first_name'],
    #     'last_name':request.form['last_name'],
    #     'email':request.form['email'],
    #     'password':bcrypt.generate_password_hash(request.form['password'])
    # }
    data={
        **request.form,
        'password':bcrypt.generate_password_hash(request.form['password'])
    }
    user=User.save_user(data)
    session['user_id']=user

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:#if he has not an id redirect to the register page
        return redirect('/')
    all_orders = Order.get_orders()
    user= User.get_by_id({'id': session['user_id']})
    return render_template('dashboard.html',user=user,all_orders=all_orders)






@app.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'GET':
        user = User.get_by_id({'id': user_id})  # Fetch user data by ID
        if not user:
            flash('User not found', 'error')
            return redirect('/dashboard')  # Redirect to dashboard if user not found
        return render_template('edit_user.html', user=user)
    elif request.method == 'POST':
        if not User.validate_Edituser(request.form):  # Add a colon here
            flash('Invalid form data', 'error')
            return redirect(f'/user/edit/{user_id}')  # Redirect back to edit page with error
        order_data = {
            **request.form,
            'id': user_id
        }
        try:
            User.update_user(order_data)
            flash('User information updated successfully', 'success')
            return redirect('/dashboard')
        except Exception as e:
            flash('An error occurred while updating user information', 'error')
            return redirect(f'/user/edit/{user_id}')






#Login user with validate form
@app.route('/users/login',methods=['POST'])
def login():
    users_db = User.get_by_email(request.form)
    if not users_db:
        flash('Invalid email or password', "login")
        return redirect('/')
    if not bcrypt.check_password_hash(users_db.password, request.form['password']):
        flash('Invalid email or password', "login")
        return redirect('/')
    session['user_id']=users_db.id
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')