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

### 1. 推到 GitHub（首次）

```bash
cd "新媒体矩阵专家市场"
git remote add origin git@github.com:<你的账号>/newmedia-matrix.git
git push -u origin main
```

仓库设为 **Public**（私有仓库需要对方配置 SSH/Token 才能订阅）。

### 2. 以后每次更新（一条命令发版）

```bash
# 改了某个专家内容后，先提升版本号，再推送
python tools/bump_version.py legal-compliance-auditor patch
git add -A
git commit -m "update: legal-compliance-auditor v1.0.1"
git push
```

用户那边点「刷新市场」→「更新」即可拿到新版本。

- `patch` = 修错别字/微调；`minor` = 新增能力/章节；`major` = 结构性重做
- **不改版本号，用户端不会识别到更新**，这一步不能省
- 版本号同时写入 `plugin.json` 与 `.codebuddy-plugin/marketplace.json`

---

## 三、使用者：怎么订阅

1. 打开 WorkBuddy →「专家 / 技能 / 连接器」→ 插件市场 → **「添加市场」**
2. 市场源填以下任一种：
   - `你的账号/newmedia-matrix`（GitHub 简写）
   - `https://github.com/你的账号/newmedia-matrix`（完整地址）
   - `git@github.com:你的账号/newmedia-matrix.git`（SSH）
   - 本地目录路径（如 `./newmedia-matrix`）或一个市场 zip 的 URL
3. 提交 → 自动下载/解压/安装市场
4. 在市场里逐个安装 8 个专家

**以后更新**：市场列表里点「刷新」→ 对提示可更新的专家点「更新」；已是最新会提示「已是最新版本」。

---

## 四、注意事项

- 仓库内**不含任何账号、密钥或对话数据**，可公开。
- 若点「添加市场」提示 **「当前环境不支持添加插件市场」**，说明该环境被策略禁用远程市场，退回 ZIP 导入方式。
- 私有仓库订阅需要对方已配置对应 Git 凭证，否则会拉取失败。
- 只复制目录、不刷新市场，用户端不会自动同步——**在线更新靠"刷新+更新"两步**。

---

版本：1.0.0 ｜ 打包日期：2026-09-21
