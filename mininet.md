# SDN Project Documentation: Handling Link Failures with Mininet

## 🔍 Project Goal

The goal of this project is to simulate a network using Mininet and the POX controller to demonstrate how a Software-Defined Network (SDN) can automatically recover from link failures. This showcases SDN's resilience and intelligent traffic control capabilities.

---

## 🌐 How the Project Works

### ✅ Network Setup

Mininet is used to create a virtual topology with interconnected virtual switches and hosts, providing a controlled environment for network simulation.

### ✅ POX Controller Logic

The POX controller (Python-based) handles core logic:

* *Topology Discovery:* It processes OpenFlow messages to dynamically build a real-time map of network devices and links.
* *Link Failure Detection:* Detects when links go down through OpenFlow events.
* *Shortest Path Calculation:* Uses Dijkstra's algorithm to calculate a new path between affected nodes.
* *Flow Rule Updates:* Installs new flow rules along the computed path to re-establish connectivity.

### ✅ Link Failure Simulation

Link failures can be manually triggered in Mininet CLI using:

bash
link s1 s3 down


To restore the link:

bash
link s1 s3 up


---

## 🚀 Setting Everything Up

### ✅ Environment Preparation

* *Mininet VM:* Use a virtual machine with POX pre-installed.
* *Verify POX:*

bash
cd ~/pox


### ✅ Project Files

Two essential Python scripts:

* create_topology.py: Defines the network topology.
* dijkstra.py: Contains logic for topology discovery, link failure handling, and rerouting via Dijkstra's algorithm.

*Place these in:*


/home/mininet/pox/ext/


Use scp or copy directly within the VM.

### 🖊 Topology Code (create\_topology.py)

python
# Add your topology creation code here



### 🖊 Controller Code (dijkstra.py)

python
# Add your controller logic implementing Dijkstra's algorithm here



### ✅ Starting POX Controller

Open Terminal 1:

bash
cd ~/pox
./pox.py openflow.discovery dijkstra


### ✅ Creating the Network

Open Terminal 2:

bash
sudo python /home/mininet/pox/ext/create_topology.py


### ✅ Testing Link Failures

From Mininet CLI:

bash
link s1 s3 down
link s1 s3 up


Check the POX terminal for rerouting logs.

### ✅ Testing Host Connectivity

From Mininet CLI:

bash
h1 ping h2


Run before and after a link failure to observe behavior.

### ✅ Cleanup

Exit with:

bash
sudo mn -c


---

## 📊 Expected Behavior

* *Before Failure:* Full connectivity with successful pings.
* *After Failure:* Temporary packet loss, then restored connectivity after rerouting.
* *Controller Output:* Logs showing detection, rerouting decisions, and flow rule installations.

---

## ⚖ Dijkstra's Algorithm in SDN

* *Nodes:* Switches in the topology.
* *Edges:* Links with weights (e.g., 1 per hop).

When a link fails, the updated topology is used to compute a new shortest path. The controller installs new flow rules based on this path, ensuring traffic reroutes successfully.

---

## ✨ Future Improvements

1. *Enhanced Logging:* Show original vs. new path, failed links, and rule installation details.
2. *Visualization:* Integrate with Ryu GUI or mn --gui for graphical insight.
3. *Packet Analysis:* Use Wireshark to analyze OpenFlow traffic for deeper understanding.

---

End of Documentation
