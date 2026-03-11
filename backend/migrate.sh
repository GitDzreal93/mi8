#!/bin/bash

# Backend Refactoring Migration Script
# This script helps migrate from the old structure to the new one

set -e

echo "🔄 MI8 Backend Refactoring Migration Script"
echo "=============================================="
echo ""

# Step 1: Backup current code
echo "📦 Step 1: Creating backup..."
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Copy important files
cp -r app/models.py "$BACKUP_DIR/" 2>/dev/null || true
cp -r app/schemas.py "$BACKUP_DIR/" 2>/dev/null || true
cp -r app/db.py "$BACKUP_DIR/" 2>/dev/null || true
cp -r app/config.py "$BACKUP_DIR/" 2>/dev/null || true
cp -r app/services "$BACKUP_DIR/" 2>/dev/null || true
cp -r app/api "$BACKUP_DIR/" 2>/dev/null || true
cp -r app/main.py "$BACKUP_DIR/" 2>/dev/null || true

echo "✅ Backup created: $BACKUP_DIR"
echo ""

# Step 2: Show what needs to be migrated
echo "📋 Step 2: Files to migrate:"
echo ""
echo "From → To"
echo "------------------------"
echo "models.py → models/database.py"
echo "schemas.py → schemas/event.py, source.py, alert.py, common.py"
echo "db.py → core/database.py"
echo "config.py → core/config.py"
echo "services/auth.py → core/security.py"
echo "services/alerts.py → services/alert_service.py"
echo "services/deepseek.py → integrations/llm/deepseek.py"
echo "services/ingest/* → integrations/sources/*"
echo "services/scheduler.py → tasks/scheduler.py"
echo "services/quota.py → utils/quota.py"
echo "services/dedup.py → utils/dedup.py"
echo "services/source_health.py → services/source_service.py"
echo "api/routes/* → api/v1/*"
echo ""

# Step 3: Check what's been done
echo "✅ Step 3: Checking progress..."
echo ""

# Check if new structure exists
check_dir() {
    if [ -d "app/$1" ]; then
        echo "  ✅ app/$1"
        return 0
    else
        echo "  ❌ app/$1 (not created yet)"
        return 1
    fi
}

check_dir "core"
check_dir "models"
check_dir "schemas"
check_dir "api/v1"
check_dir "services"
check_dir "integrations/llm"
check_dir "integrations/sources"
check_dir "tasks"
check_dir "utils"

echo ""
echo "📝 Migration Status:"
echo ""
echo "✅ Completed:"
echo "  - New directory structure created"
echo "  - Core modules created (config, database, security, exceptions)"
echo "  - Model schemas created"
echo "  - API schemas created"
echo ""
echo "🚧 Pending:"
echo "  - Migrate API routes to api/v1/"
echo "  - Migrate services to new structure"
echo "  - Migrate integrations (LLM and sources)"
echo "  - Update all import statements"
echo "  - Run tests"
echo ""
echo "📖 See .docs/backend-refactoring.md for detailed documentation"
echo ""
