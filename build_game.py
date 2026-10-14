# -*- coding: utf-8 -*-
"""
万蛊之王 v2 —— 生成器
把 SCRIPT_BODY / STYLE_BODY 注入 TPL，输出 wan-gu-zhi-wang.html
新增：五行克制、物种梯度(20种)、融合失败、特殊天赋、忠心度/反叛、不败信念
配图：assets/gu/<speciesId>.<ext>（512px）与 sm_<id>.<ext>（160px 缩略）
"""
import io, os

OUT = "wan-gu-zhi-wang.html"
# 配图开关：True 用 assets/gu 的插画，False 回退到内置程序化 SVG
USE_IMAGES = True
# 立绘扩展名：网页部署用 webp（比 png 小约 7 倍）
IMG_EXT = "webp"

def images_ready():
    need = ["m1", "w1", "s1", "f1", "e1", "x7"]
    return all(os.path.exists(os.path.join("assets", "gu", i + "." + IMG_EXT)) for i in need)

# ============================================================ CSS ============
STYLE_BODY = r"""
    *{margin:0;padding:0;box-sizing:border-box}

    :root{
        --ink:#0b0d14; --ink2:#11141f; --jade:#3fd0b0; --paper:#e8e6df;
        --gold:#e8b44a; --red:#e94560;
        --metal:#d8c98a; --wood:#5fc98a; --water:#63a9e8; --fire:#ff8a4a; --earth:#d8b878;
        --primal:#c07ae8;
    }

    body{
        font-family:'Microsoft YaHei','PingFang SC',sans-serif;
        background:
            radial-gradient(1100px 620px at 50% -12%, rgba(63,208,176,.10), transparent 62%),
            radial-gradient(820px 520px at 12% 108%, rgba(192,122,232,.10), transparent 60%),
            linear-gradient(168deg,#0b0d14 0%,#11141f 52%,#0a0c12 100%);
        color:#dfe4ee;
        min-height:100vh;
        overflow-x:hidden;
    }

    body::before{
        content:'';position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.05;
        background-image:radial-gradient(rgba(255,255,255,.9) 1px,transparent 1px);
        background-size:32px 32px;
        animation:qiDrift 26s linear infinite;
    }
    @keyframes qiDrift{from{background-position:0 0}to{background-position:32px 320px}}

    #fx{position:fixed;inset:0;pointer-events:none;z-index:9999}

    .container{max-width:940px;margin:0 auto;padding:22px 18px 70px;position:relative;z-index:1}

    /* 标题 */
    .game-title{
        text-align:center;font-size:2.7em;letter-spacing:.22em;font-weight:700;
        background:linear-gradient(180deg,#fff6d8 0%,var(--gold) 42%,#a8621f 100%);
        -webkit-background-clip:text;background-clip:text;color:transparent;
        filter:drop-shadow(0 0 16px rgba(232,180,74,.55));
        margin:14px 0 4px;animation:titleBreath 3.4s ease-in-out infinite;
    }
    @keyframes titleBreath{
        0%,100%{filter:drop-shadow(0 0 12px rgba(232,180,74,.4))}
        50%{filter:drop-shadow(0 0 26px rgba(232,180,74,.9))}
    }
    .game-sub{text-align:center;color:#7d8798;font-size:.82em;letter-spacing:.34em;margin-bottom:18px}

    /* 面板 */
    .panel{
        position:relative;background:linear-gradient(160deg,rgba(255,255,255,.055),rgba(255,255,255,.018));
        border:1px solid rgba(232,180,74,.20);border-radius:14px;padding:18px;margin:14px 0;
        backdrop-filter:blur(3px);
        box-shadow:0 10px 34px rgba(0,0,0,.42),inset 0 1px 0 rgba(255,255,255,.05);
        animation:panelIn .55s cubic-bezier(.22,1,.36,1) backwards;
    }
    .panel:nth-of-type(2){animation-delay:.06s}
    .panel:nth-of-type(3){animation-delay:.12s}
    .panel:nth-of-type(4){animation-delay:.18s}
    @keyframes panelIn{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}

    .panel-title{
        color:var(--gold);font-size:1.12em;letter-spacing:.14em;margin-bottom:14px;
        padding-bottom:9px;border-bottom:1px solid rgba(232,180,74,.24);
        display:flex;align-items:center;gap:8px;
    }
    .panel-title::before{content:'';width:4px;height:15px;border-radius:2px;
        background:linear-gradient(180deg,var(--gold),transparent);box-shadow:0 0 10px var(--gold)}

    /* 按钮 */
    .btn{
        position:relative;overflow:hidden;border:none;cursor:pointer;
        padding:11px 22px;margin:4px;border-radius:9px;font-size:.94em;color:#0d1017;
        font-family:inherit;font-weight:700;letter-spacing:.05em;
        background:linear-gradient(155deg,#ffe6a8,var(--gold) 58%,#b8801f);
        box-shadow:0 5px 18px rgba(232,180,74,.34);
        transition:transform .18s,box-shadow .25s,filter .25s;
    }
    .btn:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 9px 26px rgba(232,180,74,.55)}
    .btn:active:not(:disabled){transform:translateY(0) scale(.975)}
    .btn:disabled{opacity:.3;cursor:not-allowed;filter:grayscale(.7);box-shadow:none}
    .btn::after{content:'';position:absolute;inset:0;pointer-events:none;opacity:0;
        background:radial-gradient(circle at center,rgba(255,255,255,.75),transparent 62%);
        transform:scale(.25);transition:opacity .34s,transform .34s}
    .btn:active:not(:disabled)::after{opacity:1;transform:scale(1.7);transition:none}

    .btn-ghost{background:linear-gradient(155deg,#38414f,#232a35);color:#cfd6e2;
        box-shadow:0 5px 16px rgba(0,0,0,.45)}
    .btn-ghost:hover:not(:disabled){box-shadow:0 9px 22px rgba(0,0,0,.6)}
    .btn-jade{background:linear-gradient(155deg,#a9f0dd,var(--jade) 58%,#1c8b74);color:#04201a;
        box-shadow:0 5px 18px rgba(63,208,176,.34)}
    .btn-jade:hover:not(:disabled){box-shadow:0 9px 26px rgba(63,208,176,.55)}
    .btn-danger{background:linear-gradient(155deg,#ffb3bd,#e94560 58%,#8f1d30);color:#fff}
    .btn-row{display:flex;flex-wrap:wrap;align-items:center;gap:2px}

    /* 资源栏 */
    .stats-row{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}
    .stat{flex:1;min-width:96px;background:rgba(0,0,0,.34);border:1px solid rgba(255,255,255,.06);
        border-radius:10px;padding:9px;text-align:center}
    .stat-label{display:block;font-size:.74em;color:#8590a2;letter-spacing:.16em}
    .stat-value{display:block;font-size:1.28em;color:var(--gold);margin-top:3px;font-weight:700}
    .stat-value.pulse{animation:pulseAnim .52s cubic-bezier(.3,1.6,.5,1)}
    @keyframes pulseAnim{
        0%{transform:scale(1)}45%{transform:scale(1.42);color:#fff;text-shadow:0 0 16px var(--gold)}
        100%{transform:scale(1)}}

    /* 蛊虫网格 */
    .guchong-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(252px,1fr));gap:14px;margin:12px 0}
    .guchong-card{
        position:relative;overflow:hidden;cursor:pointer;
        background:linear-gradient(168deg,rgba(255,255,255,.06),rgba(0,0,0,.32));
        border:1px solid rgba(255,255,255,.10);border-radius:12px;padding:12px;
        transition:transform .22s,border-color .22s,box-shadow .28s;
    }
    .guchong-card:hover{transform:translateY(-4px);border-color:rgba(232,180,74,.5);
        box-shadow:0 12px 30px rgba(0,0,0,.5)}
    .guchong-card.selected{border-color:var(--jade);
        box-shadow:0 0 22px rgba(63,208,176,.45),inset 0 0 20px rgba(63,208,176,.12);
        animation:selectedBreath 1.7s ease-in-out infinite}
    @keyframes selectedBreath{
        0%,100%{box-shadow:0 0 15px rgba(63,208,176,.32),inset 0 0 14px rgba(63,208,176,.1)}
        50%{box-shadow:0 0 30px rgba(63,208,176,.72),inset 0 0 24px rgba(63,208,176,.24)}}
    .guchong-card.card-enter{animation:cardEnter .6s cubic-bezier(.34,1.56,.64,1)}
    @keyframes cardEnter{
        0%{opacity:0;transform:scale(.5) translateY(26px) rotate(-5deg)}
        62%{opacity:1;transform:scale(1.07) translateY(-5px) rotate(1.5deg)}
        100%{opacity:1;transform:scale(1) translateY(0) rotate(0)}}

    /* 图腾 / 立绘 */
    .gu-figure{position:relative;width:100%;height:158px;margin:-4px 0 6px;
        display:flex;align-items:center;justify-content:center}
    .gu-figure svg{height:100%;width:auto;overflow:visible;
        filter:drop-shadow(0 5px 10px rgba(0,0,0,.6));
        animation:guBreath 3.6s ease-in-out infinite}
    .guchong-card:hover .gu-figure svg{animation-duration:2.4s}
    /* 插画：暗底原图用 lighten 溶进深色页面，配合羽化 alpha 消除方框；
       滤镜提亮是因为 lighten 会吃掉中间调，实测 brightness(1.30) 观感最佳 */
    .gu-img{width:100%;height:100%;object-fit:contain;display:block;
        mix-blend-mode:lighten;border-radius:12px;
        filter:brightness(1.30) saturate(1.12) contrast(1.06);
        animation:guBreath 3.6s ease-in-out infinite}
    .guchong-card:hover .gu-img{animation-duration:2.4s}
    @keyframes guBreath{
        0%,100%{transform:translateY(0) scale(1)}
        50%{transform:translateY(-4px) scale(1.028)}}
    .tier-tag{position:absolute;top:6px;right:8px;z-index:3;font-size:.68em;padding:2px 7px;
        border-radius:9px;letter-spacing:.08em;background:rgba(0,0,0,.55);
        border:1px solid rgba(255,255,255,.14);color:#cfd6e2}
    .tier-tag.t6{color:#ffe9a8;border-color:rgba(232,180,74,.7);box-shadow:0 0 12px rgba(232,180,74,.5)}
    .tier-tag.t7{color:#f0d0ff;border-color:rgba(192,122,232,.75);box-shadow:0 0 14px rgba(192,122,232,.6)}

    .guchong-head{display:flex;align-items:baseline;gap:6px;flex-wrap:wrap;margin-bottom:5px}
    .guchong-name{font-size:1.04em;color:#ffe9a8;font-weight:700;letter-spacing:.04em}
    .elem-tag{font-size:.68em;padding:1px 7px;border-radius:8px;border:1px solid currentColor;opacity:.95}
    .qi-tag{font-size:.68em;padding:1px 7px;border-radius:8px;background:rgba(255,255,255,.09);color:#c8d0dd}
    .guchong-lv{position:absolute;top:6px;left:8px;z-index:3;font-size:.7em;color:#9aa5b6}

    .talent-line{display:flex;align-items:center;gap:5px;margin:6px 0;font-size:.76em;
        padding:3px 7px;border-radius:7px;background:rgba(192,122,232,.13);
        border:1px solid rgba(192,122,232,.34);color:#e0c8f5}
    .talent-line.none{background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.08);color:#6f7a8b}

    .attr-bar{display:flex;align-items:center;margin:2px 0;font-size:.75em}
    .attr-label{width:20px;color:#8590a2}
    .attr-value{width:30px;text-align:right;color:#e8b44a;font-variant-numeric:tabular-nums}
    .attr-progress{flex:1;height:5px;background:rgba(255,255,255,.09);border-radius:3px;margin:0 7px;overflow:hidden}
    .attr-fill{height:100%;border-radius:3px;transition:width .5s ease}
    .attr-攻击{background:linear-gradient(90deg,#e94560,#ff8a8a)}
    .attr-毒力{background:linear-gradient(90deg,#8b5cf6,#c4a0ff)}
    .attr-防御{background:linear-gradient(90deg,#38a169,#7ddfa8)}
    .attr-速度{background:linear-gradient(90deg,#3182ce,#7fc0ff)}
    .attr-灵性{background:linear-gradient(90deg,#d69e2e,#ffd98a)}
    .guchong-exp{margin-top:6px;font-size:.7em;color:#6f7a8b}

    /* 忠心度 */
    .loyal-row{display:flex;align-items:center;gap:5px;margin:6px 0 2px;font-size:.72em}
    .loyal-label{color:#8590a2;flex:0 0 auto}
    .loyal-bar{flex:1;height:6px;background:rgba(255,255,255,.09);border-radius:3px;overflow:hidden}
    .loyal-fill{height:100%;border-radius:3px;transition:width .45s ease}
    .loyal-val{flex:0 0 auto;font-variant-numeric:tabular-nums;font-size:.94em}
    .loy-hi  .loyal-fill{background:linear-gradient(90deg,#2f9e78,#7ddfa8)}
    .loy-hi  .loyal-val{color:#7ddfa8}
    .loy-mid .loyal-fill{background:linear-gradient(90deg,#b8892a,#ffd98a)}
    .loy-mid .loyal-val{color:#ffd98a}
    .loy-low .loyal-fill{background:linear-gradient(90deg,#c2622a,#ffab6b)}
    .loy-low .loyal-val{color:#ffab6b}
    .loy-bad .loyal-fill{background:linear-gradient(90deg,#a01f34,#ff8a96)}
    .loy-bad .loyal-val{color:#ff8a96}
    .guchong-card.low-loyal{border-color:rgba(255,138,150,.5);
        box-shadow:0 0 16px rgba(233,69,96,.3),inset 0 0 16px rgba(233,69,96,.08)}
    .guchong-card.low-loyal .gu-figure svg{animation:restless 1.1s ease-in-out infinite}
    @keyframes restless{
        0%,100%{transform:translate(0,0) rotate(0)}
        25%{transform:translate(-1.5px,0) rotate(-1.2deg)}
        75%{transform:translate(1.5px,0) rotate(1.2deg)}}

    /* 不败信念 */
    .streak-row{margin:4px 0 2px;font-size:.72em;color:#ffd76a;
        background:linear-gradient(90deg,rgba(232,180,74,.18),transparent);
        border-left:2px solid var(--gold);padding:2px 7px;border-radius:4px}
    .streak-badge{position:absolute;top:26px;right:8px;z-index:3;font-size:.66em;
        padding:1px 6px;border-radius:8px;color:#2a1c05;font-weight:700;letter-spacing:.04em;
        background:linear-gradient(155deg,#ffe9a8,var(--gold));
        box-shadow:0 0 10px rgba(232,180,74,.7)}
    .guchong-card.has-streak{border-color:rgba(232,180,74,.55)}
    .guchong-card.has-streak::before{content:'';position:absolute;inset:0;pointer-events:none;
        border-radius:12px;box-shadow:inset 0 0 22px rgba(232,180,74,.16)}
    .attr-value .buffed{display:block;font-style:normal;font-size:.82em;color:#7ddfa8;
        line-height:1;margin-top:-1px}

    /* 日志 */
    .log-box{background:rgba(0,0,0,.42);border:1px solid rgba(255,255,255,.05);border-radius:10px;
        padding:12px;max-height:230px;overflow-y:auto;font-size:.86em;line-height:1.75;scroll-behavior:smooth}
    .log-box::-webkit-scrollbar{width:7px}
    .log-box::-webkit-scrollbar-thumb{background:rgba(232,180,74,.3);border-radius:4px}
    .log-entry{padding:2px 0;border-bottom:1px solid rgba(255,255,255,.04);animation:logIn .32s ease backwards}
    @keyframes logIn{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:translateX(0)}}
    .log-info{color:#7fb6e8}.log-success{color:#5fd39a}.log-error{color:#ff8a96}
    .log-gold{color:#ffd76a}.log-bad{color:#c07ae8}

    /* 斗蛊场 */
    .battle-arena{display:flex;justify-content:space-around;align-items:center;padding:16px 10px;
        border-radius:14px;margin:10px 0;position:relative;
        background:radial-gradient(circle at 50% 50%,rgba(232,180,74,.09),transparent 72%)}
    .battle-side{text-align:center;width:43%;will-change:transform,filter}
    .battle-side .gu-figure{height:132px}
    .battle-side.atk-right{animation:atkR .24s ease}
    .battle-side.atk-left{animation:atkL .24s ease}
    @keyframes atkR{0%{transform:translateX(0)}45%{transform:translateX(20px) scale(1.08)}100%{transform:translateX(0)}}
    @keyframes atkL{0%{transform:translateX(0)}45%{transform:translateX(-20px) scale(1.08)}100%{transform:translateX(0)}}
    .battle-side.hit{animation:hitShake .34s ease}
    @keyframes hitShake{
        0%{transform:translateX(0);filter:brightness(1)}
        15%{transform:translateX(-9px);filter:brightness(2.5) saturate(1.9)}
        36%{transform:translateX(8px);filter:brightness(1.7)}
        56%{transform:translateX(-5px);filter:brightness(1.35)}
        100%{transform:translateX(0);filter:brightness(1)}}
    .battle-vs{font-size:1.7em;color:var(--red);font-weight:700;animation:vsPulse 1.7s ease-in-out infinite}
    @keyframes vsPulse{0%,100%{transform:scale(1);opacity:.78}50%{transform:scale(1.16);opacity:1;
        text-shadow:0 0 20px var(--red)}}
    .battle-name{font-size:.98em;color:#ffe9a8;font-weight:700;margin-bottom:3px;min-height:1.3em}
    .battle-sub{font-size:.72em;color:#8590a2;margin-bottom:7px;min-height:1.1em}
    .hp-bar{width:100%;height:16px;background:rgba(0,0,0,.55);border-radius:9px;overflow:hidden;
        border:1px solid rgba(232,180,74,.22)}
    .hp-fill{height:100%;width:100%;border-radius:9px;transition:width .3s ease;
        background:linear-gradient(90deg,#e94560,#ff8a6b);box-shadow:0 0 12px rgba(233,69,96,.65)}
    .hp-fill.foe{background:linear-gradient(90deg,#38a169,#7ddfa8);box-shadow:0 0 12px rgba(56,161,105,.65)}
    .hp-text{font-size:.72em;color:#8590a2;margin-top:5px;font-variant-numeric:tabular-nums}

    /* 卜卦面板 */
    .divine-panel{border:1px solid rgba(192,122,232,.34);border-radius:12px;padding:13px;margin:10px 0;
        background:linear-gradient(160deg,rgba(192,122,232,.13),rgba(0,0,0,.28));
        animation:panelIn .35s ease backwards}
    .divine-title{font-size:.9em;color:#e0c8f5;letter-spacing:.12em;margin-bottom:9px;text-align:center}
    .divine-title b{color:#ffe9a8;font-size:1.15em}
    .divine-row{display:flex;flex-wrap:wrap;justify-content:center;gap:6px}
    .divine-btn{padding:9px 14px;border-radius:9px;border:1px solid rgba(232,180,74,.35);cursor:pointer;
        background:linear-gradient(155deg,rgba(255,255,255,.09),rgba(0,0,0,.3));color:#dfe4ee;
        font-family:inherit;font-size:.84em;transition:all .2s}
    .divine-btn:hover:not(:disabled){border-color:var(--gold);transform:translateY(-2px);
        box-shadow:0 6px 16px rgba(232,180,74,.32)}
    .divine-btn:disabled{opacity:.34;cursor:not-allowed}
    .divine-result{text-align:center;font-size:.84em;margin-top:9px;min-height:1.3em}
    .tag-win{color:#5fd39a}.tag-lose{color:#ff8a96}

    /* 图鉴 */
    .codex-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:9px}
    .codex-item{position:relative;border-radius:10px;padding:6px 4px 5px;text-align:center;
        border:1px solid rgba(255,255,255,.09);background:rgba(0,0,0,.3);
        transition:transform .2s,box-shadow .25s;overflow:hidden}
    .codex-item:hover{transform:translateY(-3px)}
    .codex-item.locked{filter:grayscale(1) brightness(.36)}
    .codex-item svg{height:56px;width:auto;overflow:visible}
    .codex-item img{width:100%;height:76px;object-fit:contain;display:block;
        mix-blend-mode:lighten;border-radius:8px;
        filter:brightness(1.30) saturate(1.12) contrast(1.06)}
    .codex-name{font-size:.7em;color:#c8d0dd;margin-top:1px;letter-spacing:.02em}
    .codex-qi{font-size:.62em;color:#6f7a8b}
    .codex-item.unlocked.t6{box-shadow:0 0 14px rgba(232,180,74,.42);border-color:rgba(232,180,74,.5)}
    .codex-item.unlocked.t7{box-shadow:0 0 16px rgba(192,122,232,.5);border-color:rgba(192,122,232,.6)}

    /* 浮动文字 / 涟漪 / 横幅 */
    .float-text{position:fixed;pointer-events:none;z-index:10000;font-weight:700;font-size:1.3em;
        white-space:nowrap;transform:translate(-50%,-50%);
        animation:floatUp 1.2s cubic-bezier(.2,.8,.3,1) forwards}
    @keyframes floatUp{
        0%{opacity:0;transform:translate(-50%,-50%) scale(.4)}
        18%{opacity:1;transform:translate(-50%,-88%) scale(1.26)}
        40%{transform:translate(-50%,-112%) scale(1)}
        100%{opacity:0;transform:translate(-50%,-245%) scale(.85)}}
    .float-dmg{color:#ff8a8a;text-shadow:0 0 12px #e94560,0 2px 5px #000}
    .float-gold{color:#ffd76a;text-shadow:0 0 13px #e8b44a,0 2px 5px #000}
    .float-heal{color:#7ddfa8;text-shadow:0 0 13px #38a169,0 2px 5px #000}
    .float-crit{color:#fff2a8;font-size:1.75em;text-shadow:0 0 20px #ff8a4a,0 0 34px #e94560,0 2px 6px #000}
    .float-counter{color:#c4a0ff;text-shadow:0 0 16px #8b5cf6,0 2px 5px #000}
    .float-bad{color:#c07ae8;text-shadow:0 0 16px #7c3aed,0 2px 5px #000}

    .fuse-ring{position:fixed;width:20px;height:20px;border:3px solid var(--gold);border-radius:50%;
        pointer-events:none;z-index:9996;transform:translate(-50%,-50%);
        animation:ringExpand .78s ease-out forwards}
    @keyframes ringExpand{
        0%{width:20px;height:20px;opacity:1;border-width:6px}
        100%{width:340px;height:340px;opacity:0;border-width:1px}}

    .hatch-egg{position:fixed;z-index:9997;pointer-events:none;font-size:3.4rem;
        transform:translate(-50%,-50%);filter:drop-shadow(0 0 22px rgba(232,180,74,.85));
        animation:eggAppear .62s cubic-bezier(.34,1.56,.64,1)}
    @keyframes eggAppear{
        0%{opacity:0;transform:translate(-50%,-50%) scale(.1) rotate(-32deg)}
        62%{opacity:1;transform:translate(-50%,-50%) scale(1.24) rotate(10deg)}
        100%{opacity:1;transform:translate(-50%,-50%) scale(1) rotate(0)}}
    .hatch-egg.crack{animation:eggCrack .32s ease-in forwards}
    @keyframes eggCrack{
        0%{transform:translate(-50%,-50%) scale(1);filter:brightness(1)}
        26%{transform:translate(-50%,-50%) scale(1.32) rotate(-9deg);filter:brightness(2.6)}
        52%{transform:translate(-50%,-50%) scale(1.1) rotate(9deg);filter:brightness(3.2)}
        100%{transform:translate(-50%,-50%) scale(1.75);opacity:0;filter:brightness(4.4)}}

    .flying-clone{will-change:transform,opacity;box-shadow:0 0 30px rgba(232,180,74,.75)!important}

    .banner{position:fixed;left:50%;top:34%;transform:translate(-50%,-50%);z-index:10001;
        pointer-events:none;font-size:2.5em;font-weight:700;letter-spacing:.3em;text-align:center;
        animation:bannerPop 1.35s cubic-bezier(.2,.9,.3,1) forwards;white-space:nowrap}
    @keyframes bannerPop{
        0%{opacity:0;transform:translate(-50%,-50%) scale(.4) rotate(-6deg)}
        22%{opacity:1;transform:translate(-50%,-50%) scale(1.12) rotate(1.5deg)}
        34%{transform:translate(-50%,-50%) scale(1) rotate(0)}
        76%{opacity:1}
        100%{opacity:0;transform:translate(-50%,-88%) scale(1.04)}}
    .banner-win{color:#ffe9a8;text-shadow:0 0 22px #e8b44a,0 0 46px #ff8a4a,0 3px 8px #000}
    .banner-lose{color:#ff9aa5;text-shadow:0 0 22px #e94560,0 3px 8px #000}
    .banner-fail{color:#d9b3ff;text-shadow:0 0 24px #8b5cf6,0 0 46px #c07ae8,0 3px 8px #000}
    .banner-trib{color:#c9fff0;text-shadow:0 0 24px #3fd0b0,0 0 50px #63a9e8,0 3px 8px #000}

    .shake{animation:screenShake .42s cubic-bezier(.36,.07,.19,.97)}
    @keyframes screenShake{
        10%{transform:translate(-5px,2px)}20%{transform:translate(6px,-3px)}
        30%{transform:translate(-7px,1px)}40%{transform:translate(5px,3px)}
        55%{transform:translate(-4px,-2px)}70%{transform:translate(3px,2px)}
        85%{transform:translate(-2px,0)}100%{transform:translate(0,0)}}

    .hint{font-size:.76em;color:#6f7a8b;margin-top:9px;line-height:1.6}
    .hint b{color:#c8d0dd}
    .empty-note{color:#6f7a8b;padding:22px;text-align:center;grid-column:1/-1}

    .legend{display:flex;flex-wrap:wrap;gap:6px;font-size:.72em;color:#8590a2;margin-top:8px;align-items:center}
    .legend-chip{padding:2px 8px;border-radius:8px;border:1px solid currentColor}

    @media (max-width:560px){
        .game-title{font-size:2em}
        .guchong-grid{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}
        .gu-figure{height:120px}
        .battle-side .gu-figure{height:96px}
        .banner{font-size:1.7em}
    }
"""

