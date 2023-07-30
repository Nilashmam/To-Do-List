from flask import flash, redirect, render_template, request, Blueprint, abort,jsonify,Flask
from flask_caching import Cache
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user,logout_user,login_required
from to_do import db
from to_do.api.models import Task, User
from to_do.api.forms import RegisterForm, LoginForm, TodoForm,EditTodoForm


todo = Blueprint('tasks', __name__)
app = Flask(__name__)
cache = Cache(config={"CACHE_TYPE":"RedisCache","CACHE_REDIS_HOST":"0.0.0.0","CACHE_REDIS_PORT":6379})
cache.init_app(app)
@todo.route('/')

@todo.route('/home')
@cache.cached(timeout=36000)
def home():
    return render_template('home.html')


@todo.route('/register', methods = ['POST','GET'])
@cache.cached(timeout=3600)
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)

    if request.method == 'POST':
        if form.validate_on_submit:
            user = User(first_name =form.first_name.data,
                        last_name =form.last_name.data,
                        email =form.email.data,
                        password = generate_password_hash(form.password.data)
                        )
            db.session.add(user)
            db.session.commit()
            flash("Registered successfully!",category='success')
            login_user(user)
            return redirect('/todos')

@todo.route('/login', methods = ['POST','GET'])
@cache.cached(timeout=360000000)
def login():
        form = LoginForm()
        if form.validate_on_submit:
            user = User.query.filter_by(email = form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user,remember=True)
                flash("login Successful",category='success')
                return redirect('/todos')
              
               
        return render_template('login.html', form=form)


@todo.route('/logout', methods = ['POST','GET'])
@cache.cached(timeout=36000000)
def logout():
 if request.method == 'POST':
    logout_user()
    flash("logout successfully !",category="success")
    return redirect('/home')
 return render_template('logout_user.html')

@todo.route('/add_todo', methods = ['POST','GET'])
@cache.cached(timeout=360000000)
@login_required
def add_tasks():
    user = current_user
    ds = TodoForm()
    if request.method == 'POST':
        if ds.validate_on_submit:
            todo = Task(task_name =ds.task_name.data,status =ds.status.data,
                        due_date =ds.due_date.data, todo_owner = user.id
                       )
            db.session.add(todo)
            db.session.commit()
            flash("task added successfully !",category='success')
            return redirect('/todos')

    
@todo.route('/todos')
@cache.cached(timeout=360000000)
@login_required
def todos():
    
    todos = Task.query.filter_by(todo_owner = current_user.id)
    form = EditTodoForm()
    ds = TodoForm()
    print(todos)
    return render_template('todos.html', todos = todos , form = form , ds = ds)

    
@todo.route('/edit_task/<int:id>',methods = ['GET','POST'])
@cache.cached(timeout=360000000)
@login_required
def edit_task(id):
    form = EditTodoForm()
    task = Task.query.filter_by(id=id,todo_owner = current_user.id).first()

    if request.method == 'POST':
      if form.validate_on_submit:
        task.task_name = form.task_name.data
        task.due_date = form.due_date.data
        task.status = form.status.data
        db.session.commit()
        return redirect('/todos')
      



    
# @todo.route('/edit_task/<int:id>', methods=['GET', 'POST'])
# def edit_task(id):
#     user = current_user
#     form = EditTodoForm()
#     task = Task.query.filter_by(id =id,todo_owner = current_user.id).first()
    
#     if form.validate_on_submit():
#         print(task.task_name)
#         task.task_name = form.task_name.data
#         task.due_date = form.due_date.data
#         task.status = form.status.data
#         db.session.commit()
#         return redirect('/todos')

#     elif request.method == 'GET':
#         form.task_name.data = task.task_name
#         form.due_date.data = task.due_date
#         form.status.data = task.status
#     return render_template('edit_todo.html',form=form)

@todo.route('/delete_task/<int:id>', methods=['GET','POST'])
@cache.cached(timeout=36000)
@login_required
def delete(id):
    task = Task.query.filter_by(id =id,todo_owner = current_user.id).first()
    if task:
            db.session.delete(task)
            db.session.commit()
            return redirect('/todos')
    abort(404)
 
    
    
@todo.route('/users')
@cache.cached(timeout=36000)
@login_required
def users():
    users = User.query.all()
    print(users)

    res = {}
    for user in users:
        res = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password':user.password

        }
    return jsonify(res)