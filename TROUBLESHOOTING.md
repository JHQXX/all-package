# 常见问题与排查

---

## 🔧 构建问题

### Q: `Fatal: can't open '/Users/lizhi/.gnupg/trustdb.gpg': Operation not permitted`

**原因**：开发环境 IDE 有 sandbox，限制对 `~/.gnupg` 的写访问。

**解决**：把 GPG 数据放到 `/tmp/gpg-home`：
```bash
gpg --homedir /tmp/gpg-home --list-keys    # 应该能看到密钥
```

所有相关操作（生成、签名、导出）都要加 `--homedir /tmp/gpg-home`。

参见：[PUBLISH_GUIDE.md](PUBLISH_GUIDE.md) 步骤 3。

---

### Q: `Invalid md5 checksum` 或 `Invalid sha1 checksum`

**原因**：macOS 的 `md5` / `shasum` 默认输出 BSD 格式（带文件名）：
```
MD5 (xxx.pom) = 0a5d...    # BSD ❌
0a5d...                     # 标准 ✅
```

**解决**：
```bash
# 标准格式（只要哈希值，不要文件名）
md5 -q xxx.pom > xxx.pom.md5
shasum -a 1 xxx.pom | awk '{print $1}' > xxx.pom.sha1
```

参见：`build-and-pack.sh` 步骤 3。

---

### Q: GPG 签名通过本地验证，但 Sonatype 提示 `Could not find a public key`

**原因**：你的公钥没有上传到 Sonatype 能查询的密钥服务器。

**解决**：
```bash
SERVERS=("keyserver.ubuntu.com" "pgp.mit.edu" "keys.openpgp.org")
for s in "${SERVERS[@]}"; do
    curl -s -X POST --data-urlencode "keytext@public-key.asc" "https://$s/pks/add"
done
```

⚠️ `keys.openpgp.org` 上传后会发邮件，需要去邮箱点确认链接！

---

## 🌐 网络问题

### Q: `keyserver.ubuntu.com` 拒绝连接

**原因**：临时网络问题或防火墙。

**解决**：依次尝试其他服务器：
```bash
gpg --keyserver hkps://keyserver.ubuntu.com --send-keys <KEY_ID>  # hkps 是 https
# 或
gpg --keyserver hkp://pgp.mit.edu --send-keys <KEY_ID>
```

或者用 curl 直接 POST：
```bash
curl -X POST --data-urlencode "keytext@public-key.asc" "https://keyserver.ubuntu.com/pks/add"
```

---

### Q: Maven 下载依赖超时

**原因**：网络不通或阿里云镜像未生效。

**解决**：检查 `~/.m2/settings.xml`：
```xml
<mirrors>
    <mirror>
        <id>aliyunmaven</id>
        <url>https://maven.aliyun.com/repository/public</url>
        <mirrorOf>*,!central</mirrorOf>
    </mirror>
</mirrors>
```

注意是 `*,!central`，不是 `central`。

---

## 📦 Sonatype 上传问题

### Q: 上传 zip 后，提示 metadata 错误

**原因 1**：zip 结构不对，必须按 `io/github/jhqxx/...` 路径组织。

**原因 2**：缺文件，至少要有：
- `*.jar` + `*.jar.asc` + `*.jar.md5` + `*.jar.sha1`
- `*.pom` + `*.pom.asc` + `*.pom.md5` + `*.pom.sha1`
- 可选：`*-sources.jar` 同上

**解决**：用 `bash build-and-pack.sh` 重新打包。

---

### Q: 提示 `<version>` already exists

**原因**：Maven Central 不允许覆盖已发布的版本。

**解决**：升级到新版本（如 1.0.1）：
1. 修改 `archetype/pom.xml` 的 `<version>`
2. 修改 `build-and-pack.sh` 的 `VERSION` 变量
3. 修改 `docs/jhqxx-catalog.xml`
4. 重新打包上传

---

### Q: 发布卡在 Publishing 状态很久（超过 4 小时）

**可能原因**：
1. 公钥还在同步（首次发布）
2. Sonatype 端处理慢

**解决**：
- 查看 https://central.sonatype.com/browse 看是否有错误
- 查看注册邮箱的邮件（Sonatype 会发邮件）
- 必要时**取消重新发布**

---

## 🎯 IDEA 使用问题

### Q: 配了 GitHub Pages Catalog 但列表是空的

**原因 1**：GitHub Pages 没启用。

**解决**：仓库 → Settings → Pages → 选 `main` branch + `/docs` folder。

**原因 2**：Catalog URL 配错。

**正确 URL**：
```
https://jhqxx.github.io/all-package/jhqxx-catalog.xml
```

用浏览器访问应该能看到 XML 内容。

---

### Q: IDEA 报 "Cannot resolve archetype"

**原因**：网络不通或 Maven 配置问题。

**解决**：
1. `File → Settings → Maven → 取消 "Always update snapshots"`
2. 重启 IDEA
3. 重新选 catalog

---

## 📂 GitHub Pages 问题

### Q: docs/index.html 显示为 README 而不是页面

**原因**：GitHub Pages 默认会去渲染 `README.md`，你 `index.html` 已经在但优先级问题。

**解决**：
1. 删掉 `docs/README.md`（如果有）
2. 重新提交 `docs/index.html`
3. 等待 1-2 分钟重新部署

---

## 🐛 其他

### Q: `mvn verify` 出现奇怪的插件版本警告

**无害信息**：
```
[WARNING] Ignoring incompatible plugin version 4.0.0-beta-1
```

Maven 自动忽略了 Maven 4 的 beta 插件，下载了兼容版本。可以忽略。

---

### Q: 我换了一台电脑，GPG 密钥丢了怎么办？

**严重**：GPG 密钥丢失后**无法重新发布**同一版本！

**预防措施**：
```bash
# 1. 立即导出私钥并多地备份
gpg --homedir /tmp/gpg-home --armor --export-secret-keys 2733827845l@gmail.com > private-key.asc
# 存入密码管理器（如 1Password）
# 或加密后上传到 iCloud Drive、Google Drive 等
```

---

## 📋 调试清单

出问题前，先检查：

- [ ] `cat ~/.m2/settings.xml` | grep `<server>` - token 是否齐全
- [ ] `gpg --homedir /tmp/gpg-home --list-secret-keys` - 密钥存在吗
- [ ] `curl https://keyserver.ubuntu.com/pks/lookup?op=get&search=<FINGERPRINT>` - 公钥同步了吗
- [ ] Java、Maven 版本：`mvn -version`（需要 Java 17+）
- [ ] `~/.m2/settings.xml` 中 mirror 配置：`<mirrorOf>*,!central</mirrorOf>`
- [ ] archetype/pom.xml 中 4 个插件齐全吗
- [ ] archetype/pom.xml 中 gpgArguments 指向 `/tmp/gpg-home` 吗
