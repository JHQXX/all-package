#!/bin/bash
# 立即清理发布产物
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

rm -f central-bundle.zip public-key.asc .cleanup-at
# 同时清理 target/ 但保留 classes（如果有 IDE 缓存）
rm -rf target/

echo "✅ 已清理所有发布产物"
