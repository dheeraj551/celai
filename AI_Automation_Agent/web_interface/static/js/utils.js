/**
 * AI Automation Agent - Utility Functions
 * Common utility functions used across the web interface
 */

// Utility functions
const Utils = {
    /**
     * Format numbers with appropriate suffixes (K, M, B)
     */
    formatNumber(num) {
        if (num === null || num === undefined) return '0';
        if (num >= 1000000000) return (num / 1000000000).toFixed(1) + 'B';
        if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
        if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
        return num.toString();
    },

    /**
     * Format bytes into human readable format
     */
    formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    },

    /**
     * Format duration in seconds to human readable format
     */
    formatDuration(seconds) {
        if (seconds < 60) return `${Math.round(seconds)}s`;
        if (seconds < 3600) return `${Math.round(seconds / 60)}m`;
        if (seconds < 86400) return `${Math.round(seconds / 3600)}h ${Math.round((seconds % 3600) / 60)}m`;
        return `${Math.round(seconds / 86400)}d ${Math.round((seconds % 86400) / 3600)}h`;
    },

    /**
     * Format uptime from seconds
     */
    formatUptime(seconds) {
        const days = Math.floor(seconds / 86400);
        const hours = Math.floor((seconds % 86400) / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        
        if (days > 0) return `${days}d ${hours}h`;
        if (hours > 0) return `${hours}h ${minutes}m`;
        if (minutes > 0) return `${minutes}m`;
        return '< 1m';
    },

    /**
     * Format date to relative time (e.g., "2 hours ago")
     */
    timeAgo(timestamp) {
        const now = new Date();
        const time = new Date(timestamp);
        const diffInSeconds = (now - time) / 1000;
        
        if (diffInSeconds < 60) return 'Just now';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
        if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}d ago`;
        return time.toLocaleDateString();
    },

    /**
     * Format date to localized string
     */
    formatDate(date, options = {}) {
        const defaultOptions = {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        
        return new Date(date).toLocaleDateString('en-US', {
            ...defaultOptions,
            ...options
        });
    },

    /**
     * Truncate text to specified length
     */
    truncateText(text, maxLength = 50, suffix = '...') {
        if (!text) return '';
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + suffix;
    },

    /**
     * Generate random ID
     */
    generateId(length = 8) {
        return Math.random().toString(36).substr(2, length);
    },

    /**
     * Debounce function
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Throttle function
     */
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },

    /**
     * Copy text to clipboard
     */
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (err) {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            try {
                document.execCommand('copy');
                return true;
            } catch (err) {
                return false;
            } finally {
                document.body.removeChild(textArea);
            }
        }
    },

    /**
     * Validate email address
     */
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },

    /**
     * Validate URL
     */
    isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    },

    /**
     * Sanitize HTML to prevent XSS
     */
    sanitizeHTML(html) {
        const div = document.createElement('div');
        div.textContent = html;
        return div.innerHTML;
    },

    /**
     * Download data as file
     */
    downloadFile(data, filename, type = 'application/json') {
        const blob = new Blob([data], { type });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    },

    /**
     * Read file as text
     */
    readFileAsText(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsText(file);
        });
    },

    /**
     * Color utilities
     */
    colors: {
        /**
         * Convert hex to RGB
         */
        hexToRgb(hex) {
            const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
            return result ? {
                r: parseInt(result[1], 16),
                g: parseInt(result[2], 16),
                b: parseInt(result[3], 16)
            } : null;
        },

        /**
         * Get contrast color (black or white) for given hex color
         */
        getContrastColor(hex) {
            const rgb = this.hexToRgb(hex);
            if (!rgb) return '#000000';
            
            const brightness = (rgb.r * 299 + rgb.g * 587 + rgb.b * 114) / 1000;
            return brightness > 128 ? '#000000' : '#ffffff';
        }
    },

    /**
     * Array utilities
     */
    arrays: {
        /**
         * Group array by key
         */
        groupBy(array, key) {
            return array.reduce((groups, item) => {
                const group = (groups[item[key]] = groups[item[key]] || []);
                group.push(item);
                return groups;
            }, {});
        },

        /**
         * Sort array of objects by multiple keys
         */
        sortBy(array, ...keys) {
            return array.sort((a, b) => {
                for (let key of keys) {
                    if (a[key] < b[key]) return -1;
                    if (a[key] > b[key]) return 1;
                }
                return 0;
            });
        },

        /**
         * Remove duplicates from array
         */
        unique(array) {
            return [...new Set(array)];
        },

        /**
         * Chunk array into smaller arrays
         */
        chunk(array, size) {
            const chunks = [];
            for (let i = 0; i < array.length; i += size) {
                chunks.push(array.slice(i, i + size));
            }
            return chunks;
        }
    },

    /**
     * Object utilities
     */
    objects: {
        /**
         * Deep clone object
         */
        deepClone(obj) {
            if (obj === null || typeof obj !== 'object') return obj;
            if (obj instanceof Date) return new Date(obj.getTime());
            if (obj instanceof Array) return obj.map(item => this.deepClone(item));
            if (obj instanceof Object) {
                const cloned = {};
                for (const key in obj) {
                    if (obj.hasOwnProperty(key)) {
                        cloned[key] = this.deepClone(obj[key]);
                    }
                }
                return cloned;
            }
        },

        /**
         * Check if object is empty
         */
        isEmpty(obj) {
            return Object.keys(obj).length === 0;
        },

        /**
         * Get nested property value using dot notation
         */
        get(obj, path, defaultValue = undefined) {
            const keys = path.split('.');
            let result = obj;
            
            for (let key of keys) {
                if (result === null || result === undefined || !(key in result)) {
                    return defaultValue;
                }
                result = result[key];
            }
            
            return result;
        },

        /**
         * Set nested property value using dot notation
         */
        set(obj, path, value) {
            const keys = path.split('.');
            let current = obj;
            
            for (let i = 0; i < keys.length - 1; i++) {
                const key = keys[i];
                if (!(key in current) || typeof current[key] !== 'object') {
                    current[key] = {};
                }
                current = current[key];
            }
            
            current[keys[keys.length - 1]] = value;
        }
    },

    /**
     * Local storage utilities
     */
    storage: {
        /**
         * Set item in localStorage
         */
        set(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
                return true;
            } catch (e) {
                console.error('Failed to save to localStorage:', e);
                return false;
            }
        },

        /**
         * Get item from localStorage
         */
        get(key, defaultValue = null) {
            try {
                const item = localStorage.getItem(key);
                return item ? JSON.parse(item) : defaultValue;
            } catch (e) {
                console.error('Failed to read from localStorage:', e);
                return defaultValue;
            }
        },

        /**
         * Remove item from localStorage
         */
        remove(key) {
            try {
                localStorage.removeItem(key);
                return true;
            } catch (e) {
                console.error('Failed to remove from localStorage:', e);
                return false;
            }
        },

        /**
         * Clear all localStorage
         */
        clear() {
            try {
                localStorage.clear();
                return true;
            } catch (e) {
                console.error('Failed to clear localStorage:', e);
                return false;
            }
        }
    },

    /**
     * URL utilities
     */
    url: {
        /**
         * Get URL parameters as object
         */
        getParams() {
            const params = new URLSearchParams(window.location.search);
            const result = {};
            for (const [key, value] of params) {
                result[key] = value;
            }
            return result;
        },

        /**
         * Get specific URL parameter
         */
        getParam(name, defaultValue = null) {
            const params = new URLSearchParams(window.location.search);
            return params.get(name) || defaultValue;
        },

        /**
         * Build URL with parameters
         */
        buildUrl(base, params) {
            const url = new URL(base, window.location.origin);
            Object.entries(params).forEach(([key, value]) => {
                if (value !== null && value !== undefined) {
                    url.searchParams.set(key, value);
                }
            });
            return url.toString();
        }
    },

    /**
     * Form utilities
     */
    forms: {
        /**
         * Serialize form data
         */
        serializeForm(form) {
            const formData = new FormData(form);
            const data = {};
            
            for (const [key, value] of formData.entries()) {
                if (data[key]) {
                    // Handle multiple values (e.g., checkboxes)
                    if (Array.isArray(data[key])) {
                        data[key].push(value);
                    } else {
                        data[key] = [data[key], value];
                    }
                } else {
                    data[key] = value;
                }
            }
            
            return data;
        },

        /**
         * Validate form
         */
        validate(form, rules = {}) {
            const errors = {};
            const formData = this.serializeForm(form);
            
            Object.entries(rules).forEach(([field, fieldRules]) => {
                const value = formData[field];
                const fieldErrors = [];
                
                fieldRules.forEach(rule => {
                    const { type, message } = rule;
                    
                    switch (type) {
                        case 'required':
                            if (!value || value.toString().trim() === '') {
                                fieldErrors.push(message || `${field} is required`);
                            }
                            break;
                        case 'email':
                            if (value && !Utils.isValidEmail(value)) {
                                fieldErrors.push(message || `${field} must be a valid email`);
                            }
                            break;
                        case 'url':
                            if (value && !Utils.isValidUrl(value)) {
                                fieldErrors.push(message || `${field} must be a valid URL`);
                            }
                            break;
                        case 'min':
                            if (value && value.length < rule.value) {
                                fieldErrors.push(message || `${field} must be at least ${rule.value} characters`);
                            }
                            break;
                        case 'max':
                            if (value && value.length > rule.value) {
                                fieldErrors.push(message || `${field} must be no more than ${rule.value} characters`);
                            }
                            break;
                    }
                });
                
                if (fieldErrors.length > 0) {
                    errors[field] = fieldErrors;
                }
            });
            
            return {
                isValid: Object.keys(errors).length === 0,
                errors
            };
        },

        /**
         * Show form validation errors
         */
        showErrors(form, errors) {
            // Clear previous errors
            form.querySelectorAll('.error-message').forEach(el => el.remove());
            form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
            
            Object.entries(errors).forEach(([field, fieldErrors]) => {
                const input = form.querySelector(`[name="${field}"]`);
                if (input) {
                    input.classList.add('error');
                    
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'error-message';
                    errorDiv.textContent = fieldErrors[0];
                    input.parentNode.insertBefore(errorDiv, input.nextSibling);
                }
            });
        }
    },

    /**
     * Performance utilities
     */
    performance: {
        /**
         * Measure function execution time
         */
        measure(name, fn) {
            const start = performance.now();
            const result = fn();
            const end = performance.now();
            console.log(`${name} took ${(end - start).toFixed(2)} milliseconds`);
            return result;
        },

        /**
         * Wait for next frame
         */
        nextFrame() {
            return new Promise(resolve => requestAnimationFrame(resolve));
        },

        /**
         * Wait for specified milliseconds
         */
        delay(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
    },

    /**
     * DOM utilities
     */
    dom: {
        /**
         * Wait for element to exist
         */
        waitForElement(selector, timeout = 5000) {
            return new Promise((resolve, reject) => {
                const element = document.querySelector(selector);
                if (element) {
                    resolve(element);
                    return;
                }

                const observer = new MutationObserver(() => {
                    const element = document.querySelector(selector);
                    if (element) {
                        observer.disconnect();
                        resolve(element);
                    }
                });

                observer.observe(document.body, {
                    childList: true,
                    subtree: true
                });

                setTimeout(() => {
                    observer.disconnect();
                    reject(new Error(`Element ${selector} not found within ${timeout}ms`));
                }, timeout);
            });
        },

        /**
         * Smooth scroll to element
         */
        scrollToElement(element, offset = 0) {
            const elementPosition = element.getBoundingClientRect().top + window.pageYOffset;
            const offsetPosition = elementPosition - offset;
            
            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        },

        /**
         * Create element with attributes and content
         */
        createElement(tag, attributes = {}, content = '') {
            const element = document.createElement(tag);
            
            Object.entries(attributes).forEach(([key, value]) => {
                if (key === 'className') {
                    element.className = value;
                } else if (key === 'textContent') {
                    element.textContent = value;
                } else if (key === 'innerHTML') {
                    element.innerHTML = value;
                } else {
                    element.setAttribute(key, value);
                }
            });
            
            if (content) {
                element.innerHTML = content;
            }
            
            return element;
        }
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Utils;
}
// Export to global scope
window.Utils = Utils;
