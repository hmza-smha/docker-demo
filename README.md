# Docker Demo Project

>  The Core Problem Docker Solves >> README_2.md

This project demonstrates how to containerize and run multiple FastAPI applications using Docker and Docker Compose.

---

## 📋 Project Overview

This is a microservices architecture with two independent FastAPI applications:
- **App1**: User Service - Manages user data
- **App2**: Product Service - Manages product data

Both applications run in separate Docker containers and can be managed together using Docker Compose.

---

## �📁 Project Structure

```
docker-demo/
├── app1/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── app2/
│   ├── main.py
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

### Files Description

#### **Dockerfile** (app1/)
```dockerfile
# Use Python 3.11 as the base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app1

# Copy requirements file to the container
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Copy all application files to the container
COPY . .

# Run the FastAPI application using Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
```

**What each line does:**
| Command | Purpose |
|---------|---------|
| `FROM python:3.11` | Uses Python 3.11 as the base operating system for the container |
| `WORKDIR /app1` | Creates and sets the working directory inside container |
| `COPY requirements.txt .` | Copies dependencies file from your computer to container |
| `RUN pip install -r requirements.txt` | Installs all Python packages listed in requirements.txt |
| `COPY . .` | Copies all application code to the container |
| `CMD [...]` | Starts the FastAPI server when container runs |

---

#### **requirements.txt** (app1/)
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
```

Lists all Python dependencies needed for the application.

---

#### **main.py** (app1/)
The FastAPI application that handles user-related endpoints:
- `GET /` - Welcome message
- `GET /users/{user_id}` - Get a specific user
- `POST /users` - Create a new user
- `GET /health` - Health check endpoint

---

#### **docker-compose.yml**
```yaml
version: '3.8'
services:
  app1:
    build: ./app1
    ports:
      - "8001:8001"
    volumes:
      - ./app1:/app1
  app2:
    build: ./app2
    ports:
      - "8002:8002"
    volumes:
      - ./app2:/app2
```

**Configuration breakdown:**

| Section | Purpose |
|---------|---------|
| `version: '3.8'` | Docker Compose file format version |
| `services:` | Defines containers to run |
| `app1:/app2:` | Service names (can have multiple) |
| `build: ./app1` | Tells Docker to build from Dockerfile in app1 directory |
| `ports: - "8001:8001"` | Maps port 8001 on host to port 8001 in container |
| `volumes: - ./app1:/app1` | **Live code sync** - syncs local app1 folder with /app1 in container |

---

## 🐳 Docker Fundamentals

### What is Docker?
Docker is a containerization technology that packages your application with all its dependencies into a single unit called a **container**.

**Benefits:**
- ✅ Works the same on any computer
- ✅ No "works on my machine" problems
- ✅ Easy to scale and manage
- ✅ Lightweight (smaller than virtual machines)

### Images vs Containers
- **Image**: Blueprint (like a template) - created from Dockerfile
- **Container**: Running instance of an image (like a running process)

---

## 🚀 Commands Used & What They Do

### 1. **Build Docker Image**
```bash
docker build -t app1:latest app1/
```

**Breakdown:**
- `docker build` - Creates a Docker image
- `-t app1:latest` - Tags (names) the image as "app1" with version "latest"
- `app1/` - Build using Dockerfile in app1 directory

**What happens:**
1. Reads the Dockerfile
2. Downloads Python 3.11 base image
3. Installs dependencies
4. Copies your code
5. Creates a reusable image

**Output:** An image ready to run

---

### 2. **Run Single Container**
```bash
docker run -p 8001:8001 app1:latest
```

**Breakdown:**
- `docker run` - Creates and starts a container from an image
- `-p 8001:8001` - Maps port 8001 (host:container)
- `app1:latest` - Uses the app1 image created earlier

**What happens:**
1. Creates a new container from the image
2. Forwards port 8001 to your computer
3. Starts the FastAPI server

**Access at:** http://localhost:8001

---

### 3. **Docker Compose Up** (Recommended)
```bash
docker compose up
```

**Breakdown:**
- Reads `docker-compose.yml`
- Builds images (if not already built with `--build`)
- Starts all services (app1 and app2)
- Runs in **foreground** (shows logs)

**What happens:**
- Both containers start
- App1 runs on port 8001
- App2 runs on port 8002
- Both with live code sync enabled

**Access:**
- App1: http://localhost:8001
- App2: http://localhost:8002

---

### 4. **Docker Compose Down**
```bash
docker compose down
```

**What happens:**
- Stops all running containers
- Removes containers (but keeps images)
- Frees up ports

