#!/usr/bin/env python3
"""Atualiza o README do perfil: linha "Last login" (banner SSH) + bloco de
atividade recente em formato de log de terminal.

Rodado pelo workflow update-readme.yml. Sem dependências externas — só stdlib.
Falha de API não derruba o README: mantém o bloco anterior.
"""
import json
import os
import re
import urllib.request
from datetime import datetime, timedelta, timezone

USER = "pablodlz"
# Brasília é UTC-3 fixo (sem horário de verão desde 2019) → offset fixo
# dispensa o banco IANA (tzdata), que não existe no Python do Windows
TZ = timezone(timedelta(hours=-3))
SOC_START = datetime(2025, 10, 1, tzinfo=TZ)  # início no SOC da Clavis
DIAS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
MAX_LINHAS = 6
# robô b1t em ASCII (blocos full-width → alinham em qualquer mono)
LOGO = [
    "  ▄▄▄▄▄▄▄  ",
    "  █ ▄ ▄ █  ",
    "  █  ▀  █  ",
    "  ▀▄▄▄▄▄▀  ",
    "   █   █   ",
    "  ▀▀   ▀▀  ",
]


def _get(url):
    headers = {"User-Agent": USER, "Accept": "application/vnd.github+json"}
    token = os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch_events():
    return _get(f"https://api.github.com/users/{USER}/events/public?per_page=30")


def commit_msg(repo_full, sha):
    """O payload de PushEvent não traz mais os commits → busca a mensagem
    pelo SHA. Falhou? Retorna vazio (a linha sai sem mensagem)."""
    try:
        c = _get(f"https://api.github.com/repos/{repo_full}/commits/{sha}")
        return c.get("commit", {}).get("message", "")
    except Exception:
        return ""


def short(txt, n=46):
    txt = txt.strip().splitlines()[0] if txt and txt.strip() else ""
    return (txt[: n - 1] + "…") if len(txt) > n else txt


def line_for(ev):
    t = datetime.fromisoformat(ev["created_at"].replace("Z", "+00:00")).astimezone(TZ)
    stamp = t.strftime("%d/%m %H:%M")
    repo = ev["repo"]["name"].removeprefix(f"{USER}/")
    p = ev.get("payload", {})
    kind = ev["type"]
    if kind == "PushEvent":
        branch = (p.get("ref") or "").removeprefix("refs/heads/")
        raw = commit_msg(ev["repo"]["name"], p.get("head", ""))
        if raw.startswith(("Merge branch", "Merge pull request", "Merge remote")):
            raw = ""  # ruído de merge → mostra só o push pro branch
        if "writeups" in raw.lower():
            raw = ""  # não expõe menção a repo removido no log
        msg = short(raw)
        if msg:
            return f'[{stamp}] push     {repo:<12} "{msg}"'
        return f"[{stamp}] push     {repo:<12} → {branch or 'main'}"
    if kind == "PullRequestEvent":
        pr = p.get("pull_request", {})
        act = {"opened": "abriu", "reopened": "reabriu", "closed": "fechou"}.get(p.get("action"), p.get("action", ""))
        if p.get("action") == "closed" and pr.get("merged"):
            act = "merge de"
        return f"[{stamp}] pr       {repo:<12} {act} #{p.get('number', '?')} {short(pr.get('title', ''), 32)}"
    if kind == "IssuesEvent":
        act = {"opened": "abriu", "closed": "fechou"}.get(p.get("action"), p.get("action", ""))
        return f'[{stamp}] issue    {repo:<12} {act} "{short(p.get("issue", {}).get("title", ""), 34)}"'
    if kind == "CreateEvent" and p.get("ref_type") == "repository":
        return f"[{stamp}] create   {repo:<12} novo repositório"
    if kind == "ReleaseEvent" and p.get("action") == "published":
        return f"[{stamp}] release  {repo:<12} {p.get('release', {}).get('tag_name', '')}"
    if kind == "WatchEvent":
        return f"[{stamp}] star     {ev['repo']['name']}"
    if kind == "ForkEvent":
        return f"[{stamp}] fork     {ev['repo']['name']}"
    if kind == "PublicEvent":
        return f"[{stamp}] public   {repo:<12} repositório aberto ao público"
    return None