# ==================================================== 游戏脚本 ==============
SCRIPT_BODY = r"""
/* ==================== 五行与克制 ==================== */
const ELEMS = ['金','木','水','火','土'];
/* 相克环：金克木、木克土、土克水、水克火、火克金 */
const ELEM_INFO = {
    '金': { color:'#d8c98a', deep:'#8f7f3f', key:'metal',  strong:'木', weak:'火' },
    '木': { color:'#5fc98a', deep:'#2f7a52', key:'wood',   strong:'土', weak:'金' },
    '水': { color:'#63a9e8', deep:'#2b6096', key:'water',  strong:'火', weak:'土' },
    '火': { color:'#ff8a4a', deep:'#a83f18', key:'fire',   strong:'金', weak:'水' },
    '土': { color:'#d8b878', deep:'#8a6a30', key:'earth',  strong:'水', weak:'木' },
    '混沌':{ color:'#c07ae8', deep:'#6b2f9e', key:'primal', strong:null, weak:null }
};
const ELEM_ADV = 1.5;    /* 克制倍率 */
const ELEM_DIS = 0.65;   /* 被克倍率 */

/* ==================== 物种图鉴（五行各四阶 + 混沌） ==================== */
/* tier: 1凡虫 2灵虫 3古兽 6神兽 7混沌神兽 */
const SPECIES = [
    /* 金 */
    { id:'m1', name:'铁背蜈',  elem:'金', tier:1, power:1.00, w:52, focus:'攻击', form:'milli',  note:'甲胄初成，性喜噬铁。' },
    { id:'m2', name:'金甲蝎',  elem:'金', tier:2, power:1.10, w:6,  focus:'防御', form:'scorp',  note:'尾钩含金精，破甲如纸。' },
    { id:'m3', name:'白螭',    elem:'金', tier:3, power:1.30, w:1,  focus:'速度', form:'serp',   note:'无角之龙，游走如电。' },
    { id:'m6', name:'金翅大鹏',elem:'金', tier:6, power:1.70, w:0,  focus:'攻击', form:'roc',    note:'振翅九万里，爪裂山河。' },
    /* 木 */
    { id:'w1', name:'茧蚕',    elem:'木', tier:1, power:1.00, w:52, focus:'防御', form:'worm',   note:'吐丝自缚，静待化形。' },
    { id:'w2', name:'青螳',    elem:'木', tier:2, power:1.10, w:6,  focus:'攻击', form:'mantis', note:'双刃凝青木之气。' },
    { id:'w3', name:'万古藤蟒',elem:'木', tier:3, power:1.30, w:1,  focus:'毒力', form:'serp',   note:'身缠万年藤，毒浸骨髓。' },
    { id:'w6', name:'建木苍龙',elem:'木', tier:6, power:1.70, w:0,  focus:'灵性', form:'dragon', note:'栖于建木之巅，通晓百草。' },
    /* 水 */
    { id:'s1', name:'幽泉蛭',  elem:'水', tier:1, power:1.00, w:52, focus:'毒力', form:'worm',   note:'生于阴泉，嗜血为生。' },
    { id:'s2', name:'玄水母',  elem:'水', tier:2, power:1.10, w:6,  focus:'灵性', form:'jelly',  note:'触须含玄水，触之则寒。' },
    { id:'s3', name:'冰蜮',    elem:'水', tier:3, power:1.30, w:1,  focus:'速度', form:'toad',   note:'射影含沙，寒毒入骨。' },
    { id:'s6', name:'玄武蛊',  elem:'水', tier:6, power:1.70, w:0,  focus:'防御', form:'turtle', note:'龟蛇交缠，不动如山。' },
    /* 火 */
    { id:'f1', name:'赤焰蚁',  elem:'火', tier:1, power:1.00, w:52, focus:'速度', form:'ant',    note:'群居焦土，性烈如火。' },
    { id:'f2', name:'焚天蝶',  elem:'火', tier:2, power:1.10, w:6,  focus:'灵性', form:'moth',   note:'翅上火星，可焚原野。' },
    { id:'f3', name:'焱麒麟',  elem:'火', tier:3, power:1.30, w:1,  focus:'攻击', form:'qilin',  note:'蹄下生焱，仁而好斗。' },
    { id:'f6', name:'朱雀蛊',  elem:'火', tier:6, power:1.70, w:0,  focus:'攻击', form:'roc',    note:'南离之精，浴火重生。' },
    /* 土 */
    { id:'e1', name:'食土蚯',  elem:'土', tier:1, power:1.00, w:52, focus:'防御', form:'worm',   note:'吞泥化石，皮坚如岩。' },
    { id:'e2', name:'岩背蛛',  elem:'土', tier:2, power:1.10, w:6,  focus:'毒力', form:'spider', note:'背负岩壳，网如石锁。' },
    { id:'e3', name:'山岳龟',  elem:'土', tier:3, power:1.30, w:1,  focus:'防御', form:'turtle', note:'负山而行，寿逾千载。' },
    { id:'e6', name:'麒麟蛊',  elem:'土', tier:6, power:1.70, w:0,  focus:'防御', form:'qilin',  note:'中土瑞兽，践土成春。' },
    /* 混沌 */
    { id:'x7', name:'混沌蛊',  elem:'混沌', tier:7, power:2.05, w:0, focus:'灵性', form:'dragon', note:'无形无相，吞五行而归一。' }
];
const SPECIES_BY_ID = {};
SPECIES.forEach(s => { SPECIES_BY_ID[s.id] = s; });
const OBTAINABLE = SPECIES.filter(s => s.w > 0);
const HATCH_TOTAL_W = OBTAINABLE.reduce((a, s) => a + s.w, 0);
const TIER_LABEL = { 1:'凡虫', 2:'灵虫', 3:'古兽', 6:'神兽', 7:'混沌神兽' };

/* ==================== 品质 ==================== */
const QUALITIES = [
    { name:'凡品', mult:1.00 },
    { name:'良品', mult:1.28 },
    { name:'精品', mult:1.60 },
    { name:'绝品', mult:2.00 },
    { name:'灵品', mult:2.50 },
    { name:'仙品', mult:3.10 }
];
const QI_PREFIX = ['', '灵', '玄', '幽冥', '天罡', '太古'];

/* ==================== 天赋 ==================== */
const TALENTS = [
    { id:'dusha',  name:'毒煞',   icon:'☠', color:'#c4a0ff', desc:'攻击 +28%，出手自带瘴气' },
    { id:'tieja',  name:'铁甲',   icon:'⛨', color:'#7ddfa8', desc:'防御 +36%，气血 +12%' },
    { id:'jifeng', name:'疾风',   icon:'⚡', color:'#7fc0ff', desc:'速度 +40%，先手更稳' },
    { id:'tongling',name:'通灵',  icon:'✦', color:'#ffd98a', desc:'灵性 +30%，克制伤害额外 +18%' },
    { id:'bumie',  name:'不灭',   icon:'❤', color:'#ff8a96', desc:'每回合回复 4% 气血' },
    { id:'huaxing',name:'化形',   icon:'☯', color:'#e0c8f5', desc:'融合成功率 +14%' },
    { id:'chunyang',name:'纯阳',  icon:'☀', color:'#ffb35c', desc:'同属性融合成功率 +20%，品质晋升更易' },
    { id:'tianji', name:'天机',   icon:'卦', color:'#a9f0dd', desc:'卜卦猜中时伤害加成由 15% 提升至 35%' }
];
const TALENT_BY_ID = {};
TALENTS.forEach(t => { TALENT_BY_ID[t.id] = t; });

/* ==================== 常量 ==================== */
const ATTRS = ['攻击','毒力','防御','速度','灵性'];
const ATTR_SHORT = { '攻击':'攻','毒力':'毒','防御':'防','速度':'速','灵性':'灵' };
const MAX_GU = 12;
const HATCH_COST = 20;
const FUSE_COST = 10;
const SOOTHE_COST = 15;      /* 安抚消耗灵液 */
const LOYAL_MAX = 100;
const LOYAL_INIT = 75;
const LOYAL_REBEL = 30;      /* 低于此值败北可能反叛 */
const STREAK_STEP = 0.06;    /* 每连胜一场的属性加成 */
const STREAK_CAP = 10;       /* 计入加成的连胜上限（10×6% = 60%） */
const SPIRIT_MAX = 99999;
const SAVE_KEY = 'wanguzhiwang_save_v2';
const MAX_LOG = 70;
const MAX_PARTICLES = 700;
const MAX_ROUND = 15;

/* ==================== 工具 ==================== */
const $ = id => document.getElementById(id);
const rnd = (a,b) => a + Math.random()*(b-a);
const ri = (a,b) => Math.floor(rnd(a,b+1));
const pick = arr => arr[Math.floor(Math.random()*arr.length)];
const clamp = (v,a,b) => Math.max(a, Math.min(b, v));
const sleep = ms => new Promise(r => setTimeout(r, ms));
const qiName = i => (QUALITIES[i] || QUALITIES[0]).name;
const expNeed = lv => 34 + lv*26;
const pct = v => Math.round(v*100) + '%';

function elemOf(g){ return ELEM_INFO[g.elem] || ELEM_INFO['混沌']; }
function speciesOf(g){ return SPECIES_BY_ID[g.species] || SPECIES[0]; }
/* 克制倍率：攻方属性 对 守方属性 */
function counterMult(atkElem, defElem){
    const a = ELEM_INFO[atkElem], d = ELEM_INFO[defElem];
    if(!a || !d) return 1;
    if(atkElem === '混沌' || defElem === '混沌') return 1;
    if(a.strong === defElem) return ELEM_ADV;
    if(a.weak === defElem) return ELEM_DIS;
    return 1;
}

/* ==================== 粒子系统 ==================== */
const fxCanvas = $('fx');
const fxCtx = fxCanvas.getContext('2d');
let particles = [];
let fxRunning = false;
let ambientOn = true;
const dpr = Math.min(1.5, window.devicePixelRatio || 1);

function resizeCanvas(){
    fxCanvas.width = Math.floor(window.innerWidth*dpr);
    fxCanvas.height = Math.floor(window.innerHeight*dpr);
    fxCanvas.style.width = window.innerWidth + 'px';
    fxCanvas.style.height = window.innerHeight + 'px';
    fxCtx.setTransform(dpr,0,0,dpr,0,0);
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

function spawnParticles(x,y,o){
    o = o || {};
    const count = o.count || 18;
    const colors = o.colors || ['#e8b44a','#ffe9a8','#ffffff'];
    const speed = o.speed || 3, size = o.size || 4;
    const spread = o.spread === undefined ? Math.PI*2 : o.spread;
    const angle = o.angle || 0;
    const gravity = o.gravity === undefined ? 0.07 : o.gravity;
    const life = o.life || 48;
    const shape = o.shape || 'circle';

    if(particles.length > MAX_PARTICLES) return;
    for(let i=0;i<count;i++){
        const a = angle + (Math.random()-0.5)*spread;
        const sp = speed*(0.4 + Math.random()*0.95);
        particles.push({
            x, y, vx:Math.cos(a)*sp, vy:Math.sin(a)*sp,
            size: size*(0.5 + Math.random()),
            color: colors[Math.floor(Math.random()*colors.length)],
            life: life*(0.6 + Math.random()*0.75),
            maxLife: life, gravity, shape,
            rot: Math.random()*Math.PI, vr:(Math.random()-0.5)*0.36
        });
    }
    startFx();
}
/* 灵气上升：修仙主题的常驻氛围 */
function spawnQiWisps(x,y,o){
    o = o || {};
    const count = o.count || 6;
    const colors = o.colors || ['#3fd0b0','#a9f0dd','#e8b44a','#ffffff'];
    if(particles.length > MAX_PARTICLES) return;
    for(let i=0;i<count;i++){
        particles.push({
            x: x + rnd(-14,14), y: y + rnd(-6,6),
            vx: rnd(-0.35,0.35), vy: rnd(-1.5,-0.6),
            size: rnd(1.6,4.0), color: colors[Math.floor(Math.random()*colors.length)],
            life: rnd(60,130), maxLife:130, gravity:-0.006, shape:'wisp',
            rot:0, vr:rnd(-0.03,0.03)
        });
    }
    startFx();
}
function startFx(){ if(fxRunning) return; fxRunning = true; requestAnimationFrame(fxLoop); }

function fxLoop(){
    fxCtx.clearRect(0,0,window.innerWidth,window.innerHeight);
    for(let i=particles.length-1;i>=0;i--){
        const p = particles[i];
        p.x += p.vx; p.y += p.vy;
        p.vy += p.gravity;
        p.vx *= 0.986; p.vy *= 0.986;
        p.rot += p.vr;
        p.life--;
        if(p.life <= 0){ particles.splice(i,1); continue; }
        const alpha = Math.min(1, p.life/(p.maxLife*0.55));
        fxCtx.globalAlpha = alpha;
        fxCtx.fillStyle = p.color;
        if(p.shape === 'star'){
            drawStar(fxCtx,p.x,p.y,5,p.size,p.size*0.42,p.rot);
        } else if(p.shape === 'wisp'){
            fxCtx.beginPath();
            fxCtx.arc(p.x,p.y,p.size*0.55,0,Math.PI*2);
            fxCtx.fill();
            fxCtx.globalAlpha = alpha*0.28;
            fxCtx.beginPath();
            fxCtx.arc(p.x,p.y,p.size*1.7,0,Math.PI*2);
            fxCtx.fill();
        } else if(p.shape === 'square'){
            fxCtx.save(); fxCtx.translate(p.x,p.y); fxCtx.rotate(p.rot);
            fxCtx.fillRect(-p.size/2,-p.size/2,p.size,p.size); fxCtx.restore();
        } else if(p.shape === 'shard'){
            fxCtx.save(); fxCtx.translate(p.x,p.y); fxCtx.rotate(p.rot);
            fxCtx.beginPath();
            fxCtx.moveTo(0,-p.size); fxCtx.lineTo(p.size*0.42,0);
            fxCtx.lineTo(0,p.size); fxCtx.lineTo(-p.size*0.42,0);
            fxCtx.closePath(); fxCtx.fill(); fxCtx.restore();
        } else {
            fxCtx.beginPath(); fxCtx.arc(p.x,p.y,p.size/2,0,Math.PI*2); fxCtx.fill();
        }
    }
    fxCtx.globalAlpha = 1;
    if(particles.length > 0){
        requestAnimationFrame(fxLoop);
    } else {
        fxRunning = false;
        fxCtx.clearRect(0,0,window.innerWidth,window.innerHeight);
    }
}

function drawStar(ctx,x,y,spikes,outer,inner,rot){
    const step = Math.PI/spikes;
    ctx.beginPath();
    ctx.moveTo(x + Math.cos(rot)*outer, y + Math.sin(rot)*outer);
    for(let i=0;i<spikes;i++){
        ctx.lineTo(x + Math.cos(rot + i*2*step + step)*inner, y + Math.sin(rot + i*2*step + step)*inner);
        ctx.lineTo(x + Math.cos(rot + (i+1)*2*step)*outer, y + Math.sin(rot + (i+1)*2*step)*outer);
    }
    ctx.closePath(); ctx.fill();
}

/* 常驻灵气微尘 */
function ambientTick(){
    if(!ambientOn || document.hidden) return;
    if(particles.length < 60 && Math.random() < 0.5){
        spawnQiWisps(rnd(0,window.innerWidth), window.innerHeight + 10,
            { count:1, colors:['#3fd0b0','#a9f0dd'] });
    }
}

/* ==================== 浮动文字 / 涟漪 / 横幅 / 震屏 ==================== */
function spawnFloatText(x,y,text,cls,scale){
    const el = document.createElement('div');
    el.className = 'float-text ' + (cls || '');
    el.textContent = text;
    el.style.left = x + 'px';
    el.style.top = y + 'px';
    if(scale) el.style.fontSize = (1.3*scale) + 'em';
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 1300);
}
function spawnRing(x,y,color){
    const el = document.createElement('div');
    el.className = 'fuse-ring';
    el.style.left = x + 'px';
    el.style.top = y + 'px';
    if(color) el.style.borderColor = color;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 820);
}
function spawnBanner(text, cls){
    const el = document.createElement('div');
    el.className = 'banner ' + (cls || 'banner-win');
    el.textContent = text;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 1400);
}
function shakeScreen(){
    document.body.classList.remove('shake');
    void document.body.offsetWidth;
    document.body.classList.add('shake');
    setTimeout(() => document.body.classList.remove('shake'), 440);
}
function pulseEl(el){
    if(!el) return;
    el.classList.remove('pulse');
    void el.offsetWidth;
    el.classList.add('pulse');
    setTimeout(() => el.classList.remove('pulse'), 540);
}
function centerOf(el){
    const r = el.getBoundingClientRect();
    return { x:r.left + r.width/2, y:r.top + r.height/2, r };
}

/* ==================== 状态 ==================== */
const state = {
    version: 2,
    spirit: 120,
    guchongs: [],
    selected: [],
    totalBattles: 0,
    wins: 0,
    logs: [],
    nextId: 1,
    codex: {},
    pity: 0,           /* 连续未出古兽计数 */
    fuseFail: 0,       /* 连续融合失败计数（梯度保底） */
    savedAt: Date.now()
};
let busy = false;
let awaitingDivine = false;

/* ==================== 生成蛊虫 ==================== */
function rollSpecies(forceTier){
    if(forceTier){
        const pool = SPECIES.filter(s => s.tier === forceTier && s.w > 0);
        if(pool.length) return pick(pool);
    }
    /* 保底：连抽 25 次未得古兽，则必出 */
    if(state.pity >= 25){
        state.pity = 0;
        return pick(SPECIES.filter(s => s.tier === 3));
    }
    let r = Math.random()*HATCH_TOTAL_W;
    for(const s of OBTAINABLE){
        r -= s.w;
        if(r <= 0){ state.pity = (s.tier >= 3) ? 0 : state.pity + 1; return s; }
    }
    state.pity++;
    return OBTAINABLE[0];
}

function rollTalent(bonus){
    const chance = 0.24 + (bonus || 0);
    if(Math.random() > chance) return null;
    return pick(TALENTS).id;
}

function baseAttrs(sp, qi, level, focusBonus){
    const mult = QUALITIES[qi].mult * sp.power * (1 + (level-1)*0.08);
    const out = {};
    ATTRS.forEach(k => {
        let v = rnd(9,14)*mult;
        if(k === sp.focus) v *= (1 + (focusBonus === undefined ? 0.55 : focusBonus));
        out[k] = Math.max(1, Math.round(v));
    });
    return out;
}

function genGuchong(sp, qi, level, talentId){
    qi = clamp(qi, 0, QUALITIES.length-1);
    level = clamp(level, 1, 99);
    const g = {
        id: 'gc' + (state.nextId++),
        species: sp.id,
        elem: sp.elem,
        tier: sp.tier,
        form: sp.form,
        base: sp.name,
        name: QI_PREFIX[qi] + sp.name,
        qi: qi,
        level: level,
        exp: 0,
        wins: 0,
        loyal: LOYAL_INIT,
        streak: 0,
        best: 0,
        talent: talentId === undefined ? rollTalent(0) : talentId
    };
    Object.assign(g, baseAttrs(sp, qi, level));
    return g;
}

function applyTalentBase(g){
    if(g.talent === 'dusha')  g.攻击 = Math.round(g.攻击*1.28);
    if(g.talent === 'tieja'){ g.防御 = Math.round(g.防御*1.36); g.hpSeed = 1.12; }
    if(g.talent === 'jifeng') g.速度 = Math.round(g.速度*1.40);
    if(g.talent === 'tongling') g.灵性 = Math.round(g.灵性*1.30);
}

function maxHp(g){
    const seed = (g.talent === 'tieja') ? 1.12 : 1;
    const base = (120 + g.防御*2.4 + g.level*9 + g.毒力*1.5) * seed;
    return Math.round(base * (1 + streakBonus(g)));
}

/* ==================== 日志 ==================== */
function addLog(msg, cls){
    state.logs.push({ msg:msg, cls:cls || 'log-info' });
    if(state.logs.length > MAX_LOG) state.logs.shift();
    renderLog();
}
function renderLog(){
    const box = $('log');
    if(!box) return;
    box.innerHTML = state.logs.map(l =>
        '<div class="log-entry ' + l.cls + '">' + l.msg + '</div>').join('');
    box.scrollTop = box.scrollHeight;
}

/* ==================== 渲染 ==================== */
function render(){
    $('spirit').textContent = Math.floor(state.spirit);
    $('count').textContent = state.guchongs.length + '/' + MAX_GU;
    $('record').textContent = state.wins + '/' + state.totalBattles;
    renderGrid();
    renderCodex();
    updateButtons();
}

function updateButtons(){
    $('btn-hatch').disabled = busy;
    $('btn-fuse').disabled = busy || state.selected.length !== 2;
    $('btn-clear').disabled = busy || state.selected.length === 0;
    $('btn-battle').disabled = busy || state.selected.length !== 1;
    $('btn-soothe').disabled = busy || state.selected.length !== 1;
}

function renderGrid(){
    const grid = $('grid');
    if(state.guchongs.length === 0){
        grid.innerHTML = '<div class="empty-note">巢穴空空如也，先孵化一只蛊虫吧</div>';
        return;
    }
    const maxAttr = Math.max(12, ...state.guchongs.map(g =>
        Math.max.apply(null, ATTRS.map(k => g[k] || 0))));
    grid.innerHTML = state.guchongs.map(g => cardHTML(g, maxAttr)).join('');
}

function talentLine(g){
    const t = TALENT_BY_ID[g.talent];
    if(!t) return '<div class="talent-line none">◇ 未觉醒天赋</div>';
    return '<div class="talent-line" style="color:' + t.color + '">' + t.icon + ' ' +
        t.name + '<span style="color:#9aa5b6;font-size:.86em">（' + t.desc + '）</span></div>';
}

function cardHTML(g, maxAttr){
    const sel = state.selected.includes(g.id);
    const sp = speciesOf(g);
    const q = qiName(g.qi);
    const ei = elemOf(g);
    const tier = TIER_LABEL[g.tier] || '';
    const loy = loyaltyOf(g);
    const ls = loyaltyState(g);
    const streak = g.streak || 0;
    const bonus = streakBonus(g);
    const bPct = Math.round(bonus*100);
    return '' +
    '<div class="guchong-card qi-' + g.qi + ' tier-' + g.tier + (sel ? ' selected' : '') +
        (streak >= 3 ? ' has-streak' : '') + (loy < LOYAL_REBEL ? ' low-loyal' : '') +
        '" data-id="' + g.id + '">' +
        '<div class="guchong-lv">Lv.' + g.level + '</div>' +
        '<div class="tier-tag t' + g.tier + '">' + tier + '</div>' +
        (streak >= 2 ? '<div class="streak-badge">连胜 ' + streak + '</div>' : '') +
        '<div class="gu-figure">' + figureHTML(g) + '</div>' +
        '<div class="guchong-head">' +
            '<span class="guchong-name">' + g.name + '</span>' +
            '<span class="elem-tag" style="color:' + ei.color + '">' + g.elem + '</span>' +
            '<span class="qi-tag">' + q + '</span>' +
        '</div>' +
        talentLine(g) +
        '<div class="loyal-row ' + ls.cls + '">' +
            '<span class="loyal-label">忠心</span>' +
            '<div class="loyal-bar"><div class="loyal-fill" style="width:' + loy + '%"></div></div>' +
            '<span class="loyal-val">' + loy + ' · ' + ls.label + '</span>' +
        '</div>' +
        (bPct > 0 ? '<div class="streak-row">不败信念 +' + bPct + '% 属性' +
            (streak > STREAK_CAP ? '（已封顶）' : '') + '</div>' : '') +
        '<div class="guchong-attrs">' +
            ATTRS.map(k =>
                '<div class="attr-bar">' +
                    '<span class="attr-label">' + ATTR_SHORT[k] + '</span>' +
                    '<div class="attr-progress"><div class="attr-fill attr-' + k +
                        '" style="width:' + Math.min(100,(g[k]/maxAttr)*100) + '%"></div></div>' +
                    '<span class="attr-value">' + g[k] +
                        (bonus ? '<i class="buffed">+' + Math.round(g[k]*bonus) + '</i>' : '') + '</span>' +
                '</div>').join('') +
        '</div>' +
        '<div class="guchong-exp">经验 ' + g.exp + '/' + expNeed(g.level) +
            ' · 胜场 ' + g.wins + ' · 气血 ' + maxHp(g) + '</div>' +
    '</div>';
}

function markCardEnter(id){
    requestAnimationFrame(() => {
        const el = document.querySelector('.guchong-card[data-id="' + id + '"]');
        if(el) el.classList.add('card-enter');
    });
}

/* ==================== 插图：立绘（配图优先，回退程序化 SVG） ==================== */
const USE_IMAGES = __USE_IMAGES__;
const IMG_EXT = '__IMG_EXT__';
const IMG_DIR = 'assets/gu/';

/* 统一入口：有配图返回 <img>，否则回退程序化 SVG，调用方不必关心 */
function figureHTML(g, small){
    const sp = speciesOf(g);
    if(USE_IMAGES && sp){
        const file = (small ? 'sm_' : '') + sp.id + '.' + IMG_EXT;
        return '<img class="gu-img t' + g.tier + '" src="' + IMG_DIR + file +
            '" alt="' + sp.name + '" loading="lazy" draggable="false">';
    }
    return guchongSVG(g);
}

/* ==================== 插图：程序化 SVG 图腾（回退方案） ==================== */
function guchongSVG(g, scale){
    const sp = speciesOf(g);
    const ei = elemOf(g);
    const colors = defsFor(g);
    const body = formBody(sp.form, colors, g);
    const aura = auraMarkup(g, ei, colors);
    const sway = (g.id ? hashStr(g.id) : hashStr(sp.id)) % 90;
    return '' +
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" ' +
        'class="gu-svg t' + g.tier + '" style="animation-delay:-' + sway + 'ms">' +
        '<defs>' +
            '<radialGradient id="' + g.id + '_body" cx="42%" cy="32%" r="72%">' +
                '<stop offset="0%" stop-color="' + colors.light + '"/>' +
                '<stop offset="62%" stop-color="' + ei.color + '"/>' +
                '<stop offset="100%" stop-color="' + colors.deep + '"/>' +
            '</radialGradient>' +
            '<radialGradient id="' + g.id + '_aura">' +
                '<stop offset="0%" stop-color="' + colors.light + '" stop-opacity=".55"/>' +
                '<stop offset="55%" stop-color="' + ei.color + '" stop-opacity=".22"/>' +
                '<stop offset="100%" stop-color="' + ei.color + '" stop-opacity="0"/>' +
            '</radialGradient>' +
            '<linearGradient id="' + g.id + '_edge" x1="0" y1="0" x2="0" y2="1">' +
                '<stop offset="0%" stop-color="' + colors.light + '" stop-opacity=".95"/>' +
                '<stop offset="100%" stop-color="' + colors.deep + '" stop-opacity=".35"/>' +
            '</linearGradient>' +
        '</defs>' +
        aura +
        '<g filter="none">' + body + '</g>' +
        eyeMarkup(g, colors) +
    '</svg>';
}

function hashStr(s){
    let h = 0;
    for(let i=0;i<s.length;i++) h = (h*31 + s.charCodeAt(i)) & 0xffffff;
    return h;
}
/* 同物种同色相，个体之间微扰 */
function defsFor(g){
    const ei = elemOf(g);
    const base = hexToRgb(ei.color);
    const seed = hashStr(g.id || g.species);
    const d = ((seed % 15) - 7) * 0.012;
    const jitter = c => clamp(Math.round(c*(1+d) + ((seed>>3)%11) - 5), 0, 255);
    const body = { r:jitter(base.r), g:jitter(base.g), b:jitter(base.b) };
    const light = { r:clamp(base.r+70,0,255), g:clamp(base.g+70,0,255), b:clamp(base.b+70,0,255) };
    const deep = { r:Math.round(base.r*0.45), g:Math.round(base.g*0.45), b:Math.round(base.b*0.45) };
    return {
        light: rgbToHex(light), deep: rgbToHex(deep), body: rgbToHex(body)
    };
}
function hexToRgb(h){
    const v = h.replace('#','');
    return { r:parseInt(v.substr(0,2),16), g:parseInt(v.substr(2,2),16), b:parseInt(v.substr(4,2),16) };
}
function rgbToHex(c){
    const f = n => ('0' + clamp(n,0,255).toString(16)).slice(-2);
    return '#' + f(c.r) + f(c.g) + f(c.b);
}

function auraMarkup(g, ei, colors){
    const t = g.tier;
    if(t < 3) return '';
    const rings = t >= 6 ? 3 : 2;
    let out = '';
    for(let i=0;i<rings;i++){
        const r = 44 + i*8;
        const dur = (t >= 6 ? 7 : 11) + i*2;
        out += '<circle cx="60" cy="60" r="' + r + '" fill="none" stroke="' + colors.light +
            '" stroke-opacity="' + (t >= 6 ? 0.34 : 0.2) + '" stroke-width="' + (t >= 6 ? 1.5 : 1) +
            '" stroke-dasharray="' + (t >= 6 ? '10 8' : '6 12') + '">' +
            '<animateTransform attributeName="transform" type="rotate" ' +
            'from="0 60 60" to="' + (i%2 ? '-' : '') + '360 60 60" dur="' + dur + 's" repeatCount="indefinite"/>' +
            '</circle>';
    }
    out += '<ellipse cx="60" cy="60" rx="50" ry="50" fill="url(#' + g.id + '_aura)">' +
        '<animate attributeName="rx" values="46;52;46" dur="' + (t >= 6 ? 3.4 : 5) + 's" repeatCount="indefinite"/>' +
        '<animate attributeName="ry" values="46;52;46" dur="' + (t >= 6 ? 3.4 : 5) + 's" repeatCount="indefinite"/>' +
        '</ellipse>';
    return out;
}

/* 通用部件 */
function legs(count, colors, y0, y1, spread, width){
    let out = '';
    for(let i=0;i<count;i++){
        const t = count === 1 ? 0.5 : i/(count-1);
        const x = 26 + t*68;
        const y = y0 + t*(y1-y0);
        const len = spread*(0.7 + 0.5*Math.sin(t*Math.PI));
        out += '<path d="M ' + x.toFixed(1) + ' ' + y.toFixed(1) +
            ' q ' + (-len*0.5).toFixed(1) + ' ' + (len*0.5).toFixed(1) +
            ' ' + (-len).toFixed(1) + ' ' + (len*0.85).toFixed(1) + '" ' +
            'stroke="' + colors.deep + '" stroke-width="' + width + '" fill="none" stroke-linecap="round">' +
            '<animateTransform attributeName="transform" type="rotate" ' +
            'values="-2 ' + x.toFixed(1) + ' ' + y.toFixed(1) + ';2 ' + x.toFixed(1) + ' ' + y.toFixed(1) +
            ';-2 ' + x.toFixed(1) + ' ' + y.toFixed(1) + '" dur="' + (1.8 + t*0.7).toFixed(2) +
            's" repeatCount="indefinite"/></path>';
    }
    return out;
}
function eyes(colors, cx, cy, n, r, glow){
    let out = '';
    for(let i=0;i<n;i++){
        const x = cx + (i - (n-1)/2) * (r*3.1);
        out += '<circle cx="' + x.toFixed(1) + '" cy="' + cy + '" r="' + r + '" fill="#0a0c12"/>' +
            '<circle cx="' + x.toFixed(1) + '" cy="' + cy + '" r="' + (r*0.55) + '" fill="' + glow + '">' +
            '<animate attributeName="opacity" values="1;.35;1" dur="' + (2.4 + i*0.4).toFixed(1) +
            's" repeatCount="indefinite"/></circle>';
    }
    return out;
}
function coreMark(colors, r){
    return '<circle cx="60" cy="66" r="' + r + '" fill="' + colors.light + '" fill-opacity=".85">' +
        '<animate attributeName="r" values="' + (r-1) + ';' + (r+1.6) + ';' + (r-1) +
        '" dur="2.6s" repeatCount="indefinite"/></circle>';
}

function formBody(form, c, g){
    const fill = 'url(#' + g.id + '_body)';
    const edge = 'url(#' + g.id + '_edge)';
    switch(form){
        case 'worm':
            /* 环节虫：分节体节 + 侧足 + 前端头壳 */
            return legs(7, c, 54, 80, 10, 2.2) +
                '<path d="M24 64 q8-18 36-18 q28 0 36 18 q-8 18-36 18 q-28 0-36-18 Z" fill="' + fill +
                '" stroke="' + c.light + '" stroke-opacity=".28" stroke-width="1"/>' +
                '<g stroke="' + edge + '" stroke-opacity=".62" stroke-width="1.6" fill="none">' +
                '<path d="M42 47 q4 17 0 34"/><path d="M56 46 q4 18 0 36"/>' +
                '<path d="M70 46 q4 18 0 36"/><path d="M84 47 q4 17 0 34"/></g>' +
                headCap(c, fill, 36, 64, 16, 14);
        case 'spider':
            /* 蛛：头胸 + 腹 + 八足 + 螯肢 */
            return '<g>' + legs(4, c, 50, 64, 20, 2.4) + legs(4, c, 84, 88, 20, 2.4) + '</g>' +
                '<path d="M40 66 q0-18 22-18 q22 0 22 18 q0 18-22 18 q-22 0-22-18 Z" fill="' + fill +
                '" stroke="' + c.light + '" stroke-opacity=".28" stroke-width="1"/>' +
                '<ellipse cx="60" cy="68" rx="9" ry="6" fill="' + c.deep + '" fill-opacity=".32"/>' +
                '<path d="M42 54 q-9-8-16-9 M78 54 q9-8 16-9" stroke="' + c.deep +
                '" stroke-width="2.4" fill="none" stroke-linecap="round"/>' +
                '<path d="M48 50 q-5-7-11-8 M72 50 q5-7 11-8" stroke="' + c.light +
                '" stroke-width="2" fill="none" stroke-opacity=".6" stroke-linecap="round"/>';
        case 'ant':
            /* 蚁：头 + 胸 + 腹 + 触角 */
            return legs(3, c, 50, 80, 13, 2.6) +
                '<ellipse cx="78" cy="66" rx="20" ry="16" fill="' + fill + '" stroke="' + c.light +
                '" stroke-opacity=".28" stroke-width="1"/>' +
                '<ellipse cx="56" cy="66" rx="9" ry="8" fill="' + c.deep + '" fill-opacity=".85"/>' +
                headCap(c, fill, 34, 64, 13, 12) +
                '<path d="M26 56 q-10-10-18-12 M26 72 q-10 8-18 10" stroke="' + c.light +
                '" stroke-width="1.8" fill="none" stroke-opacity=".72" stroke-linecap="round"/>';
        case 'scorp':
            /* 蝎：前螯 + 环节尾 + 尾针 */
            return legs(4, c, 58, 78, 12, 2.4) +
                '<path d="M42 60 q16-14 36-8 q20 6 14 20 q-6 14-24 10 q-20-4-26-22 Z" fill="' + fill +
                '" stroke="' + c.light + '" stroke-opacity=".28" stroke-width="1"/>' +
                '<path d="M44 56 q-10-8-20-6 M42 74 q-10 6-20 6" stroke="' + c.deep +
                '" stroke-width="4" fill="none" stroke-linecap="round"/>' +
                '<path d="M88 64 q12-16 4-28 q-8-12-24-8" stroke="' + c.deep + '" stroke-width="3.6" ' +
                'fill="none" stroke-linecap="round"/>' +
                '<path d="M66 24 l16 3 l-9 11 Z" fill="' + c.light + '" fill-opacity=".9">' +
                '<animateTransform attributeName="transform" type="rotate" values="-6 66 24;6 66 24;-6 66 24" ' +
                'dur="2.4s" repeatCount="indefinite"/></path>' +
                headCap(c, fill, 36, 60, 13, 12);
        case 'milli':
            /* 蜈蚣：甲片体节 + 颚肢 + 前端小头壳（头部不得再叠眼睛图层） */
            return legs(8, c, 48, 82, 12, 2.4) +
                '<path d="M26 60 q6-16 34-16 q28 0 34 16 q-6 16-34 16 q-28 0-34-16 Z" fill="' + fill +
                '" stroke="' + c.light + '" stroke-opacity=".28" stroke-width="1"/>' +
                segPlate(c) +
                '<path d="M34 46 q-10-6-18-12 M86 46 q10-6 18-12" stroke="' + c.deep +
                '" stroke-width="2.4" fill="none" stroke-linecap="round"/>' +
                headCap(c, fill, 33, 60, 13, 11);
        case 'mantis':
            /* 螳螂：三角头 + 前臂镰刀 + 长腹 */
            return legs(4, c, 58, 78, 12, 2.6) +
                '<path d="M46 62 q8-15 30-12 q16 2 14 15 q-2 13-18 13 q-22 0-26-16 Z" fill="' + fill +
                '" stroke="' + c.light + '" stroke-opacity=".28" stroke-width="1"/>' +
                '<path d="M46 50 l-18-16 l-5 7 l17 14 Z" fill="' + c.deep + '" fill-opacity=".92"/>' +
                '<path d="M48 58 l-20-8 l-3 8 l20 7 Z" fill="' + c.light + '" fill-opacity=".75">' +
                '<animateTransform attributeName="transform" type="rotate" values="0 48 58;-9 48 58;0 48 58" ' +
                'dur="1.6s" repeatCount="indefinite"/></path>' +
                headCap(c, fill, 80, 58, 13, 12);
        case 'moth':
            /* 蛾：双翅 + 绒腹 + 羽状触角 */
            return '<path d="M58 60 q-28-32-44-16 q-14 13 7 28 q19 14 37 2 Z" fill="' + fill +
                '" fill-opacity=".82" stroke="' + c.light + '" stroke-opacity=".35" stroke-width="1">' +
                '<animateTransform attributeName="transform" type="rotate" values="0 58 62;-9 58 62;0 58 62" ' +
                'dur="1.5s" repeatCount="indefinite"/></path>' +
                '<path d="M62 60 q28-32 44-16 q14 13-7 28 q-19 14-37 2 Z" fill="' + fill +
                '" fill-opacity=".82" stroke="' + c.light + '" stroke-opacity=".35" stroke-width="1">' +
                '<animateTransform attributeName="transform" type="rotate" values="0 62 62;9 62 62;0 62 62" ' +
                'dur="1.5s" repeatCount="indefinite"/></path>' +
                '<ellipse cx="60" cy="68" rx="7" ry="17" fill="' + c.deep + '" fill-opacity=".92"/>' +
                headCap(c, fill, 60, 48, 12, 12) +
                '<path d="M55 40 q-5-11-13-15 M65 40 q5-11 13-15" stroke="' + c.light +
                '" stroke-width="1.5" fill="none" stroke-opacity=".8"/>';
        case 'jelly':
            /* 水母：伞盖 + 触须 */
            return '<path d="M34 64 q0-24 26-24 q26 0 26 24 q-26 10-52 0 Z" fill="' + fill +
                '" fill-opacity=".82" stroke="' + c.light + '" stroke-opacity=".35" stroke-width="1">' +
                '<animate attributeName="d" dur="3.4s" repeatCount="indefinite" values="' +
                'M34 64 q0-24 26-24 q26 0 26 24 q-26 10-52 0 Z;' +
                'M32 66 q0-28 28-28 q28 0 28 28 q-28 12-56 0 Z;' +
                'M34 64 q0-24 26-24 q26 0 26 24 q-26 10-52 0 Z"/></path>' +
                tentacles(c, 5, 74, 20) + coreMark(c, 4.4);
        case 'serp':
            /* 蛇/蟒：蜿蜒长身 + 覆在身端的大头 + 信子 + 尾尖 */
            return '<path d="M22 78 q10-26 26-24 q16 2 12-12 q-4-14 14-16 q18-2 24 12" ' +
                'stroke="' + c.deep + '" stroke-width="11" fill="none" stroke-linecap="round"/>' +
                '<path d="M22 78 q10-26 26-24 q16 2 12-12 q-4-14 14-16 q18-2 24 12" ' +
                'stroke="' + fill + '" stroke-width="8" fill="none" stroke-linecap="round"/>' +
                '<ellipse cx="99" cy="37" rx="12" ry="10" fill="' + fill + '" stroke="' + c.light +
                '" stroke-opacity=".42" stroke-width="1.1"/>' +
                '<path d="M101 29 q7-6 12-4" stroke="' + c.light + '" stroke-width="1.6" ' +
                'fill="none" stroke-opacity=".75" stroke-linecap="round"/>' +
                '<path d="M108 43 q6 3 7 8 M24 74 q6 9 2 17" stroke="' + c.light + '" stroke-width="1.6" ' +
                'fill="none" stroke-opacity=".55" stroke-linecap="round"/>';
        case 'toad':
            /* 蟾：宽体 + 头顶鼓眼 + 疣粒 */
            return legs(2, c, 82, 82, 18, 4) +
                '<ellipse cx="60" cy="74" rx="30" ry="20" fill="' + fill + '" stroke="' + c.light +
                '" stroke-opacity=".28" stroke-width="1"/>' +
                '<path d="M42 60 q18-7 36 0" stroke="' + c.light + '" stroke-width="1.6" ' +
                'fill="none" stroke-opacity=".45"/>' +
                '<path d="M44 84 q16 9 32 0" stroke="' + c.light + '" stroke-width="1.6" ' +
                'fill="none" stroke-opacity=".55"/>' +
                '<g fill="' + c.light + '" fill-opacity=".3">' +
                '<circle cx="50" cy="70" r="2.2"/><circle cx="70" cy="74" r="2"/><circle cx="60" cy="64" r="1.8"/></g>';
        case 'turtle':
            /* 龟：缩颈探出的头 + 穹背六角甲纹 + 四肢（头先画，甲后盖，再补颈） */
            return legs(2, c, 84, 84, 15, 4.4) +
                headCap(c, fill, 60, 42, 12, 11) +
                '<ellipse cx="60" cy="70" rx="30" ry="21" fill="' + fill + '" stroke="' + c.light +
                '" stroke-opacity=".38" stroke-width="1.3"/>' +
                '<path d="M60 51 l15 11 l-6 17 h-18 l-6-17 Z" fill="' + c.deep + '" fill-opacity=".35"/>' +
                '<path d="M60 51 l0-9 M45 60 l-11-3 M75 60 l11-3 M50 78 l-7 8 M70 78 l7 8" ' +
                'stroke="' + c.light + '" stroke-width="1.4" fill="none" stroke-opacity=".42"/>' +
                '<path d="M55 56 q-2-10-1-15 M65 56 q2-10 1-15" stroke="' + fill +
                '" stroke-width="11" fill="none" stroke-linecap="round"/>';
        case 'qilin':
            /* 麒麟：兽身 + 双角 + 鬃尾 */
            return legs(4, c, 62, 84, 15, 3.4) +
                '<ellipse cx="62" cy="68" rx="26" ry="17" fill="' + fill + '" stroke="' + c.light +
                '" stroke-opacity=".28" stroke-width="1"/>' +
                headCap(c, fill, 40, 62, 13, 12) +
                '<path d="M34 52 q-7-14 3-20 q9-4 12 6" fill="' + c.light + '" fill-opacity=".55"/>' +
                '<path d="M46 48 q-2-16 8-19 q8-2 6 10" fill="' + c.light + '" fill-opacity=".45"/>' +
                '<path d="M86 60 q16-8 24-2 q-8 10-22 12 Z" fill="' + c.light + '" fill-opacity=".55">' +
                '<animateTransform attributeName="transform" type="rotate" values="-4 86 60;8 86 60;-4 86 60" ' +
                'dur="2s" repeatCount="indefinite"/></path>';
        case 'dragon':
            /* 龙：蜿蜒长身 + 大头 + 龙角 + 利爪 */
            return '<path d="M8 84 q8-30 30-28 q22 2 20-16 q-2-18 20-18 q22 0 26 18" ' +
                'stroke="' + c.deep + '" stroke-width="14" fill="none" stroke-linecap="round"/>' +
                '<path d="M8 84 q8-30 30-28 q22 2 20-16 q-2-18 20-18 q22 0 26 18" ' +
                'stroke="' + fill + '" stroke-width="10" fill="none" stroke-linecap="round"/>' +
                '<path d="M26 80 q-10-6-18-4 M40 70 q-12 2-20 8" stroke="' + c.light +
                '" stroke-width="1.8" fill="none" stroke-opacity=".5"/>' +
                '<path d="M92 42 q6-11 8-16 q2-5-4-8 q-6-3-9 5 q-2 8 5 19 Z" fill="' + fill +
                '" stroke="' + c.light + '" stroke-opacity=".45" stroke-width="1.2"/>' +
                '<path d="M94 20 q-4-10 2-15 M86 22 q-8-7-14-6" stroke="' + c.light +
                '" stroke-width="2.2" fill="none" stroke-opacity=".8"/>';
        case 'roc':
            /* 大鹏：双翼 + 首 + 利爪 */
            return '<path d="M58 62 q-32-28-48-11 q-11 13 11 25 q23 13 39 1 Z" fill="' + fill +
                '" fill-opacity=".85" stroke="' + c.light + '" stroke-opacity=".4" stroke-width="1">' +
                '<animateTransform attributeName="transform" type="rotate" values="0 58 62;-12 58 62;0 58 62" ' +
                'dur="1.2s" repeatCount="indefinite"/></path>' +
                '<path d="M62 62 q32-28 48-11 q11 13-11 25 q-23 13-39 1 Z" fill="' + fill +
                '" fill-opacity=".85" stroke="' + c.light + '" stroke-opacity=".4" stroke-width="1">' +
                '<animateTransform attributeName="transform" type="rotate" values="0 62 62;12 62 62;0 62 62" ' +
                'dur="1.2s" repeatCount="indefinite"/></path>' +
                '<ellipse cx="60" cy="68" rx="10" ry="15" fill="' + c.deep + '" fill-opacity=".9"/>' +
                headCap(c, fill, 60, 48, 12, 11) +
                '<path d="M60 38 q-6-6-1-12 q6 4 7 10" fill="' + c.light + '" fill-opacity=".85"/>' +
                '<path d="M49 82 q-4 12-12 16 M71 82 q4 12 12 16" stroke="' + c.deep +
                '" stroke-width="3" fill="none" stroke-linecap="round"/>';
        default:
            return '<ellipse cx="60" cy="64" rx="24" ry="18" fill="' + fill + '"/>' + coreMark(c, 4);
    }
}
/* 通用头部：带高光的头壳 */
function headCap(c, fill, cx, cy, rx, ry){
    return '<ellipse cx="' + cx + '" cy="' + cy + '" rx="' + rx + '" ry="' + ry + '" fill="' + fill +
        '" stroke="' + c.light + '" stroke-opacity=".4" stroke-width="1"/>' +
        '<ellipse cx="' + (cx - rx*0.3) + '" cy="' + (cy - ry*0.35) + '" rx="' + (rx*0.34) +
        '" ry="' + (ry*0.28) + '" fill="#ffffff" fill-opacity=".28"/>';
}
function segPlate(c){
    let out = '';
    for(let i=0;i<5;i++){
        const x = 36 + i*12;
        out += '<circle cx="' + x + '" cy="62" r="5.4" fill="' + c.light + '" fill-opacity=".3" stroke="' +
            c.light + '" stroke-opacity=".35" stroke-width=".8"/>';
    }
    return out;
}
function tentacles(c, n, yTop, len){
    let out = '';
    for(let i=0;i<n;i++){
        const x = 60 + (i-(n-1)/2)*9;
        out += '<path d="M' + x + ' ' + yTop + ' q' + rnd(-6,6).toFixed(1) + ' ' + (len*0.55).toFixed(1) +
            ' ' + rnd(-8,8).toFixed(1) + ' ' + len.toFixed(1) + '" stroke="' + c.light +
            '" stroke-width="2" fill="none" stroke-opacity=".62" stroke-linecap="round">' +
            '<animateTransform attributeName="transform" type="rotate" ' +
            'values="-5 ' + x + ' ' + yTop + ';5 ' + x + ' ' + yTop + ';-5 ' + x + ' ' + yTop +
            '" dur="' + (2.2 + i*0.3).toFixed(1) + 's" repeatCount="indefinite"/></path>';
    }
    return out;
}
function eyeMarkup(g, c){
    const sp = speciesOf(g);
    const glow = c.light;
    switch(sp.form){
        case 'worm':   return eyes(c, 32, 63, 2, 2.6, glow);
        case 'milli':  return '';
        case 'scorp':  return eyes(c, 34, 60, 2, 2.6, glow);
        case 'spider': return eyes(c, 52, 62, 4, 1.9, glow);
        case 'ant':    return eyes(c, 31, 61, 2, 2.4, glow);
        case 'mantis': return eyes(c, 82, 56, 2, 2.7, glow);
        case 'moth':   return eyes(c, 60, 47, 2, 2.5, glow);
        case 'jelly':  return eyes(c, 60, 60, 3, 2.0, glow);
        case 'toad':   return eyes(c, 44, 54, 1, 3.4, glow) + eyes(c, 76, 54, 1, 3.4, glow);
        case 'serp':   return eyes(c, 97, 36, 2, 2.6, glow);
        case 'turtle': return eyes(c, 60, 37, 2, 2.3, glow);
        case 'qilin':  return eyes(c, 38, 60, 2, 2.7, glow);
        case 'dragon': return eyes(c, 96, 37, 2, 2.6, glow);
        case 'roc':    return eyes(c, 60, 47, 2, 2.4, glow);
        default:       return eyes(c, 60, 60, 2, 2.2, glow);
    }
}

/* ==================== 图鉴 ==================== */
function renderCodex(){
    const grid = $('codex');
    if(!grid) return;
    grid.innerHTML = SPECIES.map(sp => {
        const rec = state.codex[sp.id];
        const unlocked = !!rec;
        const fake = { id:'cx_' + sp.id, species:sp.id, elem:sp.elem, tier:sp.tier, qi:(rec ? rec.qi : 0) };
        return '<div class="codex-item ' + (unlocked ? 'unlocked' : 'locked') + ' t' + sp.tier +
            '" title="' + sp.name + ' · ' + sp.elem + ' · ' + (TIER_LABEL[sp.tier] || '') + '\n' + sp.note + '">' +
            figureHTML(fake, true) +
            '<div class="codex-name">' + (unlocked ? sp.name : '？？？') + '</div>' +
            '<div class="codex-qi">' + sp.elem + ' · ' + (TIER_LABEL[sp.tier] || '') + '</div>' +
        '</div>';
    }).join('');
}

/* ==================== 选择 ==================== */
function toggleSelect(id){
    const i = state.selected.indexOf(id);
    if(i >= 0){
        state.selected.splice(i,1);
    } else {
        if(state.selected.length >= 2) state.selected.shift();
        state.selected.push(id);
        const el = document.querySelector('.guchong-card[data-id="' + id + '"]');
        if(el){
            const p = centerOf(el);
            spawnParticles(p.x, p.y, { count:8, colors:['#3fd0b0','#a9f0dd','#ffffff'],
                speed:2.4, size:4, life:26, gravity:0.04 });
        }
    }
    render();
}

/* ==================== 孵化动画 ==================== */
async function playHatchAnimation(){
    const grid = $('grid');
    const r = grid.getBoundingClientRect();
    let cx = r.left + r.width/2;
    let cy = r.top + Math.max(r.height/2, 60);

    const egg = document.createElement('div');
    egg.className = 'hatch-egg';
    egg.textContent = '🥚';
    egg.style.left = cx + 'px';
    egg.style.top = cy + 'px';
    document.body.appendChild(egg);

    /* 灵气汇聚 */
    for(let i=0;i<7;i++){
        spawnQiWisps(cx, cy + 30, { count:4, colors:['#e8b44a','#ffe9a8','#3fd0b0'] });
        await sleep(80);
    }
    await sleep(240);

    egg.classList.add('crack');
    spawnRing(cx, cy, '#e8b44a');
    await sleep(170);

    spawnParticles(cx, cy, { count:42, colors:['#ffd76a','#e94560','#fff2a8','#ff8a4a'],
        speed:6, size:8, gravity:0.17, life:62, shape:'star' });
    spawnParticles(cx, cy, { count:24, colors:['#ffffff','#ffe9a8'],
        speed:2.6, size:5, gravity:0.03, life:46 });
    spawnParticles(cx, cy, { count:16, colors:['#a9f0dd','#3fd0b0'],
        speed:4, size:4, gravity:-0.02, life:70, shape:'shard' });

    await sleep(170);
    egg.remove();
    await sleep(40);
}

/* ==================== 融合动画 ==================== */
function makeFlyingClone(el, rect){
    const clone = el.cloneNode(true);
    clone.classList.remove('selected','card-enter');
    clone.classList.add('flying-clone');
    clone.style.position = 'fixed';
    clone.style.left = rect.left + 'px';
    clone.style.top = rect.top + 'px';
    clone.style.width = rect.width + 'px';
    clone.style.height = rect.height + 'px';
    clone.style.margin = '0';
    clone.style.zIndex = '9000';
    clone.style.pointerEvents = 'none';
    clone.style.transformOrigin = 'center center';
    clone.style.transition = 'transform .62s cubic-bezier(.55,-0.25,.7,1.35), opacity .62s ease';
    return clone;
}

async function playFuseAnimation(a, b, success){
    const ea = document.querySelector('.guchong-card[data-id="' + a.id + '"]');
    const eb = document.querySelector('.guchong-card[data-id="' + b.id + '"]');
    if(!ea || !eb) return;
    const ra = ea.getBoundingClientRect();
    const rb = eb.getBoundingClientRect();
    const grid = $('grid');
    const gr = grid.getBoundingClientRect();
    const cx = gr.left + gr.width/2;
    const cy = gr.top + Math.max(gr.height/2, 90);

    ea.style.visibility = 'hidden';
    eb.style.visibility = 'hidden';
    const ca = makeFlyingClone(ea, ra);
    const cb = makeFlyingClone(eb, rb);
    document.body.appendChild(ca);
    document.body.appendChild(cb);

    await sleep(30);
    ca.style.transform = 'translate(' + (cx-ra.left-ra.width/2) + 'px,' +
        (cy-ra.top-ra.height/2) + 'px) scale(.5) rotate(-16deg)';
    cb.style.transform = 'translate(' + (cx-rb.left-rb.width/2) + 'px,' +
        (cy-rb.top-rb.height/2) + 'px) scale(.5) rotate(16deg)';
    ca.style.opacity = '.86';
    cb.style.opacity = '.86';

    /* 吞噬过程：灵气旋涡 */
    for(let i=0;i<5;i++){
        spawnParticles(cx, cy, { count:5, colors:['#c07ae8','#e0c8f5','#3fd0b0'],
            speed:2.6, size:4.6, gravity:-0.02, life:44, shape:'wisp' });
        await sleep(110);
    }
    await sleep(90);

    ca.remove();
    cb.remove();

    if(success){
        spawnRing(cx, cy, '#e8b44a');
        spawnRing(cx, cy, '#3fd0b0');
        shakeScreen();
        spawnParticles(cx, cy, { count:48,
            colors:['#e8b44a','#ffd76a','#ff8a4a','#ffffff','#c07ae8'],
            speed:7.6, size:8, gravity:0.13, life:70, shape:'star' });
        spawnParticles(cx, cy, { count:28, colors:['#8b5cf6','#ffffff'],
            speed:3.4, size:5, gravity:0.02, life:54 });
    } else {
        /* 失败：暗色溃散 + 裂片 */
        spawnRing(cx, cy, '#c07ae8');
        shakeScreen();
        spawnParticles(cx, cy, { count:34, colors:['#8b5cf6','#5b3a7a','#c07ae8'],
            speed:4.6, size:7, gravity:0.24, life:60, shape:'shard' });
        spawnParticles(cx, cy, { count:18, colors:['#3a3345','#6b2f9e'],
            speed:2.2, size:6, gravity:0.3, life:52 });
        spawnBanner('融 合 失 败', 'banner-fail');
    }
    await sleep(120);
}

/* ==================== 融合成功率 ==================== */
function fuseChance(a, b){
    const qAvg = (a.qi + b.qi)/2;
    /* 基础盘：品质越高越"娇贵"，融合越易失败
       用平方曲线让凡品→良品几乎无感，只在灵品/仙品才明显咬人（满品质约 -11%） */
    let c = 0.66 - 0.0045*qAvg*qAvg;
    /* 物种梯度：越高阶越难融合 */
    c -= 0.085*(a.tier + b.tier)/2;
    /* 灵性微调（Tanh 衰减，避免高级个体抵消梯度惩罚） */
    c += 0.05 * Math.tanh((a.灵性 + b.灵性)/600);
    /* 属性相性 */
    if(a.elem === b.elem) c += 0.08; else c -= 0.05;
    /* 天赋 */
    if(a.talent === 'huaxing') c += 0.14;
    if(b.talent === 'huaxing') c += 0.14;
    if(a.talent === 'chunyang' && a.elem === b.elem) c += 0.20;
    if(b.talent === 'chunyang' && a.elem === b.elem) c += 0.20;
    if(!a.talent && !b.talent) c += 0.05;
    /* 保底：连续失败累积 */
    c += Math.min(0.18, state.fuseFail * 0.035);
    return clamp(c, 0.12, 0.94);
}

/* 融合结果物种：同属性同梯度可晋阶 */
function fuseSpecies(a, b){
    const sa = speciesOf(a), sb = speciesOf(b);
    const hi = sa.tier >= sb.tier ? sa : sb;
    if(sa.tier >= 6 && sb.tier >= 6) return SPECIES_BY_ID['x7'];
    if(sa.elem === sb.elem && sa.tier === sb.tier && sa.tier <= 3){
        const next = SPECIES.find(x => x.elem === sa.elem && x.tier === sa.tier + 1);
        if(next && Math.random() < 0.42) return next;
    }
    return hi;
}

/* ==================== 孵化 ==================== */
async function hatch(){
    if(busy) return;
    if(state.guchongs.length >= MAX_GU){ addLog('巢穴已满，先融合或清理蛊虫吧', 'log-error'); return; }
    if(state.spirit < HATCH_COST){ addLog('灵液不足，无法孵化', 'log-error'); return; }

    busy = true; updateButtons();
    await playHatchAnimation();

    state.spirit -= HATCH_COST;
    const sp = rollSpecies(null);
    const qi = sp.tier >= 6 ? ri(3,5) : (sp.tier === 3 ? ri(1,3) : ri(0,2));
    const g = genGuchong(sp, qi, 1);
    applyTalentBase(g);
    state.guchongs.push(g);
    unlockCodex(g);

    addLog('🥚 孵化出 ' + g.name + '（' + g.elem + '·' + TIER_LABEL[g.tier] + '·' + qiName(g.qi) + '）' +
        (g.talent ? ' 【觉醒 ' + TALENT_BY_ID[g.talent].name + '】' : ''),
        g.tier >= 3 ? 'log-gold' : 'log-success');

    busy = false;
    render();
    markCardEnter(g.id);
    save(true);
}

function unlockCodex(g){
    const cur = state.codex[g.species];
    if(!cur || cur.qi < g.qi){
        state.codex[g.species] = { qi:g.qi, at:Date.now() };
    }
}

/* ==================== 忠心度 / 不败信念 ==================== */
function loyaltyOf(g){
    return typeof g.loyal === 'number' ? g.loyal : LOYAL_INIT;
}
/* 信念加成：连胜越高越强，低忠心会削弱它 */
function streakBonus(g){
    const n = Math.min(STREAK_CAP, g.streak || 0);
    let b = n * STREAK_STEP;
    const loy = loyaltyOf(g);
    if(loy < 40) b *= 0.5;
    else if(loy < 60) b *= 0.75;
    return b;
}
/* 战斗时按信念放大的属性（不改存档数值，只在结算时生效） */
function effAttr(g, k){
    const b = streakBonus(g);
    return b ? g[k] * (1 + b) : g[k];
}
function loyaltyState(g){
    const l = loyaltyOf(g);
    if(l >= 70) return { label:'死忠', cls:'loy-hi' };
    if(l >= 45) return { label:'顺从', cls:'loy-mid' };
    if(l >= LOYAL_REBEL) return { label:'动摇', cls:'loy-low' };
    if(l >= 15) return { label:'离心', cls:'loy-bad' };
    return { label:'将叛', cls:'loy-bad' };
}
/* 败北掉忠心：品质与梯度越高越"娇贵" */
function loyaltyLoss(g){
    let d = 12 + g.qi * 1.4 + Math.max(0, g.tier - 1) * 1.5 + rnd(-2, 3);
    if(g.talent === 'chunyang') d -= 3;      /* 纯阳心性稳 */
    return Math.max(5, Math.round(d));
}
/* 反叛判定：忠心越低概率越高 */
function rebelChance(g){
    const l = loyaltyOf(g);
    if(l >= LOYAL_REBEL) return 0;
    let p = (LOYAL_REBEL - l) / 100 + 0.06;
    if(g.talent === 'chunyang') p *= 0.4;
    return clamp(p, 0, 0.55);
}
function sootheCost(g){
    return SOOTHE_COST + Math.round((LOYAL_MAX - loyaltyOf(g)) * 0.4);
}
/* ==================== 融合 ==================== */
async function fuse(){
    if(busy) return;
    if(state.selected.length !== 2){ addLog('请选择两只蛊虫进行融合', 'log-error'); return; }
    if(state.spirit < FUSE_COST){ addLog('灵液不足，无法融合', 'log-error'); return; }

    const a = state.guchongs.find(g => g.id === state.selected[0]);
    const b = state.guchongs.find(g => g.id === state.selected[1]);
    if(!a || !b){ addLog('选择的蛊虫不存在', 'log-error'); return; }

    busy = true; updateButtons();

    const chance = fuseChance(a, b);
    const ok = Math.random() < chance;
    const ca = counterMult(a.elem, b.elem);
    let relation = '同源';
    if(a.elem !== b.elem){
        if(ca > 1) relation = a.elem + '克' + b.elem;
        else if(ca < 1) relation = a.elem + '被' + b.elem + '克';
        else relation = '异属';
    }

    addLog('🔥 以 <b>' + a.name + '</b> 为主蛊，吞噬 <b>' + b.name + '</b>（' + relation +
        '）｜成功率 ' + pct(chance), 'log-info');

    await playFuseAnimation(a, b, ok);

    state.spirit -= FUSE_COST;

    if(!ok){
        /* 失败：主蛊存活但属性下降，副蛊消散 */
        state.fuseFail++;
        b.消 = true;
        ATTRS.forEach(k => {
            a[k] = Math.max(1, Math.round(a[k] * rnd(0.82, 0.92)));
        });
        state.guchongs = state.guchongs.filter(g => g.id !== b.id);
        state.selected = [];
        addLog('💥 反噬！' + b.name + ' 化为灰烬，' + a.name + ' 元气受损，属性下降 ' +
            Math.round((1 - 0.87)*100) + '% 左右（连续失败 ' + state.fuseFail + ' 次，成功率已提升）', 'log-bad');

        const ea = document.querySelector('.guchong-card[data-id="' + a.id + '"]');
        if(ea){
            const p = centerOf(ea);
            spawnFloatText(p.x, p.y, '属性下降', 'float-bad');
        }
    } else {
        state.fuseFail = 0;
        const sp = fuseSpecies(a, b);
        const base = Math.max(a.qi, b.qi);
        let newQi = base, promoted = false;
        if(base < QUALITIES.length-1 && sp.tier >= 3 && Math.random() < 0.55){ newQi = base+1; promoted = true; }
        else if(base < QUALITIES.length-1 && Math.random() < 0.30){ newQi = base+1; promoted = true; }

        const newLevel = clamp(Math.max(a.level, b.level) + (promoted ? 1 : 0), 1, 99);
        /* 天赋遗传：55% 继承，12% 突变 */
        let talent = null;
        const roll = Math.random();
        if(roll < 0.55) talent = Math.random() < 0.5 ? a.talent : b.talent;
        else if(roll < 0.67) talent = pick(TALENTS).id;
        if(!talent && (a.talent || b.talent) && Math.random() < 0.3) talent = a.talent || b.talent;

        const child = genGuchong(sp, newQi, newLevel, talent);
        /* 继承并强化：取父母较高值 ×1.12 */
        ATTRS.forEach(k => {
            const hi = Math.max(a[k], b[k]);
            child[k] = Math.max(child[k], Math.round(hi * 1.12));
        });
        applyTalentBase(child);
        /* 忠心上，新个体取父母较高者略降（吞噬同伴总归有阴影） */
        child.loyal = clamp(Math.round(Math.max(loyaltyOf(a), loyaltyOf(b)) * 0.9), 5, LOYAL_MAX);
        child.streak = 0;   /* 信念不跨界，需重新打出来 */
        child.best = Math.max(a.best || 0, b.best || 0);

        state.guchongs = state.guchongs.filter(g => g.id !== a.id && g.id !== b.id);
        state.guchongs.push(child);
        state.selected = [];
        unlockCodex(child);

        const tierUp = sp.tier > Math.max(a.tier, b.tier);
        let msg = '✨ 诞生了 <b>' + child.name + '</b>（' + child.elem + '·' + TIER_LABEL[child.tier] +
            '·' + qiName(newQi) + ' Lv.' + newLevel + '）';
        if(tierUp) msg += ' —— <b>晋阶为 ' + TIER_LABEL[child.tier] + '</b>！';
        if(promoted) msg += ' 品质提升！';
        if(child.talent) msg += ' 觉醒【' + TALENT_BY_ID[child.talent].name + '】';
        addLog(msg, (tierUp || child.tier >= 6) ? 'log-gold' : 'log-success');

        if(tierUp){
            const g2 = $('grid');
            const p = centerOf(g2);
            spawnBanner(TIER_LABEL[child.tier] + ' 诞 生', 'banner-trib');
            shakeScreen();
            spawnParticles(p.x, p.y, { count:56,
                colors:[elemOf(child).color,'#ffffff','#e8b44a'],
                speed:8, size:9, gravity:0.1, life:76, shape:'star' });
        }
    }

    busy = false;
    render();
    if(ok) markCardEnter(state.guchongs[state.guchongs.length-1].id);
    save(true);
}

/* ==================== 战斗 ==================== */
function genWild(me){
    const lvl = clamp(me.level + ri(-1,2), 1, 99);
    let sp;
    if(me.tier <= 1) sp = pick(SPECIES.filter(s => s.tier <= 2));
    else if(me.tier <= 2) sp = pick(SPECIES.filter(s => s.tier <= 3));
    else sp = pick(SPECIES.filter(s => s.tier >= 2 && s.tier <= 3));
    let qi = clamp(me.qi + ri(-1,1), 0, Math.min(4, QUALITIES.length-1));
    const g = genGuchong(sp, qi, lvl, Math.random() < 0.15 ? pick(TALENTS).id : null);
    applyTalentBase(g);
    return g;
}

function animateAttack(side){
    const el = side === 'left' ? $('side-left') : $('side-right');
    const cls = side === 'left' ? 'atk-right' : 'atk-left';
    el.classList.add(cls);
    return sleep(240).then(() => el.classList.remove(cls));
}
function animateHit(side){
    const el = side === 'left' ? $('side-left') : $('side-right');
    el.classList.remove('hit');
    void el.offsetWidth;
    el.classList.add('hit');
    setTimeout(() => el.classList.remove('hit'), 350);
}
function setBattleSide(side, g, hp, max){
    const fig = $('battle-' + side + '-fig');
    $('battle-' + side + '-name').textContent = g ? g.name : '—';
    $('battle-' + side + '-sub').textContent = g
        ? g.elem + '·' + (TIER_LABEL[g.tier]||'') + '·' + qiName(g.qi) + ' Lv.' + g.level +
          (g.talent ? ' 【' + TALENT_BY_ID[g.talent].name + '】' : '')
        : '';
    if(fig) fig.innerHTML = g ? figureHTML(g) : '';
    $('battle-' + side + '-hp').style.width = '100%';
    $('battle-' + side + '-text').textContent = hp + ' / ' + max;
}
function updateBars(hpMe, maxMe, hpFoe, maxFoe){
    $('battle-left-hp').style.width = Math.max(0,(hpMe/maxMe)*100) + '%';
    $('battle-right-hp').style.width = Math.max(0,(hpFoe/maxFoe)*100) + '%';
    $('battle-left-text').textContent = Math.max(0,hpMe) + ' / ' + maxMe;
    $('battle-right-text').textContent = Math.max(0,hpFoe) + ' / ' + maxFoe;
}

function calcDamage(atk, def, opts){
    opts = opts || {};
    const eMult = counterMult(atk.elem, def.elem);
    let tal = 1;
    if(atk.talent === 'tongling' && eMult > 1) tal += 0.18;
    if(atk.talent === 'tianji' && opts.guessed) tal += 0.20;
    const crit = Math.random() < 0.13 ? 1.55 : 1;
    /* 不败信念在此真实生效 */
    const raw = (effAttr(atk,'攻击')*0.85 + effAttr(atk,'毒力')*0.35) * (opts.might || 1);
    const reduce = 100/(100 + effAttr(def,'防御')*2.2);
    const dmg = Math.max(3, Math.round(raw*reduce*eMult*tal*crit*rnd(0.9,1.12)));
    return { dmg, eMult, crit };
}

function divineHand(){
    return pick(ATTRS);
}

async function doBattle(){
    if(busy) return;
    if(state.selected.length !== 1){ addLog('请选择一只蛊虫出战', 'log-error'); return; }
    const me = state.guchongs.find(g => g.id === state.selected[0]);
    if(!me) return;

    busy = true; updateButtons();

    const foe = genWild(me);
    state.totalBattles++;

    let maxMe = maxHp(me), maxFoe = maxHp(foe);
    let hpMe = maxMe, hpFoe = maxFoe;
    setBattleSide('left', me, hpMe, maxMe);
    setBattleSide('right', foe, hpFoe, maxFoe);

    const rel = counterMult(me.elem, foe.elem);
    const foeRel = counterMult(foe.elem, me.elem);
    let relTxt = '属性相持';
    if(rel > 1) relTxt = me.elem + '克' + foe.elem + '（我方伤害 ×' + ELEM_ADV + '）';
    else if(rel < 1) relTxt = me.elem + '被' + foe.elem + '克（我方伤害 ×' + ELEM_DIS + '）';
    addLog('⚔ ' + me.name + ' 迎战野生 ' + foe.name + '（' + foe.elem + '·' +
        TIER_LABEL[foe.tier] + ' Lv.' + foe.level + '）｜' + relTxt, 'log-info');

    const arena = document.querySelector('.battle-arena');
    const ar = arena.getBoundingClientRect();
    const lx = ar.left + ar.width*0.22, rx = ar.left + ar.width*0.78, my = ar.top + ar.height/2;
    spawnParticles(lx, my, { count:16, colors:[elemOf(me).color,'#ffffff'], speed:3.6, size:5,
        spread:Math.PI*0.7, angle:-Math.PI/2, gravity:0.1, life:40 });
    spawnParticles(rx, my, { count:16, colors:[elemOf(foe).color,'#ffffff'], speed:3.6, size:5,
        spread:Math.PI*0.7, angle:-Math.PI/2, gravity:0.1, life:40 });
    await sleep(430);

    let round = 0, winner = null;
    let mightMe = 1, mightFoe = 1;

    while(round < MAX_ROUND && hpMe > 0 && hpFoe > 0){
        round++;
        /* 卜卦：预测对手阵眼 */
        const foeHand = divineHand();
        const picked = await askDivine(round, foeHand);
        if(picked === null){ winner = 'foe'; break; }

        const win = picked === foeHand;
        const meFirst = me.速度 > foe.速度 ||
            (me.速度 === foe.速度 && Math.random() < 0.5);

        setDivineResult(win
            ? '✦ 卦象应验！你取「' + picked + '」压制对方「' + foeHand + '」'
            : '✧ 卦象失准。对方取「' + foeHand + '」，你取「' + picked + '」',
            win ? 'tag-win' : 'tag-lose');

        await sleep(340);

        /* 命中者出手：猜中则我方先手，猜错则对方先手 */
        const order = win ? ['me','foe'] : ['foe','me'];
        for(const side of order){
            if(hpMe <= 0 || hpFoe <= 0) break;
            if(side === 'me'){
                const r = calcDamage(me, foe, { might: mightMe, guessed: win });
                hpFoe = Math.max(0, hpFoe - r.dmg);
                await animateAttack('left');
                animateHit('right');
                const p = centerOf($('side-right'));
                spawnFloatText(p.x, p.y, '-' + r.dmg, r.crit ? 'float-crit' : 'float-dmg');
                if(r.eMult > 1) spawnFloatText(p.x, p.y - 34, '克制 ×' + ELEM_ADV, 'float-counter');
                if(r.eMult < 1) spawnFloatText(p.x, p.y - 34, '被克 ×' + ELEM_DIS, 'float-bad');
                spawnParticles(p.x, p.y, { count: r.crit ? 24 : 14,
                    colors: r.crit ? ['#fff2a8','#ff8a4a','#ffffff'] : ['#ff8a8a','#e94560','#ffffff'],
                    speed: r.crit ? 5.6 : 4.2, size: r.crit ? 7 : 6,
                    gravity:0.16, life:38, shape:'star' });
                if(r.crit){ spawnRing(p.x, p.y, '#ff8a4a'); shakeScreen(); }
                mightMe = 1;
            } else {
                const r = calcDamage(foe, me, { might: mightFoe, guessed: !win });
                hpMe = Math.max(0, hpMe - r.dmg);
                await animateAttack('right');
                animateHit('left');
                const p = centerOf($('side-left'));
                spawnFloatText(p.x, p.y, '-' + r.dmg, r.crit ? 'float-crit' : 'float-dmg');
                if(r.eMult > 1) spawnFloatText(p.x, p.y - 34, '被克制 ×' + ELEM_ADV, 'float-bad');
                spawnParticles(p.x, p.y, { count: r.crit ? 24 : 14,
                    colors: r.crit ? ['#fff2a8','#ff8a4a','#ffffff'] : ['#ff8a8a','#e94560','#ffffff'],
                    speed: r.crit ? 5.6 : 4.2, size: r.crit ? 7 : 6,
                    gravity:0.16, life:38, shape:'star' });
                if(r.crit){ spawnRing(p.x, p.y, '#ff8a4a'); shakeScreen(); }
                mightFoe = 1;
            }
            updateBars(hpMe, maxMe, hpFoe, maxFoe);
            await sleep(110);
        }

        /* 天赋持续效果 */
        if(hpMe > 0 && me.talent === 'bumie'){
            const heal = Math.round(maxMe*0.04);
            hpMe = Math.min(maxMe, hpMe + heal);
            const p = centerOf($('side-left'));
            spawnFloatText(p.x, p.y + 20, '+' + heal, 'float-heal');
            updateBars(hpMe, maxMe, hpFoe, maxFoe);
        }
        if(hpFoe > 0 && foe.talent === 'bumie'){
            const heal = Math.round(maxFoe*0.04);
            hpFoe = Math.min(maxFoe, hpFoe + heal);
            updateBars(hpMe, maxMe, hpFoe, maxFoe);
        }
        if(!win){ mightFoe = 1.25; }
        await sleep(90);
    }

    /* ---- 胜负 ---- */
    if(!winner){
        if(hpFoe <= 0 && hpMe > 0) winner = 'me';
        else if(hpMe <= 0 && hpFoe > 0) winner = 'foe';
        else if(hpMe <= 0 && hpFoe <= 0) winner = 'draw';
        else {
            const rm = hpMe/maxMe, rf = hpFoe/maxFoe;
            winner = rm > rf ? 'me' : (rf > rm ? 'foe' : 'draw');
        }
    }

    const sp0 = centerOf($('spirit'));
    await sleep(200);

    if(winner === 'me'){
        const reward = 15 + foe.level*4 + foe.qi*12 + (foe.tier >= 6 ? 60 : (foe.tier >= 3 ? 22 : 0));
        const expGain = 20 + foe.level*6 + foe.qi*10;
        state.spirit = Math.min(SPIRIT_MAX, state.spirit + reward);
        state.wins++; me.wins++;
        /* 连胜与忠心 */
        me.streak = (me.streak || 0) + 1;
        me.best = Math.max(me.best || 0, me.streak);
        me.loyal = Math.min(LOYAL_MAX, loyaltyOf(me) + 4);
        spawnBanner('胜', 'banner-win');
        addLog('🏆 ' + me.name + ' 获胜！获得 ' + reward + ' 灵液', 'log-gold');
        if(me.streak >= 2){
            const b = Math.round(streakBonus(me)*100);
            addLog('🔥 ' + me.name + ' 取得 ' + me.streak + ' 连胜，不败信念 +' + b + '% 属性' +
                (me.streak === STREAK_CAP ? '（已达上限）' : ''), 'log-gold');
        }
        spawnFloatText(sp0.x, sp0.y, '+' + reward, 'float-gold');
        pulseEl($('spirit'));
        const wp = centerOf($('side-right'));
        spawnParticles(wp.x, wp.y, { count:50, colors:['#ffd76a','#ffffff','#ff8a4a','#ffe9a8'],
            speed:7, size:8, gravity:0.15, life:72, shape:'star' });
        spawnRing(wp.x, wp.y, '#e8b44a');
        gainExp(me, expGain);
    } else if(winner === 'foe'){
        state.spirit = Math.min(SPIRIT_MAX, state.spirit + 5);
        /* 败北：掉忠心、断连胜 */
        const loss = loyaltyLoss(me);
        const before = loyaltyOf(me);
        me.loyal = Math.max(0, before - loss);
        const brokenStreak = me.streak || 0;
        me.streak = 0;
        spawnBanner('败', 'banner-lose');
        addLog('💀 ' + me.name + ' 败北…… 获得 5 灵液安慰奖', 'log-error');
        addLog('💔 ' + me.name + ' 忠心 ' + before + ' → ' + me.loyal + '（-' + loss + '）' +
            (brokenStreak >= 2 ? '，' + brokenStreak + ' 连胜中断' : ''), 'log-bad');
        spawnFloatText(sp0.x, sp0.y, '+' + 5, 'float-gold');
        pulseEl($('spirit'));
        const lp = centerOf($('side-left'));
        spawnParticles(lp.x, lp.y, { count:26, colors:['#6f7a8b','#ff8a96'],
            speed:3.5, size:6, gravity:0.2, life:55 });
        spawnFloatText(lp.x, lp.y - 26, '-' + loss + ' 忠心', 'float-bad');
        /* 反叛判定 */
        await checkRebel(me);
    } else {
        state.spirit = Math.min(SPIRIT_MAX, state.spirit + 10);
        me.loyal = Math.max(0, loyaltyOf(me) - 4);
        addLog('🤝 势均力敌，平局收场（10 灵液，忠心 -4）', 'log-info');
        spawnFloatText(sp0.x, sp0.y, '+10', 'float-gold');
        pulseEl($('spirit'));
    }

    hideDivinePanel();
    await sleep(200);
    busy = false;
    render();
    save(true);
}

/* ---- 反叛判定 ---- */
async function checkRebel(g){
    const p = rebelChance(g);
    if(p <= 0) return false;
    if(Math.random() >= p){
        addLog('⚠️ ' + g.name + ' 离心离德，但尚在掌控之中（反叛概率 ' + pct(p) + '）', 'log-bad');
        return false;
    }
    /* 反叛：离巢而去 */
    const p0 = centerOf($('grid'));
    spawnBanner('反 叛', 'banner-fail');
    shakeScreen();
    spawnParticles(p0.x, p0.y, { count:40, colors:['#c07ae8','#8b5cf6','#2a2130'],
        speed:6, size:8, gravity:0.2, life:66, shape:'shard' });
    spawnRing(p0.x, p0.y, '#c07ae8');
    addLog('🩸 ' + g.name + ' 忠心崩坏，反叛离巢而去！（反叛概率 ' + pct(p) + '）', 'log-bad');
    state.guchongs = state.guchongs.filter(x => x.id !== g.id);
    state.selected = state.selected.filter(id => id !== g.id);
    await sleep(260);
    return true;
}

/* ---- 安抚 ---- */
function soothe(){
    if(busy){ return; }
    if(state.selected.length !== 1){ addLog('请先选中一只蛊虫再安抚', 'log-error'); return; }
    const g = state.guchongs.find(x => x.id === state.selected[0]);
    if(!g) return;
    const loy = loyaltyOf(g);
    if(loy >= LOYAL_MAX){ addLog(g.name + ' 忠心已满，无需安抚', 'log-info'); return; }
    const cost = sootheCost(g);
    if(state.spirit < cost){ addLog('灵液不足，安抚需要 ' + cost + ' 灵液', 'log-error'); return; }
    state.spirit -= cost;
    const gain = 28 + Math.round(rnd(0, 10));
    const before = loy;
    g.loyal = Math.min(LOYAL_MAX, loy + gain);
    addLog('🕯 耗费 ' + cost + ' 灵液安抚 ' + g.name + '，忠心 ' + before + ' → ' + g.loyal, 'log-success');
    const el = document.querySelector('.guchong-card[data-id="' + g.id + '"]');
    if(el){
        const p = centerOf(el);
        spawnParticles(p.x, p.y, { count:26, colors:['#a9f0dd','#3fd0b0','#ffffff'],
            speed:3.4, size:5, gravity:-0.03, life:56, shape:'star' });
        spawnFloatText(p.x, p.y, '+' + (g.loyal - before) + ' 忠心', 'float-heal');
        spawnRing(p.x, p.y, '#3fd0b0');
    }
    pulseEl($('spirit'));
    render();
    save(true);
}

/* ---- 卜卦交互 ---- */
let divineResolver = null;
let divineToken = 0;
function askDivine(round, foeHand){
    return new Promise(resolve => {
        awaitingDivine = true;
        divineResolver = resolve;
        divineToken++;
        const myToken = divineToken;
        const panel = $('divine');
        $('divine-round').textContent = round + ' / ' + MAX_ROUND;
        $('divine-result').textContent = '';
        $('divine-result').className = 'divine-result';
        panel.style.display = 'block';
        panel.querySelectorAll('.divine-btn').forEach(b => { b.disabled = false; });
        /* 超时自动卜卦，避免卡死 */
        setTimeout(() => {
            if(awaitingDivine && divineToken === myToken) resolveDivine(pick(ATTRS));
        }, 18000);
    });
}
function resolveDivine(hand){
    if(!awaitingDivine || !divineResolver) return;
    awaitingDivine = false;
    divineToken++;
    const r = divineResolver;
    divineResolver = null;
    $('divine').querySelectorAll('.divine-btn').forEach(b => { b.disabled = true; });
    r(hand);
}
function setDivineResult(text, cls){
    const el = $('divine-result');
    el.textContent = text;
    el.className = 'divine-result ' + (cls || '');
}
function hideDivinePanel(){
    $('divine').style.display = 'none';
}

function gainExp(g, amount){
    g.exp += amount;
    let need = expNeed(g.level);
    while(g.exp >= need && g.level < 99){
        g.exp -= need;
        g.level++;
        ATTRS.forEach(k => { g[k] = Math.round(g[k]*1.07) + 1; });
        addLog('✨ ' + g.name + ' 成长至 Lv.' + g.level + '！', 'log-gold');
        const el = document.querySelector('.guchong-card[data-id="' + g.id + '"]');
        if(el){
            const p = centerOf(el);
            spawnBanner('突破', 'banner-trib');
            spawnParticles(p.x, p.y, { count:30, colors:['#ffd76a','#ffffff','#a9f0dd'],
                speed:5.4, size:7, gravity:0.04, life:58, shape:'star' });
            spawnRing(p.x, p.y, '#3fd0b0');
            shakeScreen();
        }
        need = expNeed(g.level);
    }
}

/* ==================== 存档 ==================== */
function save(silent){
    state.savedAt = Date.now();
    try {
        localStorage.setItem(SAVE_KEY, JSON.stringify(state));
        if(!silent) addLog('💾 已保存当前进度', 'log-info');
        return true;
    } catch(e){
        if(!silent) addLog('存档失败：' + e.message, 'log-error');
        return false;
    }
}
function load(silent){
    const raw = localStorage.getItem(SAVE_KEY);
    if(!raw){ if(!silent) addLog('未找到存档', 'log-error'); return false; }
    let data;
    try { data = JSON.parse(raw); } catch(e){
        if(!silent) addLog('存档解析失败，可能已损坏', 'log-error'); return false;
    }
    if(!data || !Array.isArray(data.guchongs)){
        if(!silent) addLog('存档格式不正确', 'log-error'); return false;
    }
    /* v1 存档不兼容，直接提示重开 */
    if(data.version !== 2 || data.guchongs.some(g => !g.species)){
        if(!silent) addLog('检测到旧版存档，已忽略（新版加入了五行与物种系统）', 'log-bad');
        return false;
    }
    const savedAt = data.savedAt || Date.now();
    Object.assign(state, {
        version: 2,
        spirit: typeof data.spirit === 'number' ? data.spirit : 120,
        guchongs: data.guchongs,
        selected: [],
        totalBattles: data.totalBattles || 0,
        wins: data.wins || 0,
        logs: Array.isArray(data.logs) ? data.logs : [],
        nextId: data.nextId || (data.guchongs.length + 1),
        codex: data.codex || {},
        pity: data.pity || 0,
        fuseFail: data.fuseFail || 0,
        savedAt: Date.now()
    });
    state.guchongs.forEach(g => {
        const sp = SPECIES_BY_ID[g.species];
        if(sp){ g.elem = sp.elem; g.tier = sp.tier; g.form = sp.form; }
        /* 旧存档补齐新字段 */
        if(typeof g.loyal !== 'number') g.loyal = LOYAL_INIT;
        if(typeof g.streak !== 'number') g.streak = 0;
        if(typeof g.best !== 'number') g.best = 0;
    });

    const elapsed = Math.max(0, (Date.now() - savedAt)/1000);
    const gain = Math.min(300, Math.floor(elapsed/3));
    if(gain > 0){
        state.spirit = Math.min(SPIRIT_MAX, state.spirit + gain);
        addLog('🌙 离线期间凝聚了 ' + gain + ' 点灵液', 'log-gold');
    }
    if(!silent) addLog('📂 读取存档成功', 'log-success');

    render(); renderLog();
    if(gain > 0){
        const r = centerOf($('spirit'));
        setTimeout(() => {
            spawnFloatText(r.x, r.y, '+' + gain, 'float-gold');
            pulseEl($('spirit'));
        }, 250);
    }
    return true;
}
function resetSave(){
    if(!confirm('确定要删除存档并重新开始吗？此操作不可撤销。')) return;
    localStorage.removeItem(SAVE_KEY);
    newGame();
    save(true);
    render(); renderLog();
}

/* ==================== 新游戏 ==================== */
function newGame(){
    state.spirit = 120;
    state.guchongs = [];
    state.selected = [];
    state.totalBattles = 0;
    state.wins = 0;
    state.logs = [];
    state.nextId = 1;
    state.codex = {};
    state.pity = 0;
    state.fuseFail = 0;

    /* 开局：三只凡虫，覆盖不同属性，便于体验克制 */
    const opening = ['m1','w1','s1'];
    opening.forEach(id => {
        const sp = SPECIES_BY_ID[id];
        const g = genGuchong(sp, 0, 1);
        applyTalentBase(g);
        state.guchongs.push(g);
        unlockCodex(g);
    });

    addLog('🕷 你踏入万蛊窟，开始了养蛊之路……', 'log-info');
    addLog('提示：五行相克 —— 金克木、木克土、土克水、水克火、火克金', 'log-bad');
    addLog('提示：同属性同阶相融可晋阶；融合有失败风险，主蛊会受损', 'log-info');
}

/* ==================== 事件 ==================== */
function bindEvents(){
    $('grid').addEventListener('click', e => {
        const card = e.target.closest('.guchong-card');
        if(!card || busy) return;
        toggleSelect(card.dataset.id);
    });
    $('btn-hatch').addEventListener('click', hatch);
    $('btn-fuse').addEventListener('click', fuse);
    $('btn-battle').addEventListener('click', doBattle);
    $('btn-soothe').addEventListener('click', soothe);
    $('btn-clear').addEventListener('click', () => { if(busy) return; state.selected = []; render(); });
    $('btn-save').addEventListener('click', () => save(false));
    $('btn-load').addEventListener('click', () => { if(busy) return; load(false); });
    $('btn-reset').addEventListener('click', resetSave);

    $('divine').querySelectorAll('.divine-btn').forEach(btn => {
        btn.addEventListener('click', () => resolveDivine(btn.dataset.hand));
    });

    window.addEventListener('beforeunload', () => save(true));
    document.addEventListener('visibilitychange', () => {
        if(document.hidden){
            ambientOn = false;
            save(true);
        } else {
            ambientOn = true;
        }
    });
}

/* ==================== 初始化 ==================== */
function init(){
    bindEvents();
    hideDivinePanel();

    const ok = load(true);
    if(!ok){
        newGame();
        save(true);
    }
    renderLog();
    render();

    /* 灵液自然凝聚 */
    setInterval(() => {
        if(state.spirit < SPIRIT_MAX && !document.hidden){
            state.spirit = Math.min(SPIRIT_MAX, state.spirit + 1);
            $('spirit').textContent = Math.floor(state.spirit);
        }
    }, 3000);
    /* 常驻灵气 */
    setInterval(ambientTick, 220);
    /* 静默存档 */
    setInterval(() => { if(!document.hidden) save(true); }, 20000);
}

init();
"""

