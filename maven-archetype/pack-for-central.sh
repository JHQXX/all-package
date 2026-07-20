#!/bin/bash
# 打包 springai-agent-archetype 为 Sonatype Central Portal 要求的 zip

set -e

GROUP_PATH="io/github/jhqxx"
ARTIFACT_ID="springai-agent-archetype"
VERSION="1.0.0"
TARGET_DIR="/Users/lizhi/projects/all-package/maven-archetype/target"
PACK_BASE="/tmp/central-publish"
PACK_DIR="${PACK_BASE}/${GROUP_PATH}/${ARTIFACT_ID}/${VERSION}"

echo "🧹 清理旧目录..."
rm -rf "${PACK_BASE}"
mkdir -p "${PACK_DIR}"

echo "📦 复制文件..."

# 用 find 直接拷贝
find "${TARGET_DIR}" -maxdepth 1 \( \
    -name "${ARTIFACT_ID}-${VERSION}" -o \
    -name "${ARTIFACT_ID}-${VERSION}.*" \
\) -type f -exec cp {} "${PACK_DIR}/" \;

echo ""
echo "📂 生成的文件结构："
find "${PACK_DIR}" -type f | sort
echo ""

cd "${PACK_BASE}"
echo "🗜️  打包 zip..."
zip -r "central-bundle.zip" io/ > /dev/null
echo "  ✅ 生成: ${PACK_BASE}/central-bundle.zip"
ls -lh "${PACK_BASE}/central-bundle.zip"

echo ""
echo "✨ 完成！可以上传到:"
echo "   https://central.sonatype.com/publishing"
