/**
 * AI Automation Agent - API Client
 * Handles all HTTP requests to the backend API
 */

class APIClient {
    constructor(baseURL = '', defaultHeaders = {}) {
        this.baseURL = baseURL;
        this.defaultHeaders = {
            'Content-Type': 'application/json',
            ...defaultHeaders
        };
        
        this.requestInterceptors = [];
        this.responseInterceptors = [];
    }

    /**
     * Add request interceptor
     */
    addRequestInterceptor(interceptor) {
        this.requestInterceptors.push(interceptor);
    }

    /**
     * Add response interceptor
     */
    addResponseInterceptor(interceptor) {
        this.responseInterceptors.push(interceptor);
    }

    /**
     * Build URL with base URL
     */
    buildURL(endpoint) {
        if (endpoint.startsWith('http')) {
            return endpoint;
        }
        return `${this.baseURL}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;
    }

    /**
     * Build request options
     */
    buildRequestOptions(options = {}) {
        const requestOptions = {
            ...options,
            headers: {
                ...this.defaultHeaders,
                ...options.headers
            }
        };

        // Apply request interceptors
        return this.requestInterceptors.reduce((options, interceptor) => {
            return interceptor(options) || options;
        }, requestOptions);
    }

    /**
     * Handle response
     */
    async handleResponse(response) {
        const responseData = await response.json().catch(() => ({}));
        
        // Apply response interceptors
        const processedResponse = this.responseInterceptors.reduce((data, interceptor) => {
            return interceptor(data, response) || data;
        }, responseData);

        if (!response.ok) {
            throw new APIError(
                processedResponse.message || `HTTP ${response.status}`,
                response.status,
                processedResponse
            );
        }

        return processedResponse;
    }

    /**
     * Make HTTP request
     */
    async request(endpoint, options = {}) {
        const url = this.buildURL(endpoint);
        const requestOptions = this.buildRequestOptions(options);

        try {
            const response = await fetch(url, requestOptions);
            return await this.handleResponse(response);
        } catch (error) {
            if (error instanceof APIError) {
                throw error;
            }
            
            // Network or other errors
            throw new APIError(
                error.message || 'Network error',
                0,
                { originalError: error }
            );
        }
    }

    /**
     * GET request
     */
    async get(endpoint, params = {}) {
        const url = new URL(this.buildURL(endpoint));
        
        Object.entries(params).forEach(([key, value]) => {
            if (value !== null && value !== undefined) {
                url.searchParams.set(key, value);
            }
        });

        return this.request(url.pathname + url.search, {
            method: 'GET'
        });
    }

    /**
     * POST request
     */
    async post(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    /**
     * PUT request
     */
    async put(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    /**
     * DELETE request
     */
    async delete(endpoint) {
        return this.request(endpoint, {
            method: 'DELETE'
        });
    }

    /**
     * PATCH request
     */
    async patch(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'PATCH',
            body: JSON.stringify(data)
        });
    }
}

/**
 * API Error class
 */
class APIError extends Error {
    constructor(message, status = 0, data = {}) {
        super(message);
        this.name = 'APIError';
        this.status = status;
        this.data = data;
    }
}

/**
 * Authentication interceptor
 */
class AuthInterceptor {
    constructor(getToken) {
        this.getToken = getToken;
    }

    intercept(requestOptions) {
        const token = this.getToken();
        if (token) {
            requestOptions.headers['Authorization'] = `Bearer ${token}`;
        }
        return requestOptions;
    }
}

/**
 * Retry interceptor
 */
class RetryInterceptor {
    constructor(maxRetries = 3, retryDelay = 1000) {
        this.maxRetries = maxRetries;
        this.retryDelay = retryDelay;
    }

    intercept(requestOptions, originalFetch) {
        return async (...args) => {
            let lastError;
            
            for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
                try {
                    return await originalFetch(...args);
                } catch (error) {
                    lastError = error;
                    
                    // Don't retry on client errors (4xx) except 408, 429
                    if (error instanceof APIError && 
                        error.status >= 400 && error.status < 500 && 
                        error.status !== 408 && error.status !== 429) {
                        break;
                    }
                    
                    // Don't retry on last attempt
                    if (attempt === this.maxRetries) {
                        break;
                    }
                    
                    // Wait before retry
                    await this.delay(Math.pow(2, attempt) * this.retryDelay);
                }
            }
            
            throw lastError;
        };
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

/**
 * Cache interceptor
 */
class CacheInterceptor {
    constructor() {
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    }

    intercept(requestOptions) {
        if (requestOptions.method !== 'GET') {
            return requestOptions;
        }

        const cacheKey = JSON.stringify({
            url: requestOptions.url,
            headers: requestOptions.headers
        });

        const cached = this.cache.get(cacheKey);
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            // Return cached response
            return Promise.resolve(cached.response);
        }

        return requestOptions;
    }

    set(key, response) {
        this.cache.set(key, {
            response,
            timestamp: Date.now()
        });
    }
}

/**
 * Create API client with default configuration
 */
const API = new APIClient(window.location.origin, {
    'Content-Type': 'application/json'
});

/**
 * Add global interceptors
 */

// Authentication interceptor (if token exists)
const authInterceptor = new AuthInterceptor(() => {
    return localStorage.getItem('auth_token');
});
API.addRequestInterceptor((options) => authInterceptor.intercept(options));

// Error handling interceptor
API.addResponseInterceptor((data, response) => {
    // Log errors for debugging
    if (response.status >= 400) {
        console.error('API Error:', data);
    }
    return data;
});

// Request/response logging interceptor (development only)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    API.addRequestInterceptor((options) => {
        console.log('API Request:', {
            method: options.method || 'GET',
            url: options.url,
            headers: options.headers,
            body: options.body
        });
        return options;
    });

    API.addResponseInterceptor((data, response) => {
        console.log('API Response:', {
            status: response.status,
            statusText: response.statusText,
            data
        });
        return data;
    });
}

/**
 * API endpoints for different modules
 */
const APIEndpoints = {
    // Agent endpoints
    agent: {
        status: '/api/status',
        start: '/api/agent/start',
        stop: '/api/agent/stop',
        restart: '/api/agent/restart'
    },

    // Blog automation endpoints
    blog: {
        posts: '/api/blog/posts',
        generate: '/api/blog/generate',
        series: '/api/blog/series',
        publish: '/api/blog/publish',
        delete: '/api/blog/delete',
        update: '/api/blog/update'
    },

    // Analytics endpoints
    analytics: {
        summary: '/api/analytics/summary',
        trending: '/api/analytics/trending',
        performance: '/api/analytics/performance',
        seo: '/api/analytics/seo',
        engagement: '/api/analytics/engagement'
    },

    // Settings endpoints
    settings: {
        get: '/api/settings',
        update: '/api/settings',
        reset: '/api/settings/reset',
        test: '/api/settings/test'
    },

    // System endpoints
    system: {
        health: '/api/system/health',
        logs: '/api/system/logs',
        metrics: '/api/system/metrics',
        restart: '/api/system/restart'
    }
};

/**
 * Specialized API methods for common operations
 */
const APIMethods = {
    /**
     * Agent management
     */
    async getAgentStatus() {
        return API.get(APIEndpoints.agent.status);
    },

    async startAgent() {
        return API.post(APIEndpoints.agent.start);
    },

    async stopAgent() {
        return API.post(APIEndpoints.agent.stop);
    },

    /**
     * Blog automation
     */
    async getBlogPosts(limit = 50, offset = 0) {
        return API.get(APIEndpoints.blog.posts, { limit, offset });
    },

    async generateBlog(data) {
        return API.post(APIEndpoints.blog.generate, data);
    },

    async generateBlogSeries(data) {
        return API.post(APIEndpoints.blog.series, data);
    },

    async publishBlog(postId) {
        return API.post(`${APIEndpoints.blog.publish}/${postId}`);
    },

    async deleteBlog(postId) {
        return API.delete(`${APIEndpoints.blog.delete}/${postId}`);
    },

    async updateBlog(postId, data) {
        return API.put(`${APIEndpoints.blog.update}/${postId}`, data);
    },

    /**
     * Analytics
     */
    async getAnalyticsSummary(days = 30) {
        return API.get(APIEndpoints.analytics.summary, { days });
    },

    async getTrendingTopics(days = 30) {
        return API.get(APIEndpoints.analytics.trending, { days });
    },

    async getPerformanceMetrics(days = 30) {
        return API.get(APIEndpoints.analytics.performance, { days });
    },

    async getSEOMetrics(days = 30) {
        return API.get(APIEndpoints.analytics.seo, { days });
    },

    async getEngagementMetrics(days = 30) {
        return API.get(APIEndpoints.analytics.engagement, { days });
    },

    /**
     * Settings
     */
    async getSettings() {
        return API.get(APIEndpoints.settings.get);
    },

    async updateSettings(settings) {
        return API.put(APIEndpoints.settings.update, settings);
    },

    async resetSettings() {
        return API.post(APIEndpoints.settings.reset);
    },

    async testSettings(type, config) {
        return API.post(APIEndpoints.settings.test, { type, config });
    },

    /**
     * System
     */
    async getSystemHealth() {
        return API.get(APIEndpoints.system.health);
    },

    async getSystemLogs(limit = 100, level = 'INFO') {
        return API.get(APIEndpoints.system.logs, { limit, level });
    },

    async getSystemMetrics() {
        return API.get(APIEndpoints.system.metrics);
    },

    async restartSystem() {
        return API.post(APIEndpoints.system.restart);
    }
};

/**
 * Extend API with specialized methods
 */
Object.assign(API, APIMethods);

/**
 * WebSocket connection manager for real-time updates
 * Note: This has been moved to websocket.js to avoid duplication
 * The WebSocketManager class is now defined in websocket.js only
 */

/**
 * Create global instances
 */
window.API = API;
window.APIError = APIError;

// WebSocketManager is now defined in websocket.js only
// Auto-connect WebSocket is handled in websocket.js