$ServiceName = "NetworkObservabilityAgent"

if (Get-Service $ServiceName -ErrorAction SilentlyContinue) {
    Stop-Service $ServiceName -Force
    sc.exe delete $ServiceName
}
Write-Host "Service $ServiceName uninstalled."