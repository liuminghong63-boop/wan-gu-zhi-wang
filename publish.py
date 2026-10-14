# -*- coding: utf-8 -*-
"""
一键发布到 GitHub Pages
用法：  python publish.py <GitHub_Token> [仓库名]

做的事：
  1) 用令牌建仓（已存在则复用）
  2) 经本地代理推送本地 main 分支
  3) 调用 Pages API 开启 Pages（main / 根目录）
  4) 打印最终网址

安全：令牌只在本进程内使用，不写入任何文件、不打印、不写进 git 配置。
      推送用的远程地址只存在于本次命令的命令行参数里。
"""
import sys, os, json, subprocess, base64, time
import urllib.request, urllib.error

PROXY = "http://127.0.0.1:7897"
GIT = r"C:\Users\guess\AppData\Local\GitHubDesktop\app-3.6.5\resources\app\git\cmd\git.exe"
CA = "C:/Users/guess/AppData/Local/GitHubDesktop/app-3.6.5/resources/app/git/mingw64/etc/ssl/certs/ca-bundle.crt"
OWNER = "liuminghong63-boop"
DEFAULT_REPO = "wan-gu-zhi-wang"

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
    if len(sys.argv) < 2:
        print(__doc__)
        print("错误：缺少令牌")
        return 2
    token = sys.argv[1].strip()
    repo = (sys.argv[2] if len(sys.argv) > 2 else DEFAULT_REPO).strip()

    print("=" * 56)
    print("发布 万蛊之王 到 GitHub Pages")
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

    # 3) 推送
    print("[3/4] 正在推送（约 1.8MB）…")
    remote = "https://%s:%s@github.com/%s/%s.git" % (OWNER, token, OWNER, repo)
    cmd = [GIT,
           "-c", "http.proxy=" + PROXY,
           "-c", "http.sslBackend=openssl",
           "-c", "http.sslCAInfo=" + CA,
           "-c", "credential.helper=",
           "push", remote, "main:main", "--force"]
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_ASKPASS="echo")
    p = subprocess.run(cmd, cwd=os.getcwd(), env=env, capture_output=True, text=True)
    if p.returncode != 0:
        print("[X] 推送失败:")
        # 令牌可能出现在 git 的错误输出里，这里做一次脱敏
        print((p.stderr or p.stdout).replace(token, "***")[:1200])
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
