# Assignment-3-Tier-Application-on-AWS-EC2

# Database Setup


# 🧩 MongoDB Installation Guide

## 🔄 1. System Update

```bash
sudo apt-get update
```

---

## 📦 2. Add MongoDB Repository

```bash
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
```

---

## 🔑 3. Add GPG Key

```bash
sudo rm -f /usr/share/keyrings/mongodb-server-7.0.gpg

curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg
```

---

## 🔄 4. Update Package List Again

```bash
sudo apt update
```

---

## ⬆️ 5. Upgrade System (Optional but recommended)

```bash
sudo apt-get upgrade -y
```

---

## 📥 6. Install MongoDB

```bash
sudo apt install -y mongodb-org
```

---

## 🚀 7. Start MongoDB Service

```bash
sudo systemctl start mongod
```

---

## ✅ 8. Enable Auto Start

```bash
sudo systemctl enable mongod
```

---

## 📊 9. Check Status

```bash
sudo systemctl status mongod
```

---

## 🌐 10. Allow Remote Access 

### Config file edit:

```bash
sudo nano /etc/mongod.conf
```

### Change:

```yaml
bindIp: 127.0.0.1
```

### To:

```yaml
bindIp: 0.0.0.0
```

---

## 🔁 11. Restart MongoDB

```bash
sudo systemctl restart mongod
```

---

## 🧪 12. Test MongoDB Shell

```bash
mongosh
```

---

