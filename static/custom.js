// Function to show Register form
function showRegister() {
  const loginBox = document.querySelector(".login_box.login");
  const registerBox = document.querySelector(".login_box.register");

  loginBox.style.display = "none";
  registerBox.style.display = "block";
}

// Function to show Login form
function showLogin() {
  const loginBox = document.querySelector(".login_box.login");
  const registerBox = document.querySelector(".login_box.register");

  registerBox.style.display = "none";
  loginBox.style.display = "block";
}

// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Close mobile menu when clicking on a link
        document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }));
    }
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(255, 255, 255, 0.15)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.1)';
    }
});

// ==================== LOGIN FORM FUNCTIONALITY ====================

// Login form validation and submission
function handleLogin() {
    const username = document.getElementById('user').value.trim();
    const password = document.getElementById('pass').value;
    const rememberMe = document.getElementById('remember').checked;
    
    // Clear previous error messages
    clearErrorMessages();
    
    // Validate inputs
    if (!validateLoginForm(username, password)) {
        return false;
    }
    
    // Show loading state
    const submitBtn = document.querySelector('.input-submit');
    const originalValue = submitBtn.value;
    submitBtn.value = 'Logging in...';
    submitBtn.disabled = true;
    
    // Submit the form to Flask backend
    const form = document.getElementById('loginForm');
    if (form) {
        form.submit();
    }
    
    return false; // Prevent form submission
}

// Login form validation
function validateLoginForm(username, password) {
    let isValid = true;
    
    if (!username) {
        showFieldError('user', 'Username is required');
        isValid = false;
    } else if (username.length < 3) {
        showFieldError('user', 'Username must be at least 3 characters');
        isValid = false;
    }
    
    if (!password) {
        showFieldError('pass', 'Password is required');
        isValid = false;
    } else if (password.length < 6) {
        showFieldError('pass', 'Password must be at least 6 characters');
        isValid = false;
    }
    
    return isValid;
}

// ==================== REGISTER FORM FUNCTIONALITY ====================

// Register form validation and submission
function handleRegister() {
    const fullName = document.getElementById('fullname').value.trim();
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const termsAccepted = document.getElementById('terms').checked;
    
    // Clear previous error messages
    clearErrorMessages();
    
    // Validate inputs
    if (!validateRegisterForm(fullName, username, email, password, confirmPassword, termsAccepted)) {
        return false;
    }
    
    // Show loading state
    const submitBtn = document.querySelector('.input-submit');
    const originalValue = submitBtn.value;
    submitBtn.value = 'Creating Account...';
    submitBtn.disabled = true;
    
    // Submit the form to Flask backend
    const form = document.getElementById('customRegisterForm');
    if (form) {
        form.submit();
    }
    
    return false; // Prevent form submission
}

// Register form validation
function validateRegisterForm(fullName, username, email, password, confirmPassword, termsAccepted) {
    let isValid = true;
    
    // Full name validation
    if (!fullName) {
        showFieldError('fullname', 'Full name is required');
        isValid = false;
    } else if (fullName.length < 2) {
        showFieldError('fullname', 'Full name must be at least 2 characters');
        isValid = false;
    }
    
    // Username validation
    if (!username) {
        showFieldError('username', 'Username is required');
        isValid = false;
    } else if (username.length < 3) {
        showFieldError('username', 'Username must be at least 3 characters');
        isValid = false;
    } else if (!/^[a-zA-Z0-9_]+$/.test(username)) {
        showFieldError('username', 'Username can only contain letters, numbers, and underscores');
        isValid = false;
    }
    
    // Email validation
    if (!email) {
        showFieldError('email', 'Email is required');
        isValid = false;
    } else if (!isValidEmail(email)) {
        showFieldError('email', 'Please enter a valid email address');
        isValid = false;
    }
    
    // Password validation
    if (!password) {
        showFieldError('password', 'Password is required');
        isValid = false;
    } else if (password.length < 8) {
        showFieldError('password', 'Password must be at least 8 characters');
        isValid = false;
    } else if (!isStrongPassword(password)) {
        showFieldError('password', 'Password must contain at least one uppercase letter, one lowercase letter, and one number');
        isValid = false;
    }
    
    // Confirm password validation
    if (!confirmPassword) {
        showFieldError('confirm_password', 'Please confirm your password');
        isValid = false;
    } else if (password !== confirmPassword) {
        showFieldError('confirm_password', 'Passwords do not match');
        isValid = false;
    }
    
    // Terms validation
    if (!termsAccepted) {
        showErrorMessage('You must accept the Terms & Conditions to continue');
        isValid = false;
    }
    
    return isValid;
}

