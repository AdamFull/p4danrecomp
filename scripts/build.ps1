# Configure, build and (optionally) test a preset of this repository with psvrecore's build script.
#
#   scripts\build.ps1                                  # windows-x64-debug, build + tests
#   scripts\build.ps1 -Preset windows-x64-release -NoTest
#   scripts\build.ps1 -Preset android-arm64-release
param(
    [string]$Preset = 'windows-x64-debug',
    [switch]$NoTest,
    [string[]]$Target
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
& (Join-Path $root 'psvrecore\scripts\build.ps1') -Root $root -Preset $Preset -NoTest:$NoTest -Target $Target
if ($LASTEXITCODE) { exit $LASTEXITCODE }
