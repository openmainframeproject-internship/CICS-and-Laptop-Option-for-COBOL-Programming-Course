#Start of script
Param
(
    [string] $RegionHost='127.0.0.1',
    [string] $RegionName='OMPTRAIN',
    [Parameter(Mandatory=$true)]
    [string] $JCLFileName,
    [Parameter(Mandatory=$true)]
    [string] $WSpaceFolder
)
    Import-Module -Name ".\ESCWA_Functions.psm1" -DisableNameChecking -Force

    $JobSubReturn = (Submit_JCL -RegionName $RegionName -MFDSIPAddress $RegionHost -JCLFile $JCLFileName)
    
    Write-Host ' '
    Write-Host $JobSubReturn.JobMsg[0]
    Write-Host $JobSubReturn.JobMsg[1]

    $JobDetails = $JobSubReturn.JobMsg[0] -split ' '

    $JobID = $JobDetails[1]

    $JobRunReturn = (Check_Job -RegionName $RegionName -MFDSIPAddress $RegionHost -JobID $JobID)

    #Write-Host $JobRunReturn.JobDDs
    Write-Host ' '
    Write-Host $JobRunReturn.SysoutMsgs[0]
    Write-Host $JobRunReturn.SysoutMsgs[1]

    

    