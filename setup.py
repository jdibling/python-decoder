from distutils.core import setup

setup(
    name='decoder',
    version='1.0.1',
    packages=['base', 'decoder', 'decoder.cta', 'decoder.cta.cqsmsg', 'decoder.ice', 'decoder.ice.icemsg', 'decoder.ndq',
              'decoder.ndq.itch', 'decoder.ndq.mold', 'decoder.phx', 'decoder.phx.nextgenmsg', 'decoder.arca',
              'decoder.arca.bbomsg', 'decoder.arca.xdpmsg', 'decoder.bats', 'decoder.bats.mpitchmsg', 'decoder.nyse',
              'decoder.nyse.bbomsg', 'decoder.spry', 'decoder.spry.seqfwd_cppmsg', 'decoder.input', 'decoder.input.net',
              'decoder.input.capture', 'decoder.input.capture.cap', 'decoder.input.capture.pcapng', 'decoder.output'],
    url='',
    license='',
    author='John Dibling',
    author_email='john.dibling@picotrading.com',
    description='PyDecode'
)
