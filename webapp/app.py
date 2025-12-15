"""
Industrial Object Detection Web Application
YOLOv8 + Flask + GPU Support

Author: AI Engineer
Date: December 2025
"""

import os
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import torch
from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'industrial-ai-detection-yolov8-2025'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULTS_FOLDER'] = 'static/results'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'webp'}

# Model path (relative to the webapp directory)
MODEL_PATH = '../models/deployment/best.pt'

# Global variables
model = None
device = None
model_info = {}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_device():
    """Get best available device (GPU/CPU)"""
    if torch.cuda.is_available():
        return 0  # GPU device 0
    else:
        return 'cpu'

def load_model():
    """Load YOLOv8 model once at startup"""
    global model, device, model_info
    
    print("=" * 80)
    print("🚀 LOADING YOLOV8 MODEL")
    print("=" * 80)
    
    # Get device
    device = get_device()
    device_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'
    print(f"📱 Device: {device_name}")
    
    # Load model
    model_full_path = os.path.join(os.path.dirname(__file__), MODEL_PATH)
    
    if not os.path.exists(model_full_path):
        raise FileNotFoundError(f"Model not found at: {model_full_path}")
    
    print(f"📦 Loading model from: {model_full_path}")
    model = YOLO(model_full_path)
    
    # Store model info
    model_info = {
        'device': device_name,
        'device_type': 'GPU' if torch.cuda.is_available() else 'CPU',
        'classes': list(model.names.values()),
        'num_classes': len(model.names),
        'model_path': model_full_path,
        'loaded_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    print(f"✅ Model loaded successfully!")
    print(f"📊 Number of classes: {model_info['num_classes']}")
    print(f"🏷️  Classes: {', '.join(model_info['classes'][:5])}...")
    print("=" * 80)

def run_detection(image_path, conf_threshold=0.25, iou_threshold=0.45):
    """
    Run YOLOv8 detection on an image
    
    Args:
        image_path: Path to input image
        conf_threshold: Confidence threshold (0-1)
        iou_threshold: IoU threshold for NMS
    
    Returns:
        dict: Detection results with image path, detections, and metadata
    """
    global model, device
    
    start_time = time.time()
    
    # Run inference
    results = model.predict(
        source=image_path,
        device=device,
        conf=conf_threshold,
        iou=iou_threshold,
        verbose=False
    )
    
    result = results[0]
    
    # Parse detections
    detections = []
    for box in result.boxes:
        class_id = int(box.cls[0])
        detection = {
            'class_id': class_id,
            'class_name': model.names[class_id],
            'confidence': float(box.conf[0]),
            'bbox': {
                'x1': float(box.xyxy[0][0]),
                'y1': float(box.xyxy[0][1]),
                'x2': float(box.xyxy[0][2]),
                'y2': float(box.xyxy[0][3])
            }
        }
        detections.append(detection)
    
    # Get annotated image
    annotated_img = result.plot()
    
    # Save result image
    result_filename = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    result_path = os.path.join(app.config['RESULTS_FOLDER'], result_filename)
    cv2.imwrite(result_path, annotated_img)
    
    detection_time = time.time() - start_time
    
    return {
        'success': True,
        'result_image': result_filename,
        'detections': detections,
        'num_detections': len(detections),
        'detection_time': round(detection_time, 3),
        'conf_threshold': conf_threshold,
        'iou_threshold': iou_threshold
    }

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def home():
    """Home page"""
    return render_template('home.html')

@app.route('/detection')
def detection():
    """Detection page"""
    return render_template('detection.html')

@app.route('/project')
def project():
    """Project page"""
    return render_template('project.html', model_info=model_info)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page"""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Log the message (in production, save to database or send email)
        print("=" * 80)
        print("📧 NEW CONTACT MESSAGE")
        print("=" * 80)
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Message: {message}")
        print("=" * 80)
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your message! We will get back to you soon.'
        })
    
    return render_template('contact.html')

@app.route('/api/detect', methods=['POST'])
def api_detect():
    """API endpoint for object detection"""
    try:
        # Check if file is present
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type. Only JPG, PNG, JPEG are allowed'}), 400
        
        # Get confidence threshold
        conf_threshold = float(request.form.get('confidence', 0.25))
        iou_threshold = float(request.form.get('iou', 0.45))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Run detection
        result = run_detection(filepath, conf_threshold, iou_threshold)
        result['uploaded_image'] = filename
        
        return jsonify(result)
    
    except Exception as e:
        print(f"❌ Error in detection: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/model-info')
def api_model_info():
    """API endpoint to get model information"""
    return jsonify(model_info)

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/static/results/<filename>')
def result_file(filename):
    """Serve result files"""
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('500.html'), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)
    
    # Load YOLOv8 model
    load_model()
    
    # Run Flask app
    print("\n🌐 Starting Flask application...")
    print("🔗 Open your browser at: http://127.0.0.1:5000")
    print("\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
