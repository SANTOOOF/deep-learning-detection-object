/**
 * Industrial Object Detection - Detection Page JavaScript
 * Image Upload, Preview, Detection, Results Display
 */

// ============================================================================
// GLOBAL VARIABLES
// ============================================================================
let selectedFile = null;
let currentResultImage = null;

// ============================================================================
// DOM ELEMENTS
// ============================================================================
const uploadArea = document.getElementById('upload-area');
const imageInput = document.getElementById('image-input');
const imagePreview = document.getElementById('image-preview');
const previewImg = document.getElementById('preview-img');
const removeImageBtn = document.getElementById('remove-image');
const detectBtn = document.getElementById('detect-btn');
const loadingSpinner = document.getElementById('loading');
const emptyState = document.getElementById('empty-state');
const resultsSection = document.getElementById('results');
const resultImg = document.getElementById('result-img');
const numObjects = document.getElementById('num-objects');
const detectionTime = document.getElementById('detection-time');
const detectionsContainer = document.getElementById('detections-container');
const downloadBtn = document.getElementById('download-btn');
const errorMessage = document.getElementById('error-message');
const errorText = document.getElementById('error-text');

// Sliders
const confidenceSlider = document.getElementById('confidence');
const confidenceValue = document.getElementById('confidence-value');
const iouSlider = document.getElementById('iou');
const iouValue = document.getElementById('iou-value');

// ============================================================================
// EVENT LISTENERS
// ============================================================================

// Upload Area Click
uploadArea.addEventListener('click', function() {
    imageInput.click();
});

// Drag and Drop
uploadArea.addEventListener('dragover', function(e) {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--accent-color)';
    uploadArea.style.background = 'var(--bg-tertiary)';
});

uploadArea.addEventListener('dragleave', function(e) {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--border-color)';
    uploadArea.style.background = 'var(--bg-secondary)';
});

uploadArea.addEventListener('drop', function(e) {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--border-color)';
    uploadArea.style.background = 'var(--bg-secondary)';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

// File Input Change
imageInput.addEventListener('change', function(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

// Remove Image Button
removeImageBtn.addEventListener('click', function(e) {
    e.stopPropagation();
    clearImage();
});

// Detect Button
detectBtn.addEventListener('click', function() {
    runDetection();
});

// Slider Updates
confidenceSlider.addEventListener('input', function() {
    confidenceValue.textContent = parseFloat(this.value).toFixed(2);
});

iouSlider.addEventListener('input', function() {
    iouValue.textContent = parseFloat(this.value).toFixed(2);
});

// Download Button
downloadBtn.addEventListener('click', function() {
    if (currentResultImage) {
        const link = document.createElement('a');
        link.href = `/static/results/${currentResultImage}`;
        link.download = `detection_result_${Date.now()}.jpg`;
        link.click();
    }
});

// ============================================================================
// FUNCTIONS
// ============================================================================

/**
 * Handle file selection
 */
function handleFileSelect(file) {
    // Validate file type
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];
    if (!validTypes.includes(file.type)) {
        showError('Invalid file type. Please upload a PNG, JPG, or JPEG image.');
        return;
    }
    
    // Validate file size (16MB max)
    const maxSize = 16 * 1024 * 1024; // 16MB
    if (file.size > maxSize) {
        showError('File too large. Maximum size is 16MB.');
        return;
    }
    
    // Store selected file
    selectedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = function(e) {
        previewImg.src = e.target.result;
        uploadArea.style.display = 'none';
        imagePreview.style.display = 'block';
        detectBtn.disabled = false;
    };
    reader.readAsDataURL(file);
    
    // Clear previous results
    clearResults();
}

/**
 * Clear selected image
 */
function clearImage() {
    selectedFile = null;
    imageInput.value = '';
    previewImg.src = '';
    uploadArea.style.display = 'flex';
    imagePreview.style.display = 'none';
    detectBtn.disabled = true;
    clearResults();
}

/**
 * Clear results
 */
function clearResults() {
    resultsSection.style.display = 'none';
    emptyState.style.display = 'block';
    errorMessage.style.display = 'none';
    currentResultImage = null;
}

/**
 * Show error message
 */
function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'block';
    
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

/**
 * Run object detection
 */
async function runDetection() {
    if (!selectedFile) {
        showError('Please select an image first.');
        return;
    }
    
    // Hide empty state and error
    emptyState.style.display = 'none';
    errorMessage.style.display = 'none';
    resultsSection.style.display = 'none';
    
    // Show loading spinner
    loadingSpinner.style.display = 'block';
    detectBtn.disabled = true;
    
    try {
        // Prepare form data
        const formData = new FormData();
        formData.append('image', selectedFile);
        formData.append('confidence', confidenceSlider.value);
        formData.append('iou', iouSlider.value);
        
        // Make API request
        const response = await fetch('/api/detect', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
        } else {
            throw new Error(data.error || 'Detection failed');
        }
        
    } catch (error) {
        console.error('Detection error:', error);
        showError(error.message || 'An error occurred during detection. Please try again.');
        loadingSpinner.style.display = 'none';
        emptyState.style.display = 'block';
        detectBtn.disabled = false;
    }
}

/**
 * Display detection results
 */
function displayResults(data) {
    // Hide loading
    loadingSpinner.style.display = 'none';
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Display result image
    currentResultImage = data.result_image;
    resultImg.src = `/static/results/${data.result_image}?t=${Date.now()}`;
    
    // Display detection info
    numObjects.textContent = data.num_detections;
    detectionTime.textContent = formatTime(data.detection_time);
    
    // Display detections list
    detectionsContainer.innerHTML = '';
    
    if (data.detections.length === 0) {
        detectionsContainer.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: var(--text-muted);">
                <i class="fas fa-search" style="font-size: 2rem; margin-bottom: 1rem; opacity: 0.3;"></i>
                <p>No objects detected. Try adjusting the confidence threshold.</p>
            </div>
        `;
    } else {
        // Sort by confidence (highest first)
        data.detections.sort((a, b) => b.confidence - a.confidence);
        
        data.detections.forEach((detection, index) => {
            const detectionItem = document.createElement('div');
            detectionItem.className = 'detection-item';
            detectionItem.style.animation = `fadeInUp 0.3s ease ${index * 0.05}s both`;
            
            detectionItem.innerHTML = `
                <div class="detection-name">
                    <i class="fas fa-cube"></i>
                    <strong>${detection.class_name}</strong>
                </div>
                <div class="detection-confidence">
                    ${(detection.confidence * 100).toFixed(1)}%
                </div>
            `;
            
            detectionsContainer.appendChild(detectionItem);
        });
    }
    
    // Enable detect button
    detectBtn.disabled = false;
}

/**
 * Format time helper
 */
function formatTime(seconds) {
    if (seconds < 1) {
        return (seconds * 1000).toFixed(0) + 'ms';
    }
    return seconds.toFixed(2) + 's';
}

// ============================================================================
// INITIALIZATION
// ============================================================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('Detection page loaded');
    
    // Check if model is loaded
    fetch('/api/model-info')
        .then(response => response.json())
        .then(data => {
            console.log('Model Info:', data);
        })
        .catch(error => {
            console.error('Error fetching model info:', error);
        });
});
