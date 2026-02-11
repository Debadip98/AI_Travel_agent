# Production Deployment Guide - AI Travel Agent

## Overview

This guide covers complete production deployment of the AI Travel Agent application with:
- PostgreSQL database
- User authentication (JWT + OAuth)
- All 30+ country visa support
- Real API integrations
- Error handling & logging
- Security best practices

---

## ✅ Prerequisites

### System Requirements
- **OS:** Linux (Ubuntu 20.04+ recommended) or macOS
- **Python:** 3.9 or higher
- **Node.js:** 16.0 or higher
- **PostgreSQL:** 12.0 or higher
- **Redis:** 6.0 or higher (for caching)
- **Docker:** 20.10+ (optional, for containerized deployment)

### API Keys Required

Before deploying, obtain these credentials:

```
AMADEUS_API_KEY              - Amadeus flight search
AMADEUS_API_SECRET           - Amadeus secret key
GOOGLE_MAPS_API_KEY          - Google Maps API
GOOGLE_OAUTH_CLIENT_ID       - Google OAuth ID
GOOGLE_OAUTH_CLIENT_SECRET   - Google OAuth Secret
OPENAI_API_KEY               - OpenAI GPT API (optional)
STRIPE_API_KEY               - Stripe payment gateway
PAYPAL_CLIENT_ID             - PayPal sandbox/live
RAZORPAY_KEY_ID              - Razorpay (India payments)
EXCHANGE_RATE_API_KEY        - Currency conversion
SENTRY_DSN                   - Error tracking (optional)
```

---

## 📦 Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/AI_Travel_agent.git
cd AI_Travel_agent
```

### 2. Backend Setup

```bash
# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Create .env file from template
cp ../.env.example .env

# Edit .env with your credentials
nano .env
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb travel_agent_db

# Set DATABASE_URL in .env file
# Example: DATABASE_URL=postgresql://user:password@localhost:5432/travel_agent_db

# Run migrations (when using Alembic)
# alembic upgrade head
```

### 4. Frontend Setup

```bash
cd ../frontend

# Install Node dependencies
npm install

# Create React .env file
cp .env.example .env

# Update API base URL if needed
nano .env
```

---

## 🔐 Security Configuration

### 1. Generate Secret Keys

```bash
# Generate Flask SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"

# Generate JWT_SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Update .env

```bash
SECRET_KEY=your_generated_secret_key_here
JWT_SECRET_KEY=your_generated_jwt_secret_here
FLASK_ENV=production
ENVIRONMENT=production
DEBUG=False
```

### 3. CORS Configuration

```bash
# .env
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 4. SSL/TLS Certificates

For production, use Let's Encrypt:

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Certificate files will be in /etc/letsencrypt/live/yourdomain.com/
```

---

## 🗄️ Database Initialization

### 1. Create Database Tables

```bash
cd backend
python3
```

```python
from config.settings import Config
from models.database_models import DatabaseManager

db = DatabaseManager(Config.SQLALCHEMY_DATABASE_URI)
db.init_db()
db.create_tables()
exit()
```

### 2. Create Admin User

```python
from integrations.auth_service import AuthenticationService
from models.database_models import UserModel

auth = AuthenticationService(Config.JWT_SECRET_KEY)
admin_user = UserModel(
    email="admin@yourdomain.com",
    password_hash=auth.hash_password("strong_password_123"),
    full_name="Admin User"
)
# Save to database
```

---

## 🚀 Running the Application

### Option 1: Manual Execution

```bash
# Terminal 1 - Backend
cd backend
export FLASK_ENV=production
gunicorn --workers 4 --bind 0.0.0.0:5000 main:app

# Terminal 2 - Frontend
cd frontend
npm run build
npm run preview  # Or use nginx/Apache to serve
```

### Option 2: Docker Compose

```bash
cd /workspaces/AI_Travel_agent

# Build containers
docker-compose build

# Run application
docker-compose up -d

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Option 3: Systemd Service (Linux)

Create `/etc/systemd/system/travel-agent.service`:

```ini
[Unit]
Description=AI Travel Agent
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=travel-agent
WorkingDirectory=/opt/ai_travel_agent
ExecStart=/opt/ai_travel_agent/venv/bin/gunicorn \
  --workers 4 \
  --bind unix:/tmp/travel-agent.sock \
  --timeout 120 \
  main:app
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable service
sudo systemctl enable travel-agent
sudo systemctl start travel-agent
sudo systemctl status travel-agent
```

---

## 📊 Monitoring & Logging

### 1. Enable Sentry for Error Tracking

```bash
# .env
SENTRY_DSN=https://your_sentry_dsn@sentry.io/project_id

# Logs will be sent to Sentry automatically
```

### 2. View Application Logs

```bash
# Docker
docker-compose logs -f backend

# Systemd
sudo journalctl -u travel-agent -f

