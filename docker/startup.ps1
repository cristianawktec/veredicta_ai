# Veredicta Docker Startup Script
# Execute this in a fresh PowerShell terminal to start the services

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Veredicta AI - Docker Startup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to docker directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $scriptDir

Write-Host "[1/6] Stopping any existing containers..." -ForegroundColor Yellow
docker compose --project-name veredicta-ai down 2>$null | Out-Null
Start-Sleep -Seconds 2

Write-Host "[2/6] Cleaning up old images..." -ForegroundColor Yellow
docker system prune -af --volumes 2>$null | Out-Null
Start-Sleep -Seconds 2

Write-Host "[3/6] Building images (log: build.log)..." -ForegroundColor Yellow
$buildLog = Join-Path $scriptDir "build.log"
docker compose --progress plain --project-name veredicta-ai build 2>&1 | Tee-Object -FilePath $buildLog | Out-Host

Write-Host "[4/6] Starting services..." -ForegroundColor Yellow
docker compose --project-name veredicta-ai up -d
Start-Sleep -Seconds 20

Write-Host "[5/6] Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

Write-Host "[6/6] Checking container status..." -ForegroundColor Yellow
Write-Host ""
docker compose --project-name veredicta-ai ps
Write-Host ""

# Test API health
Write-Host "Testing API health endpoint..." -ForegroundColor Yellow
$maxAttempts = 10
$apiHealthy = $false

for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:8011/health" -ErrorAction Stop -TimeoutSec 2
        if ($response.StatusCode -eq 200) {
            Write-Host "API is responding." -ForegroundColor Green
            Write-Host ""
            Write-Host "Response:" -ForegroundColor Cyan
            $response.Content | ConvertFrom-Json | Format-List
            $apiHealthy = $true
            break
        }
    } catch {
        # API not ready yet
    }

    if ($attempt -lt $maxAttempts) {
        Write-Host "  Attempt $attempt/$maxAttempts - waiting for API..." -ForegroundColor DarkYellow
        Start-Sleep -Seconds 3
    }
}

if (-not $apiHealthy) {
    Write-Host "API is not responding after $maxAttempts attempts" -ForegroundColor Red
    Write-Host ""
    Write-Host "Checking container logs:" -ForegroundColor Yellow
    docker compose --project-name veredicta-ai logs --tail 20
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Startup complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "API URL:     http://127.0.0.1:8011" -ForegroundColor Cyan
Write-Host "Health:      http://127.0.0.1:8011/health" -ForegroundColor Cyan
Write-Host "Upload:      POST http://127.0.0.1:8011/upload" -ForegroundColor Cyan
Write-Host ""

Pop-Location
