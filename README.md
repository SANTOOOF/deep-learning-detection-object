# 🏭 Industrial Object Detection Web Application

A professional AI-powered web application for detecting industrial objects using **YOLOv8** deep learning architecture, built with **Flask**, **PyTorch**, and modern web technologies.

## 🌟 Features

- ✅ **Real-time Object Detection** using YOLOv8
- ✅ **GPU Acceleration** with CUDA support
- ✅ **Modern Dark Theme** UI with industrial design
- ✅ **Drag & Drop** image upload
- ✅ **Adjustable Parameters** (confidence & IoU thresholds)
- ✅ **Detailed Results** with bounding boxes and confidence scores
- ✅ **Responsive Design** for all devices
- ✅ **Production Ready** with error handling

## 🎨 Screenshots

### Home Page
Professional hero section with AI-themed design

### Detection Page
Upload images and get instant AI-powered detection results

### Project Page
Comprehensive project documentation and model information

## 🛠️ Technology Stack

### Backend
- **Flask** - Web framework
- **YOLOv8 (Ultralytics)** - Object detection model
- **PyTorch 2.5+** - Deep learning framework
- **OpenCV** - Image processing
- **CUDA** - GPU acceleration

### Frontend
- **HTML5 & CSS3** - Modern web standards
- **JavaScript (ES6+)** - Client-side logic
- **Jinja2** - Template engine
- **Font Awesome** - Icons

## 📋 Requirements

- Python 3.10+
- NVIDIA GPU with CUDA 12.x (optional, but recommended)
- 8GB+ RAM
- Modern web browser

## 🚀 Installation

### 1. Clone the repository

```bash
cd webapp
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Verify model path

Ensure the YOLOv8 model exists at:
```
../models/deployment/best.pt
```

## ▶️ Running the Application

### Start the Flask server

```bash
python app.py
```

### Access the application

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## 📁 Project Structure

```
webapp/
│
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Home page
│   ├── detection.html    # Detection page
│   ├── project.html      # Project info
│   ├── about.html        # About page
│   └── contact.html      # Contact page
│
├── static/               # Static files
│   ├── css/
│   │   └── style.css    # Main stylesheet
│   ├── js/
│   │   ├── main.js      # Main JavaScript
│   │   ├── detection.js # Detection logic
│   │   └── contact.js   # Contact form
│   ├── uploads/         # Uploaded images
│   └── results/         # Detection results
│
└── models/              # YOLOv8 model
    └── deployment/
        └── best.pt      # Trained model
```

## 🎯 Usage

### 1. Home Page
- Navigate through the modern hero section
- Learn about the AI detection system
- Click "Test the Model" to start

### 2. Detection Page
- **Upload Image:** Click or drag & drop an image
- **Adjust Settings:** Configure confidence and IoU thresholds
- **Run Detection:** Click "Run Detection" button
- **View Results:** See detected objects with bounding boxes

### 3. Download Results
- Click "Download Result" to save the annotated image

## ⚙️ Configuration

### Adjust Confidence Threshold
Lower values detect more objects (including false positives)
Higher values are more selective

**Default:** 0.25

### Adjust IoU Threshold
Controls Non-Maximum Suppression (NMS)

**Default:** 0.45

## 🔧 API Endpoints

### `GET /`
Home page

### `GET /detection`
Detection page

### `POST /api/detect`
Run object detection

**Request:**
- `image` (file): Image to analyze
- `confidence` (float): Confidence threshold
- `iou` (float): IoU threshold

**Response:**
```json
{
  "success": true,
  "result_image": "result_20250214_120530.jpg",
  "detections": [
    {
      "class_name": "hardhat",
      "confidence": 0.95,
      "bbox": {...}
    }
  ],
  "num_detections": 3,
  "detection_time": 0.123
}
```

### `GET /api/model-info`
Get model information

## 🎨 Customization

### Change Color Theme
Edit `static/css/style.css`:

```css
:root {
    --primary-color: #ff6b35;
    --secondary-color: #004e89;
    --accent-color: #00d9ff;
}
```

### Update Model
Replace the model file:
```
models/deployment/best.pt
```

### Modify Classes
The system automatically detects classes from the model

## 🐛 Troubleshooting

### Model not found
- Check model path in `app.py`
- Ensure `best.pt` exists

### GPU not detected
- Install CUDA toolkit
- Verify PyTorch CUDA version

### Port already in use
Change port in `app.py`:
```python
app.run(port=5001)
```

## 📊 Performance

- **Detection Time:** < 100ms (GPU) / < 1s (CPU)
- **Batch Processing:** Supported
- **Max Image Size:** 16MB
- **Supported Formats:** JPG, PNG, JPEG

## 🔐 Security

- File type validation
- File size limits
- Secure filename handling
- Error handling & logging

## 📝 License

This project is for educational and research purposes.

## 👤 Author

**AI Engineer**
- Master's Degree in Artificial Intelligence
- Specialized in Computer Vision & Deep Learning

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📧 Contact

For questions or support:
- Email: rahliyoussef43@gmail.com
- GitHub: SANTOOOFF

## 🙏 Acknowledgments

- **Ultralytics** for YOLOv8
- **PyTorch** team
- **Flask** framework
- All contributors

---

**Built with ❤️ using YOLOv8 + Flask + PyTorch**