# File logs
tail -f logs/travel_agent.log
```

### 3. Monitor Database

```bash
# Connect to PostgreSQL
psql -U user -d travel_agent_db

# Check table stats
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

## ✅ Health Checks

### API Health Endpoint

```bash
# Check backend status
curl -X GET http://localhost:5000/api/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2024-02-11T10:30:00Z",
  "database": "connected",
  "cache": "connected"
}
```

### Database Health

```bash
# Test connection
python3 -c "from models.database_models import DatabaseManager; db = DatabaseManager(os.getenv('DATABASE_URL')); print('DB OK')"
```

---

## 🔄 Backup & Recovery

### Automated Backups

```bash
# Create backup script: backup.sh
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/travel_agent"
mkdir -p $BACKUP_DIR

# PostgreSQL backup
pg_dump travel_agent_db | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Application files backup
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /opt/ai_travel_agent --exclude=venv

# Keep only last 30 days
find $BACKUP_DIR -mtime +30 -delete

echo "Backup completed: $DATE"
```

```bash
# Add to crontab to run daily at 2 AM
0 2 * * * /scripts/backup.sh
```

### Restore from Backup

```bash
# Restore database
gunzip -c backups/db_20240211_020000.sql.gz | psql travel_agent_db

# Restore application files
tar -xzf backups/app_20240211_020000.tar.gz -C /opt
```

---

## 📈 Scaling Recommendations

### Horizontal Scaling

```yaml
# docker-compose override for load balancing
version: '3.8'
services:
  backend:
    scale: 3  # Run 3 instances
  
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - /etc/letsencrypt:/etc/nginx/certs
```

### Performance Optimization

1. **Enable Caching**
   ```bash
   CACHE_ENABLED=True
   CACHE_TTL_SECONDS=3600
   REDIS_URL=redis://localhost:6379/0
   ```

2. **Database Connection Pooling**
   ```bash
   DB_POOL_SIZE=20
   DB_POOL_RECYCLE=3600
   ```

3. **CDN for Static Files**
   - Upload frontend assets to CloudFront/Cloudflare
   - Set `REACT_APP_CDN_URL` in frontend .env

---

## 🔍 Troubleshooting

### Issue: Database Connection Failed

```bash
# Check PostgreSQL service
sudo systemctl status postgresql

# Verify connection string
psql postgresql://user:password@localhost:5432/travel_agent_db

# Check logs
sudo tail -f /var/log/postgresql/postgresql.log
```

### Issue: API Key Not Working

```bash
# Verify key is set in .env
grep AMADEUS_API_KEY .env

# Test API connection
python3 -c "from integrations.apis import FlightAPI; api = FlightAPI(); print(api.get_amadeus_token())"
```

### Issue: Frontend Not Loading

```bash
# Check frontend process
ps aux | grep node

# Check port 3000 is accessible
curl http://localhost:3000

# Check browser console for errors
# Open browser developer tools (F12)
```

---

## 📝 Maintenance

### Regular Tasks

**Daily:**
- Monitor logs for errors
- Check database performance
- Verify backup completion

**Weekly:**
- Review application metrics
- Check API rate limits
- Update dependencies if available

**Monthly:**
- Full database backup verification
- Security audit
- Performance analysis
- Update documentation

### Update Procedure

```bash
# 1. Backup current state
./backup.sh

# 2. Pull latest changes
git pull origin main

# 3. Install updated dependencies
pip install -r requirements.txt --upgrade

# 4. Run database migrations (if any)
alembic upgrade head

# 5. Rebuild frontend
cd frontend && npm install && npm run build && cd ..

# 6. Restart services
docker-compose restart
# OR
sudo systemctl restart travel-agent
```

---

## 🔗 Production URLs

After deployment at `yourdomain.com`:

```
API Base URL:           https://api.yourdomain.com
Frontend URL:           https://yourdomain.com
Gmail OAuth Redirect:   https://api.yourdomain.com/auth/gmail/callback
Admin Dashboard:        https://yourdomain.com/admin
API Documentation:      https://api.yourdomain.com/docs
Health Check:           https://api.yourdomain.com/api/health
```

---

## 📞 Support & Next Steps

1. **Enable API Integrations**
   - Add real Amadeus credentials
   - Configure Google Maps API
   - Setup Gmail OAuth

2. **Customize Visa Data**
   - Add country-specific information
   - Update visa fees and processing times
   - Add embassy contact information

3. **Extend Features**
   - Add more cities to guide
   - Implement payment processing
   - Enable multi-language support

4. **Monitor Performance**
   - Setup Sentry for error tracking
   - Configure CloudWatch/DataDog for metrics
   - Setup alerts for critical errors

---

**Deployment Status: ✅ READY FOR PRODUCTION**

For questions or issues, refer to the main documentation or contact support.
