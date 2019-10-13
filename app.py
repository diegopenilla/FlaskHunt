'''ZDNA app initializes server, handles everything'''
import markdown
from zhunt import z_hunt
from flask import Flask, url_for, redirect, session
from flask import render_template, request
from flask import Markup
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, BooleanField, SelectField  
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
import webbrowser
import collections as collections

# DATABASE CONFIGURATION
import pyrebase
config = {
    "apiKey": "AIzaSyCxOq7pbj3FdAhP6TNuh_wmoZyMWzqe8ec",
    "authDomain": "z-hunt.firebaseapp.com",
    "databaseURL": "https://z-hunt.firebaseio.com",
    "projectId": "z-hunt",
    "storageBucket": "z-hunt.appspot.com",
    "messagingSenderId": "579159102064",
    "appId": "1:579159102064:web:e74b47716cf0373b"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# _ _ _ _ _ INIT __
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'epigen'


# ERROR HANDLERS _____________________________________
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#____________________________________________________

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
# _______________________________________________

@app.route('/info')
def info():
    information = open("static/info_program.txt", "r") 
    content = information.read() 
    information.close()
    content = Markup(markdown.markdown(content))
    return render_template('info.html', content=content)

# Displays ZForm, Memory, Info
@app.route('/')
def index():
    # need to get the link right!
    direction = url_for('huntform')
    return render_template('index2.html', direction=direction)

# Stores all searched sequences, includes delete option and loading into HuntForm
@app.route('/memory', methods=['GET', 'POST'])
def memory():
    # shows options of genes in the database
    form = MemoryForm(request.form)
    try:    
        genes = [(str(i), i) for i in db.child('sequences').get().val().keys()]
        form.menu.choices = genes
    except:
        genes = [("", "")]
        form.menu.choices = genes
  
    if form.remove.data == True and request.method == 'POST' and form.validate_on_submit():
        name = form.menu.data
        remove = form.remove.data
        form.menu.data = ''
        form.remove.data = False

        # Sequence to be sent to HuntForm
        db.child("sequences").child(str(name)).remove()
        return render_template('table?del.html', form=form)

    if request.method == 'POST' and form.validate_on_submit():
        name = form.menu.data
        form.menu.data = ''
        # Sequence to be sent to HuntForm
        session['memory'] = (name, str(db.child('sequences').child(name).get().val()['sequence']))
        return redirect(url_for('huntform'))
    return render_template('table?.html', form=form)

   
@app.route('/huntform', methods=['GET', 'POST']) 
def huntform():
# """ Define Form with sequence: ATGC only and a name create a plot and a table with the results uploads the sequence and z-scores in firebase"""
    # DNA TO BE GIVEN:
    sequence = None
    form = HuntForm(request.form)
    if 'memory' in session and session['memory'] is not None:
        form.name.data = session['memory'][0]
        form.sequence.data = session['memory'][1]
        session['memory']= None

    # IF HUNTFORM IS SENT: (PRINT THE RESULTS IN RESULTS.HTML)
    if request.method == 'POST' and form.validate_on_submit():
            sequence = form.sequence.data
            name = form.name.data
            plot_option = form.plot_option.data
            form.sequence.data = ''
            form.name.data = ''
            #NOTE: MAYBE HERE IS WHERE YOU PROCESS THE DATA ALREADY???
            data, url_image = z_hunt(sequence, name)
            # UPLOADING TO THE DATABASE
            upload = {'sequence':sequence}
                      #'scores':list(data['Z-Score'])}
            db.child("sequences").child(name).set(upload)
            path = f'static/images/{name}.png'
            return render_template('results.html', name=name, path=path, sequence=sequence, data=data, 
                                  url_image=url_image, plot_option=plot_option) 
    
    return render_template('HuntForm.html', form=form, sequence=sequence)

# Forms
class HuntForm(FlaskForm):
    '''Form '''
    name = StringField('Enter a name', validators=[Required()])
    sequence = TextAreaField('Enter DNA sequence', validators=[Required()])
    plot_option = BooleanField('Check for an Interactive Plot')
    submit = SubmitField('Submit')
class MemoryForm(FlaskForm):
    '''Form '''
    menu = SelectField("Select a gene")
    submit = SubmitField('Submit')
    remove = BooleanField('Remove')

@app.route('/newform', methods=['GET', 'POST'])
def newform():
    if request.method == 'POST': #this block is only entered when the form is submitted
        NAME = request.form.get('name')
        DNA = request.form.get('text')
        return '''<h1> The DNA is "{}</h1>
                  <h2> The Name is {}</h2>'''.format(DNA, NAME)

    return render_template(
        'cool_custom_form.html')



@app.route('/newform2', methods=['GET', 'POST'])
def newform2():
    
    sequence = None
    form = HuntForm(request.form)
    if 'memory' in session and session['memory'] is not None:
        name = session['memory'][0]
        sequence = session['memory'][1]
        session['memory']= None

    if request.method == 'POST': #this block is only entered when the form is submitted
        name = request.form.get('name')
        sequence = request.form.get('text')
        data, url_image = z_hunt(sequence, name)
        # UPLOADING TO THE DATABASE
        upload = {'sequence':sequence}
        db.child("sequences").child(name).set(upload)
        return render_template('results.html', name=name, sequence=sequence, data=data, 
                                  url_image=url_image, plot_option=True) 

    # ANADIR FORM

    return render_template(
        'cool_custom_form.html')

