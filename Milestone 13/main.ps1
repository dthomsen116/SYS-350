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

# function to gather specific VM information with a parameter for VM name
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

function menu{
    # Menu to choose which function to run
    Write-Host "1. Get all VMs"
    Write-Host "2. Get specific VM"
    Write-Host "3. Exit"
    $choice = Read-Host "Enter your choice"
    switch ($choice) {
        1 {
            allVmInfo}
        2 {
            $VMName = Read-Host "Enter VM name: "
            specificVMInfo $VMName}
        3 {
            exit}
    }
}

while ($true) {
    menu
}
