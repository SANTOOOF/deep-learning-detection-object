/**
 * Industrial Object Detection - Contact Page JavaScript
 * Contact Form Submission
 */

// ============================================================================
// DOM ELEMENTS
// ============================================================================
const contactForm = document.getElementById('contact-form');
const submitBtn = document.getElementById('submit-btn');
const successMessage = document.getElementById('success-message');
const formError = document.getElementById('form-error');

// ============================================================================
// EVENT LISTENERS
// ============================================================================
contactForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(contactForm);
    
    // Validate
    const name = formData.get('name');
    const email = formData.get('email');
    const subject = formData.get('subject');
    const message = formData.get('message');
    
    if (!name || !email || !subject || !message) {
        showFormError('Please fill in all fields.');
        return;
    }
    
    // Validate email
    if (!isValidEmail(email)) {
        showFormError('Please enter a valid email address.');
        return;
    }
    
    // Disable submit button
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
    
    try {
        // Send form data
        const response = await fetch('/contact', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Hide form
            contactForm.style.display = 'none';
            formError.style.display = 'none';
            
            // Show success message
            successMessage.style.display = 'block';
            
            // Reset form after 5 seconds
            setTimeout(() => {
                contactForm.reset();
                contactForm.style.display = 'block';
                successMessage.style.display = 'none';
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
            }, 5000);
        } else {
            throw new Error(data.error || 'Failed to send message');
        }
        
    } catch (error) {
        console.error('Contact form error:', error);
        showFormError(error.message || 'An error occurred. Please try again.');
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
    }
});

// ============================================================================
// FUNCTIONS
// ============================================================================

/**
 * Show form error
 */
function showFormError(message) {
    const errorTextElement = document.getElementById('error-text');
    errorTextElement.textContent = message;
    formError.style.display = 'block';
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        formError.style.display = 'none';
    }, 5000);
}

/**
 * Validate email
 */
function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// ============================================================================
// REAL-TIME VALIDATION
// ============================================================================
const emailInput = document.getElementById('email');

emailInput.addEventListener('blur', function() {
    if (this.value && !isValidEmail(this.value)) {
        this.style.borderColor = 'var(--error-color)';
    } else {
        this.style.borderColor = 'var(--border-color)';
    }
});

emailInput.addEventListener('focus', function() {
    this.style.borderColor = 'var(--accent-color)';
});
