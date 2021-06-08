
Function Set_Origin_and_Header {

    $Origin = 'http://' + $MFDSIPAddress + ':10086'

    $headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
    $headers.Add("accept","application/json")
    $headers.Add("X-Requested-With","CreateRegion")
    $headers.Add("Origin",$Origin)

}
Function Check_MFDS_List {

Param
(
    [Parameter(Mandatory=$true)]
    [string] $MFDSIPAddress
)
    $Origin = 'http://' + $MFDSIPAddress + ':10086'

    $headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
    $headers.Add("accept","application/json")
    $headers.Add("X-Requested-With","CreateRegion")
    $headers.Add("Origin",$Origin)

    $RequestURI = 'http://' + $MFDSIPAddress + ':10086/server/v1/config/mfds'
    

    $Response = (Invoke-RestMethod $RequestURI -Method Post -Headers $headers)

    $MFDSList = $Response | ConvertFrom-Json

    return $MFDSList
}


Function Add_MFDS_to_List {

Param 
(
    [Parameter(Mandatory=$true)]
    [string] $MFDSIPAddress,
	[Parameter(Mandatory=$true)]
	[string] $MFDSDescription
  )

  $Origin = 'http://' + $MFDSIPAddress + ':10086'

  $headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
  $headers.Add("accept","application/json")
  $headers.Add("X-Requested-With","CreateRegion")
  $headers.Add("Origin",$Origin)

  $Jmessage = '{\"MfdsHost\":\"' + $MFDSIPAddress + '\",\"MfdsPort\":\"86\",\"MfdsIdentifier\":\"CI60Test\",\"MfdsDescription\":\" ' + $MFDSDescription + '\"}'

  $RequestURI = 'http://' + $MFDSIPAddress + ':10086/server/v1/config/mfds'
  
  Invoke-RestMethod $RequestURI -Method Post -Headers $headers -Body $Jmessage
  
  return $global:ESCWASession
}

Function Add_Region {

Param
(
    [Parameter(Mandatory=$true)]
    [string] $RegionName,
    [Parameter(Mandatory=$true)]
    [string] $MFDSIPAddress,
    [Parameter(Mandatory=$true)]
    [string] $Port,
	[Parameter(Mandatory=$true)]
	[string] $TemplateFile
)

$Origin = 'http://' + $MFDSIPAddress + ':10086'

$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("accept","application/json")
$headers.Add("X-Requested-With","CreateRegion")
$headers.Add("Content-Type","application/json")
$headers.Add("Origin",$Origin)

$JmessageIn = (Get-Content  -Raw $TemplateFile | ConvertFrom-Json -ErrorAction Stop) 

$JmessageIn.CN = $RegionName
$JmessageIn.mfTN3270ListenerPort = $Port
#$JmessageIn.mfTN3270ListenerPort = 5523

$Jmessage = ($JmessageIn) | ConvertTo-Json

$RequestURI = 'http://' + $MFDSIPAddress + ':10086/native/v1/regions/' + $MFDSIPAddress + '/86'

#$Jmessage = $Jmessage -Replace '"', '\"'

Invoke-RestMethod $RequestURI -Method Post -Headers $headers -Body $Jmessage -SessionVariable $wsheader

Write-Host $wsheader
}

Function Delete_Region {

    Param
    (
        [Parameter(Mandatory=$true)]
        [string] $RegionName,
        [Parameter(Mandatory=$true)]
        [string] $MFDSIPAddress
    )

    Set_Origin_and_Header
    $RequestURI = 'http://' + $MFDSIPAddress + ':10086/native/v1/regions/' + $MFDSIPAddress + '/86/' + $RegionName

    $Response = (Invoke-WebRequest $RequestURI -Method Delete -Headers $headers)

    $DeleteStatus = $Response.StatusCode

    return $DeleteStatus
}
Function Update_Region {

Param
(
    [Parameter(Mandatory=$true)]
    [string] $RegionName,
    [Parameter(Mandatory=$true)]
    [string] $MFDSIPAddress,
	[Parameter(Mandatory=$true)]
	[string] $TemplateFile,
    [Parameter(Mandatory=$true)]
    [string] $EnvironmentFile,
    [Parameter(Mandatory=$true)]
    [string] $RegionDescription,
    [Parameter(Mandatory=$true)]
    [string] $RegionBase
)

$Origin = 'http://' + $MFDSIPAddress + ':10086'

$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("accept","application/json")
$headers.Add("X-Requested-With","CreateRegion")
$headers.Add("Content-Type","application/json")
$headers.Add("Origin",$Origin)

$JmessageIn = (Get-Content  -Raw $TemplateFile | ConvertFrom-Json -ErrorAction Stop) 

$ESEnvIn = (Get-Content -Raw $EnvironmentFile)
$ESEnvIn = $ESEnvIn -Replace '##RegionBase',$RegionBase

$JmessageIn.CN = $RegionName
$JmessageIn.mfConfig = $ESEnvIn
$JmessageIn.description = $RegionDescription

$Jmessage = ConvertTo-Json -InputObject $JmessageIn -Compress

$RequestURI = 'http://' + $MFDSIPAddress + ':10086/native/v1/regions/' + $MFDSIPAddress + '/86/' + $RegionName

#$Jmessage = $Jmessage -Replace '"', '\"'

Invoke-RestMethod $RequestURI -Method Put -Headers $headers -Body $Jmessage
}

