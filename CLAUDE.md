# MazyOS — Sistema operacional do negócio

Sua empresa roda em cima desse arquivo. Aqui ficam as regras de operação
do MazyOS — como o Claude lê o contexto, aprende com correções, mantém
tudo atualizado e cria skills novas conforme a operação evolui.

Esse arquivo é editável. Quando o `/instalar` rodar, ele complementa o
final dessa página com as regras específicas do seu negócio.

---

## Contexto do negócio

No início de toda conversa, ler os seguintes arquivos (quando existirem
e estiverem preenchidos):

1. `_memoria/empresa.md` — quem é o usuário, o que faz, como funciona o negócio
2. `_memoria/preferencias.md` — tom de voz, estilo de escrita, o que evitar
3. `_memoria/estrategia.md` — foco atual, prioridades, prazos

Usar essas informações como base pra qualquer resposta ou decisão. Ao
sugerir prioridades, formatos ou abordagens, considerar o foco atual
descrito em `estrategia.md`.

Pra qualquer tarefa visual (carrossel, post, landing page), consultar
`identidade/design-guide.md` como referência de estilo.

Não é necessário listar o que foi lido nem confirmar a leitura. Apenas
usar o contexto naturalmente.

---

## Fluxo de trabalho

Antes de executar qualquer tarefa, verificar se existe skill relevante
em `.claude/skills/`. Se encontrar, seguir as instruções da skill. Se
não encontrar, executar a tarefa normalmente.

Ao concluir uma tarefa que não tinha skill mas parece repetível (o
usuário provavelmente vai pedir de novo no futuro), perguntar:

> "Isso pode virar uma skill pra próxima vez. Quer que eu crie?"

Não perguntar pra tarefas pontuais ou perguntas simples. Só quando o
padrão de repetição for claro.

---

## Aprender com correções

Quando o usuário corrigir algo, melhorar uma resposta ou dar uma
instrução que parece permanente (frases como "na verdade é assim", "não
faça mais isso", "prefiro assim", "sempre que...", "evita...", "da
próxima vez..."), perguntar:

> "Quer que eu salve isso pra não precisar repetir?"

Se sim, identificar onde faz mais sentido salvar:

- **Sobre o negócio** (clientes, serviços, mercado) → `_memoria/empresa.md`
- **Sobre preferências e estilo** (tom de voz, formato, o que evitar) → `_memoria/preferencias.md`
- **Sobre prioridades e foco** (projetos, metas, prazos) → `_memoria/estrategia.md`
- **Regra de comportamento nessa pasta** → próprio `CLAUDE.md`

Salvar com uma linha nova clara, sem reformatar o arquivo inteiro.
Confirmar mostrando a linha adicionada.

Não perguntar se a correção for óbvia de contexto imediato (ex: "na
verdade o arquivo se chama X"). Só perguntar quando a informação tiver
valor duradouro.

---

## Manter contexto atualizado

Ao terminar uma tarefa que mudou algo relevante (cliente novo, skill
nova, mudança de foco, processo novo, ferramenta instalada, estrutura
alterada), perguntar:

> "Isso mudou algo no teu contexto. Quer que eu atualize a memória?"

Se sim, identificar o que atualizar:

- **Cliente, serviço, ferramenta, equipe** → `_memoria/empresa.md`
- **Mudança de prioridade ou foco** → `_memoria/estrategia.md`
- **Tom ou estilo** → `_memoria/preferencias.md`
- **Pasta, regra de organização, skill criada** → `CLAUDE.md`
- **Visual (cores, fontes, logo)** → `identidade/design-guide.md`

Mostrar o que vai mudar antes de salvar. Não reformatar o arquivo
inteiro, só adicionar ou editar a linha relevante.

**Quando NÃO perguntar:**
- Tarefas pontuais sem impacto no contexto (escrever um email avulso, criar um post)
- Perguntas simples ou conversas sem ação
- Mudanças já salvas pelo bloco "Aprender com correções"

**Dica:** rode `/atualizar` pra uma varredura completa quando houver dúvida.

---

## Criação de skills

Quando o usuário pedir skill nova:

1. Verificar se existe template relevante em `templates/skills/`. Se
   existir, usar como base e adaptar pro contexto
2. Perguntar se é específica desse projeto ou útil em qualquer:
   - Específica → `.claude/skills/nome-da-skill/SKILL.md` (local)
   - Universal → `~/.claude/skills/nome-da-skill/SKILL.md` (global)
3. Ler `_memoria/empresa.md` e `_memoria/preferencias.md` pra calibrar
   o conteúdo da skill ao contexto do negócio
4. Se a skill precisar de arquivos de apoio (templates, exemplos),
   criar dentro da pasta da skill
5. Seguir o fluxo da skill-creator nativa do Claude Code

---

# Trainer Chat — MazyOS (perfil Freelancer)

## O que é esse workspace

Operação do Trainer Chat: construção do produto (agente de IA no WhatsApp) e atendimento dos clientes que compram ele.

**Estrutura de pastas:**
- `_memoria/` — quem sou, como falo, foco atual
- `identidade/` — marca Trainer Chat (logo, cores, fontes)
- `clientes/` — uma subpasta por cliente, com a ficha do negócio dele
- `propostas/` — propostas em rascunho ou enviadas
- `marketing/` — conteúdo do Trainer Chat (Insta, demos)
- `saidas/` — emails, documentos pontuais
- `dados/` — arquivos a analisar
- `tarefas.md` — pipeline, prazos, próximos passos

## Quem sou

Sou Rafael, freelancer, toco sozinho. Trabalho com pequenos negócios locais (academia, salão, loja, restaurante) entregando um atendente de IA no WhatsApp que responde e agenda clientes 24h.

## Meu serviço

- Implantação do agente no WhatsApp do cliente (API oficial da Meta)
- Montagem da ficha do negócio (serviços, preços, horários, perguntas frequentes, regras)
- Integração com agenda e manutenção mensal

Ticket médio: a definir. Modelo: implantação + mensalidade.

## Clientes ativos

Nenhum ainda.

## Como trabalho

Produto em construção. Arquitetura: WhatsApp (Cloud API oficial) → servidor → IA trocável → memória da conversa → ficha do negócio → ferramentas (agenda) → VPS 24h.

## Tom de voz

Direto, informal, simples. Explicar com comparação do dia a dia, sem jargão. Evitar: muitos emojis.

## Regras do sistema

- Cliente novo → criar pasta `clientes/<Nome>/` com `briefing.md` e `ficha-do-negocio.md`
- Proposta enviada → `clientes/<Nome>/proposta.html` (ou `propostas/` se ainda não fechou)
- Nunca usar conector não oficial de WhatsApp (Baileys/QR code) em cliente: risco de banimento
- O agente sempre fica focado no negócio do cliente (regra da Meta contra IA de uso geral)

## Ferramentas conectadas

- [ ] WhatsApp Cloud API (Meta for Developers)
- [ ] Provedor de IA (OpenAI / Gemini / Claude / OpenRouter)
- [ ] Agenda (Cal.com ou Google Calendar)
- [ ] VPS

*(Marcar conforme for instalando)*

## Ferramentas instaladas no projeto

- **Superpowers** — plugin do Claude Code (escopo do projeto): planejamento, TDD, debug sistemático
- **REA** — MCP de engenharia reversa (global, `rea-agents` via npm); usar só pra analisar programas/apps já prontos
- **Pipecat** — framework Python pra agente de voz, instalado em `.venv/` (ativar com `.venv\Scripts\activate`); reservado pra uma possível versão por telefone do Trainer Chat
