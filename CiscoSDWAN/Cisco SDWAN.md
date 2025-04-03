

#### Validator (vBond)

- This device acts as an 'authenticator'. Think of it as a Gatekeeper (Bar Analogy).
- Orchestrates control & management plane
- WAN Edges are pre-configured with Validator IPs. It exchanges certificates with WAN Edges. After successful authentication, shares the IPs of Manager & Controller.
- Requires public IP reach-ability. Could sit behind 1:1 NAT.
- Highly resilient.
- Between Validator & WAN Edge there is a dynamic DTLS tunnel, which goes down after successful authentication.
- Facilitates NAT-Traversal. Validator acts as a STUN Server: **S**ession **T**raversal **U**tilities for **N**AT

#### Manager (vManage)

- Management-Plane
- Can be a Virtual Device (VM), On-Prem or Cloud Installation
- It’s a single pane of glass for Day0, Day1 & Day2 operations.
- It does:
  - Centralized Provisioning
  - Policies & Templates
  - Troubleshooting & Monitoring
  - Software Upgrades
- It does not establish OMP tunnels with WAN Edges.
- To push config to WAN Edges, it uses NETCONF APIs over DTLS Tunnels.
- Validator is also configured via Manager. 💪

#### Analytics (vAnalytics)

- An optional component of SD-WAN fabric and only available as a SAAS (same like O365).
- Offers insights into the performance of applications and the underlying SD-WAN network infrastructure. e.g., link utilization, performance, delay etc.
- Manager collects data from all WAN Edges and shares the raw data with Analytics, then it presents it in a better way.

#### Controller (vSmart)

- Control Plane. Brain of the SD-WAN.
- Distributes control plane information to the WAN Edges using OMP. Also implements control plane policies such as service-chaining, multi-topology and multi-hop.
- Distributes data plane and app aware routing policies to the WAN Edges.
- All the policies are defined centrally on Manager and distributed to WAN Edges using Controller.
- Controller does not store policies locally, it only loads the currently active policy in its running-configuration.
- WAN Edges talks to Controller, but not with each other. It acts as a Route-Reflector and does not participate in Data-Plane, which means if you’re on WAN Edge #1, and look for a route from WAN Edge #2, next hop would be WAN Edge #2 and not Controller.

#### WAN Edge (vEdge)

- Data-Plane
- Communicates to Controller controllers using OMP to setup the Data Flow
- Each WAN Edge is uniquely identified by its Chassis ID and serial number
- Establishes permanent tunnels with Manager & Controller, but dynamic tunnels with Validator.
- Tunnels to Controller are established via each available transport on WAN Edge.

## Misc.

#### VPN_0

- Transport VPN, can neither be deleted or modified
- The purpose is to enforce a separation between the WAN transport networks (the underlay) and network services (the overlay).
- Authentication traffic between Validator & WAN Edges
- Template deployment traffic between Manager & WAN Edges.

#### VPN_512: Out of Band Mgmt VPN (Mgmt VRF)

#### Service VPN

- Where LAN is connected
- Ranges between 1 -to- 65530 (except 512, reserved for OOBM). Depending on hardware or license can support a limited number of service VPNs.
- E.g., Data users in VPN 10, Voice Users in VPN 11. It's a kind of segments in the VeloCloud world.

#### Transport Side

- Controllers or WAN Edges side (interfaces) connected to the underlay/WAN network. Always VPN0.
- Traffic typically tunneled / encrypted. In some special cases we need to specifically tell WAN Edges not to encrypt traffic but rather send it as native like in case of Direct Internet Access or split-tunnel.

#### Service Side

- WAN Edge interfaces facing LAN
- Traffic is forwarded as is from the original source

#### DTLS vs TLS

- Cisco SD WAN supports two Transport Layer Security protocols to provide end-to-end transport security
- DTLS uses UDP and implements its own sequence numbers, fragment offers and re-transmissions because UDP does not guarantee reliable delivery of packets. DTLS is default, because it’s faster compared to TLS.
- TLS uses TCP.
- Both are used between Manager, Controller & Validator and they use protocol NETCONF for communication with each other.

#### Gateway Tracking

This feature that is enabled by default and can’t be stopped or modified. Each device probes using ARP the next-hop IP of each underlay static route every 10 seconds. If the device receives an ARP response, it maintains the static route in the VPN0’s routing table. If the device misses ten consecutive ARP responses for a next-hop IP, the device removes the static route that points to this IP from the routing table.

#### NETCONF

Network management protocol to manage remote configurations. It works on the RPC layer (Remote Procedure Call) and uses XML or JSON for data encoding. Typically the protocol messages are exchanged over the TLS with mutual X.509 authentication.






