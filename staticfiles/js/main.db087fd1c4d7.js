// Portfolio Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initVoteSystem();
    initSearchAndFilters();
    initSmoothScrolling();
    initAnimations();
    initFormValidation();
});

// Vote System
function initVoteSystem() {
    const voteButtons = document.querySelectorAll('.vote-btn');
    
    voteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const projectId = this.dataset.projectId;
            const voteType = this.dataset.voteType;
            const voteCount = this.querySelector('.vote-count');
            
            // Add loading state
            this.classList.add('loading');
            
            // Make AJAX request
            fetch(`/projects/${projectId}/vote/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    vote_type: voteType
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update vote count
                    if (voteCount) {
                        voteCount.textContent = data.likes_count;
                    }
                    
                    // Update button state
                    updateVoteButtonState(this, voteType, data.user_vote);
                    
                    // Show success message
                    showMessage('Voto registrado exitosamente', 'success');
                } else {
                    showMessage(data.message || 'Error al registrar el voto', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('Error al registrar el voto', 'error');
            })
            .finally(() => {
                this.classList.remove('loading');
            });
        });
    });
}

function updateVoteButtonState(button, voteType, userVote) {
    const allVoteButtons = button.closest('.vote-buttons').querySelectorAll('.vote-btn');
    
    // Remove active class from all buttons
    allVoteButtons.forEach(btn => btn.classList.remove('active'));
    
    // Add active class to current vote
    if (userVote === voteType) {
        button.classList.add('active');
    }
}

// Search and Filters
function initSearchAndFilters() {
    const searchInput = document.querySelector('#search-input');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');
    
    // Search functionality
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            projectCards.forEach(card => {
                const title = card.querySelector('.card-title').textContent.toLowerCase();
                const description = card.querySelector('.card-text').textContent.toLowerCase();
                const technologies = Array.from(card.querySelectorAll('.badge-technology'))
                    .map(tech => tech.textContent.toLowerCase())
                    .join(' ');
                
                const matches = title.includes(searchTerm) || 
                              description.includes(searchTerm) || 
                              technologies.includes(searchTerm);
                
                card.style.display = matches ? 'block' : 'none';
            });
        });
    }
    
    // Filter functionality
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.dataset.category;
            
            // Update active filter button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Filter projects
            projectCards.forEach(card => {
                const cardCategory = card.dataset.category;
                
                if (category === 'all' || cardCategory === category) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

// Smooth Scrolling
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Animations
function initAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);
    
    // Observe elements with animation classes
    const animatedElements = document.querySelectorAll('.card, .skill-item, .timeline-item');
    animatedElements.forEach(el => observer.observe(el));
}

// Form Validation
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                    
                    // Add error message
                    let errorDiv = field.parentNode.querySelector('.invalid-feedback');
                    if (!errorDiv) {
                        errorDiv = document.createElement('div');
                        errorDiv.className = 'invalid-feedback';
                        field.parentNode.appendChild(errorDiv);
                    }
                    errorDiv.textContent = 'Este campo es obligatorio';
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showMessage('Por favor, completa todos los campos obligatorios', 'error');
            }
        });
    });
}

// Utility Functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showMessage(message, type = 'info') {
    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    messageDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the page
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(messageDiv, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 5000);
}

// Comment System
function initCommentSystem() {
    const commentForms = document.querySelectorAll('.comment-form');
    
    commentForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const projectId = this.dataset.projectId;
            
            fetch(`/projects/${projectId}/comment/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Add new comment to the list
                    addCommentToList(data.comment);
                    
                    // Clear form
                    this.reset();
                    
                    showMessage('Comentario agregado exitosamente', 'success');
                } else {
                    showMessage(data.message || 'Error al agregar el comentario', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('Error al agregar el comentario', 'error');
            });
        });
    });
}

function addCommentToList(commentData) {
    const commentsContainer = document.querySelector('.comments-list');
    if (!commentsContainer) return;
    
    const commentHtml = `
        <div class="comment">
            <div class="comment-header">
                <span class="comment-author">${commentData.author}</span>
                <span class="comment-date">${commentData.created_at}</span>
            </div>
            <div class="comment-content">
                ${commentData.content}
            </div>
        </div>
    `;
    
    commentsContainer.insertAdjacentHTML('afterbegin', commentHtml);
}

// Initialize comment system if on project detail page
if (document.querySelector('.comment-form')) {
    initCommentSystem();
}

// Mobile menu toggle
function initMobileMenu() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });
        
        // Close menu when clicking on a link
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navbarCollapse.classList.remove('show');
            });
        });
    }
}

// Initialize mobile menu
initMobileMenu();

// Lazy loading for images
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading
initLazyLoading(); 