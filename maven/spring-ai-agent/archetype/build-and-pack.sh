#!/bin/bash
# ============================================
# Maven Archetype 中央仓库打包脚本
# ============================================
# 位置: maven/spring-ai-agent/archetype/build-and-pack.sh
# 作用:
#   1. 在 archetype 目录执行 mvn clean verify
#   2. 在 archetype 目录内生成 central-bundle.zip
#   3. 在 24 小时后自动清理 zip 和 target/
# 用法:
#   bash build-and-pack.sh
# ============================================

set -e

# ========== 配置（可在此修改） ==========
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

GROUP_PATH="io/github/jhqxx"
ARTIFACT_ID="springai-agent-archetype"
VERSION="1.0.1"
OUTPUT_ZIP="central-bundle.zip"
PACK_DIR_NAME=".publish-pack"     # 临时目录，藏在 archetype 下
PACK_DIR="${SCRIPT_DIR}/${PACK_DIR_NAME}"
GPG_HOME="/tmp/gpg-home"

# 自动清理时间（秒）：24小时 = 86400
AUTO_CLEAN_SECONDS=86400

echo "=========================================="
echo "  📦 SpringAI Agent Archetype 中央仓库打包"
echo "=========================================="
echo "📁 工作目录: ${SCRIPT_DIR}"
echo "📦 输出文件: ${SCRIPT_DIR}/${OUTPUT_ZIP}"
echo "🧹 自动清理: ${AUTO_CLEAN_SECONDS}秒后（24小时）"
echo ""

# ========== 第 1 步：清理旧的 zip 和临时目录 ==========
echo "🧹 清理旧的输出..."
rm -rf "${OUTPUT_ZIP}" "${PACK_DIR}"

# ========== 第 2 步：构建（仅在本目录内） ==========
echo "🔨 执行 mvn clean verify -DskipTests..."
mvn clean verify -DskipTests -q

# ========== 第 3 步：补全 pom 的 md5/sha1 ==========
echo "🔐 生成 pom 系列校验和..."
cd "${SCRIPT_DIR}/target"
for base in "${ARTIFACT_ID}-${VERSION}.pom" "${ARTIFACT_ID}-${VERSION}.pom.asc"; do
    MD5=$(md5 -q "$base")
    SHA1=$(shasum -a 1 "$base" | awk '{print $1}')
    printf "%s" "$MD5" > "$base.md5"
    printf "%s" "$SHA1" > "$base.sha1"
done
cd "${SCRIPT_DIR}"

# ========== 第 4 步：按 Sonatype 要求的目录结构组织 ==========
echo "📂 组织目录结构..."
mkdir -p "${PACK_DIR}/${GROUP_PATH}/${ARTIFACT_ID}/${VERSION}"

# 复制所有需要的文件
find "${SCRIPT_DIR}/target" -maxdepth 1 -name "${ARTIFACT_ID}-${VERSION}*" -type f \
    -exec cp {} "${PACK_DIR}/${GROUP_PATH}/${ARTIFACT_ID}/${VERSION}/" \;

# 验证文件数量
FILE_COUNT=$(ls "${PACK_DIR}/${GROUP_PATH}/${ARTIFACT_ID}/${VERSION}/" | wc -l | tr -d ' ')
echo "📄 共复制 ${FILE_COUNT} 个文件"

if [ "$FILE_COUNT" -lt 12 ]; then
    echo "❌ 文件数量太少，请检查构建是否成功"
    exit 1
fi

# ========== 第 5 步：打包成 zip（输出到当前位置） ==========
echo "🗜️  打包 zip..."
cd "${PACK_DIR}"
zip -r "${SCRIPT_DIR}/${OUTPUT_ZIP}" "${GROUP_PATH%%/*}/" > /dev/null
cd "${SCRIPT_DIR}"

ZIP_SIZE=$(ls -lh "${OUTPUT_ZIP}" | awk '{print $5}')
echo "✅ 生成: ${OUTPUT_ZIP} (${ZIP_SIZE})"

# ========== 第 6 步：导出 GPG 公钥（备用） ==========
echo "🔑 导出 GPG 公钥..."
gpg --homedir "${GPG_HOME}" --armor --export 2733827845l@gmail.com > "${SCRIPT_DIR}/public-key.asc" 2>/dev/null || true

# ========== 第 7 步：清理临时目录 ==========
rm -rf "${PACK_DIR}"

# ========== 第 8 步：设置 24 小时后自动清理 ==========
CLEANUP_TIME=$(date "+%Y-%m-%d %H:%M:%S")
echo ""
echo "=========================================="
echo "  ✅ 打包完成！"
echo "=========================================="
echo "📦 文件位置: ${SCRIPT_DIR}/${OUTPUT_ZIP}"
echo "🔑 公钥位置: ${SCRIPT_DIR}/public-key.asc"
echo "⏰ 自动清理时间: $(date -v+24H "+%Y-%m-%d %H:%M:%S" 2>/dev/null || date -d "+24 hours" "+%Y-%m-%d %H:%M:%S")"
echo ""

# 创建一个标记文件，记录清理时间
CLEANUP_MARKER="${SCRIPT_DIR}/.cleanup-at"
echo "$(date +%s) + ${AUTO_CLEAN_SECONDS}" > "${CLEANUP_MARKER}"
echo "$(date "+%Y-%m-%d %H:%M:%S")" >> "${CLEANUP_MARKER}"

# ========== 第 9 步：注册自动清理任务 ==========
register_auto_cleanup() {
    local zip_file="$1"
    local marker="$2"
    local seconds="$3"

    # 在 macOS 上，可以用 at 命令
    # 在 Linux 上，可以用 crontab

    if command -v at >/dev/null 2>&1; then
        # macOS / Linux 都有 at 命令
        echo "rm -f '${zip_file}' '${marker}' '${zip_file%.*}.asc' 2>/dev/null && echo '✅ 自动清理完成'" | \
            at "now + ${seconds} seconds" 2>/dev/null && \
            echo "⏰ 已注册自动清理任务（at 命令）" || \
            echo "⚠️  at 命令注册失败，请手动清理"
    else
        echo ""
        echo "📝 自动清理说明："
        echo "  ${zip_file} 和 target/ 将在 24 小时后需要手动清理"
        echo "  手动清理命令: rm -rf '${zip_file%.zip}.pub-key' '${zip_file}' target/"
    fi
}

register_auto_cleanup "${SCRIPT_DIR}/${OUTPUT_ZIP}" "${CLEANUP_MARKER}" "${AUTO_CLEAN_SECONDS}"

# 提供立即清理的脚本（方便未来手动清除）
cat > "${SCRIPT_DIR}/clean-publish.sh" <<'EOF'
#!/bin/bash
# 立即清理发布产物
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

rm -f central-bundle.zip public-key.asc .cleanup-at
# 同时清理 target/ 但保留 classes（如果有 IDE 缓存）
rm -rf target/

echo "✅ 已清理所有发布产物"
EOF
chmod +x "${SCRIPT_DIR}/clean-publish.sh"

echo ""
echo "🧹 手动清理命令: bash clean-publish.sh"
echo ""
echo "📤 下一步：上传到 Sonatype Central Portal"
echo "   https://central.sonatype.com/publishing"
