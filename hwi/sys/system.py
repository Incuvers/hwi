import sys
import time
import socket
import logging

_logger = logging.getLogger(__name__)

def shutdown():
    """
    Shutdown handler
    """
    _logger.info("Exiting hwi")
    sys.exit(0)

def test_connection(host: str = "8.8.8.8", port: int = 53, timeout: int = 3):
    """
    Tests internet connectivity
    Test intenet connectivity by checking with Google
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    :param host: (str) the host to test connection
    :param port: (int) the port to use
    :param timeout:
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
    except socket.error:
        return False
    return True


def wfi(host:str, port:int, timeout:int) -> None:
    """
    Wait for server to be available on the network

    :param host: address host
    :type host: str
    :param port: address port
    :type port: int
    :param timeout: loopback timeout
    :type timeout: int
    :raises TimeoutError: if loopback timeout is reached and server is not available
    """
    _logger.info("Starting wfi test on %s:%s for %ss", host, port, timeout)
    result = test_connection(host, port, timeout)
    timer = 0
    BACKOFF = 0.2
    while not result:
        if timer >= timeout:
            _logger.warning("Server at %s:%s was not reached by the loopback timeout", host, port)
            raise TimeoutError
        _logger.debug("Connection to %s:%s failed applying backoff: %ss", host, port, BACKOFF)
        time.sleep(BACKOFF)
        timer += BACKOFF
        result = test_connection(host, port, timeout)
        
