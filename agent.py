import os
from google import genai

# Initialize the AI Agent using your GitHub Secret
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def inspect_system_logs():
    """Simulates pulling failed service logs from a Linux/AWS server."""
    return """
    Nov 12 07:45:12 ip-10-0-1-45 systemd: Starting nginx.service - A high performance web server...
    Nov 12 07:45:12 ip-10-0-1-45 nginx: nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)
    Nov 12 07:45:12 ip-10-0-1-45 systemd: nginx.service: Control process exited, code=exited, status=1/FAILURE
    Nov 12 07:45:12 ip-10-0-1-45 systemd: Failed to start nginx.service.
    """

def run_triage_agent():
    print("AIOps Agent started: Collecting server logs...")
    logs = inspect_system_logs()

    prompt = f"""
    You are a Senior AWS & Linux Site Reliability Engineer (SRE).
    Analyze the following server failure log and provide:
    1. Root Cause Summary (1 sentence)
    2. Exact Linux/AWS CLI commands to diagnose and fix the issue
    3. Prevention recommendation

    Logs:
    {logs}
    """

    print("Analyzing failure with AI...")
    response = client.models.generate_content(
        model="gemini-3.0-flash",
        contents=prompt,
    )

    print("\n" + "="*50)
    print("AUTOMATED INCIDENT TRIAGE REPORT")
    print("="*50)
    print(response.text)

if __name__ == "__main__":
    run_triage_agent()
