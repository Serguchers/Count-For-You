from distutils.debug import DEBUG
import logging
import logging.handlers


_format = logging.Formatter("%(asctime)s - %(levelname)s - %(module)-10s -%(message)s")
log_hand = logging.FileHandler("log/client_logs.log", encoding="UTF-8")
log_hand.setFormatter(_format)

log = logging.getLogger("client_logger")
log.addHandler(log_hand)
log.setLevel(logging.DEBUG)


if __name__ == "__main__":
    log.info("Test")
