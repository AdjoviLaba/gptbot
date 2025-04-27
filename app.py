from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_login import LoginManager, current_user
from werkzeug.utils import secure_filename
import os
from config import Config
from extensions import db, login_manager 


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Import and register blueprints
from auth.routes import auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

# Import ML processing modules
from ml_processing.review_analyzer import get_product_review
from ml_processing.image_processor import process_image

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Render the user dashboard."""
    if not current_user.is_authenticated:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/get_review', methods=['POST'])
def get_review():
    """Process the user's product review request."""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Authentication required'}), 401
    
    product_info = request.form.get('product_info')
    product_image = request.files.get('product_image')
    
    # Process the image if provided
    if product_image and allowed_file(product_image.filename):
        filename = secure_filename(product_image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        product_image.save(filepath)
        
        # Get product name from image
        product_name = process_image(filepath)
        if product_name:
            product_info = product_name if not product_info else f"{product_info} {product_name}"
    
    # Get product review
    if product_info:
        review = get_product_review(product_info)
        return jsonify({'review': review})
    else:
        return jsonify({'error': 'No product information provided'}), 400

if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()
    app.run(debug=True)