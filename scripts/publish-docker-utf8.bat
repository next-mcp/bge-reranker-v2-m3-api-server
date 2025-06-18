@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM 配置
if "%DOCKER_USERNAME%"=="" set DOCKER_USERNAME=yarnovo
set IMAGE_NAME=%DOCKER_USERNAME%/bge-reranker-v2-m3-api-server

REM 从pyproject.toml读取版本号
echo [INFO] 从pyproject.toml读取版本号...
for /f "tokens=2 delims== " %%a in ('findstr /r "^version" pyproject.toml') do (
    set PYPROJECT_VERSION=%%a
    REM 移除引号
    set PYPROJECT_VERSION=!PYPROJECT_VERSION:"=!
)

REM 设置版本号优先级：1.命令行参数 2.pyproject.toml 3.latest
if not "%1"=="" (
    set VERSION=%1
    echo [INFO] 使用命令行参数版本号: %1
) else if not "!PYPROJECT_VERSION!"=="" (
    set VERSION=!PYPROJECT_VERSION!
    echo [INFO] 使用pyproject.toml版本号: !PYPROJECT_VERSION!
) else (
    set VERSION=latest
    echo [INFO] 使用默认版本号: latest
)

REM 检测版本号类型（正式版本 vs 预发布版本）
set IS_PRERELEASE=false
echo !VERSION! | findstr /r /c:"[0-9]*\.[0-9]*\.[0-9]*a[0-9]*" >nul && set IS_PRERELEASE=true
echo !VERSION! | findstr /r /c:"[0-9]*\.[0-9]*\.[0-9]*b[0-9]*" >nul && set IS_PRERELEASE=true
echo !VERSION! | findstr /r /c:"[0-9]*\.[0-9]*\.[0-9]*rc[0-9]*" >nul && set IS_PRERELEASE=true
echo !VERSION! | findstr /r /c:"[0-9]*\.[0-9]*\.[0-9]*alpha[0-9]*" >nul && set IS_PRERELEASE=true
echo !VERSION! | findstr /r /c:"[0-9]*\.[0-9]*\.[0-9]*beta[0-9]*" >nul && set IS_PRERELEASE=true
echo !VERSION! | findstr /r /c:"[0-9]*\.[0-9]*\.[0-9]*\.dev[0-9]*" >nul && set IS_PRERELEASE=true

if "!IS_PRERELEASE!"=="true" (
    echo [INFO] 检测到预发布版本: !VERSION! - 不会推送latest标签
    set SHOULD_TAG_LATEST=false
) else (
    echo [INFO] 检测到正式版本: !VERSION! - 将同时推送latest标签
    set SHOULD_TAG_LATEST=true
)

echo [START] 开始构建和发布Docker镜像...
echo 镜像名称: %IMAGE_NAME%
echo 版本标签: %VERSION%

REM 检查Docker Hub登录状态
echo [INFO] 验证Docker Hub登录状态...
REM 直接尝试Docker Hub API调用来检查认证状态
docker pull hello-world:latest >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Hub连接失败，请检查网络连接
    exit /b 1
)
echo [SUCCESS] Docker Hub连接正常，准备构建镜像...

REM 检查是否支持多平台构建
docker buildx version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  buildx不可用，使用单平台构建
    
    REM 单平台构建
    echo 🔨 构建AMD64镜像...
    docker build -t %IMAGE_NAME%:%VERSION% .
    if errorlevel 1 exit /b 1
    
    echo 📤 推送镜像...
    docker push %IMAGE_NAME%:%VERSION%
    if errorlevel 1 exit /b 1
    
    REM 根据版本类型决定是否推送latest标签
    if "!SHOULD_TAG_LATEST!"=="true" (
        if not "%VERSION%"=="latest" (
            echo 📤 推送latest标签...
            docker tag %IMAGE_NAME%:%VERSION% %IMAGE_NAME%:latest
            docker push %IMAGE_NAME%:latest
        )
    ) else (
        echo [INFO] 跳过latest标签推送（预发布版本）
    )
) else (
    echo 🔨 多平台构建中...
    
    REM 创建buildx构建器（如果不存在）
    docker buildx ls | findstr "multiplatform-builder" >nul
    if errorlevel 1 (
        docker buildx create --use --name multiplatform-builder
        docker buildx inspect --bootstrap
    ) else (
        docker buildx use multiplatform-builder
    )
    
    REM 多平台构建并推送
    set TAGS=-t %IMAGE_NAME%:%VERSION%
    if "!SHOULD_TAG_LATEST!"=="true" (
        if not "%VERSION%"=="latest" (
            echo [INFO] 添加latest标签到构建中...
            set TAGS=!TAGS! -t %IMAGE_NAME%:latest
        )
    ) else (
        echo [INFO] 跳过latest标签（预发布版本）
    )
    
    docker buildx build --platform linux/amd64,linux/arm64 !TAGS! --push .
    if errorlevel 1 exit /b 1
)

echo ✅ 镜像发布完成！
echo 📋 查看镜像信息：
echo    docker pull %IMAGE_NAME%:%VERSION%
echo    docker buildx imagetools inspect %IMAGE_NAME%:%VERSION% 