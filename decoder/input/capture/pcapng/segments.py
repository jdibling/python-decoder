from base.descriptor import *
from decoder.input.capture.pcapng.field import *


BlockHeader = Descriptor([
    WireField('pcapng-block-type', 'I', type=int),
    WireField('pcapng-block-total-length', 'I', type=int)
])

BlockFooter = Descriptor([
    WireField('pcapng-block-total-length-check', 'I', type=int)
])

SectionHeader = Descriptor([
    WireField('pcapng-magic-number', 'I', type=int),
    WireField('pcapng-major-version', 'H', type=int),
    WireField('pcapng-minor-version', 'H', type=int),
    WireField('pcapng-section-length', 'Q', type=int)
])

InterfaceDefinition = Descriptor([
    WireField('pcapng-link-type', 'H', type=int),
    WireField('resv', 'H', hidden=True),
    WireField('pcapng-snap-len', 'I', type=int)
])

EnhancedPacket = Descriptor([
    WireField('pcapng-ifc-id', 'I', type=int),
    WireField('pcapng-timestamp-high', 'I', type=int),
    WireField('pcapng-timestamp-low', 'I', type=int),
    WireField('pcapng-captured-length', 'I', type=int),
    WireField('pcapng-packet-length', 'I', type=int)
])

OptionHeader = Descriptor([
    WireField('pcapng-option-code', 'H', type=int),
    WireField('pcapng-option-length', 'H', type=int)
])

TsResolOption = Descriptor([
    WireField('pcap-tsresol', 'B', type=int)
])

EthernetHeader = Descriptor([
    WireField('pcapng-dest-mac', '6s', type=HexArray),
    WireField('pcapng-source-mac', '6s', type=HexArray),
    WireField('pcapng-eth-protocol', 'H', type=int)
], endian='Big')

VlanTag = Descriptor([
    WireField('pcapng-vlan-id', '2s', type=TrimmedString),
    WireField('pcapng-eth-protocol', 'H', type=int) # this will overwrite the pcapng-eth-protocol extracted in EtherNetHeader
], endian='Big')

IpHeader = Descriptor([
    WireField('pcapng-ip-version', 'B', type=int),
    WireField('pcapng-ip-services', 'B', type=int),
    WireField('pcapng-ip-total-length', 'H', type=int),
    WireField('pcapng-ip-identification', 'H', type=int),
    WireField('pcapng-ip-flags', 'B', type=int),
    WireField('pcapng-ip-fragment-offset', 'B', type=int),
    WireField('pcapng-ip-ttl', 'B', type=int),
    WireField('pcapng-ip-protocol', 'B', type=int),
    WireField('pcapng-ip-header-checksum', 'H', type=int),
    WireField('pcapng-ip-source-addr', 'L', type=IpAddrField()),
    WireField('pcapng-ip-dest-addr', 'L', type=IpAddrField())
], endian='Big')

UdpHeader = Descriptor([
    WireField('pcapng-udp-source-port', 'H', type=int),
    WireField('pcapng-udp-dest-port', 'H', type=int),
    WireField('pcapng-udp-length', 'H', type=int),
    WireField('pcapng-udp-checksum', 'H', type=int)
], endian='Big')
