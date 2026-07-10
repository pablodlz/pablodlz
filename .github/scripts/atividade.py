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


def main():
    with open("README.md", encoding="utf-8") as f:
        readme = f.read()

    # banner SSH: Last login sempre fresco (fuso de Brasília)
    now = datetime.now(TZ)
    login = (
        f"Last login: {DIAS[now.weekday()]}, {now.day:02d} {MESES[now.month - 1]} "
        f"{now.year} {now:%H:%M} -03 from 10.10.14.7"
    )
    readme = re.sub(r"^Last login: .*$", login, readme, count=1, flags=re.M)

    # uptime: dias operando no SOC (estilo do comando `uptime` do portfólio)
    dias = (now - SOC_START).days
    uptime = f"uptime: {dias} dias operando no SOC @ Clavis · rumo ao OSCP"
    readme = re.sub(r"^uptime: .*$", uptime, readme, count=1, flags=re.M)

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
        readme = re.sub(
            r"<!--ATIVIDADE:START-->.*?<!--ATIVIDADE:END-->",
            "<!--ATIVIDADE:START-->\n" + block + "\n<!--ATIVIDADE:END-->",
            readme,
            flags=re.S,
        )

    with open("README.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(readme)
    print(f"ok: {login} · {len(lines)} evento(s)")


if __name__ == "__main__":
    main()