def replace_block(readme, name, content):
    return re.sub(
        rf"<!--{name}:START-->.*?<!--{name}:END-->",
        f"<!--{name}:START-->\n{content}\n<!--{name}:END-->",
        readme,
        flags=re.S,
    )


def aggregate_langs(repos):
    agg = {}
    for r in repos:
        if r.get("fork"):
            continue
        try:
            for lang, b in _get(r["languages_url"]).items():
                agg[lang] = agg.get(lang, 0) + b
        except Exception:
            pass
    return agg


def render_langs_bar(langs, n=6, width=22):
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda x: -x[1])[:n]
    rows = []
    for name, b in top:
        pct = b / total * 100
        fill = round(pct / 100 * width)
        bar = "█" * fill + "░" * (width - fill)
        rows.append(f"{name:<13}{bar} {pct:5.1f}%")
    return "\n".join(rows)


def render_neofetch(dias, n_repos, followers, stars, top_langs):
    info = [
        "pablodlz@github",
        "─────────────────────────────────",
        " role.....: SOC Analyst @ Clavis",
        f" uptime...: {dias}d no SOC · rumo ao OSCP",
        f" repos....: {n_repos} públicos · seguidores {followers}",
        f" stars....: {stars}",
        " top langs: " + (" · ".join(top_langs[:3]) if top_langs else "—"),
        " certs....: 50+ · CEH v13 (AI)",
        " stack....: Kali · Splunk · Burp · Python",
    ]
    pad = " " * len(LOGO[0])
    rows = []
    for i, txt in enumerate(info):
        art = LOGO[i - 2] if 2 <= i < 2 + len(LOGO) else pad
        rows.append(f"{art}  {txt}")
    return "\n".join(rows)


def main():
    with open("README.md", encoding="utf-8") as f:
        readme = f.read()

    # NOTA: as linhas "Last login:" e "uptime:" foram removidas do README
    # (o dono deixou o bloco "Sobre mim" estático) → o bot NÃO as mexe mais.
    now = datetime.now(TZ)
    dias = (now - SOC_START).days  # ainda usado no neofetch, se o marcador existir

    # atividade recente (log de terminal)
    lines = []
    try:
        for ev in fetch_events():
            ln = line_for(ev)
            if ln:
                lines.append(ln)
            if len(lines) >= MAX_LINHAS:
                break
    except Exception as e:  # API indisponível → mantém bloco anterior
        print(f"aviso: eventos indisponíveis ({e})")
    if lines:
        block = "```text\n" + "\n".join(lines) + "\n```"
        readme = replace_block(readme, "ATIVIDADE", block)

    # stats + linguagens auto-computados (substituem o serviço externo que cai)
    n_langs = 0
    try:
        user = _get(f"https://api.github.com/users/{USER}")
        repos = _get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&sort=pushed")
        langs = aggregate_langs(repos)
        n_langs = len(langs)
        stars = sum(r.get("stargazers_count", 0) for r in repos if not r.get("fork"))
        n_repos = user.get("public_repos", sum(1 for r in repos if not r.get("fork")))
        followers = user.get("followers", 0)
        top = [k for k, _ in sorted(langs.items(), key=lambda x: -x[1])[:3]]
        readme = replace_block(readme, "NEOFETCH", "```text\n" + render_neofetch(dias, n_repos, followers, stars, top) + "\n```")
        if langs:
            readme = replace_block(readme, "LANGS", "```text\n" + render_langs_bar(langs) + "\n```")
    except Exception as e:  # API indisponível → mantém blocos anteriores
        print(f"aviso: stats indisponíveis ({e})")

    with open("README.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(readme)
    print(f"ok: {len(lines)} evento(s) · {n_langs} linguagem(ns)")


if __name__ == "__main__":
    main()
