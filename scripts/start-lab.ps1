[CmdletBinding()]
param([string]$Distro = '', [int]$Port = 8765, [switch]$NoBrowser)
$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/python-command.ps1"
. "$PSScriptRoot/wsl-command.ps1"
$Distro = Get-LabDistro $Distro
$taskPython = Get-LabPython
$taskOptions = @('-m', 'programmo_evolvens.lab', '--port', "$Port")
if ($Distro) { $taskOptions += @('--distro', $Distro) }
if (-not $NoBrowser) { $taskOptions += '--open' }
Push-Location (Split-Path $PSScriptRoot -Parent)
try { & $taskPython.Exe @($taskPython.Prefix) @taskOptions }
finally { Pop-Location }
exit $LASTEXITCODE
