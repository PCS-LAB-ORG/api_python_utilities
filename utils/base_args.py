#!python

import argparse

parser = argparse.ArgumentParser(description="Core Prisma Parameters")
parser.add_argument(
    "--DOMAIN",
    required=False,
    help="like https://api.prismacloud.io for Canada. Will otherwise be required in local creds.py file with DOMAIN variable",
)
parser.add_argument(
    "--PRISMA_ACCESS_KEY",
    required=False,
    help="Will otherwise be required in local creds.py file with PRISMA_ACCESS_KEY variable by command `import creds`",
)
parser.add_argument(
    "--PRISMA_SECRET_KEY",
    required=False,
    help="Will otherwise be required in local creds.py file with PRISMA_SECRET_KEY variable by command `import creds`",
)
parser.add_argument("--force", required=False, default=False, help="Delete and Create key without prompting.")

from datetime import datetime
# Get the current date and time
now = datetime.now()
formatted_datetime = now.strftime("%Y_%m_%d_%H_%M_%S")
parser.add_argument("--log_file", required=False, default=f"output_{formatted_datetime}.log" help="General log file.")

args = parser.parse_args()