**Use when:** You want to clean up and restart

---

### 5. **Docker Compose Build**
```bash
docker compose build --no-cache
```

**Breakdown:**
- Rebuilds images from docker-compose.yml
- `--no-cache` - Rebuilds from scratch (ignores previous builds)

**Use when:** You've changed dependencies or want a fresh build

---

### 6. **Full Restart (Clean)**
```bash
docker compose down
docker system prune -f
docker compose up --build
```

**Breakdown:**
- `docker compose down` - Stops all containers
- `docker system prune -f` - Removes unused images/containers/networks
- `docker compose up --build` - Rebuilds and starts everything fresh

**Use when:** Something is broken or you want a completely fresh start

---

### 7. **View Logs**
```bash
docker compose logs app1
```

**Purpose:** See what's happening inside the app1 container - useful for debugging

---

### 8. **Check Running Containers**
```bash
docker ps
```

**Shows:** All currently running containers with their ports and status

---

## 📦 Volumes Explained

### What are Volumes?
Volumes are **connections between your computer and the container** - they sync files in real-time.

### Docker Compose Volumes
```yaml
volumes:
  - ./app1:/app1
```

**Breakdown:**
- `./app1` - Your local folder on your computer
- `:/app1` - Folder inside the container
- `-` - Creates a link (sync) between them

### Why We Added Volumes

**During Development:**
```yaml
volumes:
  - ./app1:/app1
  - ./app2:/app2
```

**Benefits:**
1. **Live Code Reloading** - Change code → Container detects change → Server reloads automatically
2. **No Rebuild Needed** - Don't have to rebuild image every time you edit code
3. **Faster Development** - See changes instantly (seconds, not minutes)
4. **Debugging** - Easier to test and debug

**How it works:**
1. You edit `main.py` locally
2. The change syncs to `/app1/main.py` inside container
3. Uvicorn (with `--reload` flag) detects the change
4. Server restarts automatically
5. Refresh browser to see changes

### Volume Diagram
```
Your Computer          Container
-----------            ---------
./app1/main.py  <----> /app1/main.py
./app1/...             /app1/...
```

---

## ⚙️ Advanced Docker Topics & Answered Questions

### Question 1: Why Are Commands in the Dockerfile in That Order?

**The order matters BECAUSE OF DOCKER CACHING AND EFFICIENCY!**

```dockerfile
FROM python:3.11          # 1. Start base image
WORKDIR /app1             # 2. Create working directory
COPY requirements.txt .   # 3. Copy only dependencies FIRST
RUN pip install -r requirements.txt  # 4. Install packages
COPY . .                  # 5. Copy application code LAST
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]  # 6. Run app
```

**Why This Order:**

| Step | Why |
|------|-----|
| `FROM` first | Base image must come first (like setting up OS) |
| `WORKDIR` | Organize files and set starting point |
| `COPY requirements.txt` | Dependencies change less frequently |
| `RUN pip install` | Only reinstalls if requirements.txt changes |
| `COPY . .` | Application code changes frequently |
| `CMD` last | Execution instruction goes at the end |

**Docker Caching Example:**

```
Build 1: ./app1/main.py is changed
├─ FROM python:3.11 ✅ (cached - reuse from before)
├─ WORKDIR /app1 ✅ (cached)
├─ COPY requirements.txt . ✅ (cached - file unchanged)
├─ RUN pip install ✅ (cached - requirements unchanged)
├─ COPY . . ❌ (NOT cached - main.py changed - rebuild from here)
└─ CMD [...] ❌ (rebuilt)

Build 2: Only requirements.txt is changed
├─ FROM python:3.11 ✅ (cached)
├─ WORKDIR /app1 ✅ (cached)
├─ COPY requirements.txt . ❌ (NOT cached - file changed - rebuild from here)
├─ RUN pip install ❌ (rebuilt)
├─ COPY . . ❌ (rebuilt)
└─ CMD [...] ❌ (rebuilt)
```

**The Rule:** Put things that change **less frequently FIRST**, things that change **more frequently LAST**. This way Docker reuses cached layers and builds faster!

---

### Question 2: What Does ':latest' Mean? Can We Have Versions?

**`:latest` is a TAG - it's just a label/name for your image.**

#### Understanding Image Names

```
app1:latest
 │   │
 │   └─ TAG (version/label)
 └──── IMAGE NAME (app name)
```

**You can use ANY tag name you want:**

