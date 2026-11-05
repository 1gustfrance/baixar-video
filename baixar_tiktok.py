"""
Downloader de vídeos do TikTok e Instagram.
Baixa sem marca d'água, remove metadados embutidos e nunca sobrescreve arquivos.

Uso:
    python baixar_tiktok.py <URL>

Exemplos:
    python baixar_tiktok.py https://www.tiktok.com/@usuario/video/123456
    python baixar_tiktok.py https://www.instagram.com/reel/ABC123/
    python baixar_tiktok.py https://www.instagram.com/p/ABC123/
"""

import subprocess
import json
import sys
import os
import re
import tempfile
from datetime import datetime


# ──────────────────────────────────────────────────────────────
# Detecção de plataforma
# ──────────────────────────────────────────────────────────────

def detectar_plataforma(url: str) -> str:
    """Detecta a plataforma a partir da URL."""
    url_lower = url.lower()
    if "tiktok.com" in url_lower:
        return "tiktok"
    elif "instagram.com" in url_lower:
        return "instagram"
    else:
        return "desconhecida"


def limpar_url(url: str) -> str:
    """Remove query strings desnecessárias da URL."""
    return url.split("?")[0] if "?" in url else url


# ──────────────────────────────────────────────────────────────
# Nome único para o arquivo (nunca sobrescreve)
# ──────────────────────────────────────────────────────────────

def gerar_nome_unico(output_dir: str, plataforma: str, video_id: str, ext: str = "mp4") -> str:
    """
    Gera um nome de arquivo único baseado na plataforma e ID do vídeo.
    Se já existir, adiciona um sufixo numérico (_2, _3, ...).
    """
    base = f"{plataforma}_{video_id}"
    nome = f"{base}.{ext}"
    caminho = os.path.join(output_dir, nome)

    contador = 2
    while os.path.exists(caminho):
        nome = f"{base}_{contador}.{ext}"
        caminho = os.path.join(output_dir, nome)
        contador += 1

    return caminho


def extrair_video_id(url: str, plataforma: str) -> str:
    """Tenta extrair o ID do vídeo da URL."""
    if plataforma == "tiktok":
        match = re.search(r"/video/(\d+)", url)
        if match:
            return match.group(1)
    elif plataforma == "instagram":
        match = re.search(r"/(reel|p|tv)/([A-Za-z0-9_-]+)", url)
        if match:
            return match.group(2)
    # Fallback: timestamp
    return datetime.now().strftime("%Y%m%d_%H%M%S")


# ──────────────────────────────────────────────────────────────
# Metadados (apenas exibe no terminal, não salva arquivo)
# ──────────────────────────────────────────────────────────────

def extrair_metadados(url: str, cookies_args: list) -> dict | None:
    """Extrai metadados do vídeo usando yt-dlp --dump-json."""
    print("📋 Extraindo informações do vídeo...")
    cmd = ["yt-dlp", "--dump-json", "--no-warnings"] + cookies_args + [url]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"⚠️  Não foi possível extrair metadados: {result.stderr.strip()[:200]}")
        return None
    return json.loads(result.stdout)


def exibir_metadados(metadata: dict, plataforma: str):
    """Exibe um resumo dos metadados no terminal."""
    print("\n" + "=" * 60)
    print(f"📊 INFORMAÇÕES DO VÍDEO ({plataforma.upper()})")
    print("=" * 60)

    titulo = metadata.get("title") or metadata.get("description", "N/A")
    if len(titulo) > 80:
        titulo = titulo[:77] + "..."

    print(f"  🎬 Título:       {titulo}")
    print(f"  👤 Autor:        {metadata.get('uploader', metadata.get('creator', 'N/A'))}")
    print(f"  📅 Data:         {metadata.get('upload_date', 'N/A')}")
    print(f"  ⏱️  Duração:      {metadata.get('duration', 0)}s")

    views = metadata.get("view_count")
    likes = metadata.get("like_count")
    comments = metadata.get("comment_count")
    print(f"  👁️  Visualizações: {views:,}" if isinstance(views, int) else "  👁️  Visualizações: N/A")
    print(f"  ❤️  Curtidas:     {likes:,}" if isinstance(likes, int) else "  ❤️  Curtidas:     N/A")
    print(f"  💬 Comentários:  {comments:,}" if isinstance(comments, int) else "  💬 Comentários:  N/A")
    print(f"  📐 Resolução:    {metadata.get('width', '?')}x{metadata.get('height', '?')}")

    musica = metadata.get("track") or metadata.get("artist")
    if musica:
        print(f"  🎵 Música:       {musica}")

    tags = metadata.get("tags", [])
    if tags:
        print(f"  🏷️  Hashtags:     {', '.join('#' + t for t in tags[:10])}")

    print("=" * 60)


