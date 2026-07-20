"""
Maven Archetype 构建和发布脚本
==============================

将 maven-archetype 项目打包成 Maven Archetype Catalog，
发布到 GitHub Pages，可在 IntelliJ IDEA 中直接添加。

使用方法：
    python3 build_and_publish.py
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent
ARCHETYPE_DIR = PROJECT_ROOT / "maven-archetype"
REPO_DIR = ARCHETYPE_DIR / "repo"
DOCS_DIR = PROJECT_ROOT / "docs"


def run_command(cmd, cwd=None, check=True):
    """运行 shell 命令"""
    print(f"  $ {cmd}")
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=True, text=True
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(result.stderr, file=sys.stderr)
    if check and result.returncode != 0:
        sys.exit(f"命令执行失败: {cmd}")
    return result


def check_maven():
    """检查 Maven 是否已安装"""
    print("\n🔍 检查 Maven...")
    result = subprocess.run("mvn --version", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ 未找到 Maven")
        print("\n请先安装 Maven:")
        print("  macOS:   brew install maven")
        print("  Ubuntu:  sudo apt install maven")
        print("  Windows: 下载 https://maven.apache.org/download.cgi")
        sys.exit(1)
    print("✅ Maven 已安装")
    print(result.stdout.split('\n')[0])


def clean():
    """清理旧的构建产物"""
    print("\n🧹 清理旧产物...")
    if REPO_DIR.exists():
        shutil.rmtree(REPO_DIR)
        print(f"  删除: {REPO_DIR}")
    target = ARCHETYPE_DIR / "target"
    if target.exists():
        shutil.rmtree(target)
        print(f"  删除: {target}")


def build_archetype():
    """构建 archetype jar"""
    print("\n🔨 构建 Maven Archetype...")
    run_command(
        "mvn clean install -DskipTests",
        cwd=ARCHETYPE_DIR
    )
    print("✅ Archetype 构建完成")


def prepare_repo():
    """准备发布目录（GitHub Pages）"""
    print("\n📦 准备发布目录...")

    # 在 archetype 目录下创建 repo
    REPO_DIR.mkdir(parents=True, exist_ok=True)

    # 从 .m2 目录复制 jar 到 repo
    m2_path = Path.home() / ".m2" / "repository" / "io" / "github" / "jhqxx" / "springai-agent-archetype" / "1.0.0"
    if not m2_path.exists():
        print(f"❌ 找不到构建产物: {m2_path}")
        sys.exit(1)

    for f in m2_path.iterdir():
        shutil.copy2(f, REPO_DIR / f.name)
        print(f"  复制: {f.name}")

    print(f"✅ 发布目录准备完成: {REPO_DIR}")


def update_catalog_url():
    """更新 catalog XML 中的 URL（指向 GitHub Pages）"""
    print("\n🔗 更新 Catalog URL...")
    catalog_path = DOCS_DIR / "archetype-catalog.xml"
    content = catalog_path.read_text()

    # 替换为 GitHub Pages URL
    new_url = "https://jhqxx.github.io/ai-siyuan-agent/maven-archetype/repo/"
    content = content.replace(
        "https://raw.githubusercontent.com/JHQXX/ai-siyuan-agent/main/maven-archetype/repo/",
        new_url
    )
    catalog_path.write_text(content)
    print(f"  Catalog URL: {new_url}")


def main():
    print("=" * 60)
    print("🚀 SpringAI Agent Archetype 构建发布工具")
    print("=" * 60)

    check_maven()
    clean()
    build_archetype()
    prepare_repo()
    update_catalog_url()

    print("\n" + "=" * 60)
    print("✅ 发布准备完成！")
    print("=" * 60)
    print("\n📋 接下来的步骤：")
    print("""
  1. 提交代码到 GitHub:
     git add .
     git commit -m "feat: 添加 Maven Archetype"
     git push origin main

  2. 启用 GitHub Pages:
     - 访问 https://github.com/JHQXX/ai-siyuan-agent/settings/pages
     - Source: 选择 "main" 分支
     - 点击 Save

  3. 等待几分钟后，使用以下 Catalog URL:
     https://jhqxx.github.io/ai-siyuan-agent/archetype-catalog.xml

  4. 在 IntelliJ IDEA 中:
     - File → New → Project → Maven
     - 勾选 "Create from archetype"
     - 添加 Catalog URL
     - 选择 "springai-agent-archetype"
""")


if __name__ == "__main__":
    main()