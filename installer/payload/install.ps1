$ServiceName = "NetworkObservabilityAgent"
$ExePath = "C:\Program Files\NetworkObservabilityAgent\agent.exe"

if (-not (Get-Service $ServiceName -ErrorAction SilentlyContinue)) {
    New-Service `
      -Name $ServiceName `
      -BinaryPathName "`"$ExePath`"" `
      -DisplayName "Network Observability Agent" `
      -StartupType Automatic
}

sc.exe failure $ServiceName reset= 86400 actions= restart/60000/restart/60000/restart/60000
sc.exe failureflag $ServiceName 1

Start-Service $ServiceName
Write-Host "Service $ServiceName installed and started."