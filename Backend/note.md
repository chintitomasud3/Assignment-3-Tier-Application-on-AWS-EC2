তোমার FastAPI + MongoDB app টা রান করাতে গেলে ৩টা জিনিস ঠিকভাবে setup করতে হবে:

1. **MongoDB Server setup**
2. **Python FastAPI environment**
3. **Network / deployment (IP access + port)**

আমি step-by-step clean করে দিচ্ছি 👇

---

# 🧱 1. MongoDB Setup (Most important)

তোমার code এ আছে:

```python
MONGO_URL = "mongodb://10.0.13.224:27017"
```

এটার মানে:
👉 MongoDB অন্য server (10.0.13.224) এ চলছে

### ✅ সেই server এ MongoDB setup করতে হবে:

#### Install MongoDB

```bash
sudo apt update
sudo apt install -y mongodb-org
```

#### Start MongoDB

```bash
sudo systemctl start mongod
sudo systemctl enable mongod
```

---

## 🌐 Remote access enable (IMPORTANT)

`/etc/mongod.conf` এ change করো:

```yaml
net:
  port: 27017
  bindIp: 0.0.0.0
```

তারপর restart:

```bash
sudo systemctl restart mongod
```

---

## 🔥 Firewall (EC2 / VPS হলে)

```bash
sudo ufw allow 27017
```

⚠️ Better practice:
👉 IP restrict করা (10.0.0.x only allow)

---

# 🐍 2. FastAPI setup (App server)

### Install Python + venv

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

---

### Project setup

```bash
mkdir fastapi-app
cd fastapi-app
python3 -m venv venv
source venv/bin/activate
```

---

### Install dependencies

```bash
pip install fastapi uvicorn motor pydantic
```

---

### Run app

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

# 🌍 3. Network / Access setup

## 🔹 If local test:

```
http://127.0.0.1:8000
```

## 🔹 If server:

```
http://YOUR_SERVER_IP:8000
```

---

# 🔥 4. Production setup (IMPORTANT upgrade)

## Option A: run with PM2 (simple)

```bash
npm install -g pm2
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000"
```

---

## Option B: Nginx reverse proxy (best)

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

# ⚠️ 5. Common problems (তোমার ক্ষেত্রে important)

## ❌ MongoDB connect fail

✔ check:

* bindIp = 0.0.0.0
* port 27017 open
* correct IP (10.0.13.224 reachable)

---

## ❌ CORS issue

তুমি already ঠিক করছো:

```python
allow_origins=["*"]
```

---

## ❌ ObjectId error

Install bson comes with motor, but ensure:

```bash
pip install pymongo
```

---

# 🧠 Architecture summary

```
Browser
   ↓
FastAPI (8000)
   ↓
MongoDB (27017 on 10.0.13.224)
```

---

# 🚀 Recommended production upgrade (important)

* MongoDB auth enable (username/password)
* IP whitelist (not open 0.0.0.0)
* Nginx reverse proxy
* HTTPS (Let’s Encrypt)

---

যদি চাও, আমি তোমার জন্য next step এ:

👉 **full AWS EC2 production architecture (FastAPI + MongoDB + Nginx + SSL + PM2)**

একদম real industry setup বানিয়ে দিতে পারি।
