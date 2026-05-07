# 📄 README: 3-Tier Application Deployment on AWS EC2

> **Assignment Submission** | **Author: Masudur Rahman**  
> **Repository:** `https://github.com/chintitomasud3/Assignment-3-Tier-Application-on-AWS-EC2)`  
> **Date:** `7 May 2026`

---

## 🎯 Objective
Design and deploy a scalable 3-tier web application on AWS EC2 with proper separation of concerns:
- **Presentation Layer**: Nginx + Frontend Application (Port 8000)
- **Application Layer**: FastAPI (Python) Backend (Port 9000)
- **Data Layer**: MongoDB Database (Port 27017)

---

## 🧱 Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│            PRESENTATION LAYER                        │
│  ┌─────────────────────────────────────────┐       │
│  │  EC2: Nginx + Frontend                  │       │
│  │  Private IP: 10.0.10.230                │       │
│  │  Public Access: ✓ Port 80               │       │
│  │                                         │       │
│  │  Nginx Routing:                         │       │
│  │  • /       → http://10.0.10.230:8000   │       │
│  │  • /api/   → http://10.0.1.226:9000    │       │
│  └─────────────────────────────────────────┘       │
└─────────────────┬───────────────────────────────────┘
                  │ proxy_pass /api/
                  ▼
┌─────────────────────────────────────────────────────┐
│            APPLICATION LAYER                         │
│  ┌─────────────────────────────────────────┐       │
│  │  EC2: FastAPI Backend                   │       │
│  │  Private IP: 10.0.1.226:9000            │       │
│  │  Public Access: ✗ (Private Only)        │       │
│  │                                         │       │
│  │  • REST API with CRUD operations        │       │
│  │  • Async MongoDB via Motor              │       │
│  └─────────────────────────────────────────┘       │
└─────────────────┬───────────────────────────────────┘
                  │ motor (async)
                  ▼
┌─────────────────────────────────────────────────────┐
│              DATA LAYER                              │
│  ┌─────────────────────────────────────────┐       │
│  │  EC2: MongoDB 7.0                       │       │
│  │  Private IP: 10.0.13.224:27017          │       │
│  │  Public Access: ✗ (Private Only)        │       │
│  │                                         │       │
│  │  • NoSQL database for user data         │       │
│  │  • Bound to private network             │       │
│  └─────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────┘
```

> 🔐 **Network Design**: Public access only via Nginx (port 80). Backend & Database communicate via private IPs only.

---

## 📋 Prerequisites

| Component | Requirement |
|-----------|------------|
| AWS Account | EC2 access with `t2.micro` or higher |
| SSH Client | Key pair (.pem file) for instance access |
| Local Machine | Git, Terminal, Browser, curl |
| Security Groups | Configured as per section below |

---

## ⚙️ Setup Steps

### 🔹 Step 1: Launch 3 EC2 Instances (Ubuntu 22.04 LTS)

| Instance | Role | Private IP | Public IP | Security Group |
|----------|------|------------|-----------|---------------|
| `ec2-presentation` | Nginx + Frontend | `10.0.10.230` | `✓` | `80/tcp` from `0.0.0.0/0`, `22/tcp` from your IP |
| `ec2-application` | FastAPI Backend | `10.0.1.226` | `✗` | `9000/tcp` from `10.0.10.230`, `22/tcp` from your IP |
| `ec2-data` | MongoDB | `10.0.13.224` | `✗` | `27017/tcp` from `10.0.1.226`, `22/tcp` from your IP |

---

### 🔹 Step 2: Configure Data Layer (MongoDB) 🗄️

**SSH into `ec2-data` **(10.0.13.224):
```bash
ssh -i "your-key.pem" ubuntu@10.0.13.224
```

#### 🧩 MongoDB Installation Steps:

```bash
# 🔄 1. System Update
sudo apt-get update

# 📦 2. Add MongoDB Repository
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# 🔑 3. Add GPG Key
sudo rm -f /usr/share/keyrings/mongodb-server-7.0.gpg
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg

# 🔄 4. Update Package List Again
sudo apt update

# ⬆️ 5. Upgrade System (Optional but recommended)
sudo apt-get upgrade -y

# 📥 6. Install MongoDB
sudo apt install -y mongodb-org

