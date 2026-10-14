# 部署到 GitHub Pages · 手把手

目标：得到一个可以发给任何人的网址，比如 `https://你的用户名.github.io/wan-gu-zhi-wang/`。
全程免费，不需要服务器，不需要买域名。

---

## 准备：确认部署目录

要上传的是 **`docs/` 目录里的内容**（这就是整个网站）：

```
docs/
├── index.html            ← 网站入口，文件名必须是 index.html
├── .nojekyll             ← 必须上传，否则 GitHub 可能漏掉资源文件
├── README.md
├── preview-species.webp
├── preview-game.webp
└── assets/gu/            ← 42 个 .webp 立绘
```

⚠️ 两个最常见的坑：

1. **`index.html` 必须在站点根目录**。如果它被套在 `docs/` 之类的子目录里，访问根网址会 404。
2. **`.nojekyll` 不能漏**。它是空文件，Windows 资源管理器默认隐藏，别忘了它。
   （用下面的方法一上传时，它就在文件夹里，正常拖进去即可。）

---

## 方法一：网页上传（不需要装任何东西）

1. 打开 <https://github.com/new>
2. **Repository name** 填 `wan-gu-zhi-wang`
3. 选 **Public**（Pages 免费版需要公开仓库）
4. **不要**勾选 Add README / .gitignore / license，保持空仓库
5. 点 **Create repository**
6. 在新页面点 **uploading an existing file** 链接
7. 打开你电脑上的 `docs` 文件夹，**全选里面的所有内容**（含 `assets` 文件夹、`.nojekyll`、`index.html`）
   - 如果看不到 `.nojekyll`：在资源管理器「查看」里勾上**隐藏的项目**
8. 把它们拖进浏览器上传区，等上传完成
9. 下方 Commit changes 填个说明，点 **Commit changes**

> 拖拽时请拖**文件夹里面的内容**，而不是 `docs` 文件夹本身——否则文件会多一层 `docs/`，
> 那也**可以用**，只是后面 Pages 的目录要选 `/docs`。

---

## 方法二：命令行（装了 git 的话更快）

```bash
cd docs
git init
git add -A
git commit -m "万蛊之王 首次发布"
git branch -M main
git remote add origin https://github.com/你的用户名/wan-gu-zhi-wang.git
git push -u origin main
```

> 如果之后要更新，改完文件再执行 `git add -A && git commit -m "更新" && git push` 即可，
> Pages 会在 1 分钟内自动重新发布。

---

## 开启 GitHub Pages

1. 进入仓库页面，点 **Settings**
2. 左侧栏点 **Pages**
3. **Source** 选 `Deploy from a branch`
4. **Branch** 选 `main`
5. **目录**：
   - 文件在仓库根目录 → 选 **`/ (root)`**
   - 文件在 `docs/` 子目录 → 选 **`/docs`**
6. 点 **Save**
7. 等 1–2 分钟，刷新页面，顶部会出现绿色提示和你的网址

访问 `https://你的用户名.github.io/wan-gu-zhi-wang/` 即可。

---

## 常见问题

**打开是 404**
- 等几分钟，首次部署有延迟
- 检查 `index.html` 是否在所选目录的**最外层**
- 检查仓库是否 Public

**页面能开但蛊虫立绘全都不显示**
- 说明 `assets/` 没上传成功，或者路径层级错了
- 在仓库里点进 `assets/gu/`，确认能看到 42 个 `.webp` 文件
- 确认 `.nojekyll` 已上传

**更新了文件但网页没变**
- Pages 有缓存，强制刷新（`Ctrl` + `F5`）
- 到 **Actions** 标签看部署是否还在跑

**想用自己的域名**
- Settings → Pages → Custom domain 填入域名
- 在域名商处加一条 CNAME 记录指向 `你的用户名.github.io`

**想统计有多少人玩**
- 可以用 [GoatCounter](https://www.goatcounter.com/)（免费、无 Cookie），
  在 `index.html` 的 `</body>` 前加一行它的统计脚本即可

---

## 注意

- GitHub Pages 是**公开**的，仓库和网址任何人都能访问
- 免费版要求仓库公开；想私密仓库用 Pages 需要付费账号
- 分享给别人时，直接发网址就行，无需对方做任何设置
