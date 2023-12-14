# Author: David Thomsen
# function to grab all VMs on the local Hyper-V server
function allVmInfo {
    # Get all VMs on the local Hyper-V server
    Get-VM | ForEach-Object {
        $_ | Select-Object -Property Name, State, 
        @{Name='IPAddresses'; Expression={($_.NetworkAdapters).IPAddresses}},
        HardDrives,
        @{Name='MemoryAssignedMB'; Expression={$_.MemoryAssigned / 1MB}},
        Uptime, 
        Status
        Write-Host "----------------------"
    }
}

# function to gather specific VM information with a search for VM name

function specificVMInfo {
    param (
        [Parameter(Mandatory=$true)]
        [string]$VMName
    )

    # Get specific VM information with a search for VM name
    Get-VM -Name $VMName | ForEach-Object {
        $_ | Select-Object -Property Name, State, 
        @{Name='IPAddresses'; Expression={($_.NetworkAdapters).IPAddresses}},
        HardDrives,
        @{Name='MemoryAssignedMB'; Expression={$_.MemoryAssigned / 1MB}},
        Uptime, 
        Status
        Write-Host "----------------------"
    }
}

specificVMInfo -VMName "TempleOS"