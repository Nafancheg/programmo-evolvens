function Get-LabPython {
    foreach ($name in @('py', 'python')) {
        $command = Get-Command $name -ErrorAction SilentlyContinue
        if (-not $command -or $command.Source -like '*WindowsApps*') { continue }
        $prefix = @()
        if ($name -eq 'py') { $prefix = @('-3') }
        & $command.Source @prefix -c 'import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)' 2>$null
        if ($LASTEXITCODE -eq 0) { return @{ Exe = $command.Source; Prefix = $prefix } }
    }
    throw 'Python 3.11+ is required. Install Python, then rerun setup. https://www.python.org/downloads/windows/'
}
