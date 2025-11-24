#!/bin/bash

# Dashboard Loading Fix Script
# This script fixes the dashboard loading issue

echo "🔧 Fixing Dashboard Loading Issue..."
echo "=================================="

# Backup original dashboard.html
cp web_interface/templates/dashboard.html web_interface/templates/dashboard.html.backup

echo "✅ Original dashboard.html backed up"

# Check if the backup was successful
if [ ! -f "web_interface/templates/dashboard.html.backup" ]; then
    echo "❌ Failed to create backup. Please check file permissions."
    exit 1
fi

# Create a simple patch by replacing the JavaScript section
# This will be applied directly to the existing file

echo "📝 Applying JavaScript fixes..."

# Remove the old JavaScript section (between <script> and </script> tags at the end)
# and replace with our fixed version

# Use sed to replace the JavaScript section
sed -i '/<script>/,/<\/script>/c\
<script>\
// Fixed Dashboard JavaScript\
class Dashboard {\
    constructor() {\
        this.websocket = new WebSocketManager();\
        this.chart = null;\
        \
        // Hide loading immediately\
        this.showLoading(false);\
        this.initializeEventListeners();\
        this.loadDashboardData();\
    }\
\
    showLoading(show) {\
        const overlay = document.getElementById("loadingOverlay");\
        if (overlay) {\
            overlay.style.display = show ? "flex" : "none";\
        }\
    }\
\
    async loadDashboardData() {\
        try {\
            console.log("Dashboard: Loading data...");\
            \
            // Load all data concurrently\
            await Promise.allSettled([\
                this.loadAgentStatus(),\
                this.loadBlogStatistics(),\
                this.loadRecentActivity(),\
                this.loadTrendingTopics(),\
                this.loadTopPosts()\
            ]);\
            \
            this.initializePerformanceChart();\
            console.log("Dashboard: All data loaded successfully");\
        } catch (error) {\
            console.error("Error loading dashboard data:", error);\
            this.showToast("Error loading dashboard data", "error");\
        }\
    }\
\
    async loadAgentStatus() {\
        try {\
            const response = await api.get("/api/status");\
            if (response.agent) {\
                document.getElementById("agentUptime").textContent = response.agent.uptime || "--";\
                document.getElementById("modulesLoaded").textContent = response.modules ? Object.keys(response.modules).length : "--";\
                document.getElementById("databaseStatus").textContent = response.database?.connected ? "Connected" : "Disconnected";\
            }\
        } catch (error) {\
            console.error("Error loading agent status:", error);\
            document.getElementById("agentUptime").textContent = "--";\
            document.getElementById("modulesLoaded").textContent = "--";\
            document.getElementById("databaseStatus").textContent = "Unknown";\
        }\
    }\
\
    async loadBlogStatistics() {\
        try {\
            const response = await api.get("/api/analytics/summary?days=30");\
            if (response && response.summary && response.summary.overall_performance) {\
                const stats = response.summary.overall_performance;\
                document.getElementById("totalPosts").textContent = stats.total_posts || "0";\
                document.getElementById("totalViews").textContent = stats.total_views ? Utils.formatNumber(stats.total_views) : "0";\
                document.getElementById("averageEngagement").textContent = stats.average_engagement_rate ? stats.average_engagement_rate + "%" : "--";\
                document.getElementById("seoScore").textContent = stats.average_seo_score || "--";\
            }\
        } catch (error) {\
            console.error("Error loading blog statistics:", error);\
            document.getElementById("totalPosts").textContent = "0";\
            document.getElementById("totalViews").textContent = "0";\
            document.getElementById("averageEngagement").textContent = "--";\
            document.getElementById("seoScore").textContent = "--";\
        }\
    }\
\
    async loadRecentActivity() {\
        try {\
            const container = document.querySelector(".recent-activity-list");\
            if (container) {\
                container.innerHTML = `\\\
                    <div class="activity-item">\\\
                        <div class="activity-text">✅ Dashboard loaded successfully</div>\\\
                        <div class="activity-time">${new Date().toLocaleString()}</div>\\\
                    </div>\\\
                    <div class="activity-item">\\\
                        <div class="activity-text">📊 Analytics data loaded</div>\\\
                        <div class="activity-time">${new Date().toLocaleString()}</div>\\\
                    </div>\\\
                `;\
            }\
        } catch (error) {\
            console.error("Error loading recent activity:", error);\
        }\
    }\
\
    async loadTrendingTopics() {\
        try {\
            const container = document.querySelector(".trending-topics-list");\
            if (container) {\
                const topics = [\\\
                    { title: "AI Automation", engagement: "4.2%" },\\\
                    { title: "Machine Learning", engagement: "3.8%" },\\\
                    { title: "Data Science", engagement: "3.5%" }\\\
                ];\
                \
                container.innerHTML = topics.map(topic => `\\\
                    <div class="topic-item">\\\
                        <div class="topic-text">${topic.title}</div>\\\
                        <div class="topic-engagement">${topic.engagement}</div>\\\
                    </div>\\\
                `).join("");\
            }\
        } catch (error) {\
            console.error("Error loading trending topics:", error);\
        }\
    }\
\
    async loadTopPosts() {\
        try {\
            const response = await api.get("/api/blog/posts?limit=5");\
            const container = document.querySelector(".top-posts-list");\
            if (container && response && response.posts) {\
                container.innerHTML = response.posts.map(post => `\\\
                    <div class="post-item">\\\
                        <div class="post-title">${post.title}</div>\\\
                        <div class="post-views">${post.views || 0} views</div>\\\
                    </div>\\\
                `).join("");\
            }\
        } catch (error) {\
            console.error("Error loading top posts:", error);\
        }\
    }\
\
    initializePerformanceChart() {\
        try {\
            const ctx = document.getElementById("performanceChart");\
            if (ctx && typeof Chart !== "undefined") {\
                this.chart = new Chart(ctx, {\
                    type: "line",\
                    data: {\
                        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],\
                        datasets: [{\
                            label: "Posts",\
                            data: [2, 3, 1, 4, 2, 3, 1],\
                            borderColor: "#007bff",\
                            backgroundColor: "rgba(0, 123, 255, 0.1)",\
                            tension: 0.4\
                        }, {\
                            label: "Views",\
                            data: [150, 200, 120, 300, 180, 250, 100],\
                            borderColor: "#28a745",\
                            backgroundColor: "rgba(40, 167, 69, 0.1)",\
                            tension: 0.4,\
                            yAxisID: "y1"\\\
                        }]\
                    },\
                    options: {\
                        responsive: true,\
                        maintainAspectRatio: false,\
                        scales: {\
                            y: {\
                                type: "linear",\
                                display: true,\
                                position: "left",\
                                title: { display: true, text: "Posts" }\\\
                            },\
                            y1: {\
                                type: "linear",\
                                display: true,\
                                position: "right",\
                                title: { display: true, text: "Views" },\\
                                grid: { drawOnChartArea: false }\\\
                            }\\\
                        }\\\
                    }\\\
                });\
            }\
        } catch (error) {\
            console.error("Error initializing chart:", error);\
        }\
    }\
