param(
    [switch]$Clean
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$backend = Join-Path $repo 'backend'

Push-Location $backend
try {
    if ($Clean) {
        & .\gradlew.bat clean
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }

    & .\gradlew.bat test `
        --tests 'com.sinapuml.assistant.vision.AssistantImageInputValidatorTests' `
        --tests 'com.sinapuml.assistant.vision.VisionProposalGroundingValidatorTests' `
        --tests 'com.sinapuml.assistant.vision.VisionProposalCompilerTests' `
        --tests 'com.sinapuml.assistant.vision.VisionEvidenceBoundsValidatorTests' `
        --tests 'com.sinapuml.assistant.vision.LlamaCppVisionModelGatewayTests' `
        --tests 'com.sinapuml.assistant.vision.AssistantImagePlanIntegrationTests'

    exit $LASTEXITCODE
} finally {
    Pop-Location
}