Function Start_Region {

Param
(
    [Parameter(Mandatory=$true)]
    [string] $RegionName,
    [Parameter(Mandatory=$true)]
    [string] $MFDSIPAddress
)

$Origin = 'http://' + $MFDSIPAddress + ':10086'

$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("accept","application/json")
$headers.Add("X-Requested-With","CreateRegion")
$headers.Add("Content-Type","application/json")
$headers.Add("Origin",$Origin)



$Jmessage = '{"mfUser":"SYSAD","mfPassword":"SYSAD","mfUseSession":true,"mfColdStart":true}'
$RequestURI = 'http://' + $MFDSIPAddress + ':10086/native/v1/regions/' + $MFDSIPAddress + '/86/' + $RegionName + '/start'


Invoke-RestMethod $RequestURI -Method Post -Headers $headers -Body $Jmessage
}
Function Mark_Region_Stopped {

    Param
    (
        [Parameter(Mandatory=$true)]
        [string] $RegionName,
        [Parameter(Mandatory=$true)]
        [string] $MFDSIPAddress
    )
    
    $Origin = 'http://' + $MFDSIPAddress + ':10086'
    
    $headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
    $headers.Add("accept","application/json")
    $headers.Add("X-Requested-With","CreateRegion")
    $headers.Add("Content-Type","application/json")
    $headers.Add("Origin",$Origin)
    
    
    
    $Jmessage = '{"mfServerStatus":"Stopped"}'
    $RequestURI = 'http://' + $MFDSIPAddress + ':10086/native/v1/regions/' + $MFDSIPAddress + '/86/' + $RegionName
    
    
    Invoke-RestMethod $RequestURI -Method Put -Headers $headers -Body $Jmessage
    }
    
Function Check_Region_Status {

Param
(
    [Parameter(Mandatory=$true)]
    [string] $RegionName,
    [Parameter(Mandatory=$true)]
    [string] $MFDSIPAddress,
    [Parameter(Mandatory=$true)]
    [int] $Minsallowed
)

$RequestURI = 'http://' + $MFDSIPAddress + ':10086/native/v1/regions/' + $MFDSIPAddress + '/86/' + $RegionName + '/status'
$Origin = 'http://' + $MFDSIPAddress + ':10086'

$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("accept","application/json")
$headers.Add("X-Requested-With","CreateRegion")
$headers.Add("Content-Type","application/json")
$headers.Add("Origin",$Origin)

if ($Minsallowed -eq 0) {
    $Response = (Invoke-RestMethod $RequestURI -Method Get -Headers $headers)
} else {    
for ($i=1; $i -le $Minsallowed; $i++)
{

    Start-Sleep -seconds 60
    $Response = (Invoke-RestMethod $RequestURI -Method Get -Headers $headers)

}
}

$RegionStatus = $Response.mfServerStatus #| ConvertFrom-Json

return $RegionStatus

}