# ──────────────────────────────────────────────────────────────
# Download
# ──────────────────────────────────────────────────────────────

def baixar_video(url: str, output_dir: str, cookies_args: list) -> str | None:
    """
    Baixa o vídeo usando yt-dlp para um arquivo temporário.
    Retorna o caminho do arquivo baixado ou None em caso de falha.
    """
    print("⬇️  Baixando vídeo...")

    # Usa um nome temporário para o download (yt-dlp renomeia depois)
    temp_template = os.path.join(output_dir, "_temp_download.%(ext)s")

    cmd = [
        "yt-dlp",
        "--format", "best",
        "--output", temp_template,
        "--no-warnings",
        "--progress",
        "--force-overwrites",
    ] + cookies_args + [url]

    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")

    if result.returncode != 0:
        print(f"❌ Erro ao baixar: {result.stderr.strip()[:300]}")
        return None

    print(result.stdout)

    # Encontrar o arquivo temporário baixado
    for f in os.listdir(output_dir):
        if f.startswith("_temp_download."):
            return os.path.join(output_dir, f)

    return None


# ──────────────────────────────────────────────────────────────
# Limpeza de metadados com ffmpeg
# ──────────────────────────────────────────────────────────────

def limpar_metadados(input_path: str, output_path: str) -> bool:
    """Remove todos os metadados embutidos do vídeo usando ffmpeg."""
    print("🧹 Removendo metadados embutidos do vídeo...")

    result = subprocess.run(
        [
            "ffmpeg", "-i", input_path,
            "-map_metadata", "-1",
            "-map", "0",
            "-c", "copy",
            "-fflags", "+bitexact",
            "-movflags", "+faststart",
            output_path, "-y"
        ],
        capture_output=True, text=True, encoding="utf-8"
    )

    if result.returncode == 0:
        return True
    else:
        print(f"⚠️  Falha ao limpar metadados: {result.stderr.strip()[:200]}")
        return False


# ──────────────────────────────────────────────────────────────
# Instagram: autenticação com cookies (opcional)
# ──────────────────────────────────────────────────────────────

