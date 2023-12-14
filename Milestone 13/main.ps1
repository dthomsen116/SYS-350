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
    $vmName = read-host "Enter VM name to search for: "

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
    Get-VM $vmName | Start-VM
}

# functions to power on and off a VM with a parameter for VM name
function powerOff{
    $vmName = read-host "Enter VM name to power off: "
    Get-VM $vmName | Stop-VM
}

# function to search for a VM and create a new Snapshot
function createSnapshot{
    $vmName = read-host "Enter VM name to create a snapshot: "
    $vm = Get-VM $vmName
    $snapName = read-host "Enter snapshot name: "
    $vm | Checkpoint-VM -SnapshotName $snapName
}

# function to list and revert to a previous snapshot
function revertSnapshot{
    $vmName = read-host "Enter VM name to revert to a snapshot: "
    $vm = Get-VM $vmName
    $snapName = read-host "Enter snapshot name: "
    $vm | Restore-VMSnapshot -Name $snapName
}

# function to search for a VM and create a Linked Clone
function linkedClone {
    $originalVM = read-host "Enter VM name to clone: "
    $cloneName = read-host "Enter clone name: "

    $Path = "C:\Users\Public\Documents\Hyper-V\Virtual hard disks\"
    $originalVHD = $Path + $originalVM + ".vhdx"
    $cloneVHD = $Path + $cloneName + ".vhdx"
    New-VHD -ParentPath $originalVHD -Path $cloneVHD -Differencing

    New-VM -Name $cloneName -MemoryStartupBytes 1GB -VHDPath $cloneVHD -Generation 2 -SwitchName "LAN-INTERNAL"
    Set-VMFirmware -VMName $cloneName -EnableSecureBoot Off
    Checkpoint-VM -Name $cloneName -SnapshotName "Base"

    Write-Host "Would you like to turn on the VM? (Y/N): "
    $choice = Read-Host
    if ($choice -eq "Y") {
        Start-VM -Name $cloneName
    }
}

# function to search for a VM and delete it (with confirmation)
function deleteVM{
    $vmName = read-host "Enter VM name to delete: "
    $vm = Get-VM $vmName
    if $vm.state -eq "Running" {
        $ans = write-host "VM is running, would you like to stop the VM? (y/n)"
        if $ans -eq "y" {
            Stop-VM $vmName -Force
        }
        else{
            write-host "VM will not be deleted"
            return
        }
        Stop-VM $vmName -Force
    }

    $confirm = read-host "Are you sure you want to delete $vmName? (y/n)"
    if ($confirm -eq "y") {
        $vm | Remove-VM -Force
    }
}

# function to display a menu to choose which function to run
function menu{
    # Menu to choose which function to run
    Write-Host "1. Get all VMs"
    Write-Host "2. Search for a specific VM"
    Write-Host "3. Power on a VM"
    Write-Host "4. Power off a VM"
    Write-Host "5. Create a snapshot"
    Write-Host "6. Revert to a snapshot"
    Write-Host "7. Create a linked clone"
    Write-Host "8. Delete a VM"
    Write-Host "9. Exit"
    $choice = Read-Host "Enter your choice"
    switch ($choice) {
        1 {allVmInfo}
        2 {specificVMInfo}
        3 {powerOn}
        4 {powerOff}
        5 {createSnapshot}
        6 {revertSnapshot}
        7 {linkedClone}
        8 {deleteVM}
        9 {exit}
    }
}

while ($true) {
    menu
}