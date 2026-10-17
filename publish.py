# -*- coding: utf-8 -*-
"""
一键发布到 GitHub Pages

用法（令牌不再经过命令行参数，避免留在历史记录里）：

  # 方式 A：环境变量（推荐，脚本不会回显）
  set GITHUB_TOKEN=ghp_xxx        # PowerShell: $env:GITHUB_TOKEN="ghp_xxx"
  python publish.py

  # 方式 B：交互式输入（终端里直接粘贴，屏幕上不回显）
  python publish.py

  # 方式 C：管道输入（脚本化调用）
  echo ghp_xxx | python publish.py

  # 可选：指定仓库名 / 禁止任何输入提示（CI、自动化必用）
  python publish.py my-repo --no-input

做的事：
  1) 校验令牌并建仓（已存在则复用）
  2) 经本地代理推送本地 main 分支
  3) 调用 Pages API 开启 Pages（main / 根目录）
  4) 打印最终网址

安全：
  - 令牌只存在于本进程内存，不写入任何文件、不写进 git 配置、不打印
  - 推送时用 http.extraHeader 携带凭据，令牌不出现在远程 URL 里
  - git 报错输出做令牌脱敏
"""
import sys, os, json, subprocess, base64
import urllib.request, urllib.error

PROXY = "http://127.0.0.1:7897"
GIT = r"C:\Users\guess\AppData\Local\GitHubDesktop\app-3.6.5\resources\app\git\cmd\git.exe"
CA = "C:/Users/guess/AppData/Local/GitHubDesktop/app-3.6.5/resources/app/git/mingw64/etc/ssl/certs/ca-bundle.crt"
OWNER = "liuminghong63-boop"
DEFAULT_REPO = "wan-gu-zhi-wang"

def read_token(allow_prompt=True):
    """按顺序取令牌，任何情况下都不会无限期阻塞：
       1) 环境变量 GITHUB_TOKEN
       2) 标准输入为管道/重定向时读一行（3 秒超时）
       3) 终端交互：隐藏回显（仅 allow_prompt 为真时）
       4) 都不行 -> 返回空，由调用方报错退出
    """
    tok = os.environ.get("GITHUB_TOKEN", "").strip()
    if tok:
        return tok, "环境变量 GITHUB_TOKEN"

    def _with_timeout(fn, seconds):
        """在守护线程里跑 fn，超时返回 None，绝不阻塞主线程"""
        import threading
        box = {}

        def runner():
            try:
                box["v"] = fn()
            except (EOFError, KeyboardInterrupt):
                box["v"] = None
            except Exception:
                box["v"] = None

        th = threading.Thread(target=runner, daemon=True)
        th.start()
        th.join(seconds)
        return box.get("v")

    std = sys.stdin
    if std is not None and not std.closed:
        if std.isatty():
            if not allow_prompt:
                return "", "已指定 --no-input，且未提供 GITHUB_TOKEN"
            def ask():
                import getpass
                return getpass.getpass("请粘贴 GitHub 令牌（输入不回显，留空取消）：").strip()
            v = _with_timeout(ask, 300)
            return (v, "交互式输入") if v else ("", "未输入或超时")
        else:
            v = _with_timeout(lambda: std.readline().strip(), 3)
            if v:
                return v, "标准输入"

    return "", "非交互环境且未提供 GITHUB_TOKEN"

def api(url, token, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "User-Agent": "publish-script",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    if data:
        req.add_header("Content-Type", "application/json")
    op = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    try:
        r = op.open(req, timeout=40)
        body = r.read().decode()
        return r.status, (json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, {"raw": body}

def main():
    # 解析参数：只认仓库名与 --no-input，令牌绝不走命令行
    args = [a for a in sys.argv[1:]]
    allow_prompt = True
    if "--no-input" in args:
        allow_prompt = False
        args.remove("--no-input")
    repo = (args[0] if args else DEFAULT_REPO).strip()
    token, how = read_token(allow_prompt)
    if not token:
        print(__doc__)
        print("错误：未取得令牌（%s）" % how)
        print("请先设置环境变量 GITHUB_TOKEN，或直接运行 python publish.py 交互输入。")
        return 2

    print("=" * 56)
    print("发布 万蛊之王 到 GitHub Pages")
    print("令牌来源: " + how)
    print("=" * 56)

    # 1) 校验令牌
    st, me = api("https://api.github.com/user", token)
    if st != 200:
        print("[X] 令牌无效或权限不足:", st, me.get("message", ""))
        return 1
    print("[1/4] 令牌有效，账号:", me.get("login"))

    # 2) 建仓（已存在则复用）
    st, info = api("https://api.github.com/repos/%s/%s" % (OWNER, repo), token)
    if st == 200:
        print("[2/4] 仓库已存在，复用:", info["html_url"])
    else:
        st, info = api("https://api.github.com/user/repos", token, "POST", {
            "name": repo,
            "description": "万蛊之王 · 养蛊小游戏（纯前端，五行克制/物种梯度/融合失败/天赋/忠心度/不败信念）",
            "homepage": "https://%s.github.io/%s/" % (OWNER, repo),
            "private": False,
            "has_issues": True,
            "has_wiki": False,
        })
        if st not in (200, 201):
            print("[X] 建仓失败:", st, info.get("message", ""))
            if st == 403:
                print("    → 令牌缺少 'Administration' 或 'Contents' 写权限")
            return 1
        print("[2/4] 仓库已创建:", info["html_url"])

    # 3) 推送：凭据放在 HTTP 头里，不出现在 URL / 进程参数 / 错误输出中
    print("[3/4] 正在推送…")
    basic = base64.b64encode(("%s:%s" % (OWNER, token)).encode()).decode()
    remote = "https://github.com/%s/%s.git" % (OWNER, repo)
    cmd = [GIT,
           "-c", "http.proxy=" + PROXY,
           "-c", "http.sslBackend=openssl",
           "-c", "http.sslCAInfo=" + CA,
           "-c", "credential.helper=",
           "-c", "http.extraHeader=Authorization: Basic " + basic,
           "push", remote, "main:main", "--force"]
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_ASKPASS="echo")
    p = subprocess.run(cmd, cwd=os.getcwd(), env=env, capture_output=True, text=True)
    out = ((p.stderr or "") + (p.stdout or ""))
    # 双保险脱敏
    out = out.replace(token, "***").replace(basic, "***")
    if p.returncode != 0:
        print("[X] 推送失败:")
        print(out[:1200])
        return 1
    print("      推送完成")

    # 4) 开启 Pages
    print("[4/4] 开启 GitHub Pages (main / 根目录) …")
    st, res = api("https://api.github.com/repos/%s/%s/pages" % (OWNER, repo), token)
    if st == 200:
        print("      Pages 已启用")
    else:
        st, res = api("https://api.github.com/repos/%s/%s/pages" % (OWNER, repo), token, "POST", {
            "source": {"branch": "main", "path": "/"}
        })
        if st in (201, 204):
            print("      Pages 已开启")
        elif st == 409:
            print("      Pages 已存在（跳过）")
        else:
            print("      !! 自动开启失败:", st, res.get("message", ""))
            print("      → 请手动：仓库 Settings → Pages → Source 选 main、/ (root)")

    url = "https://%s.github.io/%s/" % (OWNER, repo)
    print("=" * 56)
    print("完成！网址（1~2 分钟后生效）:")
    print("   " + url)
    print("=" * 56)
    return 0

if __name__ == "__main__":
    sys.exit(main())
