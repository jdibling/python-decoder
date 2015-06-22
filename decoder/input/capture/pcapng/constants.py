from decoder.input.capture.pcapng.segments import *

BlockTypes = {
    0x00000001: (InterfaceDefinition, "InterfaceDefinition"),
    0x00000006: (EnhancedPacket, "EnhancedPacket"),
    0x0A0D0D0A: (SectionHeader, "SectionHeader")
}

BlockTypeIndex = dict((v[1],k) for k,v in BlockTypes.iteritems())

BlockOptionTypes = {
    BlockTypeIndex['SectionHeader']: {
        0: ('endofopt', None),
        1: ('comment', TrimmedString),
        2: ('hardware', TrimmedString),
        3: ('os', TrimmedString),
        4: ('userappl', TrimmedString)
    },
    BlockTypeIndex['InterfaceDefinition']: {
        0: ('endofopt', None),
        1: ('comment', TrimmedString),
        2: ('name', TrimmedString),
        3: ('description', TrimmedString),
        4: ('ipv4_addr', int),
        5: ('ipv6_addr', TrimmedString),
        6: ('mac_addr', HexArray),
        7: ('eui_addr', int),
        8: ('speed', int),
        9: ('tsresol', str),
        10: ('tzone', int),
        11: ('filter', TrimmedString),
        12: ('os', TrimmedString),
        13: ('fcslen', int),
        14: ('tsoffset', int)
    },
    BlockTypeIndex['EnhancedPacket']: {
        0: ('endofopt', None),
        1: ('comment', TrimmedString),
        2: ('flags', int),
        3: ('hash', int),
        4: ('dropcount', int)
    }
}
