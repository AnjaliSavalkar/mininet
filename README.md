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







# Link Failure Recovery in SDN with Mininet and POX Controller

## 🧠 Project Goal:

To simulate a network where, when a link fails, the controller automatically reroutes the traffic using Dijkstra’s shortest path algorithm. This demonstrates a key SDN feature – dynamic recovery and intelligent routing.

## 🔩 How It Works (Conceptual Flow)

1.  **Mininet Topology:** Mininet creates the virtual network topology consisting of virtual switches and hosts.
2.  **POX Controller:** A POX controller runs a Python module that performs the following:
    * **Topology Discovery:** Discovers the network topology (switches and links).
    * **Link Failure Detection:** Listens for events indicating link failures in the network.
    * **Path Computation:** Computes a new shortest path between source and destination switches using Dijkstra's algorithm when a link failure occurs.
    * **Flow Rule Updates:** Updates the flow tables of the switches along the new path to redirect traffic.
3.  **Simulating Failure:** When a link in the Mininet topology is intentionally brought down, the POX controller detects this change.
4.  **Rerouting:** Upon detecting a link failure, the POX controller recalculates the optimal path and pushes new flow rules to the relevant switches, ensuring traffic continues to flow through the network via the new path.

## ⚙️ Step-by-Step Setup Instructions

### 🛠️ 1. Setup the Environment

* Use a Mininet Virtual Machine (preferably Ubuntu with Mininet pre-installed).
* **Recommended:** Mininet version 2.2.2, with the POX controller already present in the VM.
* **✅ Verify POX Location:**
    ```bash
    cd ~/pox
    ```

### 📁 2. Add the Project Files

* You should have two Python files:
    * `create_topology.py`: This script will define and build the Mininet network topology.
    * `dijkstra.py`: This POX module will contain the logic for discovering the topology, handling link failures, and computing shortest paths using Dijkstra's algorithm.
* **✅ Place the files in the POX extensions directory:**
    ```
    /home/mininet/pox/ext/
    ```
    You can use `scp` to transfer the files from your host machine to the VM or directly copy-paste within the virtual machine environment.

### 🧠 3. Start the POX Controller

* Open a terminal in your Mininet VM and navigate to the POX directory:
    ```bash
    cd ~/pox
    ```
* Run the POX controller with the necessary modules:
    ```bash
    ./pox.py openflow.discovery dijkstra
    ```
    * `openflow.discovery`: This is a built-in POX module that automatically discovers the network topology by listening to OpenFlow messages from the switches.
    * `dijkstra`: This is your custom module (`dijkstra.py`) that contains the logic for handling link failures and implementing the Dijkstra's shortest path algorithm. The POX controller will load and execute this module.

### 🌐 4. Run the Topology Script

* Open another terminal in your Mininet VM and execute the topology creation script:
    ```bash
    sudo python /home/mininet/pox/ext/create_topology.py
    ```
    This script will use the Mininet API to create a virtual network with switches and hosts, and it will connect them in a topology that allows for multiple paths between hosts. This is crucial for demonstrating the rerouting capability.

### 🔧 5. Simulate Link Failure

* Once the Mininet CLI is running (after executing `create_topology.py`), you can simulate a link failure using the `link` command. For example, to bring down the link between switch `s1` and switch `s3`:
    ```mininet
    link s1 s3 down
    ```
* To restore the link, use the `up` option:
    ```mininet
    link s1 s3 up
    ```
* The POX controller (running in the other terminal) should detect the `link down` event and automatically recompute the shortest paths based on the updated topology. When the link is brought `up`, the controller might revert to the original or another optimal path.

### 📶 6. Test Connectivity

* Within the Mininet CLI, you can test the connectivity between hosts using the `ping` command. For example, to ping from host `h1` to host `h2`:
    ```mininet
    h1 ping h2
    ```
* Try pinging between hosts *before* and *after* simulating a link failure. You should observe that the ping might fail for a brief period immediately after the link goes down while the controller calculates and installs the new routes. After the rerouting is complete, the ping should resume successfully.

### 🧹 7. Cleanup

* When you are finished experimenting, you can clean up the Mininet environment by running:
    ```bash
    sudo mn -c
    ```
    This command removes any leftover virtual interfaces and processes created by Mininet.

## ✅ Expected Output

* **Normal Operation:** Pinging between hosts should be successful before any link failures are introduced.
* **Link Failure Scenario:** When a link fails, you might see a few ping packets drop as the controller reacts to the topology change. Subsequently, the controller should have computed a new path and updated the switch flow tables, allowing the ping to succeed again.
* **Controller Logs:** The terminal where the POX controller is running should display logs indicating the detection of the link failure, the execution of Dijkstra's algorithm, and the installation of new flow rules on the switches.

## 📘 Extra Notes

### What is Dijkstra's Algorithm Doing Here?

* The POX controller views the network topology as a graph where:
    * **Nodes:** Represent the switches in the network.
    * **Edges:** Represent the links between the switches. The "weight" of these edges can be considered as 1 (or any other metric you define).
* When a link failure occurs, the topology of this graph changes. Dijkstra's algorithm is used to find the shortest path (in terms of the number of hops or based on a defined cost metric) between the source switch and the destination switch, considering the new topology.
* Once the shortest path is computed, the POX controller translates this path into a series of flow rules that are pushed to the OpenFlow switches along the path. These flow rules instruct the switches on how to forward traffic to ensure it follows the newly calculated optimal route.

### 🧪 Optional Enhancements:

* **Logging:** Modify the `dijkstra.py` module to log the computed paths and the flow rules installed on the switches to a file for better analysis.
* **Visualization:** Explore tools like the Ryu Network GUI or the Mininet-WiFi GUI to visualize the network topology and observe the changes in paths in real-time during link failures.
* **Packet Analysis:** Use Wireshark on the virtual interfaces created by Mininet to capture and analyze the OpenFlow packets exchanged between the controller and the switches, allowing you to see the flow rule updates.
