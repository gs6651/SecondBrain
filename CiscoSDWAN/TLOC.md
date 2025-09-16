
# CiscoSDWAN

## TLOCs

- Transport Locator. Data-Plane attachment point
- Collection of entities making up a transport side connection. Think of it as a identity card given to WAN interfaces, it uniquely identifies with tuple of three values:
  - *System-IP:* It’s similar to router-ID and does not need to be route-able or reachable across the fabric
  - *Transport Color:* Interface identifier on local WAN Edge. One color for MPLS and other one for Internet etc.
  - *Encapsulation:* The type of encapsulation this TLOC uses - IPsec or GRE.
- Transport interfaces (ones with TLOC configuration) do not forward traffic. They only serve as tunnel endpoints for the overlay tunnels
- TLOC Restrict: To restrict tunnels within same color
- TLOC Carrier: Between two clouds
- Tunnel Group:
  - Only one interface can be marked with a particular color per WAN edge router. That's a limitation of color, and Tunnel Group comes into picture.
  - TLOCs can only establish tunnels with remote TLOCs with the same tunnel-group IDs irrespective of the TLOC color.
  - TLOCs with any tunnel-group ID will also form tunnels with TLOCs that have no tunnel-group IDs assigned.
  - If the restrict-option is configured in conjunction with the tunnel-group option, then TLOCs will only form an overlay tunnel to remote TLOCs having the same tunnel-group ID and TLOC color.
- NAT Detection
- All Cisco SD-WAN devices have an embedded STUN client and the Validator orchestrator acts as a STUN Server (Session Traversal Utilities for NAT).

### NAT Types

- **Full-Cone NAT:** A full-cone is one where all packets from the same internal IP address are mapped to the same NAT IP address. External hosts can send packets to the internal host, by sending packets to the mapped NAT IP address. In other words, One-to-One NAT.
- **Restricted-Cone NAT:** Same as Full-Cone NAT, only difference is that an external host can send packets to the internal host only if the internal host had previously sent a packet to that IP address. Once the NAT mapping state is created, the external destination can communicate back to the internal host on any port. It is also known as Address-Restricted-Cone.
- **Port-Restricted-Cone NAT:** Same as Restricted-Cone NAT, but the restriction also includes port numbers. The difference is that an external destination can send back packets to the internal host only if the internal host had previously sent a packet to this destination on this exact port number. It is known as Port Address Translation (PAT).
- **Symmetric:** In this NAT, all requests from the same internal IP & port to a specific destination IP & port, are mapped to a unique NAT IP & and NAT port. Only the external destination that received a packet can send packets back to the internal host. It is the most restrictive of all other types. It is also known as Port Address Translation (PAT) with port-randomization.
- Recommendation is to have Full-Cone NAT at the Hubs, DC, DR sites.
- In GRE tunnels, any type of NAT with port overloading is not supported since GRE packets lack an L4 header.

**Loopback TLOC:** When loopback interface is used as local TLOC endpoint.

- Standard Mode: Loopback interface bound to multiple physical interfaces. The service provider network must have IP reach-ability to the loopback IP. Tunnel config would be done under loopback instead of physical interface.
- Bind Mode: Loopback interface is strictly bound to a single physical link. Used when the last mile provider assigns an IP address to the WAN link, and this IP is filtered within the MPLS cloud or in another transit WAN along the way. Command is:  `bind <interface>`.
