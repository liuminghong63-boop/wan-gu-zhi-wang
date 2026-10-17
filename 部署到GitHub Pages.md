# 部署到 GitHub Pages · 说明与维护

**当前线上地址：<https://liuminghong63-boop.github.io/wan-gu-zhi-wang/>**

仓库：<https://github.com/liuminghong63-boop/wan-gu-zhi-wang>

> 本文档分两部分：**日常更新**（你以后最常用）和 **从零重建**（换账号或重做时看）。

---

# 一、日常更新网站

改完游戏内容后，只需要跑两条命令。

## 1. 重新生成网页

```powershell
cd C:\Users\guess\Documents\deepseek-harness\default-workspace
python build_game.py
```

这会同时产出：
- `index.html` —— GitHub Pages 的入口
- `wan-gu-zhi-wang.html` —— 内容相同的副本（单文件用）

## 2. 发布

```powershell
python publish.py
```

脚本会提示 `请粘贴 GitHub 令牌（输入不回显）`，粘贴后回车即可。令牌**不会显示在屏幕上、不会写进文件、不会留在命令历史**。

推送成功后 1 分钟内，Pages 自动重新发布。

## 令牌怎么来

1. 打开 <https://github.com/settings/tokens/new>
2. **Note** 随便填，如 `发布`
3. **Expiration** 选 7 days
4. **Scopes** 勾 `repo`
5. Generate token，复制 `ghp_...`

**用完立刻撤销**：<https://github.com/settings/tokens> → Delete。撤销不影响已发布的网站。

## publish.py 的其他用法

```powershell
# 用环境变量传令牌（不会出现在命令参数里）
$env:GITHUB_TOKEN="ghp_xxx"; python publish.py; Remove-Item Env:\GITHUB_TOKEN

# 管道输入
echo ghp_xxx | python publish.py

# 指定仓库名
python publish.py my-repo

# 禁止任何输入提示（自动化/CI 必用，无令牌时立即报错退出）
python publish.py --no-input
```

安全设计：
- 令牌只存在于进程内存，**不写入任何文件、不打印、不写进 git 配置**
- 推送时用 `http.extraHeader` 传凭据，令牌**不进远程 URL、不进进程参数**
- git 报错输出做**双重脱敏**（令牌 + Basic 串）

---

# 二、仓库结构

```
wan-gu-zhi-wang/
├── index.html            ← 网站入口（必须在根目录）
├── .nojekyll             ← 阻止 Jekyll 处理，必须存在
├── README.md
├── assets/gu/            ← 42 个 .webp 立绘（512px + 160px 缩略）
├── build_game.py         ← 游戏生成器
├── publish.py            ← 发布脚本
├── preview-species.webp
└── preview-game.webp
```

## 两个最容易踩的坑

1. **`index.html` 必须在站点根目录**。之前放在 `docs/` 子目录、而 Pages 源设为根目录，导致构建成功却整站 404。现在已改为根目录。
2. **`.nojekyll` 不能删**。它是空文件，Windows 默认隐藏；缺了它 GitHub 可能忽略以 `_` 或 `.` 开头的资源。

## 立绘为什么是 WebP

原始 PNG 立绘 2048px、共 26.8 MB，直接上线首屏要等十几秒。转换成 WebP 后全站只有 **1.25 MB**（约 1/21），画质看不出差别。

需要改回 PNG：编辑 `build_game.py` 顶部的 `IMG_EXT = "png"`，并确保 `assets/gu/` 下放的是 PNG。

---

# 三、从零重建（换账号或重做）

## 方式 A：用 publish.py（推荐）

```powershell
# 1. 改脚本顶部的 OWNER 为你的 GitHub 用户名
# 2. 运行
$env:GITHUB_TOKEN="ghp_xxx"; python publish.py my-repo-name
```

脚本会自动建仓库、推送、开启 Pages，最后打印网址。

## 方式 B：网页上传（不装任何东西）

1. 打开 <https://github.com/new>，建一个 **Public** 空仓库
2. 点 **uploading an existing file**
3. 把项目根目录的这些文件/文件夹拖进去：
   - `index.html`、`.nojekyll`、`README.md`
   - `assets/` 整个文件夹
   - （可选）`build_game.py`、`publish.py`、预览图
   - 看不到 `.nojekyll` 就在「查看」里勾上**隐藏的项目**
4. Commit changes
5. 进 **Settings → Pages**：
   - **Source** 选 `Deploy from a branch`
   - **Branch** 选 `main`，目录选 **`/ (root)`**
   - 点 **Save**
6. 等 1–2 分钟，访问 `https://你的用户名.github.io/仓库名/`

## 方式 C：命令行 git

```powershell
cd C:\Users\guess\Documents\deepseek-harness\default-workspace
git add -A
git commit -m "更新"
git push
```

> 本机 git 用的是 GitHub Desktop 自带的：
> `C:\Users\guess\AppData\Local\GitHubDesktop\app-3.6.5\resources\app\git\cmd\git.exe`
> 若提示找不到 `git`，把该目录加进 PATH 即可。

---

# 四、常见问题

**打开是 404**
- 等几分钟，首次构建有延迟
- 检查 `index.html` 是否在 Pages 所选目录的**最外层**
- 检查仓库是否 Public
- 到仓库 **Actions** 标签看部署是否失败

**页面能开但立绘全不显示**
- `assets/` 没上传成功，或路径层级错了
- 在仓库里点进 `assets/gu/`，确认能看到 42 个 `.webp`
- 确认 `.nojekyll` 已上传

**更新了但网页没变**
- 强刷 `Ctrl` + `F5`（Pages 有 CDN 缓存）
- 等 1–2 分钟再看

**想用自己的域名**
- Settings → Pages → Custom domain 填域名
- 在域名商处加 CNAME 记录指向 `你的用户名.github.io`

**想统计有多少人玩**
- 用 [GoatCounter](https://www.goatcounter.com/)（免费、无 Cookie），
  在 `index.html` 的 `</body>` 前加一行统计脚本

**推送时报 401 Bad credentials**
- 令牌过期或已被撤销，重新生成一个

**推送报 `Connection was reset` / TLS 错误**
- 本机需要走代理：脚本内已配 `http.proxy=http://127.0.0.1:7897`
- 若你的代理端口不同，改 `publish.py` 顶部的 `PROXY`

---

# 五、注意

- GitHub Pages 是**公开**的，仓库和网址任何人都能访问
- 免费版要求仓库公开；私密仓库用 Pages 需付费账号
- 分享给别人时直接发网址即可，对方无需任何设置
- 21 张立绘由第三方图像生成工具产出，商用前请自行确认生成工具的使用条款
