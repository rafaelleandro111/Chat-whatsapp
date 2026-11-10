---
name: analisar-video
description: >
  Analisa um vídeo completo — imagem E fala. Baixa do YouTube, TikTok, Instagram
  (ou usa arquivo local), pega a legenda do site ou transcreve o áudio com Whisper
  local quando a legenda falha, extrai grades de frames e entrega uma análise:
  resumo, passo a passo, recursos mostrados, o que é promessa vs o que aparece de
  verdade, e o que isso significa pro negócio do usuário. Use quando o usuário
  mandar um link de vídeo ou arquivo .mp4/.webm e pedir "analisa esse vídeo",
  "vê esse vídeo", "o que ele ensina", "transcreve", ou /analisar-video.
---

# /analisar-video — Análise completa de vídeo

Analisar só os frames não basta: o que importa costuma estar na fala. Sempre
juntar **transcrição + imagens** antes de concluir qualquer coisa.

## Dependências

- `yt-dlp`, `ffmpeg`, `ffprobe` no PATH
- Ambiente do Whisper em `C:\tools\whisper` (Windows) — ver "Instalar o Whisper" abaixo
- Contexto do negócio, se existir: `_memoria/empresa.md` e `_memoria/estrategia.md` da pasta atual

---

## Workflow

### Passo 1 — Preparar

Pasta de trabalho: o scratchpad da sessão (se houver) + `/video-<id-curto>`;
senão uma pasta temporária. Nunca dentro do projeto do usuário.

Rodar o script com o Python do ambiente do Whisper (é ele que tem `faster-whisper`):

```bash
/c/tools/whisper/Scripts/python -I ~/.claude/skills/analisar-video/scripts/preparar_video.py "<url-ou-arquivo>" "<pasta>"
```

- Vídeo de até ~15 min: rodar em foreground com timeout de 10 min.
- Vídeo maior: rodar em background e avisar o usuário que está transcrevendo.
  Acima de 40 min, usar `--modelo base` (mais rápido, um pouco menos preciso).
- O script tenta primeiro a legenda do site; se vier vazia ou der erro (YouTube
  costuma dar `429 Too Many Requests`), cai no Whisper sozinho.
- `--forcar-whisper` quando a legenda automática do site vier ruim.

Saídas: `info.txt`, `transcricao.txt` (`[mm:ss] texto`), `frames/g_XX.jpg`.

### Passo 2 — Ler tudo

1. `info.txt` (título, canal, data, descrição — links da descrição dizem muito)
2. `transcricao.txt` inteira
3. Todas as grades em `frames/` (cada grade = 12 frames em ordem, esquerda→direita, cima→baixo)

Cruzar: o que é falado em cada minuto com o que aparece na tela.

### Passo 3 — Entregar a análise

Formato (em markdown, direto, no tom de `_memoria/preferencias.md` se existir):

1. **Cabeçalho:** título, canal, duração, data
2. **Em uma frase:** o que o vídeo realmente é
3. **Promessa vs realidade:** se o título/thumbnail promete algo que o vídeo não
   entrega (ex: "agente de IA" que é só menu de botões; "grátis" que capta lead),
   dizer claramente no começo
4. **Passo a passo** do que é ensinado ou mostrado
5. **Recursos/ferramentas** mostrados — tabela quando forem vários
6. **Riscos ou pegadinhas** (ferramenta não oficial, custo escondido, prazo)
7. **Pro teu negócio:** o que aproveitar, o que ignorar, o que vira diferencial —
   baseado em `_memoria/` quando existir

Citar minutos (`[05:30]`) quando um ponto depender de algo específico da fala.
Não inventar o que não está na transcrição nem nos frames.

---

## Instalar o Whisper (uma vez só)

Se `C:\tools\whisper\Scripts\python.exe` não existir:

```bash
python -m venv /c/tools/whisper
/c/tools/whisper/Scripts/python -m pip install -q faster-whisper
```

O primeiro uso baixa o modelo `small` (~460 MB) do Hugging Face.

## Pegadinhas conhecidas

- **Caminho longo no Windows:** instalar o venv em pasta temporária profunda
  falha (`OSError ... Long Path`) por causa do `onnxruntime`. Por isso o venv fica
  em `C:\tools\whisper`.
- **PyAV x faster-whisper:** `transcribe("arquivo")` quebra com
  `open() got an unexpected keyword argument 'metadata_errors'`. O script já
  contorna convertendo pra WAV e passando o áudio como array.
- **Legenda 429:** o YouTube limita pedidos de legenda; não ficar tentando —
  o Whisper resolve.
- **Instagram/TikTok privados** ou com login: o yt-dlp falha; pedir pro usuário
  baixar o vídeo e passar o arquivo local.
