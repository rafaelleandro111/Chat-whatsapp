# Empresa

> Memória central do negócio. O Claude lê esse arquivo antes de cada resposta.
> Você pode editar a qualquer momento.

**Nome:** Trainer Chat
**Negócio:** Rafael — freelancer, toca sozinho
**O que faz:** Monto um atendente de IA no WhatsApp que responde e agenda clientes 24h pro teu negócio.
**Perfil:** Freelancer (vende o agente pronto e configurado pra cada cliente)
**Atende clientes:** Pequenos negócios locais — academia, salão, loja, restaurante e afins
**Equipe:** Só o Rafael
**Ferramentas:** A definir (produto ainda em construção)
**Principais entregas:** Agente de IA no WhatsApp personalizado por cliente (ficha do negócio + agendamento + memória da conversa)

## Contexto adicional

- Produto em fase inicial: o Rafael ainda está aprendendo a construir o sistema.
- Referência de arquitetura: vídeo em `Desktop/aqui/` — WhatsApp → IA → Memória → Base do negócio → Ferramentas (agenda) → VPS no ar.
- Decisões tomadas: usar a API oficial da Meta (Cloud API), sem conector não oficial, pra não arriscar banimento do número do cliente; motor de IA trocável (OpenAI, Gemini, Claude ou via OpenRouter), sem depender de um fornecedor só.
- Regra da Meta (desde 15/01/2026): proibido assistente de IA "de uso geral" no WhatsApp Business. O agente tem que ficar focado no negócio do cliente.
- Modelo de cobrança de referência no mercado: taxa de implantação + mensalidade (mercado cobra de R$ 99 a R$ 1.500/mês conforme o nível).
