$ServiceName = "NetworkObservabilityAgent"

sc.exe stop $ServiceName
sc.exe delete $ServiceName
Write-Host "Service $ServiceName uninstalled."