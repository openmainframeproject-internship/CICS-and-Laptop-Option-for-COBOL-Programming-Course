
#Set-DefaultAWSRegion -Region us-west-2

Param
(
  [Parameter(Mandatory=$true)]
  [string] $ProgName,
  [Parameter(Mandatory=$true)]
  [string] $Outdir,
  [Parameter(Mandatory=$true)]
  [string] $BaseDir
)

$env:ANT_HOME = 'C:\OpenMainframeProject\cobol-programming-course\OFFHost\apache-ant-1.10.9'
$env:JAVA_HOME = 'C:\Program Files (x86)\Java\jre1.8.0_261'
$InstallEntry = (Get-ItemProperty -path 'HKLM:\SOFTWARE\Micro Focus\Visual COBOL\6.0')
$InstallDir = $InstallEntry.INSTALLDIR
$env:path +=';' + $InstallDir + '\bin\;' + $InstallDir + '\binn\'
$env:COBDIR=$InstallDir

$SourceLocation = $BaseDir
#$LibFile = "'" + $env:COBDIR + "bin\mfant.jar'"

$AntCMD = $env:ANT_HOME + '\bin\ant -f build.xml -Dbasedir=' + $SourceLocation + ' -Dloaddir=' + $OutDir + ' -Dprogname=' + $ProgName
Write-Host $AntCMD
cmd.exe /c $AntCMD

#}
