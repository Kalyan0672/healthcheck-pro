
import urllib.request
import urllib.error
import csv
import os
import time
import html
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# ==============================
# HEALTHCHECK PRO
# Smart Website Monitoring System
# ==============================

WEBSITES = [
    "https://www.google.com",
    "https://github.com",
    "https://example.com",
    "https://www.wikipedia.org",
    "https://www.python.org"
]

CSV_FILE = "monitoring_history.csv"
HTML_FILE = "dashboard.html"

# Change to True to monitor continuously
CONTINUOUS_MONITORING = False

# Interval between checks (seconds)
CHECK_INTERVAL = 60

# Response time threshold (seconds)
SLOW_THRESHOLD = 2.0


# STEP 1: CHECK WEBSITE HEALTH
def check_website(url):
    start_time = time.perf_counter()
    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "HealthCheckPro/1.0"
            }
        )

        with urllib.request.urlopen(
            request, timeout=8
        ) as response:
            status_code = response.status

        response_time = round(
            time.perf_counter() - start_time, 2
        )

        if 200 <= status_code < 400:
            if response_time > SLOW_THRESHOLD:
                status = "SLOW"
            else:
                status = "UP"
        else:
            status = "DOWN"

    except urllib.error.HTTPError as error:
        status_code = error.code
        response_time = round(
            time.perf_counter() - start_time, 2
        )
        status = "DOWN"

    except Exception:
        status_code = 0
        response_time = round(
            time.perf_counter() - start_time, 2
        )
        status = "DOWN"

    return {
        "timestamp": timestamp,
        "website": url,
        "status": status,
        "status_code": status_code,
        "response_time": response_time
    }


# STEP 2: SAVE MONITORING HISTORY
def save_to_csv(results):
    file_exists = os.path.exists(CSV_FILE)

    with open(
        CSV_FILE, "a", newline="", encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "timestamp",
                "website",
                "status",
                "status_code",
                "response_time"
            ]
        )

        if not file_exists or os.path.getsize(CSV_FILE) == 0:
            writer.writeheader()

        writer.writerows(results)


# STEP 3: CALCULATE HISTORICAL UPTIME
def calculate_uptime():
    history = {}

    if not os.path.exists(CSV_FILE):
        return history

    with open(
        CSV_FILE, "r", encoding="utf-8", newline=""
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            website = row["website"]

            if website not in history:
                history[website] = {
                    "total": 0,
                    "successful": 0
                }

            history[website]["total"] += 1

            if row["status"] in ("UP", "SLOW"):
                history[website]["successful"] += 1

    uptime = {}

    for website, data in history.items():
        uptime[website] = round(
            data["successful"] / data["total"] * 100,
            2
        )

    return uptime


# STEP 4: GENERATE HTML DASHBOARD
def generate_dashboard(results):
    uptime = calculate_uptime()

    total = len(results)
    up = sum(r["status"] == "UP" for r in results)
    slow = sum(r["status"] == "SLOW" for r in results)
    down = sum(r["status"] == "DOWN" for r in results)

    rows = ""

    for result in results:
        website = html.escape(result["website"])
        status = result["status"]
        response_time = result["response_time"]
        code = result["status_code"]

        css_class = status.lower()
        percentage = uptime.get(result["website"], 0)

        rows += f"""
        <tr>
            <td>{website}</td>
            <td>
                <span class="badge {css_class}">
                    {status}
                </span>
            </td>
            <td>{code if code else "N/A"}</td>
            <td>{response_time:.2f} sec</td>
            <td>{percentage:.2f}%</td>
        </tr>
        """

    updated = datetime.now().strftime(
        "%d %B %Y, %I:%M:%S %p"
    )

    dashboard = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1">
        <meta http-equiv="refresh" content="60">
        <title>HealthCheck Pro Dashboard</title>

        <style>
            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #0f172a;
                color: #f8fafc;
            }}

            .container {{
                max-width: 1150px;
                margin: auto;
                padding: 40px 20px;
            }}

            h1 {{
                color: #38bdf8;
                margin-bottom: 5px;
            }}

            .subtitle {{
                color: #94a3b8;
            }}

            .cards {{
                display: grid;
                grid-template-columns:
                    repeat(auto-fit, minmax(180px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}

            .card {{
                background: #1e293b;
                padding: 25px;
                border-radius: 12px;
                border: 1px solid #334155;
            }}

            .card h2 {{
                font-size: 36px;
                margin: 10px 0;
            }}

            .card p {{
                color: #94a3b8;
                margin: 0;
            }}

            .green {{ color: #22c55e; }}
            .yellow {{ color: #facc15; }}
            .red {{ color: #ef4444; }}

            .table-wrapper {{
                overflow-x: auto;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                background: #1e293b;
                border-radius: 12px;
                overflow: hidden;
            }}

            th, td {{
                padding: 17px;
                text-align: left;
                border-bottom: 1px solid #334155;
            }}

            th {{
                background: #334155;
                color: #38bdf8;
            }}

            .badge {{
                padding: 7px 14px;
                border-radius: 20px;
                font-weight: bold;
                display: inline-block;
            }}

            .up {{
                background: #14532d;
                color: #86efac;
            }}

            .slow {{
                background: #713f12;
                color: #fde047;
            }}

            .down {{
                background: #7f1d1d;
                color: #fca5a5;
            }}

            .footer {{
                margin-top: 30px;
                color: #94a3b8;
                text-align: center;
            }}
        </style>
    </head>

    <body>
        <div class="container">

            <h1>🩺 HealthCheck Pro</h1>
            <p class="subtitle">
                Smart Website Monitoring Dashboard
            </p>

            <div class="cards">
                <div class="card">
                    <p>Total Websites</p>
                    <h2>{total}</h2>
                </div>

                <div class="card">
                    <p>Healthy</p>
                    <h2 class="green">{up}</h2>
                </div>

                <div class="card">
                    <p>Slow</p>
                    <h2 class="yellow">{slow}</h2>
                </div>

                <div class="card">
                    <p>Down</p>
                    <h2 class="red">{down}</h2>
                </div>
            </div>

            <h2>Live Monitoring Results</h2>

            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>Website</th>
                            <th>Status</th>
                            <th>HTTP Code</th>
                            <th>Response Time</th>
                            <th>Observed Uptime</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>

            <div class="footer">
                Last checked: {updated}
                <p>
                    Built with Python | DevOps |
                    GitHub Actions
                </p>
                <p>
                    Dashboard refreshes every 60 seconds.
                    New data requires another monitoring run.
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    with open(
        HTML_FILE, "w", encoding="utf-8"
    ) as file:
        file.write(dashboard)


# STEP 5: DISPLAY TERMINAL RESULTS
def display_results(results):
    print("\n" + "=" * 65)
    print("             HEALTHCHECK PRO - WEBSITE MONITOR")
    print("=" * 65)

    colors = {
        "UP": "\033[92m",
        "SLOW": "\033[93m",
        "DOWN": "\033[91m"
    }

    reset = "\033[0m"

    for result in results:
        status = result["status"]
        color = colors.get(status, "")

        print(
            f"{result['website']:<35} "
            f"{color}{status:<6}{reset} "
            f"{result['response_time']:.2f}s"
        )

    print("=" * 65)


# STEP 6: RUN MONITORING
def run_monitor():
    print("\nChecking websites...")

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(
            executor.map(check_website, WEBSITES)
        )

    save_to_csv(results)
    generate_dashboard(results)
    display_results(results)

    print("\nMonitoring completed!")
    print("CSV report saved:", CSV_FILE)
    print("HTML dashboard saved:", HTML_FILE)


# MAIN PROGRAM
if __name__ == "__main__":
    try:
        if CONTINUOUS_MONITORING:
            print("Continuous monitoring started.")
            print("Press Ctrl+C to stop.")

            while True:
                run_monitor()
                time.sleep(CHECK_INTERVAL)
        else:
            run_monitor()

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
