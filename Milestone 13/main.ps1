
function Get-HyperVVMInfo {
    # Get all VMs on the local Hyper-V server
    $vms = Get-VM

    foreach ($vm in $vms) {
        $vmName = $vm.Name
        $vmIP = $vm | Get-VMNetworkAdapter | Where-Object {$_.IPAddresses -ne $null} | Select-Object -ExpandProperty IPAddresses
        $vmHostname = $vm | Get-VMIntegrationService | Where-Object {$_.Name -eq "Guest Service Interface"} | Select-Object -ExpandProperty PrimaryHostFullyQualifiedDomainName

        # Output the VM information
        [PSCustomObject]@{
            VMName = $vmName
            IP = $vmIP
            Hostname = $vmHostname
        }
    }
}