// ==================== UTILITY FUNCTIONS ====================

// Email validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Password strength validation
function isStrongPassword(password) {
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    return hasUpperCase && hasLowerCase && hasNumbers;
}

// Show field-specific error
function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const inputBox = field.closest('.input_box');
    
    // Remove existing error
    const existingError = inputBox.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    
    // Add error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    inputBox.appendChild(errorDiv);
    
    // Add error styling
    field.classList.add('error');
    inputBox.classList.add('error');
}

// Show general error message
function showErrorMessage(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    const form = document.querySelector('.login_box');
    const existingError = form.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    form.insertBefore(errorDiv, form.firstChild);
}

// Show success message
function showSuccessMessage(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    
    const form = document.querySelector('.login_box');
    const existingMessage = form.querySelector('.success-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    form.insertBefore(successDiv, form.firstChild);
}

// Clear all error messages
function clearErrorMessages() {
    // Remove field errors
    document.querySelectorAll('.field-error').forEach(error => error.remove());
    document.querySelectorAll('.error-message').forEach(error => error.remove());
    document.querySelectorAll('.success-message').forEach(message => message.remove());
    
    // Remove error styling
    document.querySelectorAll('.input-field.error').forEach(field => field.classList.remove('error'));
    document.querySelectorAll('.input_box.error').forEach(box => box.classList.remove('error'));
}

// Auto-hide flash messages
function autoHideFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        // Add close button
        const closeBtn = document.createElement('span');
        closeBtn.innerHTML = '&times;';
        closeBtn.className = 'flash-close';
        closeBtn.style.cssText = `
            position: absolute;
            top: 5px;
            right: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            opacity: 0.7;
            transition: opacity 0.3s ease;
        `;
        
        // Make message container relative for absolute positioning
        message.style.position = 'relative';
        message.appendChild(closeBtn);
        
        // Close button click handler
        closeBtn.addEventListener('click', function() {
            hideFlashMessage(message);
        });
        
        // Close button hover effect
        closeBtn.addEventListener('mouseenter', function() {
            this.style.opacity = '1';
        });
        
        closeBtn.addEventListener('mouseleave', function() {
            this.style.opacity = '0.7';
        });
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            hideFlashMessage(message);
        }, 5000);
    });
}

// Hide flash message with animation
function hideFlashMessage(message) {
    if (message && message.parentNode) {
        message.style.animation = 'slideOut 0.3s ease-out forwards';
        setTimeout(() => {
            if (message.parentNode) {
                message.parentNode.removeChild(message);
            }
        }, 300);
    }
}

// ==================== EVENT LISTENERS ====================


// Clear specific field error
function clearFieldError(fieldId) {
    const field = document.getElementById(fieldId);
    if (field) {
        const inputBox = field.closest('.input_box');
        const errorDiv = inputBox.querySelector('.field-error');
        if (errorDiv) {
            errorDiv.remove();
        }
        field.classList.remove('error');
        inputBox.classList.remove('error');
    }
}

// ==================== CHAT FUNCTIONALITY ====================

// Chat interface functionality
let chatInitialized = false;

