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

# DATABASE
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

# _ _ _ _ _
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

@app.route('/')
def index():
    # need to get the link right!
    direction = url_for('huntform')
    return render_template('index2.html', direction=direction)


class HuntForm(FlaskForm):
    '''Form '''
    name = StringField('Enter a name', validators=[Required()])
    sequence = TextAreaField('Enter DNA sequence', validators=[Required()])
    plot_option = BooleanField('Check for an Interactive Plot')
    submit = SubmitField('Submit')

@app.route('/memory', methods=['GET', 'POST'])
def memory():
    # shows options of genes in the database
    form = MemoryForm(request.form)
    genes = [(str(i), i) for i in db.child('sequences').get().val().keys()]
    form.menu.choices = genes
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
            redirected = False
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
            return render_template('results.html', name=name, sequence=sequence, data=data, 
                                  url_image=url_image, plot_option=plot_option) 
    return render_template('HuntForm.html', form=form, sequence=sequence)


class MemoryForm(FlaskForm):
    '''Form '''
    menu = SelectField("Select a gene")
    submit = SubmitField('Submit')


if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')