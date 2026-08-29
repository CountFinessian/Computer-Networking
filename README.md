# Computer Networking — Full Internet Stack Implementation

A from-scratch implementation of the Internet protocol stack, built layer by
layer on raw Ethernet frames and tested in [Cougarnet](https://github.com/cdeccio/cougarnet),
a Linux-network-namespace-based network emulator that creates virtual hosts,
switches, and routers connected by virtual links.

Rather than relying on the OS socket API or existing packet libraries, this
project implements each layer of the stack directly — parsing and
constructing headers byte-by-byte, managing TCP connection state, and
building a working IP forwarding table and distance-vector routing protocol.

## What's implemented

### Link layer
- **Switch** (`switch.py`) — a Layer 2 switch that receives and forwards raw
  Ethernet frames between hosts
- **ARP** (`host.py`) — request/reply handling for IP-to-MAC address
  resolution, frame demultiplexing by EtherType (IP vs. ARP)

### Network layer
- **IP forwarding** (`host.py`) — packet handling, TTL decrement, and
  forwarding between interfaces
- **Forwarding table** (`forwarding_table.py`) — longest-prefix-match IP
  routing using a custom `Prefix` class for CIDR matching, the same core
  logic a router's FIB (forwarding information base) uses

### Routing protocol
- **Distance-vector routing** (`dvrouter.py`) — routers periodically
  exchange reachability information with neighbors over UDP and update
  their own routing tables based on what neighbors report (a simplified
  RIP-style protocol)

### Transport layer
- **Header parsing** (`headers.py`) — manual byte-level packing/unpacking of
  IPv4, UDP, and TCP headers using `struct`
- **TCP state machine** (`mysocket.py`) — full connection lifecycle
  (`LISTEN`, `SYN_SENT`, `SYN_RECEIVED`, `ESTABLISHED`, `FIN_WAIT_1/2`,
  `CLOSE_WAIT`, `CLOSING`, `LAST_ACK`, `TIME_WAIT`, `CLOSED`), three-way
  handshake logic, congestion window (`cwnd`) and slow-start threshold
  (`ssthresh`) tracking, retransmission timers via `asyncio`, and optional
  fast retransmit
- **Buffering** (`buffer.py`) — `TCPSendBuffer` and `TCPReceiveBuffer`
  handle sequence-number tracking, sliding-window buffering, and
  out-of-order data reassembly

### Application layer
- **Echo server** (`echoservertcp.py`) — a simple TCP application built on
  top of the custom socket implementation, demonstrating the full stack
  working end-to-end

### Testing
- **Automated grader** (`test.py`) — parses live packet-capture logs against
  expected patterns to verify handshake and data-transfer behavior (correct
  SYN/SYN-ACK/ACK sequencing, flags, and payloads) across simulated
  scenarios

## Stack summary

| Layer | Concepts covered |
|---|---|
| Link | Ethernet framing, ARP resolution, switching |
| Network | IP forwarding, longest-prefix matching, TTL handling |
| Routing | Distance-vector algorithm, neighbor discovery, table convergence |
| Transport | TCP handshake, reliable delivery, sliding window, congestion control, UDP |
| Application | Socket-based echo service |

## Running

Each lab/homework directory contains a self-contained scenario, typically
run with a Cougarnet config file:

```bash
cougarnet --disable-ipv6 --terminal=none scenario.cfg
```

Test scenarios can be run and graded with:

```bash
python3 test.py
```

## Why this project

This was built as coursework for a computer networking course, with the
explicit goal of understanding what happens *inside* the stack that
`socket.connect()` normally hides — reliable delivery, congestion control,
routing convergence, and address resolution — by implementing it directly
rather than relying on existing libraries.

<img width="323" height="145" alt="Type_BUG_found" src="https://github.com/user-attachments/assets/5ed74120-2bbe-4769-b67d-dba442f4dd82" />
<img width="319" height="216" alt="Screenshot 2025-09-19 162157" src="https://github.com/user-attachments/assets/d216684d-6be6-41f3-bfe2-90b6a60cc838" />
<img width="433" height="36" alt="Screenshot 2025-09-19 151235" src="https://github.com/user-attachments/assets/7330da8b-038e-4d58-ae40-5b9890d6ea88" />
<img width="520" height="106" alt="ethier to is duplicate or lladr is garbage" src="https://github.com/user-attachments/assets/795bcede-fb57-4a5f-8f32-3a0acb870f1b" />
