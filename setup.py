from distutils.core import setup
from decoder._version import __version__

setup(
    name='decoder',
    version=__version__,
    packages=['thirdparty', 'thirdparty.progressbar23', 'thirdparty.progressbar23.progressbar', 'decoder', 'decoder.cta',
              'decoder.cta.cqsmsg', 'decoder.ice', 'decoder.ice.cap', 'decoder.ice.icemsg', 'decoder.ndq',
              'decoder.ndq.itch', 'decoder.ndq.mold', 'decoder.phx', 'decoder.phx.nextgenmsg', 'decoder.tmx',
              'decoder.tmx.cdfmsg', 'decoder.arca', 'decoder.arca.bbomsg', 'decoder.arca.xdpmsg',
              'decoder.arca.integratedmsg', 'decoder.bats', 'decoder.bats.mpitchmsg', 'decoder.nyse',
              'decoder.nyse.bbomsg', 'decoder.spry', 'decoder.spry.mdpacketmsg', 'decoder.spry.seqfwd_cppmsg',
              'decoder.input', 'decoder.input.net', 'decoder.input.capture', 'decoder.input.capture.capmsg',
              'decoder.input.capture.pcapngmsg', 'decoder.output'],
    url='',
    license='',
    author='John Dibling',
    author_email='john.dibling@picotrading.com',
    description='',
    scripts = ['decode.py']
)
