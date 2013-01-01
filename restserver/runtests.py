"""
"""
import nose
import logging


log = logging.getLogger()

# Log to console instead:
hdlr = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
log.addHandler(hdlr)
log.setLevel(logging.DEBUG)
log.propagate = False


nose.main()
