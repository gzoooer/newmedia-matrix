# 新媒体矩阵专家市场（newmedia-matrix）

WorkBuddy 专家市场仓库。含 1 位矩阵操盘总监 + 7 位内容生产与风控专业专家，共 8 个专家。

订阅本市场后，**用户可在线接收后续更新**（刷新市场 → 更新），无需重新收文件。

---

## 一、市场内容

| 专家 | 花名 | 类型 | 作用 |
|---|---|---|---|
| matrix-director | 康策 | 总监 | 总控，按 PDCA 闭环调度其余 7 位 |
| topic-insight-analyst | 闻析言 | 专家 | 选题池、选题价值预判 |
| draft-chief-writer | 毕成稿 | 专家 | 深度初稿撰写 |
| dehumanizing-polisher | 墨无迹 | 专家 | 去 AI 腔、真人语感重塑 |
| platform-content-architect | 齐分流 | 专家 | 五平台差异化改写与标题标签 |
| visual-prompt-planner | 图鸣设 | 专家 | 封面/内图方案与出图提示词 |
| data-review-analyst | 盘数真 | 专家 | 数据看板、爆款拆解、次日策略 |
| legal-compliance-auditor | 严守正 | 专家 | 发布前合规终审，拥有否决权 |

> `matrix-director` 会调度其余 7 位，建议订阅后**全部安装**，否则链路缺人。

---

## 二、发布者：怎么上线这个市场

本市场已上线：**https://github.com/gzoooer/newmedia-matrix**（Public，默认分支 `main`）

### 1. 当前远端配置

```bash
cd "新媒体矩阵专家市场"
git remote -v          # origin  git@github.com:gzoooer/newmedia-matrix.git
git push               # 已配置 upstream，直接 push 即可
```

> 本机 GitHub 的 22 端口被网络封锁，`~/.ssh/config` 已把 `github.com` 指向 `ssh.github.com:443`，命令无需改动。

### 2. 以后每次更新（两条命令发版）

```bash
# ① 改了某个专家内容后，先提升版本号
python tools/bump_version.py legal-compliance-auditor patch

# ② 重新打包市场 zip（写入 dist/），再推送
python tools/build_market_zip.py
git add -A
git commit -m "update: legal-compliance-auditor v1.0.1"
git push
```

用户那边点「刷新市场」→「更新」即可拿到新版本。

> `build_market_zip.py` 会自动排除 `dist/` 自身，**不要手工打 zip**——手打容易把上一版
> zip 套进新 zip，仓库体积会翻倍膨胀。
>
> `marketplace-latest.zip` 每次发版会被覆盖（体积不累积）；带版本号的 zip 每版新增约
> 2.4 MB，发过几版后可删掉旧版归档，仓库更轻。

- `patch` = 修错别字/微调；`minor` = 新增能力/章节；`major` = 结构性重做
- **不改版本号，用户端不会识别到更新**，这一步不能省
- 版本号同时写入 `plugin.json` 与 `.codebuddy-plugin/marketplace.json`

---

## 三、使用者：怎么订阅

1. 打开 WorkBuddy →「专家 / 技能 / 连接器」→ 插件市场 → **「添加市场」**
2. 市场源填下面任意一条（**推荐第一条，直接复制**）：
   - `gzoooer/newmedia-matrix`
   - `https://github.com/gzoooer/newmedia-matrix`
   - `git@github.com:gzoooer/newmedia-matrix.git`
   - 本地目录路径（如 `./newmedia-matrix`）或一个市场 zip 的 URL
3. 提交 → 自动下载/解压/安装市场
4. 在市场里逐个安装 8 个专家

**以后更新**：市场列表里点「刷新」→ 对提示可更新的专家点「更新」；已是最新会提示「已是最新版本」。

### 用不了「添加市场」时：改用 zip 当市场源

若环境提示「当前环境不支持添加插件市场」，可以退一步——把市场 zip 的直链当市场源填进去：

```
https://github.com/gzoooer/newmedia-matrix/raw/main/dist/marketplace-latest.zip
```

（`dist/marketplace-latest.zip` 恒指向最新版，不会随版本号变动，可长期使用。）

### 完全离线：直接下载 zip 导入

在仓库 `dist/` 目录里下载：

| 文件 | 用途 |
|---|---|
| `marketplace-latest.zip` | 最新市场源 zip（同上，可当市场源填） |
| `新媒体矩阵专家市场-v1.0.0.zip` | 带版本号的归档快照 |
| `新媒体矩阵专家包-8个-20260921.zip` | 一次性转发用，内含 8 个单包 + 分发说明 |
| `README-分发说明.md` | 直接转发给朋友的图文操作说明 |

导入路径：专家中心 →「我的专家」→「导入」→ 选 zip → 安全检测 → 「添加到我的专家」。
**导入是一次一个包**，8 位要点 8 次；导入器会识别「该专家已存在」。

---

## 四、注意事项

- 仓库内**不含任何账号、密钥或对话数据**，可公开（`.created-by-session` 等会话标识在打包与提交时均已排除）。
- `dist/` 里放的是分发用 zip，**不参与市场加载**——市场只读 `.codebuddy-plugin/marketplace.json` 与 `plugins/`，多出来的目录不影响订阅。
- 若点「添加市场」提示 **「当前环境不支持添加插件市场」**，说明该环境被策略禁用远程市场，退回 ZIP 导入方式。
- 私有仓库订阅需要对方已配置对应 Git 凭证，否则会拉取失败。
- 只复制目录、不刷新市场，用户端不会自动同步——**在线更新靠"刷新+更新"两步**。

---

版本：1.0.0 ｜ 打包日期：2026-09-21
