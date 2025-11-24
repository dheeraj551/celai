# One-line VPS Deployment Command
# Copy and paste this entire block into your VPS terminal:

cd /root && \
wget -q https://raw.githubusercontent.com/minimax/ai-automation-agent/main/deploy_to_vps.sh && \
chmod +x deploy_to_vps.sh && \
./deploy_to_vps.sh && \
echo "✅ Deployment complete! Visit: http://217.217.248.191:8000/"