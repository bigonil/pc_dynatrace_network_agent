$BaseDir = "C:\Program Files\NetworkObservabilityAgent"
$ServiceName = "NetworkObservabilityAgent"

if (!(Test-Path $BaseDir)) {
    New-Item -ItemType Directory -Path $BaseDir | Out-Null
}

sc.exe create $ServiceName `
  binPath= "`"$BaseDir\agent.exe`"" `
  start= auto

sc.exe start $ServiceName
Write-Host "Service $ServiceName installed and started."