# Configure and build a preset of this repository with psvrecore's build script, against psvrecore's package
# for the same preset (in psvrecore: scripts\build.ps1 -Preset <preset> -NoTest -Install).
#
#   scripts\build.ps1                                  # windows-x64-debug, build
#   scripts\build.ps1 -Preset windows-x64-release -NoTest
#   scripts\build.ps1 -Preset android-arm64-release
param(
    [string]$Preset = 'windows-x64-debug',
    [switch]$NoTest,
    [string[]]$Target
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
# (psvrecore's standalone checkout: PSVRECORE_ROOT, or vitarecomp/psvrecore beside this repository)
$psvrecore = if ($env:PSVRECORE_ROOT) { $env:PSVRECORE_ROOT } else { Join-Path (Split-Path -Parent $root) 'psvrecore' }
& (Join-Path $psvrecore 'scripts\build.ps1') -Root $root -Preset $Preset -NoTest:$NoTest -Target $Target
if ($LASTEXITCODE) { exit $LASTEXITCODE }