Function Stop_Region {

Param
(
    [Parameter(Mandatory=$true)]
    [string] $RegionName,
    [Parameter(Mandatory=$true)]
    [string] $MFDSIPAddress
)
$Jmessage = '{"mfUser":"SYSAD","mfPassword":"SYSAD","mfUseSession":true,"mfClearDynamic":true,"mfForceStop":true}'

$RequestURI = 'http://' + $MFDSIPAddress + ':10086/native/v1/regions/' + $MFDSIPAddress + '/86/' + $RegionName + '/stop'

$Origin = 'http://' + $MFDSIPAddress + ':10086'

$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("accept","application/json")
$headers.Add("X-Requested-With","CreateRegion")
$headers.Add("Content-Type","application/json")
$headers.Add("Origin",$Origin)

Invoke-RestMethod $RequestURI -Method Post -Headers $headers -Body $Jmessage

}

function Update_Alias {
    param (
    [Parameter(Mandatory=$true)]
    [string] $RegionName,
    [Parameter(Mandatory=$true)]
    [string] $MFDSIPAddress,
    [Parameter(Mandatory=$true)]
    [string] $AliasFile
    )

    $Origin = 'http://' + $MFDSIPAddress + ':10086'

    $headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
    $headers.Add("accept","application/json")
    $headers.Add("X-Requested-With","AddAlias")
    $headers.Add("Content-Type","application/json")
    $headers.Add("Origin",$Origin)
    
    $RequestURI = 'http://' + $MFDSIPAddress + ':10086/native/v1/regions/' + $MFDSIPAddress + '/86/' + $RegionName + '/alias'

    $Jmessage = (Get-Content -Raw $AliasFile)
    Invoke-RestMethod $RequestURI -Method Post -Headers $headers -Body $Jmessage

}
Function Add_Initiator {

    Param
    (
        [Parameter(Mandatory=$true)]
        [string] $RegionName,
        [Parameter(Mandatory=$true)]
        [string] $MFDSIPAddress,
        [Parameter(Mandatory=$true)]
        [string] $TemplateFile
    )
    
    $Origin = 'http://' + $MFDSIPAddress + ':10086'
    
    $headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
    $headers.Add("accept","application/json")
    $headers.Add("X-Requested-With","CreateRegion")
    $headers.Add("Content-Type","application/json")
    $headers.Add("Origin",$Origin)
    
    $JmessageIn = (Get-Content  -Raw $TemplateFile | ConvertFrom-Json -ErrorAction Stop) 
    
    $JmessageIn.CN = $RegionName
    
    $Jmessage = ConvertTo-Json -InputObject $JmessageIn -Compress
    
    $RequestURI = 'http://' + $MFDSIPAddress + ':10086/native/v1/regions/' + $MFDSIPAddress + '/86/' + $RegionName + '/initiator'
    
    #$Jmessage = $Jmessage -Replace '"', '\"'
    
    Invoke-RestMethod $RequestURI -Method Post -Headers $headers -Body $Jmessage
    }
