<h1 align="center">
  🎬 Video Downloader — TikTok & Instagram
</h1>

<p align="center">
  <b>Baixe vídeos do TikTok e Instagram sem marca d'água e com metadados removidos.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/yt--dlp-latest-red?logo=youtube&logoColor=white" alt="yt-dlp">
  <img src="https://img.shields.io/badge/ffmpeg-required-green?logo=ffmpeg&logoColor=white" alt="ffmpeg">
  <img src="https://img.shields.io/badge/Plataforma-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey" alt="Platform">
</p>

---

## 📖 O que faz?

Este script baixa vídeos do **TikTok** e **Instagram** de forma simples via linha de comando e:

- ⬇️ **Baixa na melhor qualidade** disponível
- 🚫 **Sem marca d'água** (TikTok)
- 🧹 **Remove metadados embutidos** do arquivo — IDs de rastreamento, informações do encoder, dados internos da plataforma
- 📁 **Nunca sobrescreve** — cada vídeo recebe um nome único baseado na plataforma e ID
- 📊 **Exibe informações** do vídeo no terminal (autor, curtidas, visualizações, etc.)

## ⚠️ Sobre remoção de metadados

> **Importante:** A remoção de metadados **protege sua privacidade** ao eliminar dados de rastreamento embutidos no arquivo (IDs internos, encoder, hashes). Porém, **não garante** que plataformas não reconheçam o vídeo como cópia — elas usam **fingerprinting visual e de áudio** (análise do conteúdo em si), e não apenas metadados, para detectar duplicatas.

## 🚀 Instalação

### Pré-requisitos

1. **Python 3.10+** — [Download](https://www.python.org/downloads/)
2. **yt-dlp** — ferramenta de download de vídeos
3. **ffmpeg** — processamento de vídeo

### Instalação rápida

```bash
# Instalar yt-dlp
pip install yt-dlp

# Instalar ffmpeg
# Windows (via winget):
winget install ffmpeg

# Windows (via choco):
choco install ffmpeg

# Linux (Debian/Ubuntu):
sudo apt install ffmpeg

# macOS:
brew install ffmpeg
```

### Clonar o repositório

```bash
git clone https://github.com/1gustfrance/baixar-video.git
cd baixar-video
```

## 💻 Como usar

```bash
python baixar_tiktok.py <URL>
```

### Exemplos

```bash
# TikTok
python baixar_tiktok.py "https://www.tiktok.com/@usuario/video/7595601629286518029"

# Instagram Reel
python baixar_tiktok.py "https://www.instagram.com/reel/ABC123/"

# Instagram Post (vídeo)
python baixar_tiktok.py "https://www.instagram.com/p/ABC123/"
```

### Saída esperada

```
🔗 URL: https://www.tiktok.com/@usuario/video/7595601629286518029
🌐 Plataforma: Tiktok
🆔 ID do vídeo: 7595601629286518029
📁 Pasta: C:\Users\...\baixar-video

📋 Extraindo informações do vídeo...

============================================================
📊 INFORMAÇÕES DO VÍDEO (TIKTOK)
============================================================
  🎬 Título:       Título do vídeo...
  👤 Autor:        @usuario
  📅 Data:         20260115
  ⏱️  Duração:      11s
  👁️  Visualizações: 386,800
  ❤️  Curtidas:     55,900
  💬 Comentários:  108
  📐 Resolução:    720x1280
============================================================

⬇️  Baixando vídeo...
🧹 Removendo metadados embutidos do vídeo...

✅ Download concluído com sucesso!
  📹 tiktok_7595601629286518029.mp4 (0.6 MB)
  🧹 Metadados removidos
```

## 📋 Nomes dos arquivos

Os vídeos são salvos com nomes únicos baseados na plataforma e ID:

| Plataforma | Formato do nome | Exemplo |
|---|---|---|
| TikTok | `tiktok_<ID>.mp4` | `tiktok_7595601629286518029.mp4` |
| Instagram | `instagram_<ID>.mp4` | `instagram_DcD5Y-rs74X.mp4` |

Se o arquivo já existir, um sufixo numérico é adicionado: `tiktok_123_2.mp4`, `tiktok_123_3.mp4`, etc.

## 🔧 Funcionalidades

| Recurso | Descrição |
|---|---|
| 🌐 Multi-plataforma | TikTok e Instagram |
| 🧹 Limpeza de metadados | Remove IDs, encoder, hashes via ffmpeg |
| 📁 Sem sobrescrita | Nome único por vídeo (nunca perde arquivo) |
| 🍪 Cookies automáticos | Detecta `cookies.txt` ou tenta navegador |
| 🔄 Fallback inteligente | Se cookies falham, tenta sem autenticação |
| 📊 Info no terminal | Exibe dados do vídeo antes de baixar |

## 🛠️ Dependências

| Ferramenta | Versão mínima | Uso |
|---|---|---|
| [Python](https://www.python.org/) | 3.10+ | Execução do script |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | latest | Download dos vídeos |
| [ffmpeg](https://ffmpeg.org/) | 5.0+ | Remoção de metadados |

## 📄 Licença

Este projeto é de uso livre. Use por sua conta e risco.

---

<p align="center">
  Feito com ❤️ por <a href="https://github.com/1gustfrance">@1gustfrance</a>
</p>

