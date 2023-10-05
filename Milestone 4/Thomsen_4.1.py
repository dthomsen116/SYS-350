# Import necessary modules
import getpass, warnings, ssl
from pyVim.connect import SmartConnect
from pyVmomi import vim
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
        print("\nSession Info\n")
        print("-----------------------------------------------------------------")
        print("Session Key: " + p.key)
        print("Session User Agent: " + p.userAgent)
        print("Session User/Domain: " + p.userName)
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
                    print("Name: " + vm.name)
                    print("Power State: " + vm.runtime.powerState)
                    print("Number of CPUs: " + str(vm.config.hardware.numCPU))
                    print("Memory in GB: " + str(vm.config.hardware.memoryMB / 1024))
                    print()
                    
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

    # Function to display the main menu
    def display_menu(self):
        while True:
            print("\nMenu:")
            print("1. Display Session Info")
            print("2. Search for VMs")
            print("7. Exit")
            
            choice = input("Enter your choice (1-7): ")

            if choice == '1':
                self.sessionInfo()
            elif choice == '2':
                self.vmInfo()
            elif choice == '7':
                print("Goodbye!")
                if self.si is not None:
                    # Terminate the current session when exiting
                    self.si.content.sessionManager.TerminateSession(self.si.content.sessionManager.currentSession.key)
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
