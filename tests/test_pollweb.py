import re


def test_token_extraction():
    content = '''<!DOCTYPE html><html class="ng-csp" data-placeholder-focus="false" lang="en" data-locale="en" >
    <head data-requesttoken="z5nRBw3rLPIeFpnusYqvvlWYigm8omtTMQ1xk8LBqXM=:o6+8MmyMZoNffvG64+vBkTOu/lDq2A5maGcppoaC2Do=">
    <meta charset="utf-8"><title>Nextcloud	</title>'''
    pattern = r'data-requesttoken=\"([^\"]+)\"'
    requesttoken = re.search(pattern, content).group(1)
    assert requesttoken == "z5nRBw3rLPIeFpnusYqvvlWYigm8omtTMQ1xk8LBqXM=:o6+8MmyMZoNffvG64+vBkTOu/lDq2A5maGcppoaC2Do="
