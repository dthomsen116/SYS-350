
function Get-HyperVVMInfo {
    # Get all VMs on the local Hyper-V server
    Get-VM | Select-Object -Property Name, State, 
    
    @{Name='IPAddresses'; Expression={($_.NetworkAdapters).IPAddresses}},
    HardDrives,
    
    @{Name='MemoryAssignedMB'; Expression={$_.MemoryAssigned / 1MB}},
    Uptime, 
    Status
}