"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from flask import render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from app import app, db
from app.models import Movie
from app.forms import MovieForm
from flask_wtf.csrf import generate_csrf


###
# Routing for your application.
###
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/api/v1/movies', methods=['POST'])
def movies():
    # Ensure the 'uploads' folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Get form data and file
    title = request.form.get('title')
    description = request.form.get('description')
    poster = request.files.get('poster')

    print("FILES:", request.files)
    print("FORM:", request.form)

    # Validate required fields
    if not title or not description or not poster:
        return jsonify({"error": "Missing fields"}), 400

    # Validate file type
    if not allowed_file(poster.filename):
        return jsonify({"error": "File type not allowed"}), 400

    # Secure the filename and set the upload path
    filename = secure_filename(poster.filename)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print("Uploading to:", upload_path)
    poster.save(upload_path)

    # Create and save the movie entry to the database
    movie = Movie(title=title, description=description, poster=filename)
    db.session.add(movie)
    db.session.commit()

    return jsonify({
        "message": "Movie successfully added",
        "title": title,
        "poster": filename,
        "description": description
    }), 201

@app.route('/api/v1/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    movie_list = [{
        "id": movie.id,
        "title": movie.title,
        "description": movie.description,
        "poster": f"/api/v1/posters/{movie.poster}"
    } for movie in movies]

    return jsonify({"movies": movie_list})
from flask import send_from_directory

@app.route('/api/v1/posters/<filename>')
def get_poster(filename):
    uploads_path = os.path.join(os.getcwd(), 'uploads')
    return send_from_directory(uploads_path, filename)

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404