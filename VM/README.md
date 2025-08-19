
# VM
provision time: minutes
- you must maintain the VM on the installed OS and software.
- VM resources (dependency)
  - Size (purpose, number of processor cores, and amount of RAM)
  - Storage disks (hard disk drives, solid state drives, etc.)
  - Networking (virtual network, public IP address, and port configuration)

# Virtual machine scale sets
a group of identical, load-balanced VMs
- demand to complete time: minutes
- it comes with a load balancer

# Virtual machine availability sets
- spread across different **update domains** and **fault domains**

Update Domain
- logical group of VMs
- stagger updates分批更新:Azure can reboot during maintenance one Update Domain at a time.
- update interval：30 minutes
  - Azure gives current update domain 30 minutes to recover and stabilize before beginning maintenance on the next update domain
  - grace period for service witinin VM

fault domain
- physical group of VMs like Availability Zone
- By default, Azure splits your VMs across up to 3 fault domains


# Azure Virtual Desktop (AVD)
A desktop and application virtualization service
- cloud-hosted version of Windows
- Exclusively offers **Windows (desktop) Enterprise multi-session**
- The tech foundation of [Windows 365](https://github.com/davidkhala/windows-utils/wiki/Windows-on-public-cloud#windows-365)
