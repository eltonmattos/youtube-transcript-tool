#!/bin/bash
python3 yt_transcript_tool.py \
 --file urls.txt \
 --output saida \
 --lang pt \
 --target-lang en \
 --generate-toc \
 --summarize \
 --skip-ads
