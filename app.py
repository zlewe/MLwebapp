#Usage: python app.py
import os
 
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
from keras.models import load_model
from scipy import misc
import keras
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import time
import uuid
import base64

def auc(y_true, y_pred):
	auc = tf.metrics.auc(y_true, y_pred)[1]
	keras.backend.get_session().run(tf.local_variables_initializer())
	return auc

model_path = './models/model.h5'
global graph
graph = tf.get_default_graph()
model = load_model(model_path,custom_objects={'auc':auc})

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

#rgb2gray
def rgb2gray(rgb):
	r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
	gray = 0.2989*r + 0.5870*g + 0.1140*b

	return gray

def get_as_base64(url):
    return base64.b64encode(requests.get(url).content)

def predict(file):
    x = plt.imread(file)
    x = misc.imresize(x,(200,200))
    x = rgb2gray(x)/255
    x = x.reshape(1,200,200,1)
    with graph.as_default():
    	answer = model.predict_classes(x)
    if answer == 0:
	    print("Label: Bar")
    elif answer == 1:
	    print("Label: Histogram")
    elif answer == 2:
	    print("Label: Pie")
    elif answer == 3:
	    print("Label: Bubble")
    elif answer == 4:
	    print("Label: Scatter")
    elif answer == 5:
	    print("Label: Line")
    else:
	    print("Label: Not a chart")
    return answer

def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def template_test():
    return render_template('template.html', label='', imagesource='../uploads/template.jpg')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        import time
        start_time = time.time()
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            result = predict(file_path)
            if result == 0:
                label = 'Bar'
            elif result == 1:
                label = 'Histogram'			
            elif result == 2:
                label = 'Pie'
            elif result == 3:
                label = 'Bubble'
            elif result == 4:
                label = 'Scatter'
            elif result == 5:
                label = 'Line'
            else:
                label = 'Fool'
            print(result)
            print(file_path)
            filename = my_random_string(6) + filename

            os.rename(file_path, os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("--- %s seconds ---" % str (time.time() - start_time))
            return render_template('template.html', label=label, imagesource='../uploads/' + filename)

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

from werkzeug import SharedDataMiddleware
app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})

if __name__ == "__main__":
    app.debug=False
    app.run(host='0.0.0.0', port=80)
