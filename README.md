# 🤖 AIOps Autonomous Log Triage Agent

An event-driven **Site Reliability Engineering (SRE) & AIOps workflow** built with **Python**, **Google GenAI SDK**, and **GitHub Actions**. Instead of relying on static `if/else` log parsers, this agent reasons over system failures, autonomously invokes live Linux diagnostic tools, and generates actionable remediation reports.

---

### 🏗️ 4-Step Agentic Architecture

```mermaid
flowchart LR
    A["1. CI/CD Trigger<br/>(GitHub Actions)"] --> B["2. Log Ingestion<br/>(Systemd / NGINX Failure)"]
    B --> C{"3. AI Reasoning &<br/>Autonomous Tool Use"}
    C -- "Runs ss -tuln / df -h" --> D["4. SRE Triage Report<br/>(RCA & Fix Commands)"]
    
    style A fill:#1f6feb,stroke:#fff,color:#fff
    style B fill:#2ea043,stroke:#fff,color:#fff
    style C fill:#8957e5,stroke:#fff,color:#fff
    style D fill:#d29922,stroke:#fff,color:#fff
```

---

### 🔍 How It Works (Interview Walkthrough)
1. **Trigger & Secure Auth:** GitHub Actions spins up an Ubuntu runner and securely injects `GEMINI_API_KEY` from **GitHub Secrets** at runtime.
2. **Autonomous Tool Calling:** The Python agent exposes read-only diagnostic functions (`get_failed_service_log`, `check_live_listening_ports`, `check_disk_usage`) to the LLM. Upon seeing a port conflict, the model independently executes `ss -tuln` on the live host while skipping unrelated disk checks.
3. **Fault-Tolerant Inference:** Includes an automatic retry loop with multi-model fallback (`gemini-3.5-flash-lite` ↔ `gemini-3.8-flash`) so transient upstream `503` demand spikes never break the pipeline.
4. **Actionable Output:** Produces a structured Root Cause Analysis (RCA) with exact Linux/AWS CLI remediation commands while keeping a human in the loop before modifying production.
