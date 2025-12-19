# Cisco SDWAN



## Architecture

* Components of Cisco SDWAN and how they connects and functions with each other.



#### Manager (vManage)

* Management-Plane
* Can be a Virtual Device (VM), On-Prem or Cloud Installation
* It’s a single pane of glass for Day0, Day1 \& Day2 operations.
* It does:

  * Centralized Provisioning
  * Configure/Define Policies \& Templates
  * Troubleshooting \& Monitoring
  * Software Upgrades
  * Establishes DTLS tunnels with WAN Edges (not the OMP Tunnels)

* To push config (especially Policies) to WAN Edges, it uses NETCONF APIs over DTLS Tunnels.
* Validator is also configured via Manager. 💪



#### Validator (vBond)

* This device acts as an 'authenticator'. Think of it as a Gatekeeper (Bar Analogy).
* Orchestrates control \& management plane
* WAN Edges are pre-configured with Validator IPs. It exchanges certificates with WAN Edges. After successful authentication, shares the IPs of Manager \& Controller.
* Requires public IP reach-ability. Could sit behind 1:1 NAT.
* Highly resilient.
* Between Validator \& WAN Edge there is a dynamic DTLS tunnel, which goes down after successful authentication.
* Facilitates NAT-Traversal. Validator acts as a STUN Server: **S**ession **T**raversal **U**tilities for **N**AT



#### Controller (vSmart)

* Control Plane. Brain of the SD-WAN.
* Distributes control plane information to the WAN Edges using OMP tunnels. Also implements control plane policies such as service-chaining, multi-topology and multi-hop.
* Distributes data plane and app aware routing policies to the WAN Edges.
* All the policies are defined centrally on Manager and distributed to WAN Edges using Controller.
* Controller does not store policies locally, it only loads the currently active policy in its running-configuration.
* WAN Edges talks to Controller, but not with each other. It acts as a Route-Reflector and does not participate in Data-Plane, which means if you’re on WAN Edge #1, and look for a route from WAN Edge #2, next hop would be WAN Edge #2 and not Controller.



#### WAN Edge (vEdge)

* Data-Plane
* Communicates to Controller controllers using OMP to setup the Data Flow
* Each WAN Edge is uniquely identified by its Chassis ID and serial number
* Establishes permanent tunnels with Manager \& Controller, but dynamic tunnels with Validator.
* Tunnels to Controller are established via each available transport on WAN Edge.



#### Analytics (vAnalytics)

* An optional component of SD-WAN fabric and only available as a SaaS (same like O365).
* Offers insights into the performance of applications and the underlying SD-WAN network infrastructure. e.g., link utilization, performance, delay etc.
* Manager collects data from all WAN Edges and shares the raw data with Analytics, then it presents it in a better way.



### Misc.



#### VPN_0

* Transport VPN, can neither be deleted or modified
* The purpose is to enforce a separation between the WAN transport networks (the underlay) and network services (the overlay).
* Authentication traffic between Validator \& WAN Edges
* Template deployment traffic between Manager \& WAN Edges.



#### VPN_512

* Out of Band Management VPN (Management VRF)



#### Service VPN

* Where LAN is connected
* Ranges between 1 -to- 65530 (except 512, reserved for OOBM). Depending on hardware or license can support a limited number of service VPNs.
* E.g., Data users in VPN 10, Voice Users in VPN 11. It's a kind of segments in the VeloCloud world.



#### Transport Side

* Controllers or WAN Edges side (interfaces) connected to the underlay/WAN network. Always VPN0.
* Traffic typically tunneled / encrypted. In some special cases we need to specifically tell WAN Edges not to encrypt traffic but rather send it as native like in case of Direct Internet Access or split-tunnel.



#### Service Side

* WAN Edge interfaces facing LAN
* Traffic is forwarded as is from the original source



#### DTLS vs TLS

* Cisco SD WAN supports two Transport Layer Security protocols to provide end-to-end transport security
* DTLS uses UDP and implements its own sequence numbers, offers fragment and re-transmissions because UDP does not guarantee reliable delivery of packets. DTLS is default, because it’s faster compared to TLS.
* TLS uses TCP.
* Both are used between Manager, Controller \& Validator and they use protocol NETCONF for communication with each other.



#### Gateway Tracking

This feature that is enabled by default and can’t be stopped or modified. Each device probes using ARP the next-hop IP of each underlay static route every 10 seconds. If the device receives an ARP response, it maintains the static route in the VPN0’s routing table. If the device misses 10 consecutive ARP responses for a next-hop IP, the device removes the static route that points to this IP from the routing table.



#### NETCONF

Network management protocol to manage remote configurations. It works on the RPC layer (Remote Procedure Call) and uses XML or JSON for data encoding. Typically the protocol messages are exchanged over the TLS with mutual X.509 authentication.



#### Onboarding

Onboarding of the controllers, WAN edges needs below mandatory parameters

* System Config

  * Hostname
  * Organization Name
  * System IP (Like Router IP, not needed to be reachable, but to identify in the network)
  * Site ID
  * vBond IP or FQDN
  * Clock Time zone (Not mandatory, but important)



#### Certificates

* Root Certificate

  * Issued by the CA Server

* ID Certificate

  * Generate a CSR (Certificate Signing Request)
  * Request a certificate from the CA Server
  * CA Server will issue the ID Certificate
  * Download and Install in vManage


## Templates

* System Template
  * System-IP
  * Site-ID
  * Hostname
  * Timezone (Important but optional)
* Transport Template
  * VPN0
    * VPN ID = 0
    * Static Route
    * VPN Interfaces
      * Interface Name
      * IP address (Device Specific)
      * Tunnel Interface
    * Routing Protocols
      * OSPF
      * BGP
  * VPN512
    * VPN Interface
* Service Template
  * VPN ID = 1 -to- 65535 (Except 512)
  * VPN Interfaces
  * Routing Protocols
    * OSPF
    * BGP
    * EIGRP



### Feature Template
### Device Template



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


## Vanilla Config

```
config-transaction
  hostname <>
  clock timezone <>
  system
    system-ip <>
    site-id <#>
    sp-organization name <>
    organization-name <>
    vbond <>
!
interface <WAN Interface>
  ip address <> <>
  no shutdown
  exit
!
ip route 0.0.0.0 0.0.0.0 <Next-Hop-IP> or <WAN Interface>
!
interface Tunnel2
  ip unnumbered <WAN Interface>
  tunnel mode sdwan
  tunnel source <WAN Interface>
  no shutdown
  exit
!
sdwan
  interface <WAN Interface>
    tunnel-interface
    encapsulation ipsec
    allow-service netconf
    allow-service sshd
    exit
  exit
exit
!
commit
```
#### Commands

* `request platform software sdwan vedge activate chassis <Chassis Number> token <Token Number>`    ! To activate the vedge
* `request platform software sdwan root-cert-chain install bootflash:filename.extension`    ! To install certificate from the bootflash
* `show sdwan certificate serial`   ! Check Certificate and Serial Number
* 


