$Env:CONDA_EXE = "/Users/alisaleh/miniforge3/bin/conda"
$Env:_CONDA_EXE = "/Users/alisaleh/miniforge3/bin/conda"
$Env:_CE_M = $null
$Env:_CE_CONDA = $null
$Env:CONDA_PYTHON_EXE = "/Users/alisaleh/miniforge3/bin/python"
$Env:_CONDA_ROOT = "/Users/alisaleh/miniforge3"
$CondaModuleArgs = @{ChangePs1 = $True}

Import-Module "$Env:_CONDA_ROOT\shell\condabin\Conda.psm1" -ArgumentList $CondaModuleArgs

Remove-Variable CondaModuleArgs