// Main JavaScript for E-Commerce Store
document.addEventListener('DOMContentLoaded', function() {
    // Initialize cart count
    updateCartCount();
    
    // Add to cart functionality
    initializeAddToCart();
    
    // Initialize quantity controls
    initializeQuantityControls();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize image lazy loading
    initializeLazyLoading();
});

// Update cart count in navigation
function updateCartCount() {
    fetch('/shop/cart/count')
        .then(response => response.json())
        .then(data => {
            const cartBadge = document.querySelector('.cart-count');
            if (cartBadge) {
                cartBadge.textContent = data.count || 0;
                cartBadge.style.display = data.count > 0 ? 'inline-block' : 'none';
            }
        })
        .catch(error => console.log('Cart count update failed:', error));
}

// Add to cart functionality
function initializeAddToCart() {
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Adding...';
            submitBtn.disabled = true;
            
            fetch('/shop/add-to-cart', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('Product added to cart!', 'success');
                    updateCartCount();
                    
                    // Show success animation
                    submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Added!';
                    submitBtn.classList.remove('btn-primary');
                    submitBtn.classList.add('btn-success');
                    
                    setTimeout(() => {
                        submitBtn.innerHTML = originalText;
                        submitBtn.classList.remove('btn-success');
                        submitBtn.classList.add('btn-primary');
                        submitBtn.disabled = false;
                    }, 2000);
                } else {
                    showAlert(data.message || 'Error adding product to cart', 'error');
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }
            })
            .catch(error => {
                showAlert('Error adding product to cart', 'error');
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            });
        });
    });
}

// Quantity controls
function initializeQuantityControls() {
    const quantityInputs = document.querySelectorAll('.quantity-input');
    
    quantityInputs.forEach(input => {
        // Add plus/minus buttons if they don't exist
        if (!input.parentNode.querySelector('.quantity-btn')) {
            wrapQuantityInput(input);
        }
        
        // Handle direct input changes
        input.addEventListener('change', function() {
            const min = parseInt(input.getAttribute('min')) || 1;
            const max = parseInt(input.getAttribute('max')) || 100;
            let value = parseInt(input.value) || min;
            
            value = Math.max(min, Math.min(max, value));
            input.value = value;
            
            // Trigger update if this is a cart item
            if (input.closest('.cart-item')) {
                updateCartItem(input);
            }
        });
    });
}

// Wrap quantity input with plus/minus buttons
function wrapQuantityInput(input) {
    const wrapper = document.createElement('div');
    wrapper.className = 'input-group input-group-sm';
    wrapper.style.width = '120px';
    
    const minusBtn = document.createElement('button');
    minusBtn.className = 'btn btn-outline-secondary quantity-btn';
    minusBtn.type = 'button';
    minusBtn.innerHTML = '<i class="fas fa-minus"></i>';
    
    const plusBtn = document.createElement('button');
    plusBtn.className = 'btn btn-outline-secondary quantity-btn';
    plusBtn.type = 'button';
    plusBtn.innerHTML = '<i class="fas fa-plus"></i>';
    
    input.parentNode.insertBefore(wrapper, input);
    wrapper.appendChild(minusBtn);
    wrapper.appendChild(input);
    wrapper.appendChild(plusBtn);
    
    // Add event listeners
    minusBtn.addEventListener('click', () => {
        const current = parseInt(input.value) || 1;
        const min = parseInt(input.getAttribute('min')) || 1;
        if (current > min) {
            input.value = current - 1;
            input.dispatchEvent(new Event('change'));
        }
    });
    
    plusBtn.addEventListener('click', () => {
        const current = parseInt(input.value) || 1;
        const max = parseInt(input.getAttribute('max')) || 100;
        if (current < max) {
            input.value = current + 1;
            input.dispatchEvent(new Event('change'));
        }
    });
}

// Update cart item via AJAX
function updateCartItem(input) {
    const cartItem = input.closest('.cart-item');
    const productId = cartItem.dataset.productId;
    const quantity = parseInt(input.value);
    
    if (!productId) return;
    
    const formData = new FormData();
    formData.append('product_id', productId);
    formData.append('quantity', quantity);
    
    fetch('/shop/update-cart', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update cart totals
            updateCartTotals();
            if (quantity === 0) {
                cartItem.remove();
            }
        } else {
            showAlert(data.message || 'Error updating cart', 'error');
        }
    })
    .catch(error => {
        showAlert('Error updating cart', 'error');
    });
}

// Update cart totals
function updateCartTotals() {
    fetch('/shop/cart/totals')
        .then(response => response.json())
        .then(data => {
            const subtotalEl = document.querySelector('.cart-subtotal');
            const totalEl = document.querySelector('.cart-total');
            
            if (subtotalEl) subtotalEl.textContent = `$${data.subtotal.toFixed(2)}`;
            if (totalEl) totalEl.textContent = `$${data.total.toFixed(2)}`;
        })
        .catch(error => console.log('Cart totals update failed:', error));
}

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('search-input');
    const searchForm = searchInput?.closest('form');
    
    if (searchInput && searchForm) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            
            if (this.value.length >= 3) {
                searchTimeout = setTimeout(() => {
                    // Auto-submit search after 500ms delay
                    searchForm.submit();
                }, 500);
            }
        });
    }
}

// Lazy loading for images
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
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
    } else {
        // Fallback for older browsers
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

// Show alert messages
function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert.auto-dismiss');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show auto-dismiss`;
    alertDiv.innerHTML = `
        ${getAlertIcon(type)}
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to page
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Get alert icon based on type
function getAlertIcon(type) {
    const icons = {
        success: '<i class="fas fa-check-circle me-2"></i>',
        error: '<i class="fas fa-exclamation-triangle me-2"></i>',
        warning: '<i class="fas fa-exclamation-circle me-2"></i>',
        info: '<i class="fas fa-info-circle me-2"></i>'
    };
    return icons[type] || icons.info;
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

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

// Export functions for use in other scripts
window.ecommerce = {
    updateCartCount,
    showAlert,
    formatCurrency,
    debounce
};