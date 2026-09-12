# Rendus fidèles au modèle OpenSCAD, sans génération d'image par IA.
# Depuis PowerShell : ./plans/outils/generer-images.ps1
param([string]$OpenSCAD = 'C:/Program Files/OpenSCAD/openscad.com')
$ErrorActionPreference = 'Stop'
$planDir = Split-Path $PSScriptRoot -Parent
$source = Join-Path $planDir 'loc-iv-4po.scad'
$imageDir = Join-Path $planDir 'images'
New-Item -ItemType Directory -Force $imageDir | Out-Null
$pieces = @(
    @('aileron','fin','packed'),
    @('ogive','nose','packed'),
    @('corps-booster','booster','packed'),
    @('section-payload','payload','packed'),
    @('coupleur','coupler','packed'),
    @('cloison','bulkhead','packed'),
    @('tube-support-moteur','motor_mount','packed'),
    @('anneau-centrage','ring','packed'),
    @('moteur-pro38-2g','motor','packed'),
    @('retention-mr-1','retainer','packed'),
    @('parachute-range','parachute','packed'),
    @('parachute-deploye','parachute','deployed'),
    @('protecteur-range','protector','packed'),
    @('protecteur-deplie','protector','deployed'),
    @('sangle','cord','packed'),
    @('bouton-rail-1010','rail_button','packed'),
    @('outil-prodat-38','prodat','packed'),
    @('point-attache','eye','packed')
)
foreach ($piece in $pieces) {
    $destination = Join-Path $imageDir ($piece[0] + '.png')
    $renderArgs = @('-o', $destination, '--render', '--imgsize=1200,900',
        '--projection=o', '--viewall', '--autocenter',
        '--camera=0,0,0,65,0,30,500', '--colorscheme=Tomorrow',
        '-D', ('part="' + $piece[1] + '"'),
        '-D', ('recovery="' + $piece[2] + '"'), $source)
    $log = & $OpenSCAD @renderArgs 2>&1
    if ($LASTEXITCODE -ne 0 -or ($log -match 'ERROR:|WARNING:')) {
        throw "Échec du rendu $($piece[0]): $log"
    }
    if (-not (Test-Path -LiteralPath $destination)) { throw "Image absente: $destination" }
    Write-Output "OK $($piece[0])"
}