function initializeChat() {
    // Prevent multiple initializations
    if (chatInitialized) {
        console.log('Chat already initialized, skipping...');
        return;
    }
    
    console.log('Initializing chat...');
    
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');
    const charCount = document.getElementById('charCount');
    const typingIndicator = document.getElementById('typingIndicator');
    const loadingOverlay = document.getElementById('loadingOverlay');
    
    if (!messageInput || !sendButton || !chatMessages) return;
    
    // Mark as initialized
    chatInitialized = true;
    
    // Auto-resize textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        
        // Update character count
        if (charCount) {
            charCount.textContent = this.value.length;
        }
    });
    
    // Send message on Enter (but allow Shift+Enter for new lines)
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Send button click
    sendButton.addEventListener('click', sendMessage);
    
    document.querySelectorAll('.quick-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();  
            e.stopPropagation(); 
            console.log('Quick button clicked:', this.getAttribute('data-message'));
            const message = this.getAttribute('data-message');
            if (message) {
                messageInput.value = message;
                messageInput.style.height = 'auto';
                messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
                sendMessage();
            }
        });
    });
    
    // Function to send message
    async function sendMessage() {
        console.log('sendMessage called with:', messageInput.value.trim());
        const message = messageInput.value.trim();
        if (!message) return;
        
        // Disable input and button
        messageInput.disabled = true;
        sendButton.disabled = true;
        
        // Add user message to chat
        addMessageToChat(message, 'user');
        
        // Clear input
        messageInput.value = '';
        messageInput.style.height = 'auto';
        if (charCount) charCount.textContent = '0';
        
        // Show typing indicator
        showTypingIndicator();
        
        try {
            // Send message to backend
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: message })
            });
            
            const data = await response.json();
            
            // Hide typing indicator
            hideTypingIndicator();
            
            if (!response.ok) {
                // Handle specific error responses
                const errorMessage = data.error || 'An error occurred';
                addMessageToChat(`Error: ${errorMessage}`, 'ai');
                return;
            }
            
            // Check if we have a valid reply
            if (data.reply) {
                addMessageToChat(data.reply, 'ai');
            } else {
                addMessageToChat('Sorry, I received an empty response. Please try again.', 'ai');
            }
            
        } catch (error) {
            console.error('Error:', error);
            hideTypingIndicator();
            
            // More specific error messages
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                addMessageToChat('Network error: Please check your internet connection and try again.', 'ai');
            } else if (error.name === 'SyntaxError') {
                addMessageToChat('Error: Invalid response from server. Please try again.', 'ai');
            } else {
                addMessageToChat('Sorry, I encountered an unexpected error. Please try again.', 'ai');
            }
        } finally {
            // Re-enable input and button
            messageInput.disabled = false;
            sendButton.disabled = false;
            messageInput.focus();
        }
    }
    
    // Function to add message to chat
    function addMessageToChat(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.innerHTML = formatMessage(text);
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = new Date().toLocaleTimeString();
        
        content.appendChild(messageText);
        content.appendChild(messageTime);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to format message text (basic markdown-like formatting)
    function formatMessage(text) {
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>')
            .replace(/`(.*?)`/g, '<code>$1</code>');
    }
    
    // Function to show typing indicator
    function showTypingIndicator() {
        if (typingIndicator) {
            typingIndicator.style.display = 'block';
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    
    // Function to hide typing indicator
    function hideTypingIndicator() {
        if (typingIndicator) {
            typingIndicator.style.display = 'none';
        }
    }
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages
    autoHideFlashMessages();
    
    // Initialize chat if on home page
    if (window.location.pathname.includes('home')) {
        initializeChat();
    }
    
    // Initialize symptom checker if on symptoms check page
    if (window.location.pathname.includes('symptoms-check')) {
        initializeSymptomChecker();
    }
    
    // Initialize profile management if on profile page
    if (window.location.pathname.includes('view-profile') || window.location.pathname.includes('profile')) {
        initializeProfileManagement();
    }
    
    // Note: Login and Register form submissions are handled inline in their respective HTML files
    // to avoid conflicts with Firebase authentication
    
    // Real-time validation for register form
    if (window.location.pathname.includes('register')) {
        const confirmPasswordField = document.getElementById('confirm_password');
        const passwordField = document.getElementById('password');
        
        if (confirmPasswordField && passwordField) {
            confirmPasswordField.addEventListener('input', function() {
                if (this.value && passwordField.value && this.value !== passwordField.value) {
                    showFieldError('confirm_password', 'Passwords do not match');
                } else {
                    clearFieldError('confirm_password');
                }
            });
        }
    }
    
    // Clear field errors on input
    document.querySelectorAll('.input-field').forEach(field => {
        field.addEventListener('input', function() {
            clearFieldError(this.id);
        });
    });
});

// ==================== SYMPTOM CHECKER FUNCTIONALITY ====================

// Initialize symptom checker when DOM is loaded
function initializeSymptomChecker() {
    const form = document.getElementById('symptomForm');
    const clearBtn = document.getElementById('clearForm');
    const submitBtn = document.getElementById('submitForm');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');

    if (!form || !clearBtn || !submitBtn) return;

    // Character counters
    const symptomTextarea = document.getElementById('mainSymptoms');
    const historyTextarea = document.getElementById('medicalHistory');
    const additionalTextarea = document.getElementById('additionalInfo');
    const symptomCounter = document.getElementById('symptomCharCount');
    const historyCounter = document.getElementById('historyCharCount');
    const additionalCounter = document.getElementById('additionalCharCount');

    // Update character counters
    function updateCharCounter(textarea, counter) {
        if (textarea && counter) {
            textarea.addEventListener('input', function() {
                counter.textContent = this.value.length;
            });
        }
    }

    updateCharCounter(symptomTextarea, symptomCounter);
    updateCharCounter(historyTextarea, historyCounter);
    updateCharCounter(additionalTextarea, additionalCounter);

    // Clear form
    clearBtn.addEventListener('click', function() {
            form.reset();
            if (resultsSection) resultsSection.style.display = 'none';
            if (symptomCounter) symptomCounter.textContent = '0';
            if (historyCounter) historyCounter.textContent = '0';
            if (additionalCounter) additionalCounter.textContent = '0';
    });

    // Form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Validate form
        const requiredFields = ['age', 'gender', 'mainSymptoms', 'onsetTime', 'severity'];
        let isValid = true;
        
        requiredFields.forEach(field => {
            const input = document.getElementById(field);
            if (!input.value.trim()) {
                input.classList.add('error');
                isValid = false;
            } else {
                input.classList.remove('error');
            }
        });

        if (!isValid) {
            alert('Please fill in all required fields.');
            return;
        }

        // Show loading spinner
        if (loadingSpinner) loadingSpinner.style.display = 'block';
        if (resultsSection) resultsSection.style.display = 'none';
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';

        try {
            // Prepare form data
            const formData = {
                age: document.getElementById('age').value,
                gender: document.getElementById('gender').value,
                mainSymptoms: document.getElementById('mainSymptoms').value,
                onsetTime: document.getElementById('onsetTime').value,
                severity: document.getElementById('severity').value,
                medicalHistory: document.getElementById('medicalHistory').value,
                additionalInfo: document.getElementById('additionalInfo').value
            };

            // Make API call
            const response = await fetch('/check-symptoms', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                // Display results
                displaySymptomResults(data);
            } else {
                throw new Error(data.error || 'Failed to analyze symptoms');
            }

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while analyzing your symptoms. Please try again.');
        } finally {
            // Hide loading spinner
            if (loadingSpinner) loadingSpinner.style.display = 'none';
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-search"></i> Analyze Symptoms';
        }
    });

    // Display results
    function displaySymptomResults(data) {
        if (!resultsContent) return;
        
        resultsContent.innerHTML = '';
        
        if (data.diagnoses && data.diagnoses.length > 0) {
            data.diagnoses.forEach((diagnosis, index) => {
                const diagnosisCard = document.createElement('div');
                diagnosisCard.className = 'symptom-diagnosis-card';
                diagnosisCard.innerHTML = `
                    <div class="symptom-diagnosis-header">
                        <h4>${diagnosis.diagnosis}</h4>
                    </div>
                    <div class="symptom-diagnosis-description">
                        <p>${diagnosis.description}</p>
                    </div>
                    ${diagnosis.recommendations ? `
                        <div class="symptom-diagnosis-recommendations">
                            <h5><i class="fas fa-lightbulb"></i> Recommendations:</h5>
                            <ul>
                                ${diagnosis.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                `;
                resultsContent.appendChild(diagnosisCard);
            });
        } else {
            resultsContent.innerHTML = `
                <div class="symptom-no-results">
                    <i class="fas fa-exclamation-circle"></i>
                    <h3>No specific diagnoses found</h3>
                    <p>Based on your symptoms, we recommend consulting with a healthcare professional for a proper evaluation.</p>
                </div>
            `;
        }

        if (resultsSection) {
            resultsSection.style.display = 'block';
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        }
    }

    // Add form validation styling
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.classList.add('error');
            } else {
                this.classList.remove('error');
            }
        });
    });
}


// Just to confirm JS is working
console.log("custom.js loaded with login, register, chat, symptom checker, and profile functionality");

// ==================== PROFILE MANAGEMENT FUNCTIONALITY ====================

// Initialize profile management when DOM is loaded
function initializeProfileManagement() {
    const editProfileBtn = document.getElementById('editProfileBtn');
    const updateProfileActionBtn = document.getElementById('updateProfileActionBtn');
    const cancelEditBtn = document.getElementById('cancelEditBtn');
    const updateProfileForm = document.getElementById('updateProfileForm');
    const deleteProfileBtn = document.getElementById('deleteProfileBtn');
    const deleteModal = document.getElementById('deleteModal');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
    const confirmDeleteInput = document.getElementById('confirmDelete');
    const modalClose = document.querySelector('.modal-close');
    const loadingOverlay = document.getElementById('loadingOverlay');

    if (!editProfileBtn || !updateProfileForm) return;

    // Edit Profile Button (in section header)
    editProfileBtn.addEventListener('click', function() {
        showEditMode();
    });

    // Update Profile Button (in action buttons)
    if (updateProfileActionBtn) {
        updateProfileActionBtn.addEventListener('click', function() {
            showEditMode();
        });
    }

    // Cancel Edit Button
    if (cancelEditBtn) {
        cancelEditBtn.addEventListener('click', function() {
            showViewMode();
        });
    }

    // Update Profile Form Submission
    updateProfileForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        await handleProfileUpdate();
    });

    // Delete Profile Button
    if (deleteProfileBtn) {
        deleteProfileBtn.addEventListener('click', function() {
            showDeleteModal();
        });
    }

    // Modal Event Listeners
    if (modalClose) {
        modalClose.addEventListener('click', hideDeleteModal);
    }

    if (cancelDeleteBtn) {
        cancelDeleteBtn.addEventListener('click', hideDeleteModal);
    }

    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', handleProfileDeletion);
    }

    // Confirm Delete Input Validation
    if (confirmDeleteInput) {
        confirmDeleteInput.addEventListener('input', function() {
            const deleteBtn = document.getElementById('confirmDeleteBtn');
            if (this.value === 'DELETE') {
                deleteBtn.disabled = false;
                deleteBtn.style.opacity = '1';
            } else {
                deleteBtn.disabled = true;
                deleteBtn.style.opacity = '0.5';
            }
        });
    }

    // Close modal when clicking outside
    if (deleteModal) {
        deleteModal.addEventListener('click', function(e) {
            if (e.target === deleteModal) {
                hideDeleteModal();
            }
        });
    }

    // Show Edit Mode
    function showEditMode() {
        const viewMode = document.getElementById('profileViewMode');
        const editMode = document.getElementById('profileEditMode');
        
        if (viewMode && editMode) {
            viewMode.style.display = 'none';
            editMode.style.display = 'block';
            
            // Scroll to edit form
            editMode.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    // Show View Mode
    function showViewMode() {
        const viewMode = document.getElementById('profileViewMode');
        const editMode = document.getElementById('profileEditMode');
        
        if (viewMode && editMode) {
            editMode.style.display = 'none';
            viewMode.style.display = 'block';
            
            // Reset form to original values
            resetFormToOriginalValues();
        }
    }

    // Reset form to original values
    function resetFormToOriginalValues() {
        const form = document.getElementById('updateProfileForm');
        if (form) {
            form.reset();
            // Clear any validation errors
            clearFormErrors();
        }
    }

    // Handle Profile Update
    async function handleProfileUpdate() {
        const form = document.getElementById('updateProfileForm');
        const formData = new FormData(form);
        
        // Validate form
        if (!validateProfileForm()) {
            return;
        }

        // Show loading
        showLoading();

        try {
            // Prepare data for API
            const updateData = {
                username: formData.get('username'),
                email: formData.get('email'),
                full_name: formData.get('full_name'),
                phone_number: formData.get('phone_number'),
                date_of_birth: formData.get('date_of_birth')
            };

            // Add password fields if they exist and have values
            const password = formData.get('password');
            const confirmPassword = formData.get('confirm_password');
            
            if (password && password.trim() !== '') {
                updateData.password = password;
                updateData.confirm_password = confirmPassword;
            }

            // Make API call
            const response = await fetch('/update-profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updateData)
            });

            const data = await response.json();

            if (response.ok) {
                // Show success message
                showSuccessMessage('Profile updated successfully!');
                
                // Switch back to view mode
                showViewMode();
                
                // Reload page to show updated data
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                throw new Error(data.error || 'Failed to update profile');
            }

        } catch (error) {
            console.error('Error updating profile:', error);
            showErrorMessage('Failed to update profile. Please try again.');
        } finally {
            hideLoading();
        }
    }

    // Validate Profile Form
    function validateProfileForm() {
        const form = document.getElementById('updateProfileForm');
        const formData = new FormData(form);
        
        let isValid = true;
        clearFormErrors();

        // Username validation
        const username = formData.get('username');
        if (!username || username.trim().length < 3) {
            showFieldError('editUsername', 'Username must be at least 3 characters');
            isValid = false;
        }

        // Email validation (only for custom accounts)
        const email = formData.get('email');
        const emailField = document.getElementById('editEmail');
        if (!emailField.readOnly && (!email || !isValidEmail(email))) {
            showFieldError('editEmail', 'Please enter a valid email address');
            isValid = false;
        }

        // Password validation (if provided)
        const password = formData.get('password');
        const confirmPassword = formData.get('confirm_password');
        
        if (password && password.trim() !== '') {
            if (password.length < 8) {
                showFieldError('editPassword', 'Password must be at least 8 characters');
                isValid = false;
            } else if (!isStrongPassword(password)) {
                showFieldError('editPassword', 'Password must contain uppercase, lowercase, and number');
                isValid = false;
            }
            
            if (password !== confirmPassword) {
                showFieldError('editConfirmPassword', 'Passwords do not match');
                isValid = false;
            }
        }

        return isValid;
    }

    // Show Delete Modal
    function showDeleteModal() {
        if (deleteModal) {
            deleteModal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
            
            // Reset confirmation input
            if (confirmDeleteInput) {
                confirmDeleteInput.value = '';
                const deleteBtn = document.getElementById('confirmDeleteBtn');
                if (deleteBtn) {
                    deleteBtn.disabled = true;
                    deleteBtn.style.opacity = '0.5';
                }
            }
        }
    }

    // Hide Delete Modal
    function hideDeleteModal() {
        if (deleteModal) {
            deleteModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }

    // Handle Profile Deletion
    async function handleProfileDeletion() {
        const confirmInput = document.getElementById('confirmDelete');
        if (!confirmInput || confirmInput.value !== 'DELETE') {
            return;
        }

        // Show loading
        showLoading();

        try {
            const response = await fetch('/delete-profile', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (response.ok) {
                // Show success message
                showSuccessMessage('Account deleted successfully. Redirecting...');
                
                // Redirect to login page after delay
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
            } else {
                throw new Error(data.error || 'Failed to delete account');
            }

        } catch (error) {
            console.error('Error deleting profile:', error);
            showErrorMessage('Failed to delete account. Please try again.');
        } finally {
            hideLoading();
            hideDeleteModal();
        }
    }

    // Show Loading
    function showLoading() {
        if (loadingOverlay) {
            loadingOverlay.style.display = 'flex';
        }
    }

    // Hide Loading
    function hideLoading() {
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
    }

    // Show Success Message
    function showSuccessMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'flash-message success';
        messageDiv.innerHTML = `
            <i class="fas fa-check-circle"></i>
            ${message}
        `;
        
        const flashContainer = document.querySelector('.flash-container');
        if (flashContainer) {
            flashContainer.appendChild(messageDiv);
        } else {
            // Create flash container if it doesn't exist
            const container = document.createElement('div');
            container.className = 'flash-container';
            container.appendChild(messageDiv);
            document.body.insertBefore(container, document.body.firstChild);
        }
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 5000);
    }

    // Show Error Message
    function showErrorMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'flash-message error';
        messageDiv.innerHTML = `
            <i class="fas fa-exclamation-circle"></i>
            ${message}
        `;
        
        const flashContainer = document.querySelector('.flash-container');
        if (flashContainer) {
            flashContainer.appendChild(messageDiv);
        } else {
            // Create flash container if it doesn't exist
            const container = document.createElement('div');
            container.className = 'flash-container';
            container.appendChild(messageDiv);
            document.body.insertBefore(container, document.body.firstChild);
        }
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 5000);
    }

    // Show Field Error
    function showFieldError(fieldId, message) {
        const field = document.getElementById(fieldId);
        if (!field) return;
        
        const formGroup = field.closest('.form-group');
        if (!formGroup) return;
        
        // Remove existing error
        const existingError = formGroup.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
        
        // Add error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.textContent = message;
        formGroup.appendChild(errorDiv);
        
        // Add error styling
        field.classList.add('error');
    }

    // Clear Form Errors
    function clearFormErrors() {
        // Remove field errors
        document.querySelectorAll('.field-error').forEach(error => error.remove());
        
        // Remove error styling
        document.querySelectorAll('.form-group input.error').forEach(field => {
            field.classList.remove('error');
        });
    }

    // Clear field error on input
    document.querySelectorAll('#updateProfileForm input').forEach(field => {
        field.addEventListener('input', function() {
            const formGroup = this.closest('.form-group');
            const errorDiv = formGroup.querySelector('.field-error');
            if (errorDiv) {
                errorDiv.remove();
            }
            this.classList.remove('error');
        });
    });
}

// Hook up Medical Info edit toggling and save for viewProfile
document.addEventListener('DOMContentLoaded', function() {
    if (!(window.location.pathname.includes('view-profile') || window.location.pathname.includes('profile'))) return;

    const editBtn = document.getElementById('editMedicalBtn');
    const viewGrid = document.getElementById('medicalViewMode');
    const editContainer = document.getElementById('medicalEditMode');
    const cancelBtn = document.getElementById('cancelMedicalEditBtn');
    const saveBtn = document.getElementById('saveMedicalBtn');

    if (editBtn && viewGrid && editContainer) {
        editBtn.addEventListener('click', () => {
            viewGrid.style.display = 'none';
            editContainer.style.display = 'block';
            editContainer.scrollIntoView({ behavior: 'smooth' });
        });
    }

    if (cancelBtn && viewGrid && editContainer) {
        cancelBtn.addEventListener('click', () => {
            editContainer.style.display = 'none';
            viewGrid.style.display = 'grid';
        });
    }

    if (saveBtn) {
        saveBtn.addEventListener('click', async () => {
            const form = document.getElementById('updateMedicalForm');
            if (!form) return;
            const fd = new FormData(form);
            const payload = Object.fromEntries(fd.entries());

            try {
                const res = await fetch('/update-medical-info', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.error || 'Failed to update');
                window.location.reload();
            } catch (e) {
                alert(e.message || 'Failed to save medical info');
            }
        });
    }
});

// Book Appointment functionality
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('book-appointment-btn') || e.target.closest('.book-appointment-btn')) {
        const button = e.target.classList.contains('book-appointment-btn') ? e.target : e.target.closest('.book-appointment-btn');
        const doctorId = button.getAttribute('data-doctor-id');
        
        if (doctorId) {
            // For now, show an alert. Later you can implement a modal or redirect to appointment page
            alert(`Upgrade to our Premium Plan To Make Appointment Via Online`);
            
        }
    }
});