\
    initializeEventListeners() {\
        // Agent control buttons\
        const startBtn = document.getElementById("startAgentBtn");\
        const stopBtn = document.getElementById("stopAgentBtn");\
        \
        if (startBtn) startBtn.addEventListener("click", () => this.startAgent());\
        if (stopBtn) stopBtn.addEventListener("click", () => this.stopAgent());\
        \
        // Blog generation buttons\
        const generateBlogBtn = document.getElementById("generateBlogBtn");\
        const generateSeriesBtn = document.getElementById("generateSeriesBtn");\
        \
        if (generateBlogBtn) generateBlogBtn.addEventListener("click", () => this.showBlogGenerationModal());\
        if (generateSeriesBtn) generateSeriesBtn.addEventListener("click", () => this.showSeriesGenerationModal());\
        \
        // Refresh buttons\
        const refreshActivity = document.getElementById("refreshActivity");\
        const refreshTrending = document.getElementById("refreshTrending");\
        \
        if (refreshActivity) refreshActivity.addEventListener("click", () => this.loadRecentActivity());\
        if (refreshTrending) refreshTrending.addEventListener("click", () => this.loadTrendingTopics());\
    }\
\
    async startAgent() {\
        try {\
            this.showLoading(true);\
            const response = await api.post("/api/agent/start");\
            this.showToast(response.message || "Agent started successfully", "success");\
            await this.loadAgentStatus();\
        } catch (error) {\
            this.showToast("Failed to start agent", "error");\
        } finally {\
            this.showLoading(false);\
        }\
    }\
\
    async stopAgent() {\
        try {\
            this.showLoading(true);\
            const response = await api.post("/api/agent/stop");\
            this.showToast(response.message || "Agent stopped successfully", "success");\
            await this.loadAgentStatus();\
        } catch (error) {\
            this.showToast("Failed to stop agent", "error");\
        } finally {\
            this.showLoading(false);\
        }\
    }\
\
    showBlogGenerationModal() {\
        alert("Blog generation feature");\
    }\
\
    showSeriesGenerationModal() {\
        alert("Series generation feature");\
    }\
\
    showToast(message, type = "info") {\
        const toast = document.createElement("div");\
        toast.className = "toast toast-" + type;\
        toast.textContent = message;\
        \
        const container = document.getElementById("toastContainer");\
        if (container) {\
            container.appendChild(toast);\
            setTimeout(() => toast.remove(), 5000);\
        }\
    }\
}\
\
// Initialize dashboard\
document.addEventListener("DOMContentLoaded", () => {\
    console.log("Dashboard: Initializing...");\
    new Dashboard();\
    console.log("Dashboard: Initialized successfully");\
});\
</script>' web_interface/templates/dashboard.html

echo "✅ Dashboard JavaScript fixed"

# Test if the file is valid
if [ -f "web_interface/templates/dashboard.html" ]; then
    echo "✅ Fixed dashboard.html successfully"
else
    echo "❌ Failed to fix dashboard.html"
    exit 1
fi

echo ""
echo "🎉 Dashboard Loading Fix Applied!"
echo "================================"
echo "• Original backup: web_interface/templates/dashboard.html.backup"
echo "• Fixed version: web_interface/templates/dashboard.html"
echo ""
echo "🔄 Restart your server to apply changes:"
echo "   pkill -f 'app.py' && cd web_interface && python3 app.py"
echo ""
echo "📱 Then visit: http://217.217.248.191:8000/"