name: AIOps Incident Triage Workflow

on:
  workflow_dispatch:
  push:
    branches: [ "main" ]

jobs:
  run-ai-agent:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository Code
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install AI SDK Dependencies
        run: pip install google-genai

      - name: Run AIOps Log Triage Agent
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python agent.py
