import sys
import logging
import fsDropBox

log = logging.getLogger("fsclient.DropBox")


class fsPipeline(fsDropBox):
    """Pipeline client manager"""

    def getMonitorParameters(self, props):
        """Get monitor parameters"""
        super().getMonitorParameters(props)


if __name__ == "__main__":
    try:
        log.info("Trying to start OMERO.fs Pipeline client")
        app = fsPipeline()
    except Exception:
        log.exception("Failed to start the client:\n")
        log.info("Exiting with exit code: -1")
        sys.exit(-1)

    exitCode = app.main(sys.argv)
    log.info("Exiting with exit code: %d", exitCode)
    sys.exit(exitCode)
