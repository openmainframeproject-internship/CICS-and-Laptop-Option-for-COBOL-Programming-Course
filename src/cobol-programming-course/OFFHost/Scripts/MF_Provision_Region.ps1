#Start of script
Param
(
  [string] $RegionHost='127.0.0.1',
  [Parameter(Mandatory=$true)]
  [string] $RegionName,
  [string] $BaseConfig='.\Config_NewRegion.json',
  [string] $ESEnvironmentFile='.\NewRegion_Environment.txt',
  [string] $UpdateConfig='.\Config_NewRegion_Update.json',
  [string] $AliasConfig='.\Config_NewRegion_Alias.json',
  [string] $InitiatorConfig='.\Config_NewRegion_initiator.json',
  [string] $DataConfig='.\Config_NewRegion_Datasets.json',
  [Parameter(Mandatory=$true)]
  [string] $SystemBase
)


Import-Module -Name ".\ESCWA_Functions.psm1" -DisableNameChecking -Force

$IIP = $RegionHost
$RegionPort = 9023

#Call Check_MFDS_List function to see if a ESCWA connection has already been established with this IP Address
#If IP address being used is localhost then the Default can be used
if ($IIP -ne '127.0.0.1') {
	$MFDSList = (Check_MFDS_List -MFDSIPAddress $IIP)
	$MFDSSet = $false

	foreach ($hostid in $MFDSList.MfdsHost) {

		if ($hostid -eq $IIP) {$MFDSSet = $true}
	}

	#If no connection has previously been established then add this IP address to the ESCWA MFDS List
	if ($MFDSSet -eq $false) {Add_MFDS_to_List -MFDSIPaddress $IIP -MFDSDescription "New Remote MFDS"}
}
#Call Add_Region function to create the region via ESCWA
Add_Region -RegionName $RegionName -MFDSIPAddress $IIP -Port $RegionPort -TemplateFile $BaseConfig


#Call the Update_Region function to apply configuration changes from provided JSON template
#$CurrentDir = (Get-Location) + 'system'
Update_Region -RegionName $RegionName -MFDSIPAddress $IIP -TemplateFile $UpdateConfig -EnvironmentFile $ESEnvironmentFile -RegionDescription "Test Region" -RegionBase $SystemBase

Set_Jes_listener -RegionName $RegionName -MFDSIPAddress $IIP -LPort 9001

Start_Region -RegionName $RegionName -MFDSIPAddress $IIP 
$Result = (Check_Region_Status -RegionName $RegionName -MFDSIPAddress $IIP -Minsallowed 1)

if ($Result -ne 'Started')  {
  Write-Host 'Region Failed to start. Environment being rewound'
  $Response = (Delete_Region -RegionName $RegionName -MFDSIPAddress $IIP)
  if ($Response -eq 204) {
    Write-Host 'Environment Cleaned successfully'
  }
  exit 1
  }


Update_Alias -RegionName $RegionName -MFDSIPAddress $IIP -AliasFile $AliasConfig

Add_Initiator -RegionName $RegionName -MFDSIPAddress $IIP -TemplateFIle $InitiatorConfig

Add_DataSets -RegionName $RegionName -MFDSIPAddress $IIP -TemplateFIle $DataConfig