```bash
# These all work:
docker build -t app1:latest app1/
docker build -t app1:1.0 app1/
docker build -t app1:1.0.1 app1/
docker build -t app1:production app1/
docker build -t app1:development app1/
docker build -t app1:stable app1/
docker build -t mycompany/app1:v2.1.4 app1/
```

#### Why `:latest`?

- **`latest` is the default** - If you don't specify a tag, Docker assumes you mean `latest`
- **Automatic reference** - `docker run app1` is same as `docker run app1:latest`
- **Convention** - Most projects use it for the most recent stable version

#### Real-World Versioning Strategies

**Strategy 1: Semantic Versioning**
```bash
docker build -t app1:1.0.0 app1/
docker build -t app1:1.0.1 app1/
docker build -t app1:1.1.0 app1/
docker build -t app1:2.0.0 app1/
```

**Strategy 2: Date-Based**
```bash
docker build -t app1:2025-03-30 app1/
docker build -t app1:2025-03-31 app1/
```

**Strategy 3: Build Numbers**
```bash
docker build -t app1:build-100 app1/
docker build -t app1:build-101 app1/
```

**Strategy 4: Environment Names**
```bash
docker build -t app1:dev app1/
docker build -t app1:staging app1/
docker build -t app1:production app1/
```

**Strategy 5: Git Commit SHA**
```bash
docker build -t app1:abc123def456 app1/
```

#### Tag Multiple Versions at Once

You can tag the same image with multiple tags:

```bash
docker build -t app1:1.0.0 -t app1:latest app1/
```

Now `docker run app1:1.0.0` and `docker run app1:latest` both work (same image)!

---

### Question 3: How to Run Different Versions?

#### Running Specific Versions

```bash
# Run version 1.0
docker run -p 8001:8001 app1:1.0

# Run version 2.0
docker run -p 8001:8001 app1:2.0

# Run production version
docker run -p 8001:8001 app1:production

# Run latest (default)
docker run -p 8001:8001 app1:latest

# Or just (without tag = automatically :latest)
docker run -p 8001:8001 app1
```

#### Using Versions in docker-compose.yml

```yaml
version: '3.8'
services:
  app1:
    image: app1:1.0          # Run app1 version 1.0
    ports:
      - "8001:8001"

  app2:
    image: app2:2.0          # Run app2 version 2.0
    ports:
      - "8002:8002"
```

Then run:
```bash
docker compose up
```

#### Real-World Example: Blue-Green Deployment

```yaml
version: '3.8'
services:
  # Old version (Blue)
  app1-blue:
    image: app1:1.0
    ports:
      - "8001:8001"

  # New version (Green)
  app1-green:
    image: app1:2.0
    ports:
      - "8003:8001"
```

Test both versions simultaneously, then switch traffic to the new one!

---

### Question 4: What if We Don't Have '--reload'? Manual Building!

**The `--reload` flag is FOR DEVELOPMENT ONLY.** It auto-restarts the server when code changes. In production, we DON'T want this!

#### Current Dockerfile (with --reload)
```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
```

**This is for development only!** The server restarts every time you change code.

#### Production Dockerfile (without --reload)
```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

Without `--reload`, code changes are NOT reflected automatically!

#### How to Build and Run Without live Reload

**Step 1: Modify the Dockerfile to remove `--reload`**

```dockerfile
# Use Python 3.11 as the base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app1

# Copy requirements file to the container
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Copy all application files to the container
COPY . .

# Run app WITHOUT auto-reload (production mode)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

**Step 2: Build the image**
```bash
docker build -t app1:production app1/
```

**Step 3: Run it**
```bash
docker run -p 8001:8001 app1:production
```

#### Workflow WITHOUT --reload

**Step 1: Make code change locally**
- Edit `app1/main.py`
- Save file

**Step 2: Rebuild the image**
```bash
docker build -t app1:production app1/
```
*(This takes 10-30 seconds)*

**Step 3: Stop old container**
```bash
docker stop <container_id>
```

Or stop everything:
```bash
docker compose down
```

**Step 4: Run new version**
```bash
docker run -p 8001:8001 app1:production
```

Or with docker-compose:
```bash
docker compose up
```

**Step 5: Refresh browser**
- See your new changes

#### Why NO --reload in Production?

| Feature | Development | Production |
|---------|-------------|-----------|
| `--reload` | ✅ YES | ❌ NO |
| Auto-restart on code change | ✅ Fast development | ❌ Waste of resources |
| Performance | Slower | ✅ Faster & Stable |
| Security | Not important | ✅ Must be secure |
| Stability | Can restart | ❌ Every change restarts = downtime |

#### Complete Comparison: Development vs Production

