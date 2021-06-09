
#Set-DefaultAWSRegion -Region us-west-2

$RegionName='OMPTRAIN'
$IIP='127.0.0.1'

Import-Module -Name ".\ESCWA_Functions.psm1" -DisableNameChecking -Force

Mark_Region_Stopped -RegionName $RegionName -MFDSIPAddress $IIP

$Result = (Check_Region_Status -RegionName $RegionName -MFDSIPAddress $IIP -MinsAllowed 1)

if ($Result -eq 'Stopped') {
  Write-Host 'Micro Focus JES Batch Server has been successfully set to ' -NoNewline; Write-Host -ForegroundColor Red $Result
} else {
  Write-Host 'Micro Focus JES Batch Server reset failed, status is ' -NoNewline; Write-Host -ForegroundColor Red $Result
}
