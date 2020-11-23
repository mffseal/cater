from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user

from app import db
from app.forms.auth import RegisterForm, LoginForm
from app.moduls.user import User
from . import web


@web.route('/register', methods=['GET', 'POST'])
def register():
    # 实例化验证层
    form = RegisterForm(request.form)
    # 当http是post时才启动校验
    if request.method == 'POST' and form.validate():
        # 操作数据库模型
        with db.auto_commit():
            user = User()
            # form.data是字典
            user.set_attrs(form.data)
            db.session.add(user)
        # db.session.commit()
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # 管理cookie
            login_user(user, remember=True)
            # 获取get中下一个页面的参数
            next = request.args.get('next')
            # 指定默认跳转页面
            # 防止重定向攻击
            if not next or next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('帐号不存在或密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    pass


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password():
    pass
