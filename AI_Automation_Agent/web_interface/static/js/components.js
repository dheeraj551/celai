/**
 * AI Automation Agent - UI Components
 * Reusable UI components for the web interface
 */

/**
 * Toast Notification System
 */
class ToastManager {
    constructor(containerId = 'toastContainer') {
        this.container = document.getElementById(containerId);
        this.toasts = new Map();
        this.maxToasts = 5;
        this.autoHideDelay = 5000;
    }

    show(message, type = 'info', options = {}) {
        const id = Utils.generateId();
        const { duration = this.autoHideDelay, actions = [] } = options;
        
        const toast = this.createToastElement(id, message, type, actions);
        this.container.appendChild(toast);
        this.toasts.set(id, toast);
        
        // Auto-hide toast
        if (duration > 0) {
            setTimeout(() => this.hide(id), duration);
        }
        
        // Limit number of toasts
        if (this.toasts.size > this.maxToasts) {
            const firstId = this.toasts.keys().next().value;
            this.hide(firstId);
        }
        
        return id;
    }

    createToastElement(id, message, type, actions) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.setAttribute('data-toast-id', id);
        
        const icon = this.getIcon(type);
        
        toast.innerHTML = `
            <div class="toast-content">
                <div class="toast-icon">
                    <i class="fas fa-${icon}"></i>
                </div>
                <div class="toast-message">${message}</div>
                ${actions.length > 0 ? this.createActionsHTML(actions, id) : ''}
            </div>
            <button class="toast-close" onclick="toastManager.hide('${id}')">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        return toast;
    }

    createActionsHTML(actions, toastId) {
        const actionsHTML = actions.map(action => `
            <button class="toast-action" onclick="toastManager.handleAction('${action.id}', '${toastId}')">
                ${action.text}
            </button>
        `).join('');
        
        return `<div class="toast-actions">${actionsHTML}</div>`;
    }

    getIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    hide(id) {
        const toast = this.toasts.get(id);
        if (toast) {
            toast.style.animation = 'slideOut 0.3s ease-in-out';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
                this.toasts.delete(id);
            }, 300);
        }
    }

    hideAll() {
        this.toasts.forEach((_, id) => this.hide(id));
    }

    handleAction(actionId, toastId) {
        // Dispatch custom event for action handling
        window.dispatchEvent(new CustomEvent('toast-action', {
            detail: { actionId, toastId }
        }));
        
        this.hide(toastId);
    }

    success(message, options = {}) {
        return this.show(message, 'success', options);
    }

    error(message, options = {}) {
        return this.show(message, 'error', { ...options, duration: 0 }); // Errors don't auto-hide
    }

    warning(message, options = {}) {
        return this.show(message, 'warning', options);
    }

    info(message, options = {}) {
        return this.show(message, 'info', options);
    }
}

/**
 * Modal Component
 */
class Modal {
    constructor(options = {}) {
        this.options = {
            title: '',
            content: '',
            size: 'medium', // small, medium, large, fullscreen
            closable: true,
            backdrop: true,
            keyboard: true,
            onClose: null,
            ...options
        };
        
        this.element = null;
        this.isOpen = false;
    }

    static create(options = {}) {
        const modal = new Modal(options);
        return modal;
    }

    open() {
        if (this.isOpen) return this;
        
        this.createElement();
        this.bindEvents();
        this.show();
        
        return this;
    }

    close() {
        if (!this.isOpen) return this;
        
        this.hide();
        this.unbindEvents();
        this.removeElement();
        
        if (typeof this.options.onClose === 'function') {
            this.options.onClose();
        }
        
        return this;
    }

    createElement() {
        this.element = document.createElement('div');
        this.element.className = `modal modal-${this.options.size}`;
        
        this.element.innerHTML = `
            <div class="modal-backdrop" ${this.options.backdrop ? '' : 'style="display: none;"'}></div>
            <div class="modal-content">
                ${this.options.title ? this.createHeader() : ''}
                <div class="modal-body">
                    ${this.options.content}
                </div>
                ${this.options.footer ? this.createFooter() : ''}
            </div>
        `;
    }

    createHeader() {
        return `
            <div class="modal-header">
                <h3 class="modal-title">${this.options.title}</h3>
                ${this.options.closable ? '<button class="modal-close">&times;</button>' : ''}
            </div>
        `;
    }

    createFooter() {
        return `<div class="modal-footer">${this.options.footer}</div>`;
    }

    bindEvents() {
        if (this.options.closable) {
            this.element.querySelector('.modal-close').addEventListener('click', () => this.close());
        }
        
        if (this.options.backdrop) {
            this.element.querySelector('.modal-backdrop').addEventListener('click', () => this.close());
        }
        
        if (this.options.keyboard) {
            document.addEventListener('keydown', this.handleKeydown.bind(this));
        }
    }

    unbindEvents() {
        if (this.options.keyboard) {
            document.removeEventListener('keydown', this.handleKeydown.bind(this));
        }
    }

    handleKeydown(event) {
        if (event.key === 'Escape' && this.options.closable) {
            this.close();
        }
    }

    show() {
        document.body.appendChild(this.element);
        
        // Trigger animation
        setTimeout(() => {
            this.element.classList.add('show');
        }, 10);
        
        this.isOpen = true;
    }

    hide() {
        if (this.element) {
            this.element.classList.remove('show');
        }
    }

    removeElement() {
        if (this.element && this.element.parentNode) {
            this.element.parentNode.removeChild(this.element);
        }
        this.element = null;
        this.isOpen = false;
    }

    setContent(content) {
        if (this.element) {
            const body = this.element.querySelector('.modal-body');
            body.innerHTML = content;
        }
        return this;
    }

    setTitle(title) {
        if (this.element) {
            const titleElement = this.element.querySelector('.modal-title');
            if (titleElement) {
                titleElement.textContent = title;
            }
        }
        return this;
    }

    static alert(message, options = {}) {
        const modal = new Modal({
            title: options.title || 'Alert',
            content: `<p>${message}</p>`,
            footer: '<button class="btn btn-primary modal-ok">OK</button>',
            ...options
        });
        
        modal.open();
        
        modal.element.querySelector('.modal-ok').addEventListener('click', () => modal.close());
        
        return modal;
    }

    static confirm(message, options = {}) {
        return new Promise((resolve) => {
            const modal = new Modal({
                title: options.title || 'Confirm',
                content: `<p>${message}</p>`,
                footer: `
                    <button class="btn btn-secondary modal-cancel">Cancel</button>
                    <button class="btn btn-primary modal-confirm">Confirm</button>
                `,
                ...options
            });
            
            modal.open();
            
            modal.element.querySelector('.modal-cancel').addEventListener('click', () => {
                modal.close();
                resolve(false);
            });
            
            modal.element.querySelector('.modal-confirm').addEventListener('click', () => {
                modal.close();
                resolve(true);
            });
        });
    }

    static prompt(message, options = {}) {
        return new Promise((resolve) => {
            const { defaultValue = '', inputType = 'text' } = options;
            
            const modal = new Modal({
                title: options.title || 'Input Required',
                content: `
                    <p>${message}</p>
                    <input type="${inputType}" class="modal-input" value="${defaultValue}" autofocus>
                `,
                footer: `
                    <button class="btn btn-secondary modal-cancel">Cancel</button>
                    <button class="btn btn-primary modal-submit">Submit</button>
                `,
                ...options
            });
            
            modal.open();
            
            const input = modal.element.querySelector('.modal-input');
            
            modal.element.querySelector('.modal-cancel').addEventListener('click', () => {
                modal.close();
                resolve(null);
            });
            
            const submit = () => {
                modal.close();
                resolve(input.value);
            };
            
            modal.element.querySelector('.modal-submit').addEventListener('click', submit);
            
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    submit();
                }
            });
            
            input.focus();
        });
    }
}

/**
 * Loading Component
 */
class LoadingManager {
    constructor() {
        this.overlay = null;
        this.count = 0;
    }

    show(message = 'Loading...', options = {}) {
        const { overlayId = 'loadingOverlay', persistent = false } = options;
        
        this.overlay = document.getElementById(overlayId);
        if (!this.overlay) {
            this.overlay = document.createElement('div');
            this.overlay.id = overlayId;
            this.overlay.className = 'loading-overlay';
            
            this.overlay.innerHTML = `
                <div class="loading-content">
                    <div class="loading-spinner">
                        <div class="spinner"></div>
                        <p class="loading-message">${message}</p>
                    </div>
                </div>
            `;
            
            document.body.appendChild(this.overlay);
        }
        
        const messageElement = this.overlay.querySelector('.loading-message');
        if (messageElement) {
            messageElement.textContent = message;
        }
        
        this.overlay.style.display = 'flex';
        this.count++;
        
        if (!persistent) {
            // Auto-hide after timeout
            setTimeout(() => this.hide(), 10000);
        }
        
        return this.count;
    }

    hide() {
        if (this.count > 0) {
            this.count--;
        }
        
        if (this.count === 0 && this.overlay) {
            this.overlay.style.display = 'none';
        }
    }

    hideAll() {
        this.count = 0;
        if (this.overlay) {
            this.overlay.style.display = 'none';
        }
    }
}

/**
 * Form Component
 */
class Form {
    constructor(formElement, options = {}) {
        this.form = formElement;
        this.options = {
            validateOnInput: false,
            validateOnBlur: true,
            showErrors: true,
            ...options
        };
        
        this.errors = {};
        this.validators = {};
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupValidators();
    }

    bindEvents() {
        if (this.options.validateOnInput) {
            this.form.addEventListener('input', () => this.validate());
        }
        
        if (this.options.validateOnBlur) {
            this.form.addEventListener('blur', (e) => {
                if (e.target.matches('input, select, textarea')) {
                    this.validateField(e.target.name);
                }
            }, true);
        }
        
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (this.validate()) {
                this.onSubmit();
            }
        });
    }

    setupValidators() {
        // Add built-in validators based on input attributes
        const inputs = this.form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            const fieldName = input.name || input.id;
            const validators = [];
            
            if (input.required) {
                validators.push({ type: 'required', message: `${this.getFieldLabel(input)} is required` });
            }
            
            if (input.type === 'email') {
                validators.push({ type: 'email', message: `${this.getFieldLabel(input)} must be a valid email` });
            }
            
            if (input.minLength) {
                validators.push({ type: 'minLength', value: input.minLength, message: `${this.getFieldLabel(input)} must be at least ${input.minLength} characters` });
            }
            
            if (input.maxLength) {
                validators.push({ type: 'maxLength', value: input.maxLength, message: `${this.getFieldLabel(input)} must be no more than ${input.maxLength} characters` });
            }
            
            if (input.pattern) {
                validators.push({ type: 'pattern', value: input.pattern, message: `${this.getFieldLabel(input)} format is invalid` });
            }
            
            if (validators.length > 0) {
                this.validators[fieldName] = validators;
            }
        });
    }

    getFieldLabel(input) {
        const label = this.form.querySelector(`label[for="${input.id}"]`);
        return label ? label.textContent : input.name || input.id || 'Field';
    }

    validate() {
        this.errors = {};
        let isValid = true;
        
        Object.entries(this.validators).forEach(([fieldName, validators]) => {
            const fieldErrors = this.validateField(fieldName);
            if (fieldErrors.length > 0) {
                this.errors[fieldName] = fieldErrors;
                isValid = false;
            }
        });
        
        this.showErrors();
        return isValid;
    }

    validateField(fieldName) {
        const input = this.form.querySelector(`[name="${fieldName}"]`);
        if (!input) return [];
        
        const value = input.value;
        const validators = this.validators[fieldName] || [];
        const errors = [];
        
        validators.forEach(validator => {
            switch (validator.type) {
                case 'required':
                    if (!value || value.trim() === '') {
                        errors.push(validator.message);
                    }
                    break;
                case 'email':
                    if (value && !Utils.isValidEmail(value)) {
                        errors.push(validator.message);
                    }
                    break;
                case 'minLength':
                    if (value && value.length < validator.value) {
                        errors.push(validator.message);
                    }
                    break;
                case 'maxLength':
                    if (value && value.length > validator.value) {
                        errors.push(validator.message);
                    }
                    break;
                case 'pattern':
                    if (value && !new RegExp(validator.value).test(value)) {
                        errors.push(validator.message);
                    }
                    break;
            }
        });
        
        return errors;
    }

    showErrors() {
        if (!this.options.showErrors) return;
        
        // Clear previous errors
        this.form.querySelectorAll('.error-message').forEach(el => el.remove());
        this.form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
        
        // Show new errors
        Object.entries(this.errors).forEach(([fieldName, fieldErrors]) => {
            const input = this.form.querySelector(`[name="${fieldName}"]`);
            if (input) {
                input.classList.add('error');
                
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error-message';
                errorDiv.textContent = fieldErrors[0];
                
                input.parentNode.insertBefore(errorDiv, input.nextSibling);
            }
        });
    }

    getData() {
        return Utils.forms.serializeForm(this.form);
    }

    setData(data) {
        Object.entries(data).forEach(([field, value]) => {
            const input = this.form.querySelector(`[name="${field}"]`);
            if (input) {
                if (input.type === 'checkbox' || input.type === 'radio') {
                    input.checked = Boolean(value);
                } else {
                    input.value = value;
                }
            }
        });
    }

    reset() {
        this.form.reset();
        this.errors = {};
        this.showErrors();
    }

    onSubmit() {
        // Override in subclass or pass callback
        const data = this.getData();
        console.log('Form submitted:', data);
    }

    addValidator(fieldName, validator) {
        if (!this.validators[fieldName]) {
            this.validators[fieldName] = [];
        }
        this.validators[fieldName].push(validator);
    }

    removeValidator(fieldName, validatorType) {
        if (this.validators[fieldName]) {
            this.validators[fieldName] = this.validators[fieldName].filter(
                v => v.type !== validatorType
            );
        }
    }
}

/**
 * Chart Component
 */
class ChartManager {
    constructor() {
        this.charts = new Map();
    }

    create(container, config) {
        const canvas = container.querySelector('canvas');
        if (!canvas) {
            throw new Error('Canvas element not found');
        }
        
        const ctx = canvas.getContext('2d');
        const chart = new Chart(ctx, config);
        
        this.charts.set(container, chart);
        return chart;
    }

    destroy(container) {
        const chart = this.charts.get(container);
        if (chart) {
            chart.destroy();
            this.charts.delete(container);
        }
    }

    update(container, data) {
        const chart = this.charts.get(container);
        if (chart) {
            chart.data = data;
            chart.update();
        }
    }

    resize(container) {
        const chart = this.charts.get(container);
        if (chart) {
            chart.resize();
        }
    }
}

/**
 * Table Component
 */
class Table {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            sortable: true,
            filterable: true,
            paginated: false,
            pageSize: 10,
            ...options
        };
        
        this.data = [];
        this.filteredData = [];
        this.currentPage = 1;
        this.sortColumn = null;
        this.sortDirection = 'asc';
        
        this.init();
    }

    init() {
        this.render();
        if (this.options.filterable) {
            this.setupFiltering();
        }
        if (this.options.sortable) {
            this.setupSorting();
        }
        if (this.options.paginated) {
            this.setupPagination();
        }
    }

    setData(data) {
        this.data = data;
        this.filteredData = [...data];
        this.render();
    }

    render() {
        this.container.innerHTML = this.generateTableHTML();
        this.bindEvents();
    }

    generateTableHTML() {
        if (this.data.length === 0) {
            return '<div class="no-data">No data available</div>';
        }
        
        const columns = Object.keys(this.data[0]);
        const displayData = this.options.paginated ? this.getPageData() : this.filteredData;
        
        return `
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            ${columns.map(col => `
                                <th ${this.options.sortable ? `data-column="${col}" class="sortable"` : ''}>
                                    ${this.formatColumnName(col)}
                                    ${this.options.sortable ? '<i class="sort-icon fas fa-sort"></i>' : ''}
                                </th>
                            `).join('')}
                        </tr>
                    </thead>
                    <tbody>
                        ${displayData.map(row => `
                            <tr>
                                ${columns.map(col => `
                                    <td>${this.formatCellValue(row[col], col)}</td>
                                `).join('')}
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            ${this.options.paginated ? this.generatePaginationHTML() : ''}
        `;
    }

    formatColumnName(column) {
        return column.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    formatCellValue(value, column) {
        if (value === null || value === undefined) return '-';
        
        if (column.toLowerCase().includes('date')) {
            return Utils.formatDate(value);
        }
        
        if (typeof value === 'boolean') {
            return value ? '<i class="fas fa-check text-success"></i>' : '<i class="fas fa-times text-error"></i>';
        }
        
        if (Array.isArray(value)) {
            return value.join(', ');
        }
        
        return Utils.sanitizeHTML(String(value));
    }

    setupFiltering() {
        const filterInput = document.createElement('input');
        filterInput.type = 'text';
        filterInput.placeholder = 'Filter...';
        filterInput.className = 'table-filter';
        
        filterInput.addEventListener('input', Utils.debounce((e) => {
            this.filter(e.target.value);
        }, 300));
        
        this.container.parentNode.insertBefore(filterInput, this.container);
    }

    filter(query) {
        if (!query) {
            this.filteredData = [...this.data];
        } else {
            const searchTerm = query.toLowerCase();
            this.filteredData = this.data.filter(row => 
                Object.values(row).some(value => 
                    String(value).toLowerCase().includes(searchTerm)
                )
            );
        }
        
        this.currentPage = 1;
        this.render();
    }

    setupSorting() {
        this.container.addEventListener('click', (e) => {
            const th = e.target.closest('th.sortable');
            if (th) {
                const column = th.dataset.column;
                this.sort(column);
            }
        });
    }

    sort(column) {
        if (this.sortColumn === column) {
            this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            this.sortColumn = column;
            this.sortDirection = 'asc';
        }
        
        this.filteredData.sort((a, b) => {
            const aVal = a[column];
            const bVal = b[column];
            
            if (aVal < bVal) return this.sortDirection === 'asc' ? -1 : 1;
            if (aVal > bVal) return this.sortDirection === 'asc' ? 1 : -1;
            return 0;
        });
        
        this.render();
    }

    setupPagination() {
        this.container.addEventListener('click', (e) => {
            const button = e.target.closest('.page-btn');
            if (button) {
                const page = parseInt(button.dataset.page);
                if (page) {
                    this.goToPage(page);
                }
            }
        });
    }

    getPageData() {
        const start = (this.currentPage - 1) * this.options.pageSize;
        const end = start + this.options.pageSize;
        return this.filteredData.slice(start, end);
    }

    generatePaginationHTML() {
        const totalPages = Math.ceil(this.filteredData.length / this.options.pageSize);
        if (totalPages <= 1) return '';
        
        let paginationHTML = '<div class="pagination">';
        
        // Previous button
        paginationHTML += `
            <button class="page-btn" data-page="${this.currentPage - 1}" ${this.currentPage === 1 ? 'disabled' : ''}>
                <i class="fas fa-chevron-left"></i>
            </button>
        `;
        
        // Page numbers
        for (let i = 1; i <= totalPages; i++) {
            if (i === 1 || i === totalPages || (i >= this.currentPage - 1 && i <= this.currentPage + 1)) {
                paginationHTML += `
                    <button class="page-btn ${i === this.currentPage ? 'active' : ''}" data-page="${i}">
                        ${i}
                    </button>
                `;
            } else if (i === this.currentPage - 2 || i === this.currentPage + 2) {
                paginationHTML += '<span class="page-ellipsis">...</span>';
            }
        }
        
        // Next button
        paginationHTML += `
            <button class="page-btn" data-page="${this.currentPage + 1}" ${this.currentPage === totalPages ? 'disabled' : ''}>
                <i class="fas fa-chevron-right"></i>
            </button>
        `;
        
        paginationHTML += '</div>';
        return paginationHTML;
    }

    goToPage(page) {
        const totalPages = Math.ceil(this.filteredData.length / this.options.pageSize);
        this.currentPage = Math.max(1, Math.min(page, totalPages));
        this.render();
    }

    bindEvents() {
        // Override in subclass or add custom event binding
    }
}

// Global instances
window.toastManager = new ToastManager();
window.loadingManager = new LoadingManager();
window.chartManager = new ChartManager();

// CSS for new components
const componentStyles = `
/* Toast Styles */
.toast {
    position: relative;
    padding: var(--spacing-md) var(--spacing-lg);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-lg);
    margin-bottom: var(--spacing-sm);
    max-width: 400px;
    animation: slideInRight 0.3s ease-out;
}

.toast-content {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
}

.toast-icon {
    flex-shrink: 0;
    width: 20px;
    text-align: center;
}

.toast-message {
    flex: 1;
    font-size: var(--font-size-sm);
}

.toast-actions {
    margin-top: var(--spacing-sm);
    display: flex;
    gap: var(--spacing-sm);
    justify-content: flex-end;
}

.toast-action {
    padding: var(--spacing-xs) var(--spacing-sm);
    border: 1px solid rgba(255, 255, 255, 0.3);
    background: transparent;
    color: white;
    border-radius: var(--radius-sm);
    font-size: var(--font-size-xs);
    cursor: pointer;
    transition: all var(--transition-fast);
}

.toast-action:hover {
    background: rgba(255, 255, 255, 0.1);
}

.toast-close {
    position: absolute;
    top: var(--spacing-xs);
    right: var(--spacing-xs);
    background: none;
    border: none;
    color: inherit;
    cursor: pointer;
    padding: var(--spacing-xs);
    border-radius: var(--radius-sm);
    opacity: 0.7;
    transition: opacity var(--transition-fast);
}

.toast-close:hover {
    opacity: 1;
}

/* Loading Overlay */
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(15, 23, 42, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9998;
    backdrop-filter: blur(4px);
}

.loading-content {
    text-align: center;
    color: white;
}

.loading-message {
    margin-top: var(--spacing-md);
    font-size: var(--font-size-lg);
}

/* Modal Enhancements */
.modal-small .modal-content {
    max-width: 400px;
}

.modal-large .modal-content {
    max-width: 800px;
}

.modal-fullscreen {
    padding: var(--spacing-lg);
}

.modal-fullscreen .modal-content {
    max-width: none;
    width: calc(100vw - 2rem);
    height: calc(100vh - 2rem);
    max-height: none;
}

.modal-input {
    width: 100%;
    padding: var(--spacing-sm) var(--spacing-md);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    font-size: var(--font-size-sm);
    margin-top: var(--spacing-sm);
}

.modal-input:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Form Enhancements */
.error {
    border-color: var(--error-color) !important;
    box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1) !important;
}

.error-message {
    color: var(--error-color);
    font-size: var(--font-size-xs);
    margin-top: var(--spacing-xs);
}

/* Table Enhancements */
.table-filter {
    width: 100%;
    max-width: 300px;
    padding: var(--spacing-sm) var(--spacing-md);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    margin-bottom: var(--spacing-md);
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    background-color: var(--bg-card);
}

.data-table th,
.data-table td {
    padding: var(--spacing-md);
    text-align: left;
    border-bottom: 1px solid var(--border-color);
}

.data-table th {
    background-color: var(--bg-tertiary);
    font-weight: 600;
    color: var(--text-primary);
    position: sticky;
    top: 0;
}

.data-table th.sortable {
    cursor: pointer;
    user-select: none;
}

.data-table th.sortable:hover {
    background-color: var(--bg-hover);
}

.sort-icon {
    margin-left: var(--spacing-xs);
    opacity: 0.5;
}

.data-table th.active .sort-icon {
    opacity: 1;
}

.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: var(--spacing-sm);
    margin-top: var(--spacing-lg);
}

.page-btn {
    padding: var(--spacing-sm) var(--spacing-md);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    background-color: var(--bg-card);
    color: var(--text-primary);
    cursor: pointer;
    transition: all var(--transition-fast);
}

.page-btn:hover:not(:disabled) {
    background-color: var(--bg-tertiary);
}

.page-btn.active {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
    color: white;
}

.page-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.page-ellipsis {
    padding: var(--spacing-sm) var(--spacing-md);
    color: var(--text-muted);
}

.no-data {
    text-align: center;
    padding: var(--spacing-xl);
    color: var(--text-muted);
    font-style: italic;
}

/* Animations */
@keyframes slideInRight {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes slideOut {
    from {
        transform: translateX(0);
        opacity: 1;
    }
    to {
        transform: translateX(100%);
        opacity: 0;
    }
}
`;

// Inject component styles
const styleSheet = document.createElement('style');
styleSheet.textContent = componentStyles;
document.head.appendChild(styleSheet);
// Export to global scope
window.ToastManager = ToastManager;