# 🚀 7. Start MongoDB Service
sudo systemctl start mongod

# ✅ 8. Enable Auto Start
sudo systemctl enable mongod

# 📊 9. Check Status
sudo systemctl status mongod --no-pager

# 🌐 10. Allow Remote Access (Edit config)
sudo nano /etc/mongod.conf
# Change: bindIp: 127.0.0.1  →  bindIp: 0.0.0.0

# 🔁 11. Restart MongoDB
sudo systemctl restart mongod

# 🧪 12. Test MongoDB Shell
mongosh --eval "db.adminCommand('ping')"
```

✅ **Expected Output**: `{ ok: 1 }`

> ⚠️ **Security Note**: `bindIp: 0.0.0.0` is used for assignment purposes. In production, restrict to backend private IP only: `bindIp: 10.0.1.226`.

---

### 🔹 Step 3: Configure Application Layer (FastAPI) ⚡

**SSH into `ec2-application` **(10.0.1.226):
```bash
ssh -i "your-key.pem" ubuntu@10.0.1.226
```

#### 🐍 Backend Setup Script:

```bash
# 🔄 Update system
sudo apt update

# 🐍 Install Python & tools
sudo apt install -y python3 python3-pip python3-venv

# 📁 Create project directory
mkdir -p Backend && cd Backend

# ⚙️ Create virtual environment
python3 -m venv venv

# 🚀 Activate virtual environment
source venv/bin/activate

# 📦 Install dependencies
pip install --upgrade pip
pip install fastapi uvicorn motor pydantic

# 📝 Create main.py (paste your FastAPI code here)
nano main.py
```

#### ▶️ Start the FastAPI Server:
```bash
cd Backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 9000
```

✅ **Verification**:
```bash
curl http://localhost:9000/
# Output: <h2>FastAPI Running Successfully 🚀</h2>

curl http://localhost:9000/users
# Output: []
```

> 🔧 **Important**: Update `MONGO_URL` in `main.py` to match your DB private IP:
```python
MONGO_URL = "mongodb://10.0.13.224:27017"  # ✅ Match your MongoDB instance
```

---

### 🔹 Step 4: Configure Presentation Layer (Nginx + Frontend) 🌐

**SSH into `ec2-presentation` **(10.0.10.230):

#### 4.1 Install & Configure Nginx
```bash
sudo apt update && sudo apt install -y nginx
sudo nano /etc/nginx/nginx.conf  # Paste the config below
sudo nginx -t && sudo systemctl restart nginx
```

#### 📄 Nginx Configuration (`/etc/nginx/nginx.conf`):
```nginx
worker_processes 1;
events { worker_connections 1024; }

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Frontend upstream (same instance)
    upstream frontend_server {
        server 10.0.10.230:8000;
    }

    # Backend upstream (separate instance)
    upstream backend_server {
        server 10.0.1.226:9000;
    }

    server {
        listen 80;
        server_name _;

        # Frontend route
        location / {
            proxy_pass http://frontend_server;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Backend API route
        location /api/ {
            proxy_pass http://backend_server/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            client_max_body_size 20M;
        }
    }
}
```

#### 4.2 Start Frontend Application (Port 8000)
```bash
# Create frontend directory
mkdir -p Frontend && cd Frontend

