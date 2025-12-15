"""
System Check Script for Industrial Object Detection Web App
Verifies all dependencies and configurations
"""

import sys
import os

print("=" * 80)
print("INDUSTRIAL OBJECT DETECTION - SYSTEM CHECK")
print("=" * 80)
print()

# Check Python version
print("[1/7] Checking Python version...")
python_version = sys.version_info
print(f"      Python {python_version.major}.{python_version.minor}.{python_version.micro}")
if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 10):
    print("      ⚠️  Warning: Python 3.10+ recommended")
else:
    print("      ✅ Python version OK")
print()

# Check Flask
print("[2/7] Checking Flask...")
try:
    import flask
    print(f"      Flask {flask.__version__}")
    print("      ✅ Flask installed")
except ImportError:
    print("      ❌ Flask not installed. Run: pip install Flask")
print()

# Check PyTorch
print("[3/7] Checking PyTorch...")
try:
    import torch
    print(f"      PyTorch {torch.__version__}")
    print(f"      CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"      CUDA Version: {torch.version.cuda}")
        print(f"      GPU: {torch.cuda.get_device_name(0)}")
    print("      ✅ PyTorch installed")
except ImportError:
    print("      ❌ PyTorch not installed. Run: pip install torch")
print()

# Check Ultralytics (YOLOv8)
print("[4/7] Checking Ultralytics...")
try:
    import ultralytics
    print(f"      Ultralytics {ultralytics.__version__}")
    print("      ✅ Ultralytics installed")
except ImportError:
    print("      ❌ Ultralytics not installed. Run: pip install ultralytics")
print()

# Check OpenCV
print("[5/7] Checking OpenCV...")
try:
    import cv2
    print(f"      OpenCV {cv2.__version__}")
    print("      ✅ OpenCV installed")
except ImportError:
    print("      ❌ OpenCV not installed. Run: pip install opencv-python")
print()

# Check model file
print("[6/7] Checking model file...")
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'deployment', 'best.pt')
model_path = os.path.abspath(model_path)
if os.path.exists(model_path):
    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"      Model found: {model_path}")
    print(f"      Size: {size_mb:.2f} MB")
    print("      ✅ Model file exists")
else:
    print(f"      ❌ Model not found at: {model_path}")
print()

# Check directory structure
print("[7/7] Checking directory structure...")
required_dirs = [
    'templates',
    'static',
    'static/css',
    'static/js',
    'static/uploads',
    'static/results',
    'static/images'
]
all_exist = True
for dir_name in required_dirs:
    dir_path = os.path.join(os.path.dirname(__file__), dir_name)
    if os.path.exists(dir_path):
        print(f"      ✅ {dir_name}/")
    else:
        print(f"      ❌ {dir_name}/ (missing)")
        all_exist = False

print()
print("=" * 80)
if all_exist:
    print("✅ ALL CHECKS PASSED! Ready to run the application.")
    print()
    print("To start the application, run:")
    print("  python app.py")
else:
    print("⚠️  Some checks failed. Please fix the issues above.")
print("=" * 80)
