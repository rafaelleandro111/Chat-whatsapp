"""Prepara um vídeo pra análise: metadados, transcrição e grades de frames.

Uso: python preparar_video.py <url-ou-arquivo> <pasta-de-saida> [--modelo small] [--forcar-whisper]

Saída em <pasta-de-saida>:
  info.txt          título, canal, duração, data
  transcricao.txt   "[mm:ss] texto" por linha (legenda do site ou Whisper)
  frames/g_XX.jpg   grades 4x3 de frames espalhados pelo vídeo
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path

GRADES_ALVO = 4          # quantas grades 4x3 gerar (48 frames no total)
FRAMES_POR_GRADE = 12


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def metadados(fonte, saida):
    if Path(fonte).exists():
        r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", fonte])
        dur = float(json.loads(r.stdout)["format"]["duration"])
        info = {"title": Path(fonte).name, "channel": "-", "upload_date": "-", "duration": dur}
    else:
        r = run(["yt-dlp", "--no-warnings", "-J", "--no-playlist", fonte])
        if r.returncode != 0:
            sys.exit(f"yt-dlp falhou ao ler o vídeo:\n{r.stderr[-800:]}")
        d = json.loads(r.stdout)
        info = {k: d.get(k) for k in ("title", "channel", "upload_date", "duration", "description")}
    (saida / "info.txt").write_text(
        "\n".join(f"{k}: {v}" for k, v in info.items() if v), encoding="utf-8")
    return info


def baixar(fonte, saida):
    if Path(fonte).exists():
        return Path(fonte)
    r = run(["yt-dlp", "-q", "--no-warnings", "--no-playlist",
             "-f", "bv*[height<=480]+ba/b[height<=480]/b",
             "-o", str(saida / "video.%(ext)s"), fonte])
    videos = [p for p in saida.glob("video.*") if p.suffix not in (".vtt", ".part")]
    if not videos:
        sys.exit(f"Não consegui baixar o vídeo:\n{r.stderr[-800:]}")
    return videos[0]


def legenda_do_site(fonte, saida):
    """Tenta a legenda (manual ou automática) do site. Retorna linhas ou None."""
    if Path(fonte).exists():
        return None
    run(["yt-dlp", "-q", "--no-warnings", "--skip-download", "--no-playlist",
         "--write-subs", "--write-auto-subs", "--sub-langs", "pt.*,pt-BR,pt,en",
         "--sub-format", "vtt", "-o", str(saida / "legenda"), fonte])
    vtts = sorted(saida.glob("legenda*.vtt"), key=lambda p: ("pt" not in p.name, p.name))
    if not vtts:
        return None
    linhas, ultimo = [], None
    tempo = None
    for linha in vtts[0].read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"(\d+):(\d+):(\d+)\.\d+ -->", linha)
        if m:
            h, mi, s = map(int, m.groups())
            tempo = f"{h * 60 + mi:02d}:{s:02d}"
            continue
        texto = re.sub(r"<[^>]+>", "", linha).strip()
        if not texto or texto == ultimo or tempo is None or texto.startswith(("WEBVTT", "Kind:", "Language:")):
            continue
        linhas.append(f"[{tempo}] {texto}")
        ultimo = texto
    return linhas or None


def transcrever_whisper(video, saida, modelo):
    from faster_whisper import WhisperModel
    import numpy as np

    wav = saida / "audio.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(wav)])
    # Lê o WAV direto: o PyAV recente quebra o loader do faster-whisper (metadata_errors).
    with wave.open(str(wav), "rb") as w:
        audio = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    m = WhisperModel(modelo, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(audio, language="pt", vad_filter=True)
    linhas = [f"[{int(s.start) // 60:02d}:{int(s.start) % 60:02d}] {s.text.strip()}" for s in segs]
    wav.unlink(missing_ok=True)
    return linhas


def frames(video, saida, duracao):
    pasta = saida / "frames"
    pasta.mkdir(exist_ok=True)
    intervalo = max(1.0, duracao / (GRADES_ALVO * FRAMES_POR_GRADE))
    run(["ffmpeg", "-v", "error", "-y", "-i", str(video),
         "-vf", f"fps=1/{intervalo:.2f},scale=480:-1,tile=4x3", str(pasta / "g_%02d.jpg")])
    return sorted(pasta.glob("g_*.jpg")), intervalo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fonte")
    ap.add_argument("saida")
    ap.add_argument("--modelo", default="small")
    ap.add_argument("--forcar-whisper", action="store_true")
    a = ap.parse_args()

    for exe in ("ffmpeg", "ffprobe", "yt-dlp"):
        if not shutil.which(exe):
            sys.exit(f"Falta '{exe}' no PATH.")

    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    info = metadados(a.fonte, saida)
    video = baixar(a.fonte, saida)
    duracao = float(info.get("duration") or 0) or float(json.loads(run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(video)]
    ).stdout)["format"]["duration"])

    linhas = None if a.forcar_whisper else legenda_do_site(a.fonte, saida)
    origem = "legenda do site"
    if not linhas:
        origem = f"whisper ({a.modelo})"
        linhas = transcrever_whisper(video, saida, a.modelo)
    (saida / "transcricao.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")

    grades, intervalo = frames(video, saida, duracao)

    print(f"titulo: {info.get('title')}")
    print(f"duracao: {int(duracao) // 60}m{int(duracao) % 60:02d}s")
    print(f"transcricao: {len(linhas)} linhas via {origem} -> {saida / 'transcricao.txt'}")
    print(f"frames: {len(grades)} grades 4x3, 1 frame a cada {intervalo:.0f}s -> {saida / 'frames'}")


if __name__ == "__main__":
    main()
