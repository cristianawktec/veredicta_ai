@echo off
REM Veredicta Docker Startup Script (Batch version)

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Veredicta AI - Docker Startup (Batch)
echo ========================================
echo.

pushd "%~dp0"

echo [1/5] Stopping existing containers...
docker compose --project-name veredicta-ai down

echo [2/5] Cleaning up images and volumes...
docker system prune -af --volumes

echo [3/5] Building and starting services...
docker compose --project-name veredicta-ai up -d

echo [4/5] Waiting for services (60 seconds)...
timeout /t 60 /nobreak

echo [5/5] Container status:
echo.
docker compose --project-name veredicta-ai ps

echo.
echo Checking API health...
powershell -NoProfile -Command "try { $r = Invoke-WebRequest -Uri 'http://127.0.0.1:8011/health' -ErrorAction Stop -TimeoutSec 2; if ($r.StatusCode -eq 200) { Write-Host 'API is RUNNING!' -ForegroundColor Green; Write-Host $r.Content } } catch { Write-Host 'API not responding yet' -ForegroundColor Yellow }"

echo.
echo ========================================
echo Setup Complete - Check status above
echo ========================================
echo API URL: http://127.0.0.1:8011
echo.

popd
pause
