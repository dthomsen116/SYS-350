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

# functions to power on and off a VM with a parameter for VM name
function powerOn{
    $vmName = read-host "Enter VM name to power on: "
    Get-VM $vmName | start-vm
}

# functions to power on and off a VM with a parameter for VM name
function powerOff{
    $vmName = read-host "Enter VM name to power on: "
    Get-VM $vmName | stop-vm
}

# function to search for a VM and create a new Snapshot
function createSnapshot{
    $vmName = read-host "Enter VM name to create a snapshot: "
    $vm = Get-VM $vmName
    $snapName = read-host "Enter snapshot name: "
    $vm | Checkpoint-VM -SnapshotName $snapName
}

# function to display a menu to choose which function to run
function menu{
    # Menu to choose which function to run
    Write-Host "1. Get all VMs"
    Write-Host "2. Search for a specific VM"
    Write-Host "3. Power on a VM"
    Write-Host "4. Power off a VM"
    Write-Host "5. Create a snapshot"
    Write-Host "(9 or exit). Exit"
    $choice = Read-Host "Enter your choice"
    switch ($choice) {
        1 {
            allVmInfo}
        2 {
            $VMName = Read-Host "Enter VM name: "
            specificVMInfo $VMName}
        3 {
            powerOn}
        4 {
            powerOff}
        5 {
            createSnapshot}
        
        9 or "exit" or "Exit" {
            exit}
    }
}

while ($true) {
    menu
}
