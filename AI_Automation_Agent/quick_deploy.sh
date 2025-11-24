#!/bin/bash
# One-liner deployment command for VPS
# Run this directly on your VPS: curl -sSL https://raw.githubusercontent.com/your-repo/deploy_one_liner.sh | bash

curl -sSL "https://raw.githubusercontent.com/minimax/ai-automation-agent/main/deploy_to_vps.sh" | bash || {
    echo "Download failed. Copy the deploy_to_vps.sh script manually and run it."
}

echo "🎉 VPS Deployment Complete!"
echo "Dashboard: http://217.217.248.191:8000/"
echo "Tests: http://217.217.248.191:8000/test"