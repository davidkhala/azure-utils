[Availability](./hadr/ha.md)

- Availability sets
-

# VM

provision time: minutes

- you must maintain the VM on the installed OS and software.
- VM resources (dependency)
    - Size (purpose, number of processor cores, and amount of RAM)
    - Storage disks (hard disk drives, solid state drives, etc.)
    - Networking (virtual network, public IP address, and port configuration)

## cloud-init

using cloud-init for some Linux OSes.

## Run-Command

Limitation

- Output is limited to the last 4,096 bytes.
- The minimum time to run a script is about 20 seconds.
- Scripts run by default as an elevated user on Linux.
- You can run one script at a time. (no parallelism)
- The maximum time a script can run is 90 minutes.

## LVM (Not recommended)

> Normally don't recommend using LVM in the cloud as it increases the complexity without benefits.

LVM should be used only when it was imported from an on-prem VM.

- If you wish to expand the root LVM partition this is
  a [helpful guide](https://www.digitalocean.com/community/tutorials/how-to-use-lvm-to-manage-storage-devices-on-ubuntu-16-04)
- Oracle Linux image on azure has only LVM snapshot, with /boot volume size only 794M

# Azure Virtual Desktop (AVD)

A desktop and application virtualization service

- cloud-hosted version of Windows
- Exclusively offers **Windows (desktop) Enterprise multi-session**
- The tech foundation
  of [Windows 365](https://github.com/davidkhala/windows-utils/wiki/Windows-on-public-cloud#windows-365)
