param([ValidateSet('smoke', 'inspect')][string]$Probe = 'smoke')
$ErrorActionPreference = 'Stop'
$taskFreeBytes = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory * 1024
if ($taskFreeBytes -lt 2GB) { throw 'Less than 2 GiB free host RAM; no probe started.' }
$taskArgs = @('-d', 'Ubuntu-26.04', '--user', 'root', '--exec', '/usr/bin/timeout', '--signal=KILL', '80s', '/usr/bin/python3', '-I', '/opt/pe-world/direct.py', $Probe, '--seed=1')
$taskCode = 2
try {
    & wsl.exe @taskArgs
    $taskCode = $LASTEXITCODE
} finally {
    & wsl.exe -d Ubuntu-26.04 --user root --exec /usr/bin/python3 -I /opt/pe-world/direct.py cleanup
}
exit $taskCode