# Create simple frontend server (if not already deployed)
cat <<EOF > frontend.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head><title>3-Tier App 🚀</title></head>
        <body>
            <h1>✅ Presentation Layer Loaded</h1>
            <p><a href="/api/users">🔗 View Users API</a></p>
        </body>
    </html>
    """
EOF

# Run frontend on port 8000 (localhost or private IP)
python3 -m venv venv && source venv/bin/activate
pip install fastapi uvicorn
uvicorn frontend:app --host 0.0.0.0 --port 8000
```

✅ **Nginx Verification**:
```bash
sudo nginx -t  # Should show: syntax is ok, test is successful
curl http://localhost/  # Should return frontend HTML
```

---

## 🔐 Security Group Configuration (Critical!)

| Instance | Port | Protocol | Source | Purpose |
|----------|------|----------|--------|---------|
| `ec2-presentation` | 80 | TCP | `0.0.0.0/0` | Public HTTP access |
| `ec2-presentation` | 22 | TCP | Your IP | SSH management |
| `ec2-presentation` | 8000 | TCP | `127.0.0.1/32` | Frontend local access |
| `ec2-application` | 9000 | TCP | `10.0.10.230/32` | Backend API (Nginx only) |
| `ec2-application` | 22 | TCP | Your IP | SSH management |
| `ec2-data` | 27017 | TCP | `10.0.1.226/32` | MongoDB (Backend only) |
| `ec2-data` | 22 | TCP | Your IP | SSH management |

> 🛡️ **Principle of Least Privilege**: Database and backend are NOT publicly accessible.

---

## 🌐 Application Access & Testing

### ✅ Access the Application
```
http://<ec2-presentation-public-ip>/
```
➡️ **Loads frontend** from `10.0.10.230:8000` via Nginx proxy

### ✅ Test API via Nginx Proxy
```
http://<ec2-presentation-public-ip>/api/users
```
➡️ **Proxied to backend** at `10.0.1.226:9000`

### ✅ Full Flow Test (curl)

```bash
# 1. Test frontend loads via Nginx
curl http://<nginx-public-ip>/
# Expected: HTML with "✅ Presentation Layer Loaded"

# 2. Test API endpoint via proxy
curl http://<nginx-public-ip>/api/users
# Expected: [] (empty array)

# 3. Create a user via proxied API
curl -X POST http://<nginx-public-ip>/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Masudur Rahman", "email": "mrahman021992@gmail.com", "age": 34}'

# Expected Response:
{
  "id": "65f8a1b2c3d4e5f6a7b8c9d0",
  "message": "User created successfully"
}

# 4. Verify user was saved in MongoDB
curl http://<nginx-public-ip>/api/users
# Expected: Array containing the newly created user
```

---

## 📸 Screenshots (Proof of Work)

> 📌 *Replace placeholders below with actual screenshots from your deployment*

### 🔹 Screenshot 1: MongoDB Running on Data Layer
```
[📸 INSERT: sudo systemctl status mongod on 10.0.13.224]
```
✅ MongoDB active and accepting connections

### 🔹 Screenshot 2: Backend API Running
```
[📸 INSERT: uvicorn log + curl localhost:9000/users on 10.0.1.226]
```
✅ FastAPI listening on port 9000

### 🔹 Screenshot 3: Frontend on Port 8000
```
[📸 INSERT: curl http://10.0.10.230:8000 response]
```
✅ Frontend app responding on presentation layer

### 🔹 Screenshot 4: Nginx Proxy - Frontend Load
```
[📸 INSERT: Browser screenshot showing http://<public-ip>/ loads frontend]
```
✅ Nginx correctly proxies `/` → `10.0.10.230:8000`

### 🔹 Screenshot 5: Nginx Proxy - API Call
```
[📸 INSERT: curl http://<public-ip>/api/users showing user data]
```
✅ Full flow: Browser → Nginx:80 → Backend:9000 → MongoDB:27017

### 🔹 Screenshot 6: AWS EC2 Console
```
[📸 INSERT: EC2 dashboard with 3 tagged instances running]
```
✅ 3-tier architecture deployed across 3 EC2 instances

---

## 🗂️ Repository Structure

```
3-tier-aws-ec2/
├── README.md                          # This file
├── infrastructure/
│   ├── security-groups.md             # SG rules documentation
│   └── scripts/
│       ├── setup-db.sh                # MongoDB installation script
│       ├── setup-backend.sh           # FastAPI setup script
│       ├── setup-frontend.sh          # Frontend setup script (optional)
│       └── nginx.conf                 # Nginx reverse proxy config
├── backend/
│   ├── main.py                        # FastAPI application code
│   ├── requirements.txt               # Python dependencies
│   └── venv/                          # (gitignored)
├── frontend/
│   ├── frontend.py                    # Simple frontend server
│   └── static/                        # HTML/CSS/JS assets
├── docs/
│   ├── architecture.png               # Architecture diagram
│   └── troubleshooting.md             # Common issues & fixes
└── .gitignore
```

---

## 🛠️ Troubleshooting Guide

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Frontend not loading on `/` | Frontend not running on port 8000 | Check `uvicorn frontend:app --host 0.0.0.0 --port 8000` |
| `502 Bad Gateway` on `/api/` | Backend unreachable | Verify backend running + SG allows `10.0.10.230` → `10.0.1.226:9000` |
| MongoDB connection error | Wrong IP or SG blocked | Check `MONGO_URL` + SG allows `10.0.1.226` → `10.0.13.224:27017` |
| Nginx config error | Syntax issue | Run `sudo nginx -t` before restart |
| CORS errors | Missing middleware | Ensure `CORSMiddleware` is configured in `main.py` |
| Timeout on API calls | Network path blocked | Test: `nc -zv 10.0.1.226 9000` from nginx instance |

**Quick Network Tests**:
```bash
# From presentation instance:
curl http://10.0.10.230:8000          # Test frontend locally
curl http://10.0.1.226:9000/users     # Test backend reachability
nc -zv 10.0.13.224 27017              # Test DB port connectivity

# From backend instance:
mongosh --host 10.0.13.224 --eval "db.adminCommand('ping')"  # Test DB connection
```

---

## 📦 Dependencies Summary

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Presentation | Nginx | 1.18+ | Reverse proxy & routing |
| Presentation | Frontend App | FastAPI/Custom | UI on port 8000 |
| Application | FastAPI | 0.109+ | REST API framework |
| Application | Uvicorn | 0.27+ | ASGI server |
| Application | Motor | 3.3+ | Async MongoDB driver |
| Application | Pydantic | 2.5+ | Data validation |
| Data | MongoDB | 7.0 | NoSQL database |
| OS | Ubuntu | 22.04 LTS | EC2 AMI |

---

## 🎓 Learning Outcomes

✅ Deployed proper 3-tier architecture across 3 EC2 instances  
✅ Implemented Nginx reverse proxy with path-based routing (`/` vs `/api/`)  
✅ Secured inter-layer communication using private IPs + Security Groups  
✅ Built async FastAPI backend with MongoDB integration  
✅ Configured MongoDB with remote access for private network  
✅ Documented full setup for reproducibility and grading  

---

## 🔄 Future Improvements (Optional Enhancements)

- [ ] Add HTTPS with Let's Encrypt on Nginx
- [ ] Implement MongoDB authentication & TLS encryption
- [ ] Use AWS Systems Manager instead of SSH keys
- [ ] Add health check endpoints for auto-scaling
- [ ] Containerize services with Docker + ECS/EKS
- [ ] Add logging & monitoring with CloudWatch

---

> 🙏 **Submitted by**: Masudur Rahman  
> 📧 mrahman021992@gmail.com | 📱 0171234567  
> 🔗 *Git Repository: [Insert Your Repo Link Here]*

---

✅ **Submission Checklist**:
- [ ] 3 EC2 instances running with proper tags
- [ ] MongoDB installed & accessible from backend private IP
- [ ] FastAPI backend running on port 9000
- [ ] Frontend running on port 8000 (presentation instance)
- [ ] Nginx configured: `/` → frontend, `/api/` → backend
- [ ] Security Groups configured with least privilege
- [ ] Screenshots captured for each layer + end-to-end test
- [ ] Application accessible via public Nginx IP
- [ ] README complete with setup, config, screenshots, access results
- [ ] Git repository link added and accessible

---

> 💡 **Bangla Note **(Masudur Bhai):  
> *Bhai, assignment-er shob requirement ekhane cover kora hoyeche:*  
> ✅ *3 ta EC2 instance - presentation, application, data layer*  
> ✅ *Nginx port 80-e click korle frontend `(10.0.10.230:8000)` load hobe*  
> ✅ *`/api/` route e request backend `(10.0.1.226:9000)`-e jabe*  
> ✅ *MongoDB setup script step-by-step deowa ache*  
> ✅ *Security group rules private IP based - production ready approach*  
>   
> *Submission-er age:*  
> 1. *Sob screenshot nia niben (mongod status, uvicorn log, nginx test, browser load)*  
> 2. *README-e `[Your Git Repo Link Here]` replace kore actual link diben*  
> 3. *Public IP gulo screenshot-e blur kore diben jodi sensitive hoy*  
>   
> *InshaAllah full marks paben! 🚀 Best of luck!*

---

*Last Updated: $(date)*  
*Response ID: #3TIER-AWS-EC2-FINAL-README-003*
