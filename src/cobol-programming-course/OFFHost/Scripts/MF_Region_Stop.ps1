
#Set-DefaultAWSRegion -Region us-west-2

$RegionName='OMPTRAIN'
$IIP='127.0.0.1'

Import-Module -Name ".\ESCWA_Functions.psm1" -DisableNameChecking -Force

Stop_Region -RegionName $RegionName -MFDSIPAddress $IIP

$Result = (Check_Region_Status -RegionName $RegionName -MFDSIPAddress $IIP -MinsAllowed 1)

if ($Result -eq 'Stopped') {
  Write-Host 'Micro Focus JES Batch Server has stopped successfully'
} else {
  Write-Host 'Micro Focus JES Batch Server has failed to stop'
}
