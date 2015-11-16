from decoder.descriptor import *
from decoder.input.capture.pcapngmsg.field import *


BlockHeader = Descriptor([
    WireField('pcap-block-type', 'I', type=int),
    WireField('pcap-block-total-length', 'I', type=int)
])

BlockFooter = Descriptor([
    WireField('pcap-block-total-length-check', 'I', type=int)
])

SectionHeader = Descriptor([
    WireField('pcap-magic-number', 'I', type=int),
    WireField('pcap-major-version', 'H', type=int),
    WireField('pcap-minor-version', 'H', type=int),
    WireField('pcap-section-length', 'Q', type=int)
])

InterfaceDefinition = Descriptor([
    WireField('pcap-link-type', 'H', type=int),
    WireField('resv', 'H', hidden=True),
    WireField('pcap-snap-len', 'I', type=int)
])

EnhancedPacket = Descriptor([
    WireField('pcap-ifc-id', 'I', type=int),
    WireField('pcap-timestamp-high', 'I', type=int),
    WireField('pcap-timestamp-low', 'I', type=int),
    WireField('pcap-captured-length', 'I', type=int),
    WireField('pcap-packet-length', 'I', type=int)
])

OptionHeader = Descriptor([
    WireField('pcap-option-code', 'H', type=int),
    WireField('pcap-option-length', 'H', type=int)
])

TsResolOption = Descriptor([
    WireField('pcap-tsresol', 'B', type=int)
])

EthernetHeader = Descriptor([
    WireField('pcap-dest-mac', '6s', type=HexArray),
    WireField('pcap-source-mac', '6s', type=HexArray),
    WireField('pcap-eth-protocol', 'H', type=int)
], endian='Big')

VlanTag = Descriptor([
    WireField('pcap-vlan-id', '2s', type=TrimmedString),
    WireField('pcap-eth-protocol', 'H', type=int) # this will overwrite the pcap-eth-protocol extracted in EtherNetHeader
], endian='Big')

IpHeader = Descriptor([
    WireField('pcap-ip-version', 'B', type=int),
    WireField('pcap-ip-services', 'B', type=int),
    WireField('pcap-ip-total-length', 'H', type=int),
    WireField('pcap-ip-identification', 'H', type=int),
    WireField('pcap-ip-flags', 'B', type=int),
    WireField('pcap-ip-fragment-offset', 'B', type=int),
    WireField('pcap-ip-ttl', 'B', type=int),
    WireField('pcap-ip-protocol', 'B', type=int),
    WireField('pcap-ip-header-checksum', 'H', type=int),
    WireField('pcap-ip-source-addr', 'L', type=IpAddrField()),
    WireField('pcap-ip-dest-addr', 'L', type=IpAddrField())
], endian='Big')

UdpHeader = Descriptor([
    WireField('pcap-udp-source-port', 'H', type=int),
    WireField('pcap-udp-dest-port', 'H', type=int),
    WireField('pcap-udp-length', 'H', type=int),
    WireField('pcap-udp-checksum', 'H', type=int)
], endian='Big')
