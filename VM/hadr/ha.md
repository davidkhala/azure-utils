# Live Migration
Live Migration is a virtual machine preserving operation that only pauses the virtual machine for a short time
- side effect: performance might be reduced before or after the event.
- for unplanned maintenance event

# heals
Azure platform automatically migrates (heals) your virtual machine to a healthy physical machine in the same datacenter. 
- side effect: During the healing procedure, virtual machines experience downtime (reboot) and in some cases loss of the temporary drive.
- for unexpected downtime


# Availability sets
- usecase
  - ensures that not all the machines are upgraded at the same time during a host operating system upgrade in the datacenter.
- spread across different **update domains** and **fault domains**
- **immutable**: A virtual machine can only be added to an availability set when the virtual machine is created.
- not for os or application-level failures
- Up to 20 update domains

load-balanced availability set
- powered by Azure Load Balancer


Update Domain
- **Tech stack**: logical group of VMs that are **upgraded together**
- Azure can reboot during maintenance one Update Domain at a time.
- update interval：30 minutes
  - Azure gives current update domain 30 minutes to recover and stabilize before beginning maintenance on the next update domain
  - grace period for service within VM
- immutable
  - In provision availability set, you can specify the # (default:5, up to 20) of update domains 
  - non-user-configurable: You cannot change the # of update domains of an existing availability set 

fault domain
- physical unit of failure
  - Think of a fault domain as nodes that belong to the **same physical rack**.
- By default, Azure splits your VMs across up to 3 fault domains
  