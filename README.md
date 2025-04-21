# Mininet Installation and Initial Configuration on a Virtual Machine

## Prerequisites

* **Host Operating System:** Windows
* **Virtual Machine Software:** VirtualBox / VMware
* **Virtual Machine Operating System:** Ubuntu 20.04 (or Mininet VM image)
* **Access:** SSH access to the Mininet virtual machine via a configured port (e.g., 2223)

## 1. Step-by-Step Installation Guide

### Option A: Using the Mininet VM Image (Recommended)

1.  **Download the Mininet VM Image:**
    * Obtain the pre-built Mininet virtual machine image from the official Mininet wiki: [https://github.com/mininet/mininet/wiki/Mininet-VM-Images](https://github.com/mininet/mininet/wiki/Mininet-VM-Images)

2.  **Import the VM Image:**
    * In your chosen virtualization software (VirtualBox or VMware), use the "Import Appliance" or similar function to import the downloaded `.ova` file.

3.  **Allocate Sufficient Resources:**
    * During the import process or in the VM settings, ensure that the virtual machine is allocated adequate RAM, CPU cores, and disk space for smooth operation.

4.  **Configure Network Settings:**
    * For network connectivity, configure the network adapter of the virtual machine to use either:
        * **Bridged Adapter:** This allows the VM to obtain an IP address from your host network's DHCP server and communicate directly with other devices on your local network.
        * **NAT with Port Forwarding:** This uses your host machine's IP address, and you'll need to set up port forwarding rules to allow SSH access to the Mininet VM. For example:
            ```yaml
            Host Port: 2223
            Guest Port: 22
            ```

5.  **Start the Virtual Machine:**
    * Power on the Mininet virtual machine.

6.  **Log In to the VM:**
    * Use the default login credentials:
        * **Username:** `mininet`
        * **Password:** `mininet`

7.  **Access via SSH from Windows Command Prompt:**
    * Open the Command Prompt on your Windows host and use the `ssh` command with the configured port (if using NAT with port forwarding):
        ```bash
        ssh mininet@127.0.0.1 -p 2223
        ```

## 2. Initial Configuration

### Update and Upgrade Packages

* Once logged into the Mininet VM via SSH, it's good practice to update the package lists and upgrade the installed packages to their latest versions:
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

### Test Mininet Installation

* To verify that Mininet is installed correctly and functioning, run the basic connectivity test:
    ```bash
    sudo mn --test pingall
    ```
    This command creates a default Mininet topology, pings all the simulated network nodes, and reports the connectivity results.
