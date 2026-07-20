#!/bin/bash
# ============================================================
# 一次性脚本：申请 Let's Encrypt SSL 证书 + 配置 Nginx
# ============================================================
# 使用：
#   1. chmod +x setup-https.sh
#   2. sudo ./setup-https.sh
# 前置：
#   - 域名 nexus.azhi-home.top 已解析到本服务器公网 IP
#   - macOS 上已装 brew install nginx
#   - macOS 上已装 brew install certbot
# ============================================================

set -e

DOMAIN="nexus.azhi-home.top"
EMAIL="${CERT_EMAIL:-your-email@example.com}"  # 改这里
NGINX_DIR="/usr/local/etc/nginx"

echo "🔍 1. 检查环境..."
if ! command -v nginx &> /dev/null; then
    echo "❌ 没装 nginx，先执行：brew install nginx"
    exit 1
fi
if ! command -v certbot &> /dev/null; then
    echo "❌ 没装 certbot，先执行：brew install certbot"
    exit 1
fi

echo ""
echo "🔍 2. 确认 DNS..."
PUBLIC_IP=$(curl -s -4 ifconfig.me)
RESOLVED_IP=$(dig +short "$DOMAIN" | head -1)
echo "公网 IP: $PUBLIC_IP"
echo "$DOMAIN 解析到: $RESOLVED_IP"
if [ "$RESOLVED_IP" != "$PUBLIC_IP" ]; then
    echo "⚠️  警告：域名解析的 IP 和本机公网 IP 不一致！"
    echo "   请检查 DNS 解析（azhi-home.top 的 A 记录）"
    read -p "继续吗？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then exit 1; fi
fi

echo ""
echo "📋 3. 复制 nginx 配置..."
mkdir -p "$NGINX_DIR/servers"
cp ../nexus/nginx.conf "$NGINX_DIR/servers/nexus.conf"
# 替换占位符
sed -i '' "s|nexus.azhi-home.top|$DOMAIN|g" "$NGINX_DIR/servers/nexus.conf"

echo ""
echo "🔒 4. 申请 Let's Encrypt 证书..."
# 临时启动 nginx 占用 80 端口
brew services start nginx

# 申请证书
sudo certbot certonly --nginx -d "$DOMAIN" --email "$EMAIL" --agree-tos --no-eff-email

echo ""
echo "🔄 5. 重启 nginx..."
nginx -t
brew services restart nginx

echo ""
echo "✅ 完成！"
echo "   https://$DOMAIN  → Nexus 管理界面"
echo ""
echo "📝 接下来："
echo "   1. cd .. && docker compose up -d"
echo "   2. 等 1-2 分钟"
echo "   3. 访问 https://$DOMAIN"
echo "   4. 用 admin / \$NEXUS_ADMIN_PASSWORD 登录"