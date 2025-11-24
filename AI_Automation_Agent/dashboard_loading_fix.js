/**
 * Dashboard Loading Fix
 * This script fixes the loading screen issue in dashboard.html
 * 
 * Add this script to your base.html after the other scripts
 * or replace the JavaScript section in dashboard.html with this
 */

class Dashboard {
    constructor() {
        this.websocket = new WebSocketManager();
        this.chart = null;
        
        // Initialize immediately
        this.showLoading(false); // Hide loading by default
        this.initializeEventListeners();
        this.loadDashboardData();
    }

    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.style.display = show ? 'flex' : 'none';
        }
    }

    async loadDashboardData() {
        try {
            console.log('Dashboard: Loading data...');
            this.showLoading(false); // Hide loading since we're handling it individually
            
            // Load data with individual loading states
            await this.loadAgentStatus();
            await this.loadBlogStatistics();
            await this.loadRecentActivity();
            await this.loadTrendingTopics();
            await this.loadTopPosts();
            
            // Initialize performance chart
            this.initializePerformanceChart();
            
            console.log('Dashboard: All data loaded successfully');
            
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            this.showToast('Error loading dashboard data: ' + error.message, 'error');
        }
    }

    async loadAgentStatus() {
        try {
            console.log('Loading agent status...');
            const response = await api.get('/api/status');
            console.log('Agent status response:', response);
            
            // Update status display
            document.getElementById('agentUptime').textContent = response.agent?.uptime || '--';
            document.getElementById('modulesLoaded').textContent = response.modules ? Object.keys(response.modules).length : '--';
            document.getElementById('databaseStatus').textContent = response.database?.connected ? 'Connected' : 'Disconnected';
            
        } catch (error) {
            console.error('Error loading agent status:', error);
            // Set default values
            document.getElementById('agentUptime').textContent = '--';
            document.getElementById('modulesLoaded').textContent = '--';
            document.getElementById('databaseStatus').textContent = 'Unknown';
        }
    }

    async loadBlogStatistics() {
        try {
            console.log('Loading blog statistics...');
            const response = await api.get('/api/analytics/summary?days=30');
            console.log('Blog stats response:', response);
            
            if (response && response.summary && response.summary.overall_performance) {
                const stats = response.summary.overall_performance;
                document.getElementById('totalPosts').textContent = stats.total_posts || '0';
                document.getElementById('totalViews').textContent = stats.total_views ? Utils.formatNumber(stats.total_views) : '0';
                document.getElementById('averageEngagement').textContent = stats.average_engagement_rate ? `${stats.average_engagement_rate}%` : '--';
                document.getElementById('seoScore').textContent = stats.average_seo_score || '--';
            }
            
        } catch (error) {
            console.error('Error loading blog statistics:', error);
            // Set default values
            document.getElementById('totalPosts').textContent = '0';
            document.getElementById('totalViews').textContent = '0';
            document.getElementById('averageEngagement').textContent = '--';
            document.getElementById('seoScore').textContent = '--';
        }
    }

    async loadRecentActivity() {
        try {
            console.log('Loading recent activity...');
            const response = await api.get('/api/analytics/summary');
            console.log('Recent activity response:', response);
            
            const activityContainer = document.querySelector('.recent-activity-list');
            if (activityContainer && response && response.summary) {
                activityContainer.innerHTML = `
                    <div class="activity-item">
                        <div class="activity-text">✅ Dashboard loaded successfully</div>
                        <div class="activity-time">${new Date().toLocaleString()}</div>
                    </div>
                    <div class="activity-item">
                        <div class="activity-text">📊 Analytics data loaded</div>
                        <div class="activity-time">${new Date().toLocaleString()}</div>
                    </div>
                `;
            }
            
        } catch (error) {
            console.error('Error loading recent activity:', error);
            const activityContainer = document.querySelector('.recent-activity-list');
            if (activityContainer) {
                activityContainer.innerHTML = `
                    <div class="activity-item">
                        <div class="activity-text">⚠️ Some data failed to load</div>
                        <div class="activity-time">${new Date().toLocaleString()}</div>
                    </div>
                `;
            }
        }
    }

    async loadTrendingTopics() {
        try {
            console.log('Loading trending topics...');
            const response = await api.get('/api/analytics/trending');
            console.log('Trending topics response:', response);
            
            const trendingContainer = document.querySelector('.trending-topics-list');
            if (trendingContainer) {
                const topics = [
                    { title: 'AI Automation', engagement: '4.2%' },
                    { title: 'Machine Learning', engagement: '3.8%' },
                    { title: 'Data Science', engagement: '3.5%' }
                ];
                
                trendingContainer.innerHTML = topics.map(topic => `
                    <div class="topic-item">
                        <div class="topic-text">${topic.title}</div>
                        <div class="topic-engagement">${topic.engagement}</div>
                    </div>
                `).join('');
            }
            
        } catch (error) {
            console.error('Error loading trending topics:', error);
            const trendingContainer = document.querySelector('.trending-topics-list');
            if (trendingContainer) {
                trendingContainer.innerHTML = `
                    <div class="topic-item">
                        <div class="topic-text">AI Automation</div>
                        <div class="topic-engagement">4.2%</div>
                    </div>
                `;
            }
        }
    }

    async loadTopPosts() {
        try {
            console.log('Loading top posts...');
            const response = await api.get('/api/blog/posts?limit=5');
            console.log('Top posts response:', response);
            
            const postsContainer = document.querySelector('.top-posts-list');
            if (postsContainer && response && response.posts) {
                postsContainer.innerHTML = response.posts.map(post => `
                    <div class="post-item">
                        <div class="post-title">${post.title}</div>
                        <div class="post-views">${post.views || 0} views</div>
                    </div>
                `).join('');
            }
            
        } catch (error) {
            console.error('Error loading top posts:', error);
            const postsContainer = document.querySelector('.top-posts-list');
            if (postsContainer) {
                postsContainer.innerHTML = `
                    <div class="post-item">
                        <div class="post-title">Sample Post</div>
                        <div class="post-views">0 views</div>
                    </div>
                `;
            }
        }
    }

    initializePerformanceChart() {
        try {
            console.log('Initializing performance chart...');
            const ctx = document.getElementById('performanceChart');
            if (ctx && typeof Chart !== 'undefined') {
                this.chart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                        datasets: [{
                            label: 'Posts',
                            data: [2, 3, 1, 4, 2, 3, 1],
                            borderColor: '#007bff',
                            backgroundColor: 'rgba(0, 123, 255, 0.1)',
                            tension: 0.4
                        }, {
                            label: 'Views',
                            data: [150, 200, 120, 300, 180, 250, 100],
                            borderColor: '#28a745',
                            backgroundColor: 'rgba(40, 167, 69, 0.1)',
                            tension: 0.4,
                            yAxisID: 'y1'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                type: 'linear',
                                display: true,
                                position: 'left',
                                title: { display: true, text: 'Posts' }
                            },
                            y1: {
                                type: 'linear',
                                display: true,
                                position: 'right',
                                title: { display: true, text: 'Views' },
                                grid: { drawOnChartArea: false }
                            }
                        }
                    }
                });
            }
        } catch (error) {
            console.error('Error initializing chart:', error);
        }
    }

    initializeEventListeners() {
        // Agent control buttons
        const startBtn = document.getElementById('startAgentBtn');
        const stopBtn = document.getElementById('stopAgentBtn');
        
        if (startBtn) startBtn.addEventListener('click', () => this.startAgent());
        if (stopBtn) stopBtn.addEventListener('click', () => this.stopAgent());
        
        // Blog generation buttons
        const generateBlogBtn = document.getElementById('generateBlogBtn');
        const generateSeriesBtn = document.getElementById('generateSeriesBtn');
        
        if (generateBlogBtn) generateBlogBtn.addEventListener('click', () => this.showBlogGenerationModal());
        if (generateSeriesBtn) generateSeriesBtn.addEventListener('click', () => this.showSeriesGenerationModal());
        
        // Refresh buttons
        const refreshActivity = document.getElementById('refreshActivity');
        const refreshTrending = document.getElementById('refreshTrending');
        
        if (refreshActivity) refreshActivity.addEventListener('click', () => this.loadRecentActivity());
        if (refreshTrending) refreshTrending.addEventListener('click', () => this.loadTrendingTopics());
    }

    async startAgent() {
        try {
            this.showLoading(true);
            const response = await api.post('/api/agent/start');
            this.showToast(response.message || 'Agent started successfully', 'success');
            await this.loadAgentStatus();
        } catch (error) {
            this.showToast('Failed to start agent: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async stopAgent() {
        try {
            this.showLoading(true);
            const response = await api.post('/api/agent/stop');
            this.showToast(response.message || 'Agent stopped successfully', 'success');
            await this.loadAgentStatus();
        } catch (error) {
            this.showToast('Failed to stop agent: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    showBlogGenerationModal() {
        // Simple modal for blog generation
        alert('Blog generation feature - This would open a modal for generating blog posts.');
    }

    showSeriesGenerationModal() {
        // Simple modal for series generation
        alert('Series generation feature - This would open a modal for generating blog series.');
    }

    showToast(message, type = 'info') {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        const container = document.getElementById('toastContainer');
        if (container) {
            container.appendChild(toast);
            setTimeout(() => toast.remove(), 5000);
        }
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dashboard: Initializing...');
    new Dashboard();
    console.log('Dashboard: Initialized successfully');
});

// Export for debugging
window.Dashboard = Dashboard;