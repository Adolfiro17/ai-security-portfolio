# One command to run Project 1 on Windows. No API key, no cloud account.
#   .\start.ps1            tests, seeded attack and guided challenges
#   .\start.ps1 test       tests only
#   .\start.ps1 attack     seeded attack only
#   .\start.ps1 lab 3      one guided challenge (or: lab all)
#   .\start.ps1 site       serve the course site at http://localhost:8000
param([string]$Command = "demo", [string]$Arg = "")
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path .venv)) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Could not create a virtual environment. Install Python 3.11+ from python.org." }
}
$py = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
& $py -m pip install -q -r requirements.txt

switch ($Command) {
    "demo"   { & $py -m pytest -q; & $py -m attacks.run_injection_attack; & $py -m lab.challenges all }
    "test"   { & $py -m pytest -q }
    "attack" { & $py -m attacks.run_injection_attack }
    "lab"    { if ($Arg) { & $py -m lab.challenges $Arg } else { & $py -m lab.challenges } }
    "site"   { Write-Host "Serving http://localhost:8000 (Ctrl+C to stop)"; & $py -m http.server 8000 --directory ..\docs }
    default  { throw "Unknown command: $Command" }
}
