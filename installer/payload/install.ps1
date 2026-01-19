$svc = "NetworkObservabilityAgent"
$exe = "C:\Program Files\NetworkObservabilityAgent\agent.exe"

if (-not (Get-Service $svc -ErrorAction SilentlyContinue)) {
    New-Service -Name $svc `
        -BinaryPathName "`"$exe`"" `
        -DisplayName "Network Observability Agent" `
        -StartupType Automatic
}

sc.exe failure $svc reset= 86400 actions= restart/60000/restart/60000/restart/60000
sc.exe failureflag $svc 1

Start-Service $svc