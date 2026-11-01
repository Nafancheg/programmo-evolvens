function Get-LabDistro([string]$Requested = '') {
    if ($Requested) { return $Requested }
    if ($env:PE_WSL_DISTRO) { return $env:PE_WSL_DISTRO }
    $config = Join-Path (Split-Path $PSScriptRoot -Parent) '.local/lab.json'
    if (Test-Path -LiteralPath $config) { return (Get-Content -LiteralPath $config -Raw | ConvertFrom-Json).distro }
    return ''
}
