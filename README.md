# Setting Up Mininet for SDN Link Failure Recovery Simulation

## What You Need Before Starting

* Windows computer
* VirtualBox or VMware installed
* Ubuntu 20.04 (or a pre-configured Mininet VM image)
* SSH client on your Windows machine to connect to the VM (you'll need the VM's IP address and potentially port forwarding configured)

## Getting Mininet Running

### Using a Pre-made Mininet VM (Recommended)

1.  **Download the Mininet VM Image:**
    * Obtain the latest Mininet VM image from the official GitHub wiki: [https://github.com/mininet/mininet/wiki/Mininet-VM-Images](https://github.com/mininet/mininet/wiki/Mininet-VM-Images)

2.  **Import the VM into VirtualBox/VMware:**
    * Open your virtualization software and use the "Import Appliance" or similar option to import the downloaded `.ova` file.

3.  **Allocate Sufficient Resources:**
    * Ensure the virtual machine is allocated adequate RAM and CPU cores for optimal performance. Running Mininet simulations can be resource-intensive.

4.  **Configure Network Settings:**
    * Choose one of the following network configurations for your VM:
        * **Bridged Adapter:** This is often preferred as it allows the VM to get its own IP address directly from your local network's DHCP server, making SSH access straightforward.
        * **NAT with Port Forwarding:** If you choose NAT, you'll need to set up a port forwarding rule in your VM settings. For example, you can forward traffic from your host machine's port `2223` to the guest VM's SSH port `22`.

5.  **Boot Up the VM and Log In:**
    * Start the Mininet virtual machine.
    * Use the default login credentials:
        * **Username:** `mininet`
        * **Password:** `mininet`

6.  **Connect via SSH from Windows:**
    * Open Command Prompt on your Windows computer.
    * If you used Bridged Adapter, find the IP address of your VM (using `ip a` or `ifconfig` within the VM) and use that in the `ssh` command.
    * If you used NAT with port forwarding, use `127.0.0.1` as the IP address and the forwarded port (`2223` in the example):
        ```bash
        ssh mininet@127.0.0.1 -p 2223
        ```

### First Steps After Installing

1.  **Update System Packages:**
    * Once you are logged into the Mininet VM via SSH, update the package lists and upgrade the installed packages:
        ```bash
        sudo apt update && sudo apt upgrade -y
        ```

2.  **Test Mininet Installation:**
    * Verify that Mininet is working correctly by running a basic test:
        ```bash
        sudo mn --test pingall
        ```
        This command creates a simple Mininet topology and tests connectivity between all the virtual hosts by sending ping packets.

## My SDN Project: Handling Link Failures with Mininet

### Project Goal

I am creating a network simulation using Mininet and the POX controller to demonstrate how a Software-Defined Network (SDN) can automatically recover from link failures by finding and implementing new traffic paths. This highlights the resilience and intelligent control capabilities of SDN.

### How My Project Works

1.  **Network Setup:** I utilize Mininet to define and create a virtual network topology consisting of interconnected virtual switches and hosts. This provides a controllable environment for simulating network behavior.

2.  **Controller Logic (POX Controller):** The POX controller, a Python-based SDN controller, plays a crucial role in this project:
    * **Topology Discovery:** It actively discovers the network topology by processing OpenFlow messages from the switches, building a real-time map of the network's devices and connections.
    * **Link Failure Detection:** The controller monitors the state of the links between switches. When a link goes down (either physically simulated or through OpenFlow events), the controller is notified.
    * **Shortest Path Calculation (Dijkstra's Algorithm):** Upon detecting a link failure, the controller employs Dijkstra's shortest path algorithm. This algorithm analyzes the current network topology to compute the most efficient alternative path between the affected source and destination switches.
    * **Flow Rule Updates:** Once a new shortest path is determined, the controller communicates with the OpenFlow switches along this path, installing new flow rules. These rules instruct the switches on how to forward traffic to ensure it follows the newly calculated route, thus restoring connectivity.

3.  **Simulating a Link Break:** Using the Mininet CLI, I can manually simulate a link failure between two switches. This allows me to observe the controller's reaction and the subsequent rerouting of traffic.

### Setting Everything Up

1.  **Environment Preparation:**
    * I am using a Mininet virtual machine environment where the POX controller is already installed.
    * **✅ Verify POX Installation:** You can check if the POX directory exists in the `mininet` user's home directory:
        ```bash
        cd ~/pox
        ```

2.  **Project Files:**
    * I have two key Python scripts for this project:
        * `create_topology.py`: This script defines the specific network topology (number of switches, hosts, and their interconnections) that will be created in Mininet.
        * `dijkstra.py`: This POX module contains the Python code implementing the logic for network topology discovery, link failure detection, and the Dijkstra's shortest path algorithm. It also handles the installation of new flow rules on the switches.
    * **✅ Place Project Files:** These two Python files need to be placed in the POX extensions directory:
        ```
        /home/mininet/pox/ext/
        ```
        You can use `scp` to transfer these files from your host machine to the VM or copy and paste them directly within the VM.

3.  **Starting the POX Controller:**
    * Open one terminal window in your Mininet VM and navigate to the POX directory:
        ```bash
        cd ~/pox
        ```
    * Start the POX controller, specifying the `openflow.discovery` module (for automatic topology discovery) and your custom `dijkstra` module:
        ```bash
        ./pox.py openflow.discovery dijkstra
        ```
        This command will launch the POX controller and load the necessary modules, making it ready to interact with the Mininet network.

4.  **Creating the Network:**
    * Open a second terminal window in your Mininet VM and execute the `create_topology.py` script with `sudo` to have the necessary permissions to create network interfaces:
        ```bash
        sudo python /home/mininet/pox/ext/create_topology.py
        ```
        This script will use the Mininet Python API to build the virtual network topology you have defined. Once executed, the Mininet CLI will appear.

5.  **Testing Link Failures:**
    * In the Mininet CLI, you can simulate a link failure between two switches using the `link` command. For example, to simulate a failure between switch `s1` and switch `s3`:
        ```mininet
        link s1 s3 down
        ```
    * To restore the link to its operational state, use the `up` option:
        ```mininet
        link s1 s3 up
        ```
    * Observe the output in the POX controller terminal when you bring a link down and back up. Your `dijkstra.py` module should be logging information about the detected failure and the rerouting process.

6.  **Testing Connections:**
    * Within the Mininet CLI, you can test the end-to-end connectivity between hosts using the `ping` command. For example, to send ping packets from host `h1` to host `h2`:
        ```mininet
        h1 ping h2
        ```
    * Run this command before and after simulating a link failure. You should see that while the controller is in the process of rerouting, some ping packets might be lost. However, once the new paths are established, the ping should resume successfully.

7.  **Cleaning Up:**
    * When you have finished your experiments, you can clean up the Mininet environment by running the following command in the Mininet CLI:
        ```mininet
        sudo mn -c
        ```
        This command removes all the virtual interfaces and processes created by Mininet, ensuring a clean state for future simulations.

### What Should Happen

* **Before Breaking Links:** Initially, when you ping between any two hosts in your Mininet network, all ping packets should be successfully transmitted and received, indicating full connectivity.
* **Right After a Link Breaks:** Immediately after you simulate a link failure using the `link down` command, you might observe a temporary disruption in connectivity. Some ping packets might be lost while the POX controller detects the failure and calculates the new shortest path.
* **After the Controller Adjusts:** Once the POX controller has executed Dijkstra's algorithm and pushed the new flow rules to the relevant switches along the alternative path, the connectivity between the hosts should be restored. Subsequent ping commands should be successful, demonstrating that the traffic is now being routed through the new path.
* **Controller Output:** The terminal where the POX controller is running should display informative messages about the link failure being detected, the Dijkstra's algorithm being executed to find a new path, and the flow rules being installed on the switches to implement this new path. These logs are crucial for understanding the controller's actions and verifying the success of the link failure recovery mechanism.

### How Dijkstra's Algorithm Helps

In this SDN project, the POX controller uses Dijkstra's algorithm to intelligently determine the best way to reroute traffic after a link failure. The controller views the network as a graph:

* **Switches as Nodes:** Each switch in the Mininet topology is represented as a node in the graph.
* **Links as Edges:** The connections (links) between the switches are represented as edges in the graph. For simplicity, each link can be assigned a weight of 1, representing a single hop.

When a link in the physical Mininet topology fails, this is reflected as a change in the graph representation within the POX controller. Dijkstra's algorithm then computes the shortest path (in terms of the number of hops or based on other defined metrics) between the source switch and the destination switch, taking into account the updated graph (i.e., the network without the failed link).

Once the shortest path is identified, the POX controller translates this path into a series of flow rules. These rules are then sent to each OpenFlow switch along the newly calculated path. The flow rules instruct the switches on how to forward incoming traffic destined for a particular host or network segment, ensuring that the traffic now flows along the newly determined optimal route, bypassing the failed link and maintaining network connectivity.

### Future Improvements

* **Detailed Logging:** Enhance the `dijkstra.py` module to include more detailed logging of the path computation process, including the original path, the failed link, the newly computed path, and the specific flow rules installed on each switch. This will provide better insights into the controller's decision-making process.
* **Network Topology Visualization:** Integrate a visualization tool (such as the Ryu Network GUI or Mininet's built-in capabilities with `mn --gui`) to provide a graphical representation of the network topology. This would allow for a more intuitive understanding of how the paths change in response to link failures.
* **Packet Analysis with Wireshark:** Utilize Wireshark on the virtual interfaces created by Mininet to capture and analyze the OpenFlow packets exchanged between the POX controller and the switches. This would provide a low-level view of the flow rule modifications and the controller's communication with the network devices.