**Development Dockerfile (with --reload)**
```dockerfile
FROM python:3.11
WORKDIR /app1
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
```

**Production Dockerfile (without --reload)**
```dockerfile
FROM python:3.11
WORKDIR /app1
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

**Development docker-compose.yml (with volumes)**
```yaml
version: '3.8'
services:
  app1:
    build: ./app1
    ports:
      - "8001:8001"
    volumes:
      - ./app1:/app1    # Live sync - code changes reflected instantly
```

**Production docker-compose.yml (no volumes)**
```yaml
version: '3.8'
services:
  app1:
    image: app1:1.0    # Don't build, use pre-built image
    ports:
      - "8001:8001"
    # NO volumes - immutable container
```

#### Quick Comparison Table

| Task | With `--reload` | Without `--reload` |
|------|-----------------|-------------------|
| Edit code | 1-2 seconds to see changes | Need to rebuild & restart |
| Performance | Slower | ✅ Faster |
| Best for | Development | Production |
| File syncing | Needs volumes | Not needed |
| Typical use | Local testing | Live servers |

---

## 🔄 Development Workflow

### Step 1: Initial Setup
```bash
docker compose up
```
First time takes longer (building images)

### Step 2: Make Code Changes
Edit `app1/main.py` or `app2/main.py` in your editor

### Step 3: Instant Reload
- Save file
- Wait 1-2 seconds (Uvicorn reloads)
- Refresh browser
- See changes immediately

### Step 4: View Logs (if troubleshooting)
```bash
docker compose logs app1
```

### Step 5: Stop When Done
```bash
docker compose down
```

---

## 🛠️ Troubleshooting

### Issue: "Port already in use"
**Solution:** Stop existing containers
```bash
docker compose down
```

Or change the port in `docker-compose.yml`:
```yaml
ports:
  - "9001:8001"  # Use 9001 instead
```

---

### Issue: Code changes not reflected
**Solution:** Either rebuild or ensure volumes are properly set up
```bash
docker compose down
docker compose up --build
```

Or verify volume mount exists:
```bash
docker compose exec app1 ls -la /app1
```

---

### Issue: "docker compose" command not found
**Solution:** Install Docker Compose
```bash
sudo apt-get update && sudo apt-get install -y docker-compose-plugin
```

---

### Issue: Can't access http://localhost:8001
**Solutions:**
1. Verify container is running: `docker ps`
2. Check logs: `docker compose logs app1`
3. Verify correct port in browser
4. Try: `docker compose down && docker compose up --build`

---

## 📊 Summary Table

| Task | Command | Time |
|------|---------|------|
| Start containers | `docker compose up` | Seconds |
| Stop containers | `docker compose down` | Seconds |
| Rebuild from scratch | `docker compose down && docker system prune -f && docker compose up --build` | ~30 seconds |
| View logs | `docker compose logs app1` | Instant |
| Check running containers | `docker ps` | Instant |

---

## 🔗 API Endpoints

### App1 - User Service (Port 8001)
- `GET http://localhost:8001/` - Welcome message
- `GET http://localhost:8001/users/123` - Get user by ID
- `POST http://localhost:8001/users` - Create new user
- `GET http://localhost:8001/health` - Health check
- `GET http://localhost:8001/docs` - **API Documentation (Swagger UI)**

### App2 - Product Service (Port 8002)
- `GET http://localhost:8002/` - Welcome message
- `GET http://localhost:8002/products/1` - Get product by ID
- `GET http://localhost:8002/products` - List all products
- `POST http://localhost:8002/products` - Create new product
- `GET http://localhost:8002/health` - Health check
- `GET http://localhost:8002/docs` - **API Documentation (Swagger UI)**

---

## 💡 Key Learning Points

1. **Dockerfile** = Recipe for building an image
2. **Docker Image** = Packaged application (like an .exe)
3. **Container** = Running instance of an image
4. **docker-compose.yml** = Configuration to run multiple containers together
5. **Volumes** = Real-time file sync between your computer and container
6. **Ports** = Map computer ports to container ports (host:container)
7. **--reload** = Auto-restart server when code changes (development feature)

---

## 📚 Next Steps

1. **Experiment with code changes** - Edit main.py and see live reloading
2. **Call the APIs** - Use `http://localhost:8001/docs` for interactive testing
3. **Check logs** - Use `docker compose logs app1` to understand what's happening
4. **Scale up** - Add more microservices by creating more app folders and updating docker-compose.yml
5. **Production Setup** - Remove `--reload`, add security headers, use environment variables

---

**Happy Docker learning! 🐳**
