[CmdletBinding()]
param([string]$Distro = '', [switch]$InstallDependencies, [switch]$UpdateWorld, [switch]$CheckOnly)
$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/python-command.ps1"
. "$PSScriptRoot/wsl-command.ps1"
$Distro = Get-LabDistro $Distro
$taskPython = Get-LabPython
$taskRepo = Split-Path $PSScriptRoot -Parent
$taskWsl = @()
if ($Distro) { $taskWsl = @('-d', $Distro) }
if (-not (Get-Command wsl.exe -ErrorAction SilentlyContinue)) { throw 'Install WSL2: wsl --install -d Ubuntu. Restart if requested, then rerun setup.' }
& wsl.exe @taskWsl --exec /usr/bin/uname -m
if ($LASTEXITCODE -ne 0) { throw 'A working WSL2 Ubuntu/Debian distribution is required. Run wsl --install -d Ubuntu, complete first launch, then rerun setup.' }
if ($CheckOnly) {
    & wsl.exe @taskWsl --user root --exec /usr/bin/python3 -I /opt/pe-world/direct.py preflight
    if ($LASTEXITCODE -ne 0) { throw 'World is not ready. Run setup with -InstallDependencies for a new installation.' }
    Write-Output 'Check complete. No configuration or installation changed.'
    return
}
$taskLinuxRepo = (& wsl.exe @taskWsl --exec wslpath -u $taskRepo).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Could not resolve checkout inside WSL.' }
$taskOptions = @()
if ($InstallDependencies) { $taskOptions += '--install-dependencies' }
if ($UpdateWorld) { $taskOptions += '--update' }
& wsl.exe @taskWsl --user root --exec /bin/sh "$taskLinuxRepo/world/wsl2/config/setup-current.sh" @taskOptions
if ($LASTEXITCODE -ne 0) { throw 'World setup failed; no acceptance is claimed.' }
New-Item -ItemType Directory -Path "$taskRepo/.local" -Force | Out-Null
@{ distro = $Distro } | ConvertTo-Json | Set-Content -LiteralPath "$taskRepo/.local/lab.json" -Encoding UTF8
Write-Output 'Ready for observation. Start: .\scripts\start-lab.ps1'
Write-Output 'Run acceptance on this PC: .\world\wsl2\config\run-acceptance.ps1'
