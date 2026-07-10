# Spec — README do perfil (`pablodlz/pablodlz`)

> Documento de especificação do README do perfil do GitHub. Mesmo método
> spec-driven do portfólio. Fonte de verdade dos dados: `data/linkedin.json`
> do repo `pablodlz/portfolio` — **nada é inventado**.

## 1. Objetivo

Um README de perfil que seja **inconfundivelmente do mesmo autor do portfólio**
(https://pablodlz.github.io/portfolio/): premium, criativo, estética de terminal
Kali com um único acento laranja. Deve comunicar em segundos: _quem é o Pablo,
o que ele faz (SOC / Ofensiva / AppSec) e onde encontrá-lo_ — e levar ao portfólio.

## 2. Público

- Recrutadores de segurança (BR, principalmente) — idioma **PT-BR**.
- Comunidade de segurança (HackerOne, Bugcrowd, HTB, LetsDefend).
- Curiosos que caem no perfil pelo portfólio ou pelo LinkedIn.

## 3. Princípios de design (herdados do site)

- **Acento único:** laranja `#ff5024` sobre fundo escuro `#0d1117`/`#151413`.
- **Identidade de terminal:** prompts `root@kali`, comandos `./algo.sh`, base64,
  `nmap · sqlmap · matrix`. Nada de dump genérico de badges.
- **Curadoria > quantidade:** só o que é real e relevante (o README antigo era um
  dump copiado de terceiros — descartado por completo).
- **Mascote b1t:** o robô cyber é a assinatura do site → aparece no README.
- **Gamificação discreta:** um easter egg (base64 → flag) que puxa pro portfólio.

## 4. Tokens

| token | valor |
|------|------|
| accent | `#ff5024` |
| bg | `#0d1117` |
| card | `#151413` |
| texto | `#c9d1d9` |
| texto-fraco | `#8a8378` |
| fonte | JetBrains Mono / monospace |

## 5. Arquitetura da informação

1. **Herói** — banner de terminal (`files/perfil-final2.png`) que o Pablo já
   produziu: janela `root@kali`, retrato ASCII, bloco `./pablodlz.sh` com whoami.
2. **Taglines** — typing SVG laranja (serviço `demolab`, mantido).
3. **Conectar** — badges: Portfólio, LinkedIn, HackerOne, Bugcrowd, HTB,
   LetsDefend, Email. + contador de visitas (`komarev`).
4. **`> cat sobre.txt`** — 3–4 linhas de bio real, punchy.
5. **`> ./stack.sh`** (colapsável) — arsenal real agrupado (SOC/Defesa, Ofensiva,
   AppSec/DevSecOps, Linguagens).
6. **`> ./certs.sh`** (colapsável) — CEH, CNSE, CSAE, CPTE, CRTA, 50+, próximos alvos.
7. **`> ./stats.sh`** — stats do GitHub no tema laranja + top langs + streak.
8. **Cobrinha** — snake de contribuições (workflow já existente).
9. **Rodapé** — mascote **b1t** + easter egg base64 + CTA pro portfólio.

## 6. Fonte dos dados (reais)

De `data/linkedin.json` (`pablodlz/portfolio`):
- Cargo: Analista de Operações de Segurança (SOC) @ Clavis Segurança da Informação.
- Formação: Tec. Segurança da Informação (Fatec) + Pós em Cibersegurança Ofensiva (Acadi-TI).
- SOC: SIEM (Octopus, Wazuh, Rapid7), phishing, triagem, playbooks, Jira/SLA.
- AppSec: SSDLC, threat modeling (DFD/STRIDE), SAST/DAST/SCA (Snyk, Horusec, OWASP ZAP), CI/CD.
- Frameworks: OWASP, NIST, MITRE ATT&CK.
- Pesquisa: ML aplicado à cibersegurança (artigo em publicação).
- Certs: CNSE/CSAE/CPTE (ok), CRTA/CEH v13 AI (andamento); alvos: Security+, Pentest+, eJPT, DCPT, OSCP.
- Sociais: HackerOne, Bugcrowd, HTB, LetsDefend (todos `pablodlz`).
- Contato: pablogalerani@gmail.com · https://pablodlz.github.io/portfolio/

## 7. Inventário de assets

| asset | uso | origem |
|------|-----|--------|
| `files/perfil-final2.png` | herói | feito pelo Pablo |
| `files/perfil-final2.svg` | alt vetorial (crisp) | feito pelo Pablo |
| `files/b1t.svg` | mascote no rodapé | recriado do `Mascot.astro` (cores fixas) |
| snake `output` branch | cobrinha | `.github/workflows/snake.yml` (mantido) |

## 8. Restrições (renderização de README no GitHub)

- HTML é sanitizado: **sem** `<script>`, `<style>`, `style=` (exceto `align`).
  Nada de CSS/JS → o "movimento" vem de serviços SVG externos (typing/stats/snake).
- SVG embutido em Markdown é removido → mascote/banner entram como **imagem**
  (`<img>`), não SVG inline. Animações SMIL/CSS em SVG referenciado por `<img>`
  **não animam** no GitHub (renderiza 1 frame) → b1t é estático.
- Imagens por **caminho relativo** funcionam no README de perfil.
- Emojis, code blocks, `<details>`, `<div align>` funcionam.

## 9. O que reaproveitar do README antigo (`bkp/`)

- ✅ Padrão de seções colapsáveis `<details>` (organização).
- ✅ Cobrinha (snake) e widgets de stats.
- ❌ Todo o CONTEÚDO — era copiado de gautamkrishnar, duartbreedt e thewhiteh4t.
  O `bkp/` **não vai** pro repo público (contém dados de terceiros).

## 10. Critérios de aceite

- [ ] Zero dados de terceiros; tudo é do Pablo e confere com o `linkedin.json`.
- [ ] Estética coerente com o site (laranja único, terminal, b1t).
- [ ] Banner do Pablo como herói; b1t no rodapé.
- [ ] Todos os links resolvem (200); imagens referenciadas existem no repo.
- [ ] Serviços de badge mantidos (nada de `herokuapp`/`glitch.me` mortos).
- [ ] Legível no mobile (largura fluida, sem overflow horizontal).
