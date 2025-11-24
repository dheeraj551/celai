#!/bin/bash
# GitHub Repository Organization Script
# This script organizes all files into a proper GitHub repository structure

set -e

echo "=========================================="
echo "📦 ORGANIZING GITHUB REPOSITORY"
echo "=========================================="

# Create the main repository directory
REPO_DIR="ai-automation-agent-github"
echo "Creating repository directory: $REPO_DIR"
rm -rf "$REPO_DIR"
mkdir -p "$REPO_DIR"

echo ""
echo "📁 Copying repository structure..."

# Copy main application
cp -r AI_Automation_Agent "$REPO_DIR/"

# Copy documentation
cp README.md "$REPO_DIR/"
cp SETUP_GUIDE.md "$REPO_DIR/"
cp API_REFERENCE.md "$REPO_DIR/"
cp TROUBLESHOOTING.md "$REPO_DIR/"

# Copy utility scripts
mkdir -p "$REPO_DIR/scripts"
cp service_manager.py "$REPO_DIR/scripts/"
cp start_background_service.py "$REPO_DIR/scripts/"
cp quick_fix_mysql_error.sh "$REPO_DIR/scripts/"
cp setup_github_repo.sh "$REPO_DIR/scripts/"

# Copy test files
mkdir -p "$REPO_DIR/tests"
cp test_mongodb_connection.py "$REPO_DIR/tests/"
cp test_nextjs_integration.py "$REPO_DIR/tests/"

# Copy configuration files
cp .env.example "$REPO_DIR/"
cp .gitignore "$REPO_DIR/"

# Create docs directory for additional documentation
mkdir -p "$REPO_DIR/docs"
echo "Additional documentation can be placed in the docs/ directory" > "$REPO_DIR/docs/README.md"

echo ""
echo "🧹 Cleaning up repository..."

# Remove sensitive files from repository
cd "$REPO_DIR"

# Remove any existing .env files (we have .env.example instead)
find . -name ".env*" -not -name ".env.example" -delete

# Remove PID files
find . -name "*.pid" -delete

# Remove log files
find . -name "*.log" -delete
rm -rf logs/

# Remove Python cache
find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete

# Remove temporary files
find . -name ".DS_Store" -delete
find . -name "Thumbs.db" -delete
find . -name "*.tmp" -delete
find . -name "*.bak" -delete

echo ""
echo "📝 Creating repository structure documentation..."

# Create detailed file structure documentation
cat > FILE_STRUCTURE.md << 'EOF'
# AI Automation Agent - File Structure

```
ai-automation-agent/
├── README.md                    # Main project documentation
├── SETUP_GUIDE.md              # Detailed setup instructions  
├── API_REFERENCE.md            # API documentation
├── TROUBLESHOOTING.md          # Common issues and solutions
├── .env.example                # Environment template (copy to .env.celorisdesigns)
├── .gitignore                  # Git ignore rules
│
├── AI_Automation_Agent/        # Main application directory
│   ├── config/                 # Configuration modules
│   │   ├── database.py         # Database connection management
│   │   └── settings.py         # Application settings
│   │
│   ├── modules/                # Core functionality modules
│   │   ├── blog_automation/    # Blog generation and scheduling
│   │   │   ├── blog_generator.py
│   │   │   ├── blog_scheduler.py
│   │   │   └── content_publisher.py
│   │   └── content_publisher/  # Multi-platform publishing
│   │       ├── base_publisher.py
│   │       ├── nextjs_publisher.py
│   │       ├── wordpress_publisher.py
│   │       └── medium_publisher.py
│   │
│   ├── web_interface/          # FastAPI web interface
│   │   ├── app.py             # Main FastAPI application
│   │   ├── templates/         # HTML templates
│   │   └── static/            # CSS, JavaScript, images
│   │
│   ├── requirements.txt        # Python dependencies
│   └── .env.celorisdesigns     # Environment configuration (NOT in repo)
│
├── scripts/                    # Utility and management scripts
│   ├── service_manager.py      # Background service management
│   ├── start_background_service.py # Service runner with monitoring
│   ├── quick_fix_mysql_error.sh    # MongoDB setup automation
│   └── setup_github_repo.sh    # GitHub repository setup
│
├── tests/                      # Test and validation scripts
│   ├── test_mongodb_connection.py  # MongoDB connectivity test
│   └── test_nextjs_integration.py  # Next.js integration test
│
└── docs/                       # Additional documentation
    └── README.md              # Documentation index
```

## Key Files Description

### Configuration Files
- `.env.example` - Template for environment configuration
- `AI_Automation_Agent/config/settings.py` - Application settings
- `AI_Automation_Agent/config/database.py` - Database connection logic

### Core Application
- `AI_Automation_Agent/web_interface/app.py` - Main web interface
- `AI_Automation_Agent/modules/blog_automation/` - Blog generation logic
- `AI_Automation_Agent/modules/content_publisher/` - Publishing logic

### Management Scripts
- `scripts/service_manager.py` - Background service control
- `scripts/start_background_service.py` - Service runner with monitoring

### Testing
- `tests/test_mongodb_connection.py` - Database connectivity validation
- `tests/test_nextjs_integration.py` - Platform integration testing

## Security Notes

❌ **Never commit these files:**
- `.env.celorisdesigns` (contains actual API keys and secrets)
- `*.pid` (process ID files)
- `logs/` (contains runtime logs)
- `__pycache__/` (Python compiled files)

✅ **Safe to commit:**
- All source code
- Configuration templates (`.env.example`)
- Documentation
- Test scripts
- Requirements files
EOF

echo ""
echo "📊 Repository Statistics:"
echo "   Total files: $(find . -type f | wc -l)"
echo "   Python files: $(find . -name "*.py" | wc -l)"
echo "   Documentation files: $(find . -name "*.md" | wc -l)"
echo "   Scripts: $(find scripts/ -name "*.py" -o -name "*.sh" | wc -l)"

echo ""
echo "🔍 Final verification..."

# Check for sensitive files that shouldn't be in repo
SENSITIVE_FILES=()
if find . -name ".env" -not -path "./.env.example" | grep -q .; then
    SENSITIVE_FILES+=("Environment files")
fi

if find . -name "*.key" -o -name "*secret*" -o -name "*password*" | grep -q .; then
    SENSITIVE_FILES+=("Sensitive files")
fi

if [ ${#SENSITIVE_FILES[@]} -gt 0 ]; then
    echo "⚠️  Warning: Found potentially sensitive files:"
    printf "   - %s\n" "${SENSITIVE_FILES[@]}"
    echo "   Please review and remove before pushing to GitHub"
else
    echo "✅ No sensitive files found in repository"
fi

echo ""
echo "📦 Repository organized successfully!"
echo ""
echo "Next steps:"
echo "1. cd $REPO_DIR"
echo "2. git init"
echo "3. git add ."
echo "4. git commit -m 'Initial commit: AI Automation Agent'"
echo "5. Create repository on GitHub: https://github.com/new"
echo "6. git remote add origin https://github.com/YOUR_USERNAME/ai-automation-agent.git"
echo "7. git branch -M main"
echo "8. git push -u origin main"
echo ""
echo "Or run: ./scripts/setup_github_repo.sh"
echo ""
echo "=========================================="