#!/bin/bash
# 运行 Market Color 早报 (Gemini 版)
cd "$(dirname "$0")"
.venv/bin/python daily_brief_gemini.py
