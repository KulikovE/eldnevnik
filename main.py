from flask import Flask, render_template, request
from flask import redirect
import datetime
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data.lessons import Lesson
from data.klass import Klass
from data.login import LoginForm
from data.students import Student
from data.appraisals import Appraisals
from data.teachers import Teacher

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/dnevnik.db")
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    if role == 'Учитель':
        return db_sess.query(Teacher).get(user_id)
    else:
        return db_sess.query(Student).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def osn():
    return render_template('base.html', title='Электронный дневник')


role = ''
name = ''
klass = ''
uchitel = ''


@app.route('/loginuchitel', methods=['GET', 'POST'])
def login_uchitel():
    global uchitel
    form = LoginForm()
    global role
    role = 'Учитель'
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Teacher).filter(Teacher.login == form.username.data).first()
        password = db_sess.query(Teacher).filter(Teacher.hashed_password == form.password.data).first()
        if user and password:
            uchitel = user
            login_user(user)
            return redirect("/uchitel")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, role='учителя')
    return render_template('login.html', title='Авторизация', form=form, role='учителя')


@app.route('/loginuchenik', methods=['GET', 'POST'])
def login_uchenik():
    form = LoginForm()
    global role, name, klass
    role = 'Ученик'
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Student).filter(Student.login == form.username.data).first()
        password = db_sess.query(Student).filter(Student.hashed_password == form.password.data).first()
        if user and password:
            login_user(user)
            name = user.name
            klass = user.klass
            return redirect("/uchenik")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, role='ученика')
    return render_template('login.html', title='Авторизация', form=form, role='ученика')


klass_names = ''


@app.route('/uchenik', methods=['GET', 'POST'])
def uchenik():
    global name, klass, klass_names, predm
    db_sess = db_session.create_session()
    klass_name = db_sess.query(Klass).filter(Klass.id == klass).first()
    data = db_sess.query(Lesson).filter(Lesson.klass == klass).all()
    klass_names = klass_name.name
    predm = data
    return render_template('uchenik.html', name=name, klass=klass_name.name, data=data)


@app.route('/uchenikka', methods=['GET', 'POST'])
def selection():
    db_sess = db_session.create_session()
    global name, klass, klass_names, predm
    lesson = request.form.get('comp_select')
    student_id = (db_sess.query(Student).filter(Student.name == name).first()).id
    lesson_id = (db_sess.query(Lesson).filter(Lesson.name == lesson).first()).id
    apprail = db_sess.query(Appraisals).filter(
        Appraisals.lesson == lesson_id and Appraisals.student == student_id).all()
    return render_template('uchenik_tabl.html', name=name, klass=klass_names, data=predm, ocenki=apprail)


@app.route('/uchitel', methods=['GET', 'POST'])
def uchitel():
    global uchitel
    db_sess = db_session.create_session()
    predm = db_sess.query(Lesson).filter(Lesson.teacher == uchitel.id).first()
    predm = predm.name
    return render_template('uchitel.html', name=uchitel.name, pred=predm)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


klassi = []
pred = []


@app.route('/uchitel/vistav-oc', methods=['GET', 'POST'])
def vist():
    db_sess = db_session.create_session()
    global uchitel, klassi, predm
    klassi = []
    predm = db_sess.query(Lesson).filter(Lesson.teacher == uchitel.id).all()
    for i in predm:
        klassi.append(db_sess.query(Klass).filter(Klass.id == i.klass).first())
    return render_template('uchitel_vist.html', name=uchitel.name, pred=predm[0].name, data=klassi)


@app.route('/uchitel/vistav-oc/sp-uch', methods=['GET', 'POST'])
def sp_uch():
    db_sess = db_session.create_session()
    global uchitel, predm, klassi
    date = datetime.date.today()
    klass_name = request.form.get('comp_select')
    klass_id = db_sess.query(Klass).filter(Klass.name == klass_name).first()
    students = db_sess.query(Student).filter(Student.klass == klass_id.id).all()
    return render_template('uchitel_vist_oc.html', name=uchitel.name, pred=predm[0].name, data=klassi, kalend=date,
                           uch=students, klass=klass_name)


@app.route('/uchitel/vistav-oc/saveoc', methods=['GET', 'POST'])
def save_oc():
    global predm, uchitel
    db_sess = db_session.create_session()
    data = request.form.get('calendar')
    uch_name = request.form.get('comp_select')
    ocen = request.form.get('ocenka')
    appraisal = Appraisals()
    appraisal.appraisals = ocen
    appraisal.lesson = predm[0].id
    appraisal.date = data
    appraisal.student = (db_sess.query(Student).filter(Student.name == uch_name).first()).id
    db_sess.add(appraisal)
    db_sess.commit()
    return render_template('oc_save.html', name=uchitel.name, pred=predm[0].name, oc=ocen, uch=uch_name,
                           date=data)


@app.route('/uchitel/prosm-oc', methods=['GET', 'POST'])
def pr_oc():
    global predm, uchitel, klassi
    klassi = []
    db_sess = db_session.create_session()
    predm = db_sess.query(Lesson).filter(Lesson.teacher == uchitel.id).all()
    for i in predm:
        klassi.append(db_sess.query(Klass).filter(Klass.id == i.klass).first())
    return render_template('uchitel_prosm_oc.html', name=uchitel.name, pred=predm[0].name, uch=klassi)


students = []


@app.route('/uchitel/prosm-oc/table', methods=['GET', 'POST'])
def pr_oc_table():
    global predm, uchitel, klassi, students
    db_sess = db_session.create_session()
    klass_name = request.form.get('comp_select')
    klass_id = (db_sess.query(Klass).filter(Klass.name == klass_name).first()).id
    students = db_sess.query(Student).filter(Student.klass == klass_id).all()
    return render_template('uchitel_prosm_oc_table.html', name=uchitel.name, pred=predm[0].name, uch=klassi,
                           names=students)


@app.route('/uchitel/prosm-oc/table/zagr', methods=['GET', 'POST'])
def pr_oc_table_zagr():
    global predm, uchitel, klassi, students
    db_sess = db_session.create_session()
    uch_name = request.form.get('comp_select_uch')
    student_id = (db_sess.query(Student).filter(Student.name == uch_name).first()).id
    appreal = db_sess.query(Appraisals).filter(Appraisals.student == student_id).all()
    return render_template('uchitel_prosm_oc_table_zg.html', name=uchitel.name, pred=predm[0].name, uch=klassi,
                           names=students, ocenki=appreal)


if __name__ == '__main__':
    main()