# ======================================================== HTML 模板 ========
TPL = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>万蛊之王 - 养蛊小游戏</title>
<style>
__STYLE__
</style>
</head>
<body>
<canvas id="fx"></canvas>

<div class="container">
    <h1 class="game-title">万蛊之王</h1>
    <div class="game-sub">五 行 相 克 · 炼 蛊 成 道</div>

    <div class="panel">
        <div class="stats-row">
            <div class="stat"><span class="stat-label">灵液</span><span class="stat-value" id="spirit">0</span></div>
            <div class="stat"><span class="stat-label">蛊虫</span><span class="stat-value" id="count">0/12</span></div>
            <div class="stat"><span class="stat-label">战绩</span><span class="stat-value" id="record">0/0</span></div>
        </div>
        <div class="btn-row">
            <button class="btn" id="btn-hatch">孵化蛊虫 (20灵液)</button>
            <button class="btn btn-jade" id="btn-fuse">融 合 (10灵液)</button>
            <button class="btn btn-ghost" id="btn-soothe">安 抚</button>
            <button class="btn btn-ghost" id="btn-clear">清空选择</button>
        </div>
        <div class="btn-row">
            <button class="btn btn-ghost" id="btn-save">手动存档</button>
            <button class="btn btn-ghost" id="btn-load">读取存档</button>
            <button class="btn btn-ghost" id="btn-reset">删除存档</button>
        </div>
        <div class="hint">
            选中 <b>1 只</b>可出战，选中 <b>2 只</b>可融合（<b>先点的是主蛊</b>，融合失败时主蛊存活但属性下降，副蛊消散）。
            <br>败北会<b>降低忠心</b>，忠心过低可能<b>反叛离巢</b>；连胜会积累<b>不败信念</b>（每胜 +6% 属性，上限 +60%），一败清零。
        </div>
        <div class="legend">
            <span>五行相克：</span>
            <span class="legend-chip" style="color:#d8c98a">金克木</span>
            <span class="legend-chip" style="color:#5fc98a">木克土</span>
            <span class="legend-chip" style="color:#d8b878">土克水</span>
            <span class="legend-chip" style="color:#63a9e8">水克火</span>
            <span class="legend-chip" style="color:#ff8a4a">火克金</span>
            <span>克制伤害 ×1.5／被克 ×0.65</span>
        </div>
    </div>

    <div class="panel">
        <div class="panel-title">蛊虫巢穴</div>
        <div class="guchong-grid" id="grid"></div>
    </div>

    <div class="panel">
        <div class="panel-title">斗蛊场</div>
        <div class="battle-arena">
            <div class="battle-side" id="side-left">
                <div class="gu-figure" id="battle-left-fig"></div>
                <div class="battle-name" id="battle-left-name">—</div>
                <div class="battle-sub" id="battle-left-sub"></div>
                <div class="hp-bar"><div class="hp-fill" id="battle-left-hp"></div></div>
                <div class="hp-text" id="battle-left-text">0 / 0</div>
            </div>
            <div class="battle-vs">VS</div>
            <div class="battle-side" id="side-right">
                <div class="gu-figure" id="battle-right-fig"></div>
                <div class="battle-name" id="battle-right-name">—</div>
                <div class="battle-sub" id="battle-right-sub"></div>
                <div class="hp-bar"><div class="hp-fill foe" id="battle-right-hp"></div></div>
                <div class="hp-text" id="battle-right-text">0 / 0</div>
            </div>
        </div>

        <div class="divine-panel" id="divine" style="display:none">
            <div class="divine-title">卜 卦 · 第 <b id="divine-round">1 / 15</b> 回合 —— 预测对手阵眼</div>
            <div class="divine-row">
                <button class="divine-btn" data-hand="攻击">⚔ 攻击</button>
                <button class="divine-btn" data-hand="毒力">☠ 毒力</button>
                <button class="divine-btn" data-hand="防御">⛨ 防御</button>
                <button class="divine-btn" data-hand="速度">⚡ 速度</button>
                <button class="divine-btn" data-hand="灵性">✦ 灵性</button>
            </div>
            <div class="divine-result" id="divine-result"></div>
        </div>

        <div class="btn-row">
            <button class="btn" id="btn-battle">挑战野生蛊虫</button>
        </div>
    </div>

    <div class="panel">
        <div class="panel-title">万蛊图鉴</div>
        <div class="codex-grid" id="codex"></div>
    </div>

    <div class="panel">
        <div class="panel-title">蛊师手札</div>
        <div class="log-box" id="log"></div>
    </div>
</div>

<script>
__SCRIPT__
</script>
</body>
</html>
"""

def main():
    use_img = bool(USE_IMAGES and images_ready())
    if USE_IMAGES and not use_img:
        print("!! 警告：assets/gu 下配图不完整，已回退到内置 SVG 插图")
    script = SCRIPT_BODY.replace("__USE_IMAGES__", "true" if use_img else "false")
    script = script.replace("__IMG_EXT__", IMG_EXT)
    html = TPL.replace("__STYLE__", STYLE_BODY).replace("__SCRIPT__", script)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("wrote %s  %.1f KB  %d lines  | 配图: %s (.%s)"
          % (OUT, len(html.encode("utf-8")) / 1024.0, html.count("\n") + 1,
             "启用 (assets/gu)" if use_img else "关闭 (内置SVG)", IMG_EXT))
    # 网页部署版：同名内容复制一份为 index.html（GitHub Pages 入口）
    if use_img:
        with io.open("index.html", "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        print("wrote index.html  (GitHub Pages 入口)")

if __name__ == "__main__":
    main()
