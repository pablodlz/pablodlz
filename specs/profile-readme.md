# Spec — README do perfil (`pablodlz/pablodlz`)

> Especificação do README do perfil. Fonte de verdade dos dados:
> `data/linkedin.json` do repo `pablodlz/portfolio` — **nada é inventado**.

## 1. Objetivo

README **minimalista, profissional e criativo**, que herda o *espírito* do
portfólio (https://pablodlz.github.io/portfolio/) — identidade de terminal e de
segurança — mas com estética enxuta e um **único acento teal `#00B2DF`**.
Comunicar em segundos: quem é o Pablo, o que faz (SOC / Ofensiva / AppSec),
onde encontrá-lo, e puxar pro portfólio.

## 2. Direção de design

- **Minimalismo:** muito respiro, sem "muros" de badges, sem widgets decorativos
  em excesso. Um acento só (`#00B2DF`) sobre fundo escuro.
- **Sem imagens locais:** removidos o banner e o mascote de `files/`. Nada de
  `<img src="files/...">`. O visual vem de tipografia, blocos de terminal e de
  serviços SVG externos discretos (typing, stats).
- **Terminal como assinatura:** blocos `$ whoami` / `$ cat about.txt` amarram
  ao site sem pesar.
- **Badges monocromáticos teal:** chip escuro `#0d1117` + ícone `#00B2DF` —
  uma única linguagem visual (conectar + stack).
- **Curadoria:** só o que é real e relevante.

## 3. Tokens

| token | valor |
|------|------|
| accent | `#00B2DF` |
| bg / chip | `#0d1117` |
| texto | `#c9d1d9` |
| texto-fraco | `#8b949e` |
| fonte | monoespaçada |

## 4. Arquitetura da informação (enxuta)

1. **Cabeçalho** (centro): nome + papel + typing SVG teal (1 linha, discreta) +
   linha de conexões (badges teal-mono).
2. **`$ whoami` / `$ cat about.txt`** — bloco de terminal com o essencial
   (cargo, bio curta, formação, local, foco). Duas primeiras linhas são
   DINÂMICAS (bot, ver §4.1): **`Last login:`** (banner SSH) e **`uptime:`**
   (dias operando no SOC — ecoa o comando `uptime` do portfólio).
3. **Stack** — badges teal-mono agrupados (Blue Team/SOC, Ofensiva,
   AppSec/DevSecOps, Linguagens) + 1 linha de pesquisa (ML).
4. **Certs** — 1 linha (chips de código): CEH, CNSE, CSAE, CPTE, CRTA, 50+, alvos.
5. **`> cat foco.md`** — "now page": foco atual (red team/pentest rumo ao OSCP,
   CEH v13, artigo de ML, rotina de CTFs). Sinal alto e barato de intenção.
6. **`> ls ~/projetos`** — projetos em destaque (tabela): portfólio (com demo)
   e este perfil.
7. **`> tail -f atividade.log`** — atividade recente REAL em formato de log de
   terminal, gerada automaticamente (ver §4.1).
7.5. **`> map --areas`** — diagrama **mermaid** (flowchart LR, tema teal via
   `%%{init}%%`) das 4 áreas + o loop blue↔red ("entender o ataque" / "defender
   melhor"). Nativo do GitHub, sem serviço externo. (ideia: pr2tik1)
8. **`> neofetch`** — card estilo neofetch (b1t ASCII + info) com stats REAIS
   (repos/seguidores/estrelas/top langs) — AUTO-COMPUTADO pelo bot (ver §4.1).
9. **`> languages --top`** — barra ASCII teal das linguagens, % por bytes,
   AUTO-COMPUTADA pelo bot. **Substitui** o github-readme-stats, que vivia
   caindo (503 DEPLOYMENT_PAUSED) — o motivo real de "stats não funciona".
10. **`> git log --graph`** — cobrinha (snake) TEAL, gerada pelo `snake.yml`
    (branch `output`). Reposta a pedido; workflow modernizado (Platane/snk@v3,
    cores teal, cron 1×/dia — o cron antigo `* */12` rodava 60×/hora).
11. **Rodapé** (centro) — GIF de código + badge **Open Source** (original, honesto:
    portfólio/perfil são de fato abertos — NÃO o "opensource story" plagiado do
    backup) + `./pablodlz.sh` + CTA pro portfólio.
12. **Bordas** (topo e rodapé) — ondas `capsule-render` em teal `#00B2DF`
    (recoloridas do backup, que era azul `#5bcdec`).

**Extras vindos do backup (a pedido do Pablo), recoloridos p/ teal:**
- **Streak** via `streak-stats.demolab.com` (herokuapp do backup morreu) — confiável.
- **WakaTime week stats** via mirror `github-readme-stats-taupe-two.vercel.app`
  (o `github-readme-stats.vercel.app` principal vive em 503). Depende de conta
  WakaTime pública (`wakatime.com/@pablodlz`) + o plugin do editor rastreando —
  senão o card vem vazio. É um serviço externo (pode oscilar).
- **"GIF"** → substituído pelo **b1t animado próprio** (`assets/b1t.svg`, SVG
  autoral com SMIL: flutua, antena pulsa, olhos piscam — tema teal). Zero
  dependência de terceiro (o `code.gif` do backup era de outro usuário) e é a
  cara do site (o mascote). SVG animado renderiza no GitHub via camo.
- streak + wakatime EMPILHADOS (cada um em sua linha, `width=460`) → responsivo
  no desktop e no mobile (evita overflow/desalinho dos aspect-ratios diferentes).


### 4.1 Conteúdo dinâmico (GitHub Actions)

O que o mercado valoriza em 2026: sinal real e vivo, não decoração. Duas
seções se atualizam sozinhas via `.github/workflows/update-readme.yml`
(cron a cada 8h + manual; SEM trigger de push, p/ não criar churn/loop de
commits do bot), que roda `.github/scripts/atividade.py` (stdlib, sem deps):

- **`Last login:`** — carimbo de data/hora (UTC-3 fixo; Brasil não tem mais
  horário de verão) no topo do bloco whoami, como um banner SSH real.
  O IP `10.10.14.7` é o clássico IP de atacante da VPN do Hack The Box (piada
  interna pra quem é da área).
- **`uptime:`** — dias operando no SOC (desde `SOC_START = 2025-10-01`),
  calculado pelo bot. Ecoa o comando `uptime` do terminal do portfólio.
- **`atividade.log`** — últimos 6 eventos públicos do GitHub (push/PR/issue/
  release/star/fork) em formato `[dd/mm hh:mm] tipo repo "mensagem"`, entre os
  marcadores `<!--ATIVIDADE:START/END-->`. Gotcha: o payload de PushEvent da
  API de eventos NÃO traz mais os commits → a mensagem é buscada à parte via
  `/repos/{repo}/commits/{sha}` (fallback: linha sem mensagem). Falha de API
  não derruba o README (mantém o bloco anterior).
- O commit do bot usa `GITHUB_TOKEN` → não re-dispara o workflow (sem loop).
- **`> neofetch` e `> languages`** (blocos `<!--NEOFETCH-->` / `<!--LANGS-->`):
  o bot busca `/users/{u}` (repos/seguidores) + `/users/{u}/repos` e soma o
  `/languages` de cada repo (bytes) → barra ASCII teal + card neofetch. Isso
  troca o github-readme-stats externo (503 recorrente) por dado próprio e
  confiável. Falha de API → mantém o bloco anterior.

## 5. Dados reais (de `linkedin.json`)

- Cargo: Analista de Operações de Segurança (SOC) @ Clavis Segurança da Informação.
- Formação: Tec. Segurança da Informação (Fatec) + Pós em Cibersegurança Ofensiva (Acadi-TI).
- SOC: SIEM (Octopus, Wazuh, Rapid7), phishing, triagem, playbooks, Jira/SLA.
- AppSec: SSDLC, threat modeling (DFD/STRIDE), SAST/DAST/SCA (Snyk, Horusec, ZAP), CI/CD.
- Frameworks: OWASP, NIST, MITRE ATT&CK. Pentest/CTFs/labs.
- Pesquisa: ML aplicado à detecção de ransomware (artigo em publicação).
- Certs: CNSE/CSAE/CPTE (ok), CRTA/CEH v13 AI (andamento); alvos: Security+, Pentest+, eJPT, DCPT, OSCP.
- Sociais (`pablodlz`): HackerOne, Bugcrowd, HTB, LetsDefend. Contato: pablogalerani@gmail.com.

## 6. Restrições (README no GitHub)

- HTML sanitizado: sem `<script>`/`<style>`/`style=` (só `align`). "Movimento"
  só via serviços SVG externos.
- Sem imagens locais nesta versão (decisão de produto).
- Emojis, code blocks, `<div align>`, badges e links funcionam.

## 7. Critérios de aceite

- [ ] Um único acento `#00B2DF`; visual minimalista e coeso.
- [ ] Sem `<img src="files/...">`; assets de imagem removidos do repo.
- [ ] Zero dados de terceiros; tudo confere com `linkedin.json`.
- [ ] Links resolvem (200); serviços de badge vivos (demolab/komarev/shields).
- [ ] Legível no mobile (largura fluida, sem overflow horizontal).
