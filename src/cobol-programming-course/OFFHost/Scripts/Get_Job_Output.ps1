#Start of script
Param
(
    [string] $RegionHost='127.0.0.1',
    [string] $RegionName='OMPTRAIN',
    [Parameter(Mandatory=$true)]
    [string] $JobID,
    [Parameter(Mandatory=$true)]
    [string] $WSpaceFolder
)
    Import-Module -Name ".\ESCWA_Functions.psm1" -DisableNameChecking -Force

    $JobRunReturn = (Check_Job -RegionName $RegionName -MFDSIPAddress $RegionHost -JobID $JobID)

    Write-Host ' '
    Write-Host $JobRunReturn.SysoutMsgs[0]
    Write-Host $JobRunReturn.SysoutMsgs[1]

    [string]$CurrentDir = $WSpaceFolder
    
    $Answer = (Test-Path $CurrentDir\Output)

    if ($Answer -eq $false) {New-Item -Path $CurrentDir\Output -ItemType Directory}

    foreach ($SpoolOut in $JobRunReturn.JobDDs) {
        $JobOutPut = (Get_Output -RegionName $RegionName -MFDSIPAddress $RegionHost -JobDDNum $SpoolOut.DDEntityName -OutCharset $SpoolOut.DDCode)
        $OutFileName = $CurrentDir + '\Output\' + $JobRunReturn.JobName + '_' + $JobID + '_' + $SpoolOut.DDName + '.txt'
        $linecount = [int]$SpoolOut.DDRecords
        for ($i=0; $i -lt  $linecount; $i++) {
            $JobOutput.Messages[$i] | Out-File -Append $OutFileName -Encoding oem 
        }
    }


    