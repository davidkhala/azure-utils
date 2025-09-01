# Route tables

Azure automatically creates a route table for **each subnet** on an vNet and adds system default routes to the table. 
 
- Azure routes **outbound traffic** from a subnet based on the routes on a subnet's route table.



## user defined route (UDR)
> You can override some of the Azure system routes with UDR and add more custom routes to route tables.
- is static route 

fields
- **Next hop type**: handles the matching packets for this route
  - **virtual network**:
  - **virtual network gateway**
    - IPv4 only: Virtual network gateways can't be used if the address prefix is IPv6. 
  - **Internet**
  - **virtual appliance**
    - **Next hop address** configuration required: The IP address of the next hop
  - **None**
- **Destination address prefix type (Destination type)** 
  - **IP addresses**
  - **Service Tag**: predefined identifiers that represent a category of IP addresses.
   