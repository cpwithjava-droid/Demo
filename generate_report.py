import pdfkit
import json

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

# Load reports
metrics = load_json("sonar-report.json")
issues = load_json("sonar-issues.json").get("issues", [])
gitleaks = load_json("gitleaks-report.json")

# Helper function for severity color
def severity_color(severity):
    colors = {
        "BLOCKER": "#d32f2f",
        "CRITICAL": "#f57c00",
        "MAJOR": "#1976d2",
        "MINOR": "#0288d1",
        "INFO": "#388e3c"
    }
    return colors.get(severity.upper(), "#000000")

# Build HTML
html = f"""
<html>
<head>
<style>
body {{ font-family: Arial, sans-serif; }}
h1 {{ color: #2e7d32; }}
h2 {{ color: #1565c0; }}
table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background-color: #f2f2f2; }}
.badge {{ padding: 2px 6px; color: white; border-radius: 4px; font-weight: bold; }}
.metric-bar {{ height: 16px; background-color: #1976d2; }}
</style>
</head>
<body>
<h1>CI/CD Security & Code Quality Report</h1>

<h2>SonarQube Summary Metrics</h2>
<table>
<tr><th>Metric</th><th>Value</th></tr>
"""

for m in metrics.get("component", {}).get("measures", []):
    html += f"<tr><td>{m['metric']}</td><td>{m['value']}</td></tr>"

html += "</table>"

# SonarQube Issues
html += "<h2>SonarQube Issues</h2>"
if issues:
    html += "<table><tr><th>File</th><th>Line</th><th>Severity</th><th>Message</th></tr>"
    for issue in issues:
        color = severity_color(issue.get("severity", ""))
        html += f"<tr><td>{issue.get('component')}</td><td>{issue.get('line')}</td><td><span class='badge' style='background-color:{color}'>{issue.get('severity')}</span></td><td>{issue.get('message')}</td></tr>"
    html += "</table>"
else:
    html += "<p>No issues detected.</p>"

# Gitleaks Report
html += "<h2>Gitleaks Report</h2>"
if gitleaks:
    html += "<table><tr><th>File</th><th>Secret Type</th><th>Line</th><th>Secret</th></tr>"
    for leak in gitleaks.get("leaks", []):
        html += f"<tr><td>{leak.get('file')}</td><td>{leak.get('rule')}</td><td>{leak.get('line')}</td><td>{leak.get('secret')}</td></tr>"
    html += "</table>"
else:
    html += "<p>No secrets detected.</p>"

html += "</body></html>"

# Generate PDF
pdfkit.from_string(html, "ci-cd-report.pdf")
print("✅ Enhanced PDF report generated successfully.")
