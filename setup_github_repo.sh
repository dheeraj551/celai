#!/bin/bash
# GitHub Repository Setup Script
# Run this script to initialize and push your AI Automation Agent to GitHub

set -e  # Exit on any error

echo "=========================================="
echo "🚀 GITHUB REPOSITORY SETUP"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -f "AI_Automation_Agent/.env.celorisdesigns" ]; then
    echo "❌ Error: Please run this script from the ai-automation-agent directory"
    echo "   This directory should contain README.md and AI_Automation_Agent/ folder"
    exit 1
fi

# Get repository name from user
echo "📝 Setting up GitHub repository..."
echo ""
read -p "Enter your GitHub username: " GITHUB_USERNAME
read -p "Enter repository name (default: ai-automation-agent): " REPO_NAME
REPO_NAME=${REPO_NAME:-ai-automation-agent}

echo ""
echo "🔧 Initializing Git repository..."

# Initialize git if not already done
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already initialized"
fi

# Add all files to git
echo "📦 Adding files to git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: AI Automation Agent

Features:
- AI-powered blog generation using OpenAI
- Advanced scheduling with cron-like functionality  
- Multi-platform publishing (Next.js, WordPress, Medium)
- Session-based authentication for secure access
- Real-time web dashboard with performance metrics
- Background service with auto-restart capability
- MongoDB database integration
- FastAPI web interface

Includes:
- Blog automation module
- Content publisher with multiple platform support
- Web interface with live monitoring
- Comprehensive setup documentation
- Background service management
- Testing utilities
- Production-ready configuration

Perfect for automating content creation and distribution across multiple platforms."

echo ""
echo "🔗 Setting up remote repository..."

# Check if remote already exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "⚠️ Remote 'origin' already exists"
    read -p "Do you want to update the remote URL? (y/n): " update_remote
    if [ "$update_remote" = "y" ] || [ "$update_remote" = "Y" ]; then
        git remote set-url origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
        echo "✅ Remote URL updated"
    else
        echo "Keeping existing remote URL"
    fi
else
    git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    echo "✅ Remote 'origin' added: https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
fi

echo ""
echo "🌿 Creating and switching to main branch..."
git branch -M main

echo ""
echo "🚀 Pushing to GitHub..."
echo "   Repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
echo ""
echo "⚠️  Note: You may be prompted for your GitHub credentials."
echo "   For easier setup, consider using GitHub CLI or personal access token."
echo ""

read -p "Ready to push? Press Enter to continue or Ctrl+C to cancel..."

# Push to GitHub
if git push -u origin main; then
    echo ""
    echo "🎉 SUCCESS! Your AI Automation Agent is now on GitHub!"
    echo ""
    echo "📋 Repository Details:"
    echo "   GitHub: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo "   Local:  $(pwd)"
    echo ""
    echo "📝 Next Steps:"
    echo "   1. Visit your repository on GitHub"
    echo "   2. Configure repository settings"
    echo "   3. Set up branches for development"
    echo "   4. Add collaborators if needed"
    echo "   5. Enable GitHub Actions for CI/CD (optional)"
    echo ""
    echo "🔄 To update your repository later:"
    echo "   git add ."
    echo "   git commit -m 'Your update message'"
    echo "   git push"
    echo ""
    echo "💡 To clone your repository on another machine:"
    echo "   git clone https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    echo ""
    echo "🔒 Security Reminder:"
    echo "   - Never commit your .env.celorisdesigns file"
    echo "   - Use environment variables for sensitive data"
    echo "   - Consider using GitHub Secrets for production"
    echo ""
else
    echo ""
    echo "❌ Push failed. This might be due to:"
    echo "   1. Authentication issues (need GitHub token)"
    echo "   2. Repository doesn't exist yet"
    echo "   3. Network connectivity issues"
    echo ""
    echo "💡 To create repository manually:"
    echo "   1. Go to https://github.com/new"
    echo "   2. Repository name: $REPO_NAME"
    echo "   3. Don't initialize with README (we already have one)"
    echo "   4. Click 'Create repository'"
    echo "   5. Then run: git push -u origin main"
    echo ""
    echo "💡 For authentication, you can:"
    echo "   - Use GitHub CLI: gh auth login"
    echo "   - Create personal access token: https://github.com/settings/tokens"
    echo "   - Use SSH keys for passwordless authentication"
fi

echo ""
echo "=========================================="