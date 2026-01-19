$svc = "NetworkObservabilityAgent"
Stop-Service $svc -Force
sc.exe delete $svc