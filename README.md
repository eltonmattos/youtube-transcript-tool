# YouTube Transcript Tool with AI (Gemini) or Offline

![image](https://github.com/user-attachments/assets/758722c6-e3bc-49e8-b81b-8a50a735f53c)

## 📄 Descrição
Ferramenta para baixar transcrições de vídeos ou playlists do YouTube e processá-las com inteligência artificial (Google Gemini) — com recursos de formatação, capítulos, tradução, resumo e remoção de anúncios — ou operar em modo offline, baixando apenas a transcrição bruta.

## 🚀 Instalação
```bash
pip install -r requirements.txt
```

## ⚙️ Uso

### Modo offline (sem IA):
```bash
python yt_transcript_tool.py --file urls.txt
```

### Com IA (Gemini):
```bash
python yt_transcript_tool.py --api-key SUA_API_KEY --file urls.txt --generate-toc --summarize --skip-ads
```

## Parâmetros disponíveis

| Parâmetro         | Tipo     | Descrição                                                                                              | Obrigatório | Default                    |
|-------------------|----------|--------------------------------------------------------------------------------------------------------|-------------|----------------------------|
| --api-key         | string   | Chave da API do Google Gemini (ativa recursos IA).                                                     | ❌           | —                          |
| --file            | string   | Arquivo `.txt` com URLs de vídeos.                                                                     | ⚠️           | —                          |
| --playlist        | string   | URL de uma playlist do YouTube.                                                                        | ⚠️           | —                          |
| --output          | string   | Pasta de saída.                                                                                        | ❌           | output_transcripts         |
| --model           | string   | Modelo Gemini.                                                                                         | ❌           | gemini-1.5-flash           |
| --lang            | string   | Idioma da transcrição (origem).                                                                        | ❌           | pt                         |
| --target-lang     | string   | Idioma destino (tradução).                                                                             | ❌           | pt                         |
| --generate-toc    | flag     | Gera título e capítulos.                                                                               | ❌           | desativado                 |
| --summarize       | flag     | Gera resumo.                                                                                           | ❌           | desativado                 |
| --skip-ads        | flag     | Remove blocos de anúncio identificados no transcript.                                                  | ❌           | desativado                 |

## Estrutura de saída

Modo offline:
```
saida/
├── raw/
├── logs.txt
```

Modo com IA:
```
saida/
├── raw/
├── markdown/
├── logs.txt
```

## 🔥 Exemplo completo
```bash
python yt_transcript_tool.py --api-key SUA_API_KEY --file urls.txt --lang pt --target-lang en --generate-toc --summarize --skip-ads
```

## ✅ Licença
Livre para uso, modificação e distribuição.
