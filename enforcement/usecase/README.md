# Archived repo exception utils

## usage: 
create_exception_from_repo_list.py [-h] --file FILE
                                          [--exception_name EXCEPTION_NAME]
                                          [--force] [--verbose]
                                          [--exception_definition_file EXCEPTION_DEFINITION_FILE]
                                          [--PRISMA_DOMAIN PRISMA_DOMAIN]
                                          [--PRISMA_ACCESS_KEY PRISMA_ACCESS_KEY]
                                          [--PRISMA_SECRET_KEY PRISMA_SECRET_KEY]

## Description:
This script is meant to do two things. 
First, it will query a list of repositories from Prisma and compare to a local list of repos that may exist and writes it to a local file.
Second, it prompts to create/update an enforcement exception for these repos with the enforcement rule definition.

## Prerequisite steps:
Python 3.11. 3.6-3.12 are expected to work.
Python libraries required: requests, prismacloud-api

## Run the script
python create_exception.py <args>

### options:
  -h, --help            show this help message and exit

  --file FILE           Relative file path csv formatted set of repositories
                        containing at least 'id' and 'fullName'. The file
                        created will have this format.
  
  --exception_name EXCEPTION_NAME
                        The name of the exception that you are creating or
                        updating. Without this it will ask to write repos to a
                        local file --file
  
  --force               Automatically accept all prompts. (equivalent to
                        passing true, yes, proceed, etc.)
  
  --verbose             Some extra logging for http calls and debugging.
  
  --exception_definition_file EXCEPTION_DEFINITION_FILE
                        Unimplemented. Currently the codeCategories flags are
                        hardcoded as variable 'exception_definition'.
  
  --PRISMA_DOMAIN PRISMA_DOMAIN
                        like https://api.ca.prismacloud.io for Canada. Default
                        environment variable PRISMA_DOMAIN
  
  --PRISMA_ACCESS_KEY PRISMA_ACCESS_KEY
                        Default environment variable PRISMA_ACCESS_KEY
  
  --PRISMA_SECRET_KEY PRISMA_SECRET_KEY
                        Default environment variable PRISMA_SECRET_KEY

## Core Use Cases
1. Get list of archived repos as a local csv
2. Create new exceptions with list of archived repos
3. Create new exception with edited local list of repos
4. Update existing exception with local list of repos
5. Update existing exception with a repo that already exists in a different exception
6. Show that argparse can be used instead of hardcoding values. 
7. Show help statement
8. Show README.md
