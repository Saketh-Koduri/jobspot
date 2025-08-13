// ========== MODERN JOB BOARD JAVASCRIPT ========== //

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    initTheme();
    initAnimations();
    initJobFilters();
    initFormValidation();
    initTooltips();
    initConfirmDialogs();
    initAutoHideAlerts();
    initSearchFunctionality();
}

// ========== THEME MANAGEMENT ========== //
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute("data-bs-theme");
    const newTheme = current === "light" ? "dark" : "light";
    
    html.setAttribute("data-bs-theme", newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
    
    // Add smooth transition effect
    document.body.style.transition = 'all 0.3s ease';
    setTimeout(() => {
        document.body.style.transition = '';
    }, 300);
}

function updateThemeIcon(theme) {
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.innerHTML = theme === 'light' ? '🌙' : '☀️';
        themeToggle.title = `Switch to ${theme === 'light' ? 'dark' : 'light'} mode`;
    }
}

// ========== ANIMATIONS ========== //
function initAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card, .job-card, .application-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-up');
    });
    
    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    });
    
    document.querySelectorAll('.stat-card').forEach(el => observer.observe(el));
}

// ========== JOB FILTERING ========== //
function initJobFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const searchInput = document.getElementById('jobSearch');
    const locationFilter = document.getElementById('locationFilter');
    const typeFilter = document.getElementById('typeFilter');
    
    if (filterButtons.length > 0) {
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => filterJobs(btn.dataset.filter));
        });
    }
    
    if (searchInput) {
        searchInput.addEventListener('input', debounce(filterJobs, 300));
    }
    
    if (locationFilter) {
        locationFilter.addEventListener('change', filterJobs);
    }
    
    if (typeFilter) {
        typeFilter.addEventListener('change', filterJobs);
    }
}

function filterJobs(filterType = 'all') {
    const jobs = document.querySelectorAll('.job-card');
    const searchTerm = document.getElementById('jobSearch')?.value.toLowerCase() || '';
    const locationFilter = document.getElementById('locationFilter')?.value || '';
    const typeFilter = document.getElementById('typeFilter')?.value || '';
    
    jobs.forEach(job => {
        const title = job.querySelector('.job-title')?.textContent.toLowerCase() || '';
        const location = job.querySelector('.job-location')?.textContent.toLowerCase() || '';
        const type = job.querySelector('.job-type-badge')?.textContent.toLowerCase() || '';
        const description = job.querySelector('.job-description')?.textContent.toLowerCase() || '';
        
        const matchesSearch = title.includes(searchTerm) || 
                            description.includes(searchTerm) ||
                            location.includes(searchTerm);
        const matchesLocation = !locationFilter || location.includes(locationFilter.toLowerCase());
        const matchesType = !typeFilter || type.includes(typeFilter.toLowerCase());
        
        if (matchesSearch && matchesLocation && matchesType) {
            job.style.display = 'block';
            job.classList.add('fade-in-up');
        } else {
            job.style.display = 'none';
        }
    });
    
    updateJobCount();
}

function updateJobCount() {
    const visibleJobs = document.querySelectorAll('.job-card[style*="block"], .job-card:not([style*="none"])');
    const countElement = document.getElementById('jobCount');
    if (countElement) {
        countElement.textContent = `${visibleJobs.length} jobs found`;
    }
}

// ========== FORM VALIDATION ========== //
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                showFormErrors(form);
            } else {
                showLoadingSpinner(form);
            }
            form.classList.add('was-validated');
        });
    });
}

function showFormErrors(form) {
    const invalidInputs = form.querySelectorAll(':invalid');
    invalidInputs.forEach(input => {
        input.classList.add('is-invalid');
        input.addEventListener('input', () => {
            if (input.checkValidity()) {
                input.classList.remove('is-invalid');
                input.classList.add('is-valid');
            }
        });
    });
}

function showLoadingSpinner(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
        submitBtn.disabled = true;
        
        // Re-enable after 10 seconds as fallback
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 10000);
    }
}

// ========== TOOLTIPS ========== //
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ========== CONFIRM DIALOGS ========== //
function initConfirmDialogs() {
    document.querySelectorAll('[data-confirm]').forEach(element => {
        element.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm');
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}

// ========== AUTO-HIDE ALERTS ========== //
function initAutoHideAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (!alert.classList.contains('alert-danger')) {
            setTimeout(() => {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500);
            }, 5000);
        }
    });
}

// ========== SEARCH FUNCTIONALITY ========== //
function initSearchFunctionality() {
    const searchInput = document.getElementById('globalSearch');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(performGlobalSearch, 300));
    }
}

function performGlobalSearch() {
    const searchTerm = document.getElementById('globalSearch').value;
    if (searchTerm.length > 2) {
        // Here you could implement AJAX search
        console.log('Searching for:', searchTerm);
        showSearchResults(searchTerm);
    }
}

function showSearchResults(term) {
    // Placeholder for search results display
    const resultsContainer = document.getElementById('searchResults');
    if (resultsContainer) {
        resultsContainer.innerHTML = `<div class="spinner"></div>`;
        // Simulate API call
        setTimeout(() => {
            resultsContainer.innerHTML = `<p>Search results for "${term}" would appear here</p>`;
        }, 1000);
    }
}

// ========== UTILITY FUNCTIONS ========== //
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    });
}

// ========== APPLICATION STATUS UPDATES ========== //
function updateApplicationStatus(applicationId, status) {
    const statusElement = document.querySelector(`[data-application-id="${applicationId}"] .application-status`);
    if (statusElement) {
        statusElement.className = `application-status status-${status}`;
        statusElement.textContent = status.charAt(0).toUpperCase() + status.slice(1);
        showNotification(`Application status updated to ${status}`, 'success');
    }
}

// ========== JOB ACTIONS ========== //
function deleteJob(jobId) {
    if (confirm('Are you sure you want to delete this job posting?')) {
        // Here you would make an AJAX call to delete the job
        console.log('Deleting job:', jobId);
        showNotification('Job deleted successfully', 'success');
    }
}

function shareJob(jobId, jobTitle) {
    const url = window.location.origin + `/jobs/${jobId}/`;
    const text = `Check out this job opportunity: ${jobTitle}`;
    
    if (navigator.share) {
        navigator.share({
            title: jobTitle,
            text: text,
            url: url
        });
    } else {
        copyToClipboard(url);
    }
}

// ========== FORM ENHANCEMENTS ========== //
function initFileUpload() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const fileName = this.files[0]?.name;
            const label = this.nextElementSibling;
            if (label && fileName) {
                label.textContent = fileName;
                label.classList.add('text-success');
            }
        });
    });
}

// ========== INITIALIZATION CALLS ========== //
document.addEventListener('DOMContentLoaded', function() {
    initFileUpload();
});

// ========== EXPORT FOR GLOBAL ACCESS ========== //
window.jobBoard = {
    toggleTheme,
    filterJobs,
    updateApplicationStatus,
    deleteJob,
    shareJob,
    showNotification,
    copyToClipboard
};