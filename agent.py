import os
import subprocess
import time
from google import genai
from google.genai import types
from google.genai.errors import APIError

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# --- REAL DIAGNOSTIC TOOLS THE AI AGENT CAN CALL ---

def get_failed_service_log() -> str:
    """Fetches the latest failing system service log."""
    return """
    Nov 12 07:45:12 ip-10-0-1-45 systemd: Starting nginx.service - A high performance web server...
    Nov 12 07:45:12 ip-10-0-1-45 nginx: nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)
    Nov 12 07:45:12 ip-10-0-1-45 systemd: Failed to start nginx.service.
    """

def check_live_listening_ports() -> str:
    """Runs a real Linux command on the host to inspect active listening network ports."""
    print("🛠️ [TOOL EXECUTED] Agent is running 'ss -tuln' on the server...")
    result = subprocess.run(["ss", "-tuln"], capture_output=True, text=True)
    return result.stdout[:1000]

def check_disk_usage() -> str:
    """Runs a real Linux command to verify disk space health."""
    print("🛠️ [TOOL EXECUTED] Agent is running 'df -h' on the server...")
    result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
    return result.stdout

# --- AGENTIC EXECUTION LOOP WITH FALLBACK ---

def run_autonomous_agent():
    prompt = """
    You are an autonomous SRE AI Agent investigating a production server alert.
    1. First, call `get_failed_service_log` to see what failed.
    2. Based on the error you find, call the relevant live diagnostic tools (`check_live_listening_ports` or `check_disk_usage`) to inspect the current host environment.
    3. Finally, write a concise Incident Triage Report with Root Cause, Live Host Findings, and Exact Remediation Commands.
    """

    tools = [get_failed_service_log, check_live_listening_ports, check_disk_usage]
    models_to_try = ["gemini-3.5-flash-lite", "gemini-3.8-flash"]

    for model_name in models_to_try:
        for attempt in range(1, 3):
            try:
                print(f"🤖 Starting Autonomous Agent with {model_name} (Attempt {attempt})...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=tools,
                        temperature=0.2,
                    ),
                )
                print("\n" + "="*55)
                print("📋 AUTONOMOUS SRE AGENT TRIAGE REPORT")
                print("="*55)
                print(response.text)
                return
            except APIError as e:
                print(f"⚠️ Temporary API issue on {model_name}: {e.message}")
                time.sleep(5)

    raise RuntimeError("All fallback models temporarily unavailable.")

if __name__ == "__main__":
    run_autonomous_agent()
