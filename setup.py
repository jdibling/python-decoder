from distutils.core import setup

setup(
    name='decoder',
    version='1.0.1',
    packages=['base', 'decoder', 'decoder.cta', 'decoder.cta.cqs', 'decoder.ice', 'decoder.ice.ice', 'decoder.ndq',
              'decoder.ndq.itch', 'decoder.ndq.mold', 'decoder.phx', 'decoder.phx.nextgen', 'decoder.arca',
              'decoder.arca.bbo', 'decoder.arca.xdp', 'decoder.bats', 'decoder.bats.mpitch', 'decoder.nyse',
              'decoder.nyse.bbo', 'decoder.spry', 'decoder.spry.seqfwd_cpp', 'decoder.input', 'decoder.input.net',
              'decoder.input.capture', 'decoder.input.capture.cap', 'decoder.input.capture.pcapng', 'decoder.output'],
    url='',
    license='',
    author='John Dibling',
    author_email='john.dibling@picotrading.com',
    description='PyDecode'
)
