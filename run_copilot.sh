#!/bin/bash
# 运行 Market Color 早报 (Copilot 版)
cd "$(dirname "$0")"
.venv/bin/python daily_brief_copilot.py
