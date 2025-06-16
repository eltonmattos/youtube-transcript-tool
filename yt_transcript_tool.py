
#!/usr/bin/env python3
import os
import re
import argparse
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        raise ValueError("Invalid URL")

def get_title_from_url(url):
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        title_tag = soup.find("title")
        if title_tag:
            return sanitize_filename(title_tag.text.replace(" - YouTube", "").strip())
        else:
            return "video"
    except Exception as e:
        print(f"[!] Error getting title from URL: {e}")
        return "video"

def get_video_urls_from_playlist(playlist_url):
    try:
        resp = requests.get(playlist_url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        video_links = soup.find_all("a")
        video_urls = set()
        for link in video_links:
            href = link.get("href")
            if href and "/watch?v=" in href:
                url = f"https://www.youtube.com{href.split('&')[0]}"
                video_urls.add(url)
        return list(video_urls)
    except Exception as e:
        print(f"[!] Error getting videos from playlist: {e}")
        return []

def download_transcript(url, lang="pt"):
    video_id = get_video_id(url)
    title = get_title_from_url(url)
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_transcript([lang])
    text_chunks = transcript.fetch()
    text = "\n".join([chunk.text for chunk in text_chunks])
    print(f"[✔] Transcript downloaded: {title}")
    return text, title

def main():
    parser = argparse.ArgumentParser(description="Download YouTube transcripts with optional AI formatting.")
    parser.add_argument("--api-key", help="Google Gemini API key.")
    parser.add_argument("--model", default="gemini-1.5-flash", help="Gemini model (default: gemini-1.5-flash).")
    parser.add_argument("--lang", default="pt", help="Transcript language (default: pt).")
    parser.add_argument("--target-lang", default="pt", help="Target language for translation (default: pt).")
    parser.add_argument("--output", default="output_transcripts", help="Output directory (default: output_transcripts).")
    parser.add_argument("--file", help="File with video URLs (one per line).")
    parser.add_argument("--playlist", help="YouTube playlist URL.")
    parser.add_argument("--generate-toc", action="store_true")
    parser.add_argument("--summarize", action="store_true")
    parser.add_argument("--skip-ads", action="store_true")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    raw_folder = os.path.join(args.output, "raw")
    markdown_folder = os.path.join(args.output, "markdown")
    os.makedirs(raw_folder, exist_ok=True)

    use_ai = args.api_key is not None
    if use_ai:
        import google.generativeai as genai
        genai.configure(api_key=args.api_key)
        model = genai.GenerativeModel(args.model)
        os.makedirs(markdown_folder, exist_ok=True)

    urls = []
    if args.playlist:
        urls = get_video_urls_from_playlist(args.playlist)
    elif args.file:
        if os.path.exists(args.file):
            with open(args.file, "r", encoding="utf-8") as f:
                urls = [line.strip() for line in f if line.strip()]
    else:
        print("[✖] Provide --file or --playlist")
        return

    for url in urls:
        try:
            text, title = download_transcript(url, lang=args.lang)
            raw_path = os.path.join(raw_folder, f"{title}.txt")
            with open(raw_path, "w", encoding="utf-8") as f:
                f.write(text)
            if use_ai:
                prompt = f"""
You will receive a raw transcript of spoken audio in {args.lang}.
- Correct punctuation, spelling, and add natural paragraph breaks.
{"- Remove advertisement blocks like promotions, sponsorships, social media mentions, or calls to subscribe." if args.skip_ads else ""}
{"- Generate a title and structured table of contents with chapters." if args.generate_toc else ""}
{"- At the end, provide a concise summary of the content." if args.summarize else ""}
{"- Translate the content from " + args.lang + " to " + args.target_lang + "." if args.lang != args.target_lang else ""}
Do not invent or remove meaningful content unrelated to ads. Preserve the logical order and integrity of the original content.

Raw text:
{text}

Final output in Markdown:
"""
                response = model.generate_content(prompt)
                markdown = response.text.strip()
                md_path = os.path.join(markdown_folder, f"{title}.md")
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(markdown)
                print(f"[✔] Markdown generated: {md_path}")
        except Exception as e:
            print(f"[✖] Error processing {url}: {e}")

if __name__ == "__main__":
    main()
