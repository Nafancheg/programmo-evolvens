[CmdletBinding()]
param([string]$Distro = '', [AllowEmptyString()][string]$Text)
$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/wsl-command.ps1"
$Distro = Get-LabDistro $Distro
if ($PSBoundParameters.ContainsKey('Text')) {
    . "$PSScriptRoot/python-command.ps1"
    $taskPython = Get-LabPython
    $taskOptions = @('-m', 'programmo_evolvens.experiment', "--text=$Text")
    if ($Distro) { $taskOptions += @('--distro', $Distro) }
    Push-Location (Split-Path $PSScriptRoot -Parent)
    try { & $taskPython.Exe @($taskPython.Prefix) @taskOptions }
    finally { Pop-Location }
    exit $LASTEXITCODE
}
$taskWsl = @()
if ($Distro) { $taskWsl = @('-d', $Distro) }
$taskFreeBytes = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory * 1024
if ($taskFreeBytes -lt 2GB) { throw 'Less than 2 GiB free host RAM; no development started.' }
$taskCode = 2
try {
    & wsl.exe @taskWsl --user root --exec /usr/bin/timeout --signal=KILL 80s /usr/bin/python3 -I /opt/pe-world/direct.py development
    $taskCode = $LASTEXITCODE
} finally {
    & wsl.exe @taskWsl --user root --exec /usr/bin/python3 -I /opt/pe-world/direct.py cleanup
    if ($LASTEXITCODE -ne 0) { $taskCode = 2 }
}
exit $taskCode
