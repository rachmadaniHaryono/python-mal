import os


def get_proxy_settings():
    proxy_host = os.environ.get("TESTS_SQUID_ADDRESS", None)
    if proxy_host is None:
        return None
    return {"https": proxy_host, 'http': proxy_host}
