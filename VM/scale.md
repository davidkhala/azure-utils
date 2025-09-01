
Configure on a target VM (in **Availability+Scale** menu group)
- **Size**: change VM Size. For vertical scale
- **Availability + scaling**: 

# Azure Virtual Machines Scale Sets (VMSS)
a group of identical, load-balanced VMs
- demand to complete time: minutes
- it comes with a load balancer for basic layer-4 traffic distribution
  - advanced: use Azure Application Gateway for layer-7 traffic distribution and TLS/SSL termination.
- can be deployed into 1+ availability zones or regionally
- up to 1000 VMs
   - limited to 600, for your own custom virtual machine images (solution: Shared Image Gallery)
- (magic) automatically upgrade to the latest OS version 
## provision
- [Orchestration mode](https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-orchestration-modes)
  - **Flexible**(recommended): manually create and add a virtual machine of any configuration to the scale set
    - aka. VMSS Flex
    - dynamic instance mixing: enabling the use of different VM type (combination of Spot and on-demand instances)
    - support all key features
      - For B/D/E/F series, support memory preserving updates and live migration
    - No update domains: maintenance or host updates are done fault domain by fault domain
  - **Uniform**: define a virtual machine model and Azure generates identical instances based on that model
    - Individual instances are are scale set **child virtual machines**
      - accessible via scale set VM API
      - not compatible with standard Azure IaaS VM API (e.g. ARM tagging, RBAC, Azure Backup, or Azure Site Recovery.) 
    - partial key features: metrics-based autoscaling, instance protection, and automatic OS upgrades.
    - up to 5 update domains  
- Spreading algorithm: how VMs in the scale set are balanced across fault domains
  - max spreading(recommended): VMs are spread across as many fault domains as possible in each zone.
  - fixed spreading: VMs are always spread across exactly 5 fault domains.
    - In the case where <5 fault domains are available, a scale set using "Fixed spreading" fails
  



# Compute Fleet
- up to 10000 VMs
- no auto scale
- no prebuilt load balancer
- usecase: HPC

# Azure Compute Gallery
- aka. Shared Image Gallery
- 解决了传统 custom image 在扩展性和分发上的瓶颈
  - geo-dist by Replication 