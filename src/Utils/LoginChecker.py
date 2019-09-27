import sys


def check(secret, token):
    #  Token check
    if secret is None:
        print('Specify LINE_CHANNEL_SECRET as environment variable.')
        sys.exit(1)
    if token is None:
        print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
        sys.exit(1)