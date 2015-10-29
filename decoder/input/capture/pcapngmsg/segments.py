from decoder.descriptor import *
from decoder.input.capture.pcapngmsg.field import *


BlockHeader = Descriptor([
    WireField('pcapngmsg-block-type', 'I', type=int),
    WireField('pcapngmsg-block-total-length', 'I', type=int)
])

BlockFooter = Descriptor([
    WireField('pcapngmsg-block-total-length-check', 'I', type=int)
])

SectionHeader = Descriptor([
    WireField('pcapngmsg-magic-number', 'I', type=int),
    WireField('pcapngmsg-major-version', 'H', type=int),
    WireField('pcapngmsg-minor-version', 'H', type=int),
    WireField('pcapngmsg-section-length', 'Q', type=int)
])

InterfaceDefinition = Descriptor([
    WireField('pcapngmsg-link-type', 'H', type=int),
    WireField('resv', 'H', hidden=True),
    WireField('pcapngmsg-snap-len', 'I', type=int)
])

EnhancedPacket = Descriptor([
    WireField('pcapngmsg-ifc-id', 'I', type=int),
    WireField('pcapngmsg-timestamp-high', 'I', type=int),
    WireField('pcapngmsg-timestamp-low', 'I', type=int),
    WireField('pcapngmsg-captured-length', 'I', type=int),
    WireField('pcapngmsg-packet-length', 'I', type=int)
])

OptionHeader = Descriptor([
    WireField('pcapngmsg-option-code', 'H', type=int),
    WireField('pcapngmsg-option-length', 'H', type=int)
])

TsResolOption = Descriptor([
    WireField('pcap-tsresol', 'B', type=int)
])

EthernetHeader = Descriptor([
    WireField('pcapngmsg-dest-mac', '6s', type=HexArray),
    WireField('pcapngmsg-source-mac', '6s', type=HexArray),
    WireField('pcapngmsg-eth-protocol', 'H', type=int)
], endian='Big')

VlanTag = Descriptor([
    WireField('pcapngmsg-vlan-id', '2s', type=TrimmedString),
    WireField('pcapngmsg-eth-protocol', 'H', type=int) # this will overwrite the pcapngmsg-eth-protocol extracted in EtherNetHeader
], endian='Big')

IpHeader = Descriptor([
    WireField('pcapngmsg-ip-version', 'B', type=int),
    WireField('pcapngmsg-ip-services', 'B', type=int),
    WireField('pcapngmsg-ip-total-length', 'H', type=int),
    WireField('pcapngmsg-ip-identification', 'H', type=int),
    WireField('pcapngmsg-ip-flags', 'B', type=int),
    WireField('pcapngmsg-ip-fragment-offset', 'B', type=int),
    WireField('pcapngmsg-ip-ttl', 'B', type=int),
    WireField('pcapngmsg-ip-protocol', 'B', type=int),
    WireField('pcapngmsg-ip-header-checksum', 'H', type=int),
    WireField('pcapngmsg-ip-source-addr', 'L', type=IpAddrField()),
    WireField('pcap-ip-dest-addr', 'L', type=IpAddrField())
], endian='Big')

UdpHeader = Descriptor([
    WireField('pcapngmsg-udp-source-port', 'H', type=int),
    WireField('pcap-udp-dest-port', 'H', type=int),
    WireField('pcapngmsg-udp-length', 'H', type=int),
    WireField('pcapngmsg-udp-checksum', 'H', type=int)
], endian='Big')
