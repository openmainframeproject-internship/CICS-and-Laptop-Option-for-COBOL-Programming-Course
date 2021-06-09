
#Set-DefaultAWSRegion -Region us-west-2

$RegionName='OMPTRAIN'
$IIP='127.0.0.1'

Import-Module -Name ".\ESCWA_Functions.psm1" -DisableNameChecking -Force

$Result = (Check_Region_Status -RegionName $RegionName -MFDSIPAddress $IIP -MinsAllowed 0)

Write-Host 'Current Status of the Micro Focus JES Batch Server is ' -NoNewline; Write-Host -ForegroundColor Red $Result
