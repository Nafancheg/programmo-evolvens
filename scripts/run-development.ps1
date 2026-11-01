[CmdletBinding()]
param([string]$Distro = '')
$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/wsl-command.ps1"
$Distro = Get-LabDistro $Distro
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
