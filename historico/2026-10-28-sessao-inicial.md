# Histórico — sessão inicial do Trainer Chat

> Resumo da primeira conversa com o Claude (28/10 a 10/11/2026): setup do MazyOS,
> pesquisas, decisões e o que ficou pendente. Serve pra retomar o projeto em
> outro computador sem perder o fio.

---

## 1. Setup (/instalar)

- **Perfil:** Freelancer
- **Produto:** Trainer Chat — "Monto um atendente de IA no WhatsApp que responde e agenda clientes 24h pro teu negócio."
- **Clientes-alvo:** academia, salão, loja, restaurante e afins
- **Equipe:** só o Rafael
- **Tom:** direto, informal, sem muitos emojis
- **Gargalo:** não saber como fazer o programa
- **Tarefa repetitiva pra automatizar:** explicar o produto pro cliente
- **Marca:** logo em `identidade/logo.png`; fundo `#012E1C`, verde `#26E662`, texto branco
- Arquivos preenchidos: `_memoria/empresa.md`, `_memoria/preferencias.md`, `_memoria/estrategia.md`, `identidade/design-guide.md`, `CLAUDE.md`

## 2. Vídeos analisados

### Vídeo 1 — "Agente de IA no WhatsApp em ~30 min" (arquivo local)
Arquitetura em 8 passos: planejar no Claude Code → app no Meta for Developers →
webhook → IA via OpenRouter → memória da conversa → base do negócio (serviços,
preços, horários, FAQ, regras) → ferramentas (agenda Cal.com) → testes e VPS 24h.
Fluxo final: **WhatsApp → IA → Memória → Negócio → Ferramentas → No ar.**

### Vídeo 2 — "WhatsApp: Como criar um CHATBOT ou AGENTE DE IA com CLAUDE" (YouTube, canal Maycon, 12 min)
- **O título engana:** não tem IA nem Claude. É um bot de **menu com botões** da plataforma **Focry** (focry.com.br), com "licença vitalícia grátis" pra captar lead.
- Conexão por **QR code** (não oficial).
- Recursos: botões (até 3), listas (até 10), título em negrito com nome do atendente, mensagem de resposta inválida, captura de resposta (`{{ultima_mensagem}}`), mídia (foto, vídeo, documento, áudio "gravado na hora"), `#` volta ao menu, pausar atendimento por X minutos.
- **Ideias pro Trainer Chat (com código próprio):** bot **híbrido** — IA conversa naturalmente + botões/listas só em etapas fechadas (produto, horário, pagamento); pausar bot quando humano assume; repetir dados do cliente.

## 3. Pesquisa de mercado

- **Concorrentes prontos:** Chatvolt, ConverZAP (R$ 99–299/mês), SocialHub (anuncia R$ 99), Clint (R$ 400–1.500 custo total PME), FiqOn (a partir de R$ 24,90).
- **Modelo de cobrança comum:** taxa de implantação (uma vez) + mensalidade.
- **"Treinar" o bot** = dar uma ficha do negócio + conversas reais como exemplo. Ninguém treina IA do zero.
- **Regra da Meta (desde 15/01/2026):** proibido assistente de IA "de uso geral" no WhatsApp Business. Bot focado no negócio do cliente é permitido.
- **SocialHub:** oferece **API oficial e QR code** (está no site deles). Qual ferramenta de QR usam por dentro não é público — perguntar na demo.

### Conexão com WhatsApp — opções

| | API oficial Meta (Cloud API) | QR code (Evolution API, WAHA, WPPConnect, Baileys) |
|---|---|---|
| Custo | 1.000 msgs de atendimento grátis/mês por número; depois ~R$ 0,035/msg (out/2026) | Grátis (só servidor) |
| Banimento | Risco muito baixo | Risco real (viola termos do WhatsApp) |
| Burocracia | Conta Meta; escalar com botão "Conectar WhatsApp" exige Tech Provider + CNPJ | Nenhuma: lê QR code |

Sem CNPJ próprio, a API oficial ainda funciona com a conta no nome/CNPJ do cliente e o Rafael como administrador.

## 4. Decisões tomadas

1. **Sem CNPJ** — nem agora nem depois. Cobrar como pessoa física (consultar contador sobre carnê-leão).
2. **Conexão por QR code (Evolution API)**, sem Meta por enquanto. Meta só no futuro, como plano premium se algum cliente pedir.
   > ⚠️ Os arquivos `CLAUDE.md` e `_memoria/empresa.md` ainda dizem "API oficial da Meta" — atualizar.
3. **Versão 1 do produto:** responder naturalmente com IA, treinar com ficha do negócio + conversas reais, lembrar a conversa, passar pra humano. Agenda e campanhas depois.
4. **Motor de IA trocável** (OpenAI, Gemini, Claude ou OpenRouter) e **conector de WhatsApp trocável** no código.
5. **Código próprio**, sem copiar código de concorrente (só funcionalidade).

### Proteções anti-banimento (construir uma vez, valem pra todos os clientes)
- Bot **só responde**, nunca dispara primeiro / em massa
- "Digitando..." + espera de 2–5 s antes de responder
- Respostas variadas (IA)
- Limite de mensagens por hora
- Bloqueio de link encurtado
- Horário de atendimento opcional
- **Alerta quando o número desconectar**
- Na implantação: número antigo/aquecido, WhatsApp Business, cliente avisado do risco por escrito

## 5. Conta de lucro (estimativa, com QR code)

| | 3 clientes × R$ 250 | 10 clientes × R$ 250 |
|---|---|---|
| Entra | R$ 750 | R$ 2.500 |
| VPS (um pra todos) | − R$ 50 | − R$ 80 |
| IA (~R$ 20/cliente) | − R$ 60 | − R$ 200 |
| **Sobra** | **≈ R$ 640** | **≈ R$ 2.220** |

Valores de IA e VPS são estimativa — medir com um cliente de teste. Limitar plano ("até X atendimentos/mês").

## 6. Ferramentas instaladas

- **Superpowers** — plugin do Claude Code, escopo do projeto (`/plugin install superpowers@anthropic-plugin-directory`)
- **REA** — MCP de engenharia reversa, global (`npm i -g rea-agents@6.4.0` + `rea setup --client claude_code --yes`). Precisa do Ghidra em `C:\tools\ghidra_12.1.4_PUBLIC`.
- **Pipecat** — `.venv/` do projeto (`python -m venv .venv` + `pip install pipecat-ai`). Reservado pra versão por telefone.
- **Mimic** — instalado e depois **removido** a pedido.
- **Skill `/analisar-video`** — global em `~/.claude/skills/analisar-video/` (cópia de backup em `backup/skills-globais/analisar-video/`). Usa Whisper em `C:\tools\whisper` (`python -m venv C:\tools\whisper` + `pip install faster-whisper`).

## 7. Próximos passos

1. Atualizar `CLAUDE.md` e `_memoria/empresa.md` com a decisão do QR code
2. Fazer a demo de 30 min do SocialHub (gravar com autorização) e perguntar: qual API de QR usam, se já tiveram número banido, como treinam o bot, preços
3. Começar a construir: subir a Evolution API e fazer o bot responder um "oi" no WhatsApp do Rafael
4. Montar tabela de planos (custo, margem, preço) e material pra explicar o produto pro cliente
