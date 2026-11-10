param([string[]]$Codes = @(), [string]$DiagramDirectory = 'docs/formal/diagramas-drawio')
$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSScriptRoot
$diagramRoot=Join-Path $taskRoot $DiagramDirectory
$drawExecutable='C:/Program Files/draw.io/draw.io.exe'
if (-not (Test-Path -LiteralPath $drawExecutable)) { throw 'No se encontró draw.io Desktop.' }
foreach ($format in @('png','svg')) {
    New-Item -ItemType Directory -Force -Path (Join-Path $diagramRoot $format) | Out-Null
}
$diagramFiles=Get-ChildItem -LiteralPath $diagramRoot -Filter '*.xml' | Sort-Object Name
foreach ($diagramFile in $diagramFiles) {
    $diagramCode=if ($diagramFile.BaseName -match '^((?:AC|CU)-SP-\d+)') { $Matches[1] } else { $diagramFile.BaseName.Substring(0,3) }
    if ($Codes.Count -gt 0 -and $diagramCode -notin $Codes) { continue }
    foreach ($format in @('png','svg')) {
        $diagramOutput=Join-Path (Join-Path $diagramRoot $format) ($diagramFile.BaseName+'.'+$format)
        # Fractional scale cropped large PNGs with this Windows build; SVG remains vector.
        $drawArgs=@('--zoom','1','--export','--format',$format,'--scale','1','--border','20','--svg-theme','light','--output',('"'+$diagramOutput+'"'),('"'+$diagramFile.FullName+'"'))
        $exportProcess=Start-Process -FilePath $drawExecutable -ArgumentList $drawArgs -WindowStyle Hidden -Wait -PassThru
        if ($exportProcess.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $diagramOutput)) { throw "Falló exportación: $diagramCode $format" }
    }
    Write-Output "$diagramCode exportado: PNG y SVG"
}