def obter_cookies_args(plataforma: str) -> list:
    """
    Retorna argumentos de cookies para yt-dlp se necessário.
    Para Instagram, tenta múltiplas estratégias de autenticação.
    """
    if plataforma != "instagram":
        return []

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Verificar se existe um arquivo cookies.txt na mesma pasta (mais confiável)
    cookies_file = os.path.join(script_dir, "cookies.txt")
    if os.path.exists(cookies_file):
        print("  🍪 Usando arquivo cookies.txt")
        return ["--cookies", cookies_file]

    print("  🔍 Procurando cookies de navegador para Instagram...")

    # 2. Tentar cada navegador com variações de perfil
    tentativas = [
        # (navegador, argumento completo)
        ("Edge",    "edge"),
        ("Chrome",  "chrome"),
        ("Firefox", "firefox"),
    ]

    for nome, browser in tentativas:
        try:
            test = subprocess.run(
                ["yt-dlp", "--cookies-from-browser", browser,
                 "--dump-json", "--no-warnings",
                 "https://www.instagram.com/instagram/"],
                capture_output=True, text=True, encoding="utf-8",
                timeout=20
            )
            if test.returncode == 0:
                print(f"  🍪 Usando cookies do {nome}")
                return ["--cookies-from-browser", browser]
            else:
                erro = test.stderr.strip().split("\n")[0] if test.stderr else "erro desconhecido"
                if "DPAPI" in erro or "cookie database" in erro:
                    print(f"  ⚠️  {nome}: navegador bloqueando acesso aos cookies")
                else:
                    print(f"  ⚠️  {nome}: {erro[:80]}")
        except subprocess.TimeoutExpired:
            print(f"  ⚠️  {nome}: timeout")
        except Exception as e:
            print(f"  ⚠️  {nome}: {e}")

    # 3. Nenhum método funcionou — instruções para o usuário
    print()
    print("  ❌ Não foi possível acessar cookies de nenhum navegador.")
    print("  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  💡 SOLUÇÃO: Exporte seus cookies para um arquivo:")
    print()
    print("     1. Instale a extensão 'Get cookies.txt LOCALLY'")
    print("        no Chrome/Edge (pesquise na Chrome Web Store)")
    print("     2. Acesse instagram.com e faça login")
    print("     3. Clique na extensão → 'Export' → salve como:")
    print(f"        {cookies_file}")
    print("     4. Execute este script novamente")
    print("  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    return []


# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("❌ Uso: python baixar_tiktok.py <URL>")
        print()
        print("Plataformas suportadas:")
        print("  • TikTok:    https://www.tiktok.com/@usuario/video/123456")
        print("  • Instagram: https://www.instagram.com/reel/ABC123/")
        print("  • Instagram: https://www.instagram.com/p/ABC123/")
        sys.exit(1)

    url = limpar_url(sys.argv[1])
    plataforma = detectar_plataforma(url)
    output_dir = os.path.dirname(os.path.abspath(__file__))

    if plataforma == "desconhecida":
        print(f"❌ Plataforma não reconhecida na URL: {url}")
        print("   Suportadas: TikTok, Instagram")
        sys.exit(1)

    video_id = extrair_video_id(url, plataforma)

    print(f"🔗 URL: {url}")
    print(f"🌐 Plataforma: {plataforma.capitalize()}")
    print(f"🆔 ID do vídeo: {video_id}")
    print(f"📁 Pasta: {output_dir}\n")

    # Cookies (necessário para Instagram em muitos casos)
    cookies_args = obter_cookies_args(plataforma)

    # 1. Extrair e exibir metadados (apenas no terminal)
    metadata = extrair_metadados(url, cookies_args)
    if metadata:
        exibir_metadados(metadata, plataforma)
        ext = metadata.get("ext", "mp4")
    else:
        ext = "mp4"
        print("⚠️  Tentando baixar mesmo sem metadados...\n")

    # 2. Baixar vídeo
    print()
    temp_path = baixar_video(url, output_dir, cookies_args)

    # Se falhou com cookies, tenta sem cookies (posts públicos)
    if not temp_path and cookies_args:
        print("\n🔄 Tentando sem cookies (conteúdo público)...")
        metadata = extrair_metadados(url, [])
        if metadata:
            exibir_metadados(metadata, plataforma)
        temp_path = baixar_video(url, output_dir, [])

    if not temp_path:
        print("\n❌ Falha no download.")
        sys.exit(1)

    # Detectar extensão real do arquivo baixado
    _, real_ext = os.path.splitext(temp_path)
    real_ext = real_ext.lstrip(".")

    # 3. Gerar nome único e limpar metadados
    final_path = gerar_nome_unico(output_dir, plataforma, video_id, real_ext)

    if limpar_metadados(temp_path, final_path):
        os.remove(temp_path)
        final_name = os.path.basename(final_path)
        size_mb = os.path.getsize(final_path) / (1024 * 1024)
        print(f"\n✅ Download concluído com sucesso!")
        print(f"  📹 {final_name} ({size_mb:.1f} MB)")
        print(f"  🧹 Metadados removidos")
    else:
        # Se falhar a limpeza, renomeia o temporário mesmo assim
        os.rename(temp_path, final_path)
        final_name = os.path.basename(final_path)
        size_mb = os.path.getsize(final_path) / (1024 * 1024)
        print(f"\n✅ Download concluído (sem limpeza de metadados)")
        print(f"  📹 {final_name} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
