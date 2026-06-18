from cougarnet.util import \
        ip_str_to_binary, ip_binary_to_str

from headers import IPv4Header, UDPHeader, TCPHeader, \
        IP_HEADER_LEN, UDP_HEADER_LEN, TCP_HEADER_LEN, \
        TCPIP_HEADER_LEN, UDPIP_HEADER_LEN
from host import Host
from mysocket import UDPSocket, TCPSocketBase

class TransportHost(Host):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.socket_mapping_udp = {}
        self.socket_mapping_tcp = {}

    def handle_tcp(self, pkt: bytes) -> None:
        IPHdr = pkt[:IP_HEADER_LEN]
        TCPHdr = pkt[IP_HEADER_LEN:TCPIP_HEADER_LEN]
        data = pkt[TCPIP_HEADER_LEN:]

        IPClass = IPv4Header(0, 0, 0, 0, "test", "test")
        TCPClass = TCPHeader(0, 0, 0, 0, 0, 0)

        TCPClass = TCPClass.from_bytes(TCPHdr)
        IPClass = IPClass.from_bytes(IPHdr)

        socKey = (IPClass.dst, TCPClass.dport, IPClass.src, TCPClass.sport)
        socKeyListener = (IPClass.dst, TCPClass.dport, None, None)

        if socKey in self.socket_mapping_tcp:
            socTCP = self.socket_mapping_tcp[socKey]
            socTCP.handle_packet(pkt)
        elif socKeyListener in self.socket_mapping_tcp:
            socListenerTCP = self.socket_mapping_tcp[socKeyListener]
            socListenerTCP.handle_packet(pkt)
        else:
            self.no_socket_tcp(pkt)

    def handle_udp(self, pkt: bytes) -> None:
        IPHdr = pkt[:IP_HEADER_LEN]
        UDPHdr = pkt[IP_HEADER_LEN:UDPIP_HEADER_LEN]

        IPClass = IPv4Header(0, 0, 0, 0, "test", "test")
        UDPClass = UDPHeader(0, 0, 0, 0)

        UDPClass = UDPClass.from_bytes(UDPHdr)
        IPClass = IPClass.from_bytes(IPHdr)

        socKey = (IPClass.dst, UDPClass.dport)

        if (socKey in self.socket_mapping_udp):
            sock = self.socket_mapping_udp[socKey]
            sock.handle_packet(pkt)
        else:
            self.no_socket_udp(pkt)

    def install_socket_udp(self, local_addr: str, local_port: int,
            sock: UDPSocket) -> None:
        self.socket_mapping_udp[(local_addr, local_port)] = sock

    def install_listener_tcp(self, local_addr: str, local_port: int,
            sock: TCPSocketBase) -> None:
        self.socket_mapping_tcp[(local_addr, local_port, None, None)] = sock

    def install_socket_tcp(self, local_addr: str, local_port: int,
            remote_addr: str, remote_port: int, sock: TCPSocketBase) -> None:
        self.socket_mapping_tcp[(local_addr, local_port, \
                remote_addr, remote_port)] = sock

    def no_socket_udp(self, pkt: bytes) -> None:
        pass

    def no_socket_tcp(self, pkt: bytes) -> None:
        pass