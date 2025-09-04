# Установка FFmpeg для Windows
Write-Host "========================================" -ForegroundColor Green
Write-Host "Установка FFmpeg для Windows" -ForegroundColor Green  
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Проверяем права администратора
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ВНИМАНИЕ: Скрипт запущен без прав администратора" -ForegroundColor Yellow
    Write-Host "Для автоматического добавления в PATH нужны права администратора" -ForegroundColor Yellow
    Write-Host ""
}

# Создаем папку для FFmpeg
$ffmpegPath = "C:\ffmpeg"
Write-Host "Создаем папку $ffmpegPath..." -ForegroundColor Cyan

if (-not (Test-Path $ffmpegPath)) {
    New-Item -ItemType Directory -Path $ffmpegPath -Force | Out-Null
}

Set-Location $ffmpegPath

# Скачиваем FFmpeg
Write-Host ""
Write-Host "Скачиваем FFmpeg (это может занять несколько минут)..." -ForegroundColor Cyan
$url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$zipFile = "ffmpeg.zip"

try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $url -OutFile $zipFile -UseBasicParsing
    Write-Host "✓ Скачивание завершено" -ForegroundColor Green
} catch {
    Write-Host "ОШИБКА: Не удалось скачать FFmpeg" -ForegroundColor Red
    Write-Host "Попробуйте скачать вручную с https://ffmpeg.org/download.html#build-windows" -ForegroundColor Yellow
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

# Извлекаем архив
Write-Host ""
Write-Host "Извлекаем архив..." -ForegroundColor Cyan
try {
    Expand-Archive -Path $zipFile -DestinationPath "." -Force
    Write-Host "✓ Архив извлечен" -ForegroundColor Green
} catch {
    Write-Host "ОШИБКА: Не удалось извлечь архив" -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

# Перемещаем файлы
Write-Host ""
Write-Host "Настраиваем файлы..." -ForegroundColor Cyan
$ffmpegFolder = Get-ChildItem -Directory -Name "ffmpeg-*" | Select-Object -First 1
if ($ffmpegFolder) {
    Copy-Item "$ffmpegFolder\bin\*" -Destination "." -Force
    Remove-Item $ffmpegFolder -Recurse -Force
    Write-Host "✓ Файлы настроены" -ForegroundColor Green
}

# Очищаем временные файлы
Remove-Item $zipFile -Force

# Проверяем установку
Write-Host ""
Write-Host "Проверяем установку..." -ForegroundColor Cyan
try {
    $version = & "$ffmpegPath\ffmpeg.exe" -version 2>$null
    if ($version) {
        Write-Host "✓ FFmpeg успешно установлен!" -ForegroundColor Green
        Write-Host ($version -split "`n")[0] -ForegroundColor Gray
    }
} catch {
    Write-Host "FFmpeg установлен, но не найден в PATH" -ForegroundColor Yellow
}

# Добавляем в PATH
Write-Host ""
Write-Host "Добавляем FFmpeg в PATH..." -ForegroundColor Cyan

$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($currentPath -notlike "*$ffmpegPath*") {
    try {
        [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$ffmpegPath", "User")
        Write-Host "✓ FFmpeg добавлен в PATH пользователя" -ForegroundColor Green
        Write-Host "Перезапустите командную строку для применения изменений" -ForegroundColor Yellow
    } catch {
        Write-Host "Не удалось автоматически добавить в PATH" -ForegroundColor Yellow
        Write-Host "Добавьте вручную $ffmpegPath в переменную PATH" -ForegroundColor Yellow
    }
} else {
    Write-Host "✓ FFmpeg уже в PATH" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Установка завершена!" -ForegroundColor Green
Write-Host "FFmpeg установлен в: $ffmpegPath" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Тестируем в новой сессии
Write-Host "Тестируем FFmpeg..." -ForegroundColor Cyan
$env:PATH += ";$ffmpegPath"
try {
    $testResult = & ffmpeg -version 2>$null
    if ($testResult) {
        Write-Host "✓ FFmpeg работает!" -ForegroundColor Green
    }
} catch {
    Write-Host "Для использования FFmpeg перезапустите командную строку" -ForegroundColor Yellow
}

Read-Host "Нажмите Enter для завершения"
