@echo off
cd /d %~dp0

python yt_transcript_tool.py^
 --file "urls.txt"^
 --output "output"^
