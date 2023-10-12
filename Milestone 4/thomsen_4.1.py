# Import necessary modules
import getpass, warnings, ssl
from pyVim.connect import SmartConnect
from pyVmomi import vim

#Mute the Deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Define a class for vCenter connection
class VCenterConnection:
    def __init__(self, creds_filename):
        # Initialize the class with credentials and SmartConnect instance
        self.creds = self.readCreds(creds_filename)
        self.si = None

    # Function to read credentials from a file
    def readCreds(self, filename):
        try:
            with open(filename, 'r') as file:
                creds = {}
                for line in file:
                    key, value = line.strip().split('=')
                    creds[key.strip()] = value.strip()
                return creds
        except Exception as e:
            print(f"Error reading credentials: {e}")
            return None

    # Function to login to vCenter
    def login(self):
        if self.creds is None:
            return
        passwd = getpass.getpass()
        try:
            # Establish an SSL connection to vCenter
            s = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            s.verify_mode = ssl.CERT_NONE
            self.si = SmartConnect(host=self.creds.get("hostname"), user=self.creds.get("username"), pwd=passwd, sslContext=s)
        except Exception as e:
            print(f"Error connecting to vCenter: {e}")

    # Function to display session information
    def sessionInfo(self):
        p = self.si.content.sessionManager.currentSession
        print("\nSession Info")
        print("-----------------------------------------------------------------")
        print("Session Key: " + p.key)
        print("Session User Agent: " + p.userAgent)
        print("Session Domain/Username: " + p.userName)
        print("Session Server: " + self.si.content.about.name)

    # Function to retrieve and display VM information
    def vmInfo(self):
        search = input("Search for a VM: ")
        print()

        for child in self.si.content.rootFolder.childEntity:
            dc = child
            vmfolder = dc.vmFolder
            vmlist = vmfolder.childEntity

        for vm in vmlist:
            if vm.name != "%2fvmfs%2fvolumes%2f64f20cb8-49d66acc-314c-3cecef4663da%2fpfsense%2fpfsense.vmx":
                if search in vm.name:
                    print()
                    print("Name: " + vm.name)
                    print("Power State: " + vm.runtime.powerState)
                    print("Number of CPUs: " + str(vm.config.hardware.numCPU))
                    print("Memory in GB: " + str(vm.config.hardware.memoryMB / 1024))
                    
                    
                    # Retrieve and display VM's IP address
                    ip_address = None
                    try:
                        for guest in vm.guest.net:
                            if guest.ipConfig.ipAddress:
                                ip_address = guest.ipConfig.ipAddress[0].ipAddress
                                break
                    except AttributeError:
                        print("IP Address: Not available (VMware Tools may not be installed)")

                    if ip_address:
                        print("IP Address: " + ip_address)
                    else:
                        continue

    # Function to alter the Power State
    def powerChange(self):
        search = input("Search for a VM: ")
        print()

        for child in self.si.content.rootFolder.childEntity:
            dc = child
            vmfolder = dc.vmFolder
            vmlist = vmfolder.childEntity

        for vm in vmlist:
            if vm.name != "%2fvmfs%2fvolumes%2f64f20cb8-49d66acc-314c-3cecef4663da%2fpfsense%2fpfsense.vmx":
                if search in vm.name:
                    print("Name: " + vm.name)
                    print("Power State: " + vm.runtime.powerState + "\n")
                    print("1. Yes")
                    print("2. No")
                    print("3. Menu\n")
                    choice = input("\nDo you want to edit the power state?:")
                    print()
                    if choice in ('1', 'y', 'Y'):
                        print("1. On")
                        print("2. Off")
                        choice2 = input("\nPower on or off?: ")

                        if choice2 == '1':
                            try:
                                if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOff:
                                    vm.PowerOn()
                                    print("VM powered on successfully.")
                                else:
                                    print("The VM is already powered on.")
                            except Exception as e:
                                print("Error occurred while powering on the VM:", str(e))
                        elif choice2 == '2':
                            try:
                                vm.PowerOff()
                            except Exception:
                                print("Error occurred...")
                        else:
                            print("Invalid choice. Returning to the menu...")

                    elif choice in ('2', 'n', 'N'):
                        print("Returning to the menu...\n")
                    else:
                        print("Invalid choice. Returning to the menu...")
                    if choice in ('3', 'exit'):
                        print("Returning to menu...")
                        continue

    # Function to take and revert snapshots
    def snapshotVM(self):
        search = input("\nSearch for a VM: ")
        print()

        for child in self.si.content.rootFolder.childEntity:
            dc = child
            vmfolder = dc.vmFolder
            vmlist = vmfolder.childEntity

        for vm in vmlist:
            if vm.name != "%2fvmfs%2fvolumes%2f64f20cb8-49d66acc-314c-3cecef4663da%2fpfsense%2fpfsense.vmx":
                if search in vm.name:
                    print("Name: " + vm.name + "\n")
                    print("1. Yes")
                    print("2. No\n")
                    choice = input("\nDo you want to work with this VM?: ")
                    print()
                    
                    if choice in ('1', 'y', 'Y'):
                        print("1. Take a Snapshot")
                        print("2. Revert to Last Snapshot")
                        print("3. Back to Menu")
                        choice2 = input("\nSelect an action (1/2/3): ")

                        if choice2 == '1':
                            try:
                                snapshot_name = input("Enter Snapshot Name: ")
                                description = input("Enter Snapshot Description: ")
                                vm.CreateSnapshot(snapshot_name, description, memory=False, quiesce=False)
                                print("Snapshot created successfully.")
                            except Exception as e:
                                print("Error occurred while taking a snapshot:", str(e))
                        
                        elif choice2 == '2':
                            try:
                                snapshots = vm.snapshot.rootSnapshotList
                                if snapshots:
                                    latest_snapshot = snapshots[0]
                                    latest_snapshot.snapshot.RevertToSnapshot_Task()
                                    
                                    print("Reverted to the latest snapshot successfully.")
                                else:
                                    print("No snapshots found for this VM.")
                            except Exception as e:
                                print("Error occurred while reverting to the latest snapshot:", str(e))
                        
                        elif choice2 == '3':
                            print("Returning to the menu...")
                        
                        else:
                            print("Invalid choice. Returning to the menu...")

                    elif choice in ('2', 'n', 'N'):
                        print("Returning to the menu...\n")
                    
                    else:
                        print("Invalid choice. Returning to the menu...")

    # Function to create a full clone of a VM
    def fullClone(self):
        search = input("Search for a VM: ")
        print()

        for child in self.si.content.rootFolder.childEntity:
            dc = child
            vmfolder = dc.vmFolder
            vmlist = vmfolder.childEntity

        for vm in vmlist:
            if vm.name != "%2fvmfs%2fvolumes%2f64f20cb8-49d66acc-314c-3cecef4663da%2fpfsense%2fpfsense.vmx":
                if search in vm.name:
                    print("Name: " + vm.name)
                    clone_name = input("Enter a name for the clone: ")

                    try:
                        # Create a clone specification
                        clone_spec = vim.vm.CloneSpec()
                        clone_spec.location = vim.vm.RelocateSpec()
                        clone_spec.powerOn = False  

                        # Clone the VM
                        vm.Clone(folder=vmfolder, name=clone_name, spec=clone_spec)
                        print("Clone creation initiated successfully.")
                        print("Check vCenter for the status of the clone operation.")

                    except Exception as e:
                        print("Error occurred while cloning the VM:", str(e))
                        continue

    # Function to delete a VM
    def deleteVM(self):
        search = input("Search for a VM: ")
        print()

        for child in self.si.content.rootFolder.childEntity:
            dc = child
            vmfolder = dc.vmFolder
            vmlist = vmfolder.childEntity

        for vm in vmlist:
            if vm.name != "%2fvmfs%2fvolumes%2f64f20cb8-49d66acc-314c-3cecef4663da%2fpfsense%2fpfsense.vmx":
                if search in vm.name:
                    print("Name: " + vm.name +'\n')

                    print("1. Yes\n")
                    print("1. No\n")
                    choich = input("Is this the VM you would like to delete? (1/2): ")
                    if vm.runtime.powerState == 'poweredOn':
                        print(f"VM "+ vm.name + " is powered on. Please power off the VM before deleting")
                        break
                    else:
                        if choich == '1':        
                            try:
                                check = input('\n Are you sure: Please print "' + vm.name + '": ')
                                if check == vm.name:
                                    vm.Destroy()
                                    print("\n VM has been Destoyed")

                            except Exception as e:
                                print("Error occurred while cloning the VM:", str(e))
                                continue                    
                        else: 
                            print("Returning to menu")
                            continue

    # Function to display the main menu
    def display_menu(self):
        while True:
            print("\nMenu:")
            print("1. Display Session Info")
            print("2. Search for VMs")
            print("3. Edit Power State")
            print("4. Take/Revert Snapshot")
            print("5. Clone VM")
            print("6. Delete VM")
            print("7. Exit")
            
            choice = input("Enter your choice (1-7): ")

            if choice == '1':
                self.sessionInfo()
            elif choice == '2':
                self.vmInfo()
            elif choice == '3':
                self.powerChange()
            elif choice == '4':
                self.snapshotVM()
            elif choice == '5':
                self.fullClone()
            elif choice == '6':
                self.deleteVM()
            elif choice == '7':
                print("Goodbye!")
                if self.si is not None:
                    # Terminate the current session when exiting
                    exit
                break
            else:
                print("Invalid choice. Please enter a valid option (1-7).")


# Entry point of the script
if __name__ == "__main__":
    # Create an instance of VCenterConnection with the credential file
    vcenter = VCenterConnection("creds.txt")
    # Perform the login
    vcenter.login()
    # Display the main menu
    vcenter.display_menu()
