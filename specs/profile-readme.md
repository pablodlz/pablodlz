# Spec — README do perfil (`pablodlz/pablodlz`)

> Especificação do README do perfil. Fonte de verdade dos dados:
> `data/linkedin.json` do repo `pablodlz/portfolio` — **nada é inventado**.

## 1. Objetivo

README **minimalista, profissional e criativo**, que herda o *espírito* do
portfólio (https://pablodlz.github.io/portfolio/) — identidade de terminal e de
segurança — mas com estética enxuta e um **único acento teal `#0DD1CA`**.
Comunicar em segundos: quem é o Pablo, o que faz (SOC / Ofensiva / AppSec),
onde encontrá-lo, e puxar pro portfólio.

## 2. Direção de design

- **Minimalismo:** muito respiro, sem "muros" de badges, sem widgets decorativos
  em excesso. Um acento só (`#0DD1CA`) sobre fundo escuro.
- **Sem imagens locais:** removidos o banner e o mascote de `files/`. Nada de
  `<img src="files/...">`. O visual vem de tipografia, blocos de terminal e de
  serviços SVG externos discretos (typing, stats).
- **Terminal como assinatura:** blocos `$ whoami` / `$ cat about.txt` amarram
  ao site sem pesar.
- **Badges monocromáticos teal:** chip escuro `#0d1117` + ícone `#0DD1CA` —
  uma única linguagem visual (conectar + stack).
- **Curadoria:** só o que é real e relevante.

## 3. Tokens

| token | valor |
|------|------|
| accent | `#0DD1CA` |
| bg / chip | `#0d1117` |
| texto | `#c9d1d9` |
| texto-fraco | `#8b949e` |
| fonte | monoespaçada |

## 4. Arquitetura da informação (enxuta)

1. **Cabeçalho** (centro): nome + papel + typing SVG teal (1 linha, discreta) +
   linha de conexões (badges teal-mono).
2. **`$ whoami` / `$ cat about.txt`** — bloco de terminal com o essencial
   (cargo, bio curta, formação, local, foco).
3. **Stack** — badges teal-mono agrupados (Blue Team/SOC, Ofensiva,
   AppSec/DevSecOps, Linguagens) + 1 linha de pesquisa (ML).
4. **Certs** — 1 linha (chips de código): CEH, CNSE, CSAE, CPTE, CRTA, 50+, alvos.
5. **`> ./stats`** — 2 cards do github-readme-stats no tema teal (stats + langs).
   Sem troféus/streak/snake (minimalismo).
6. **Rodapé** (centro) — 1 linha de terminal (`./pablodlz.sh`) + CTA pro portfólio.

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

- [ ] Um único acento `#0DD1CA`; visual minimalista e coeso.
- [ ] Sem `<img src="files/...">`; assets de imagem removidos do repo.
- [ ] Zero dados de terceiros; tudo confere com `linkedin.json`.
- [ ] Links resolvem (200); serviços de badge vivos (demolab/komarev/shields).
- [ ] Legível no mobile (largura fluida, sem overflow horizontal).
