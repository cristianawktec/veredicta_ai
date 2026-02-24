# Quick Start - Veredicta AI

## 🚀 Start Services (Choose an option)

### Option 1: Using the Startup Script (Fácil)

**Windows (PowerShell):**
```powershell
cd C:\xampp\htdocs\Veredicta\docker
.\startup.ps1
```

**Windows (CMD):**
```cmd
cd C:\xampp\htdocs\Veredicta\docker
startup.bat
```

This script will:
1. Stop any existing containers
2. Clean up old images
3. Build and start fresh services
4. Wait 60 seconds for startup
5. Show container status
6. Test the API health endpoint

---

### Option 2: Manual Commands

**Open a NEW PowerShell terminal and run:**

```powershell
# Navigate to docker directory
cd C:\xampp\htdocs\Veredicta\docker

# Stop existing services
docker compose --project-name veredicta-ai down

# Start services
docker compose --project-name veredicta-ai up -d

# Wait for services to initialize
Start-Sleep -Seconds 60

# Check status
docker compose --project-name veredicta-ai ps

# Test health endpoint
Invoke-WebRequest -Uri http://127.0.0.1:8011/health
```

---

## ✅ Expected Output

After startup, you should see:
```
NAME                               IMAGE                      STATUS     PORTS
veredicta-ai-backend-1            veredicta-ai-backend:latest  Up 30s     127.0.0.1:8011->8000/tcp
veredicta-ai-postgres-1           pgvector/pgvector:pg16       Up 30s     5432/tcp
```

And API response:
```json
{
  "status": "ok",
  "service": "veredicta-ai"
}
```

---

## 📍 Access URLs

- **API Base:** `http://127.0.0.1:8011`
- **Health Check:** `http://127.0.0.1:8011/health`
- **Metrics:** `http://127.0.0.1:8011/metrics`

---

## 🔧 Troubleshooting

### API not responding

**Symptom:** Connection refused on http://127.0.0.1:8011

**Solutions:**

```powershell
# Check if containers are running
docker ps

# If containers don't exist, rebuild
cd C:\xampp\htdocs\Veredicta\docker
docker compose --project-name veredicta-ai up -d --build

# View logs to see errors
docker compose --project-name veredicta-ai logs backend
docker compose --project-name veredicta-ai logs postgres
```

### Port already in use

If port 8011 is already in use, edit `.env`:
```
VEREDICTA_API_PORT=8012  # Change to another port
```

Then restart:
```powershell
docker compose --project-name veredicta-ai up -d --build
```

### Containers won't start

```powershell
# Clean everything and start fresh
cd C:\xampp\htdocs\Veredicta\docker
docker compose --project-name veredicta-ai down -v  # Remove volumes
docker system prune -af --volumes
docker compose --project-name veredicta-ai up -d --build
```

### Port conflicts with existing services

This project is isolated:
- **Veredicta:** Port 8011 (configurable in `.env`)
- **Existing CRM:** Port 8000, 8001, 5432 not affected
- **Database:** Internal-only, no host port exposure

---

## 📝 Testing the System

### 1. Check Health
```bash
curl http://127.0.0.1:8011/health
# or in PowerShell
(Invoke-WebRequest -Uri http://127.0.0.1:8011/health).Content
```

### 2. Upload a PDF
```powershell
$file = Get-Item "C:\path\to\your\file.pdf"
$form = @{
    file = $file
    document_type = "contract"
}

$response = Invoke-WebRequest -Uri "http://127.0.0.1:8011/upload" `
    -Method Post `
    -Form $form

$response.Content | ConvertFrom-Json | Format-List
```

---

## 🛑 Stop Services

```powershell
cd C:\xampp\htdocs\Veredicta\docker
docker compose --project-name veredicta-ai down
```

---

## Environment Variables

Key variables in `.env`:

- `VEREDICTA_API_PORT`: API port (default: 8011)
- `OPENAI_API_KEY`: OpenAI API key for embeddings
- `POSTGRES_PASSWORD`: Database password
- `CHUNK_SIZE`: PDF chunk size (default: 1200)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)

Edit `.env` and restart services for changes to take effect.