Function Add_DataSets {

    Param
    (
        [Parameter(Mandatory=$true)]
        [string] $RegionName,
        [Parameter(Mandatory=$true)]
        [string] $MFDSIPAddress,
        [Parameter(Mandatory=$true)]
        [string] $TemplateFile
    )

    $Origin = 'http://' + $MFDSIPAddress + ':10086'
    
    $headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
    $headers.Add("accept","application/json")
    $headers.Add("X-Requested-With","CreateRegion")
    $headers.Add("Content-Type","application/json")
    $headers.Add("Origin",$Origin)
    
    

    $DataSetList = (Get-Content  -Raw $TemplateFile | ConvertFrom-Json -ErrorAction Stop) 

    foreach ($dsn in $DatasetList.datasets) {
        $RequestURI = 'http://' + $MFDSIPAddress + ':10086/native/v1/regions/' + $MFDSIPAddress + '/86/' + $RegionName + '/catalog/' + $dsn.jDSN
        $Jmessage = ConvertTo-Json -InputObject $dsn -Compress
        Invoke-RestMethod $RequestURI -Method Post -Headers $headers -Body $Jmessage
    }
}
Function Submit_JCL {

    Param
    (
        [Parameter(Mandatory=$true)]
        [string] $RegionName,
        [Parameter(Mandatory=$true)]
        [string] $MFDSIPAddress,
        [Parameter(Mandatory=$true)]
        [string] $JCLFile
    )

    $Origin = 'http://' + $MFDSIPAddress + ':10086'
    
    $headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
    $headers.Add("accept","application/json")
    $headers.Add("X-Requested-With","JESProcess")
    $headers.Add("Content-Type","application/json")
    $headers.Add("Origin",$Origin)
    
    $RequestURI = 'http://' + $MFDSIPAddress + ':10086/native/v1/regions/' + $MFDSIPAddress + '/86/' + $RegionName + '/jescontrol'

    $JCLFile = $JCLFile -Replace '\\', '\\'
    $Jmessage = '{"ctlSubmit":"Submit","subJes":2,"xatSwitch":"' + $JCLFile + '"}'

    $SubmitReturn = (Invoke-RestMethod $RequestURI -Method Post -Headers $headers -Body $Jmessage)

    return $SubmitReturn
}
Function Check_job {

    Param
    (
        [Parameter(Mandatory=$true)]
        [string] $RegionName,
        [Parameter(Mandatory=$true)]
        [string] $MFDSIPAddress,
        [Parameter(Mandatory=$true)]
        [string] $JobID
    )

    $Origin = 'http://' + $MFDSIPAddress + ':10086'
    
    $headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
    $headers.Add("accept","application/json")
    $headers.Add("X-Requested-With","JESProcess")
    $headers.Add("Content-Type","application/json")
    $headers.Add("Origin",$Origin)
    
    $RequestURI = 'http://' + $MFDSIPAddress + ':10086/native/v1/regions/' + $MFDSIPAddress + '/86/' + $RegionName + '/jobview/' + $JobID

    Do {
        $RunReturn = (Invoke-RestMethod $RequestURI -Method Get -Headers $headers -Body $Jmessage)
    } Until ($RunReturn.JobStatus -eq 'Complete ')
        
    return $RunReturn
}
Function Get_Output {

    Param
    (
        [Parameter(Mandatory=$true)]
        [string] $RegionName,
        [Parameter(Mandatory=$true)]
        [string] $MFDSIPAddress,
        [Parameter(Mandatory=$true)]
        [string] $JobDDNum,
        [Parameter(Mandatory=$true)]
        [string] $OutCharset
    )

    $Origin = 'http://' + $MFDSIPAddress + ':10086'
    
    $headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
    $headers.Add("accept","application/json")
    $headers.Add("X-Requested-With","JESProcess")
    $headers.Add("Content-Type","application/json")
    $headers.Add("Origin",$Origin)
    
    $RequestURI = 'http://' + $MFDSIPAddress + ':10086/native/v1/regions/' + $MFDSIPAddress + '/86/' + $RegionName + '/spool/' + $JobDDNum + '/display?jSvStart=1&jSvFor=10000&jSvCode=' + $OutCharset

    $JobOutput = (Invoke-RestMethod $RequestURI -Method Get -Headers $headers -Body $Jmessage)
            
    return $JobOutput
}
Function Set_Jes_listener {

    Param
    (
        [Parameter(Mandatory=$true)]
        [string] $RegionName,
        [Parameter(Mandatory=$true)]
        [string] $MFDSIPAddress,
        [Parameter(Mandatory=$true)]
        [string] $LPort
    )
    
    $Origin = 'http://' + $MFDSIPAddress + ':10086'
    
    $headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
    $headers.Add("accept","application/json")
    $headers.Add("X-Requested-With","JESProcess")
    $headers.Add("Content-Type","application/json")
    $headers.Add("Origin",$Origin)

    $RequestURI = 'http://' + $MFDSIPAddress + ':10086/native/v1/regions/' + $MFDSIPAddress + '/86/' + $RegionName + '/commsserver'

    $CommServ = (Invoke-RestMethod $RequestURI -Method Get -Headers $headers -Body $Jmessage)

    $RequestURI = 'http://' + $MFDSIPAddress + ':10086/native/v1/regions/' + $MFDSIPAddress + '/86/' + $RegionName + '/commsserver/' + $CommServ.mfServerUID + '/listener'

    $ListenerList = (Invoke-RestMethod $RequestURI -Method Get -Headers $headers -Body $Jmessage)

    foreach ($llist in $ListenerList) {
        if ($llist.CN -eq 'Web Services and J2EE') {
            $RequestURI = 'http://' + $MFDSIPAddress + ':10086/native/v1/regions/' + $MFDSIPAddress + '/86/' + $RegionName + '/commsserver/' + $CommServ.mfServerUID + '/listener/' + $llist.mfUID 
            $Jmessage = '{"mfRequestedEndpoint": "tcp:127.0.0.1:' + $Lport + '"}'
            Invoke-RestMethod $RequestURI -Method Put -Headers $headers -Body $Jmessage  
        }
    }
}