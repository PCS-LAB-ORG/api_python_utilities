# Prisma Utility Scripts

This is meant to be a utility library for Prisma Cloud (PC).

It builds upon a few other common libraries for PC.
- https://github.com/PaloAltoNetworks/prismacloud-api-python/
- https://github.com/PaloAltoNetworks/pc-python-integration

These libraries have good implementations.

Consider these other libraries for viable options. The script style here may be easier, newer, or have utilities that don't exist elsewhere though the same may go for the other libraries. I could have attempted to update those others but, tracking down access can be tricky when its possible at all. I leave in some reference notes that helped me build these scripts like the format of different parameters that are valid in case you're unfamiliar with that API. 

## Files:
- `<module>/core.py` tends to hold single general API calls
- other scripts are purpose built utilities
- utils/ holds common functions not specific to modules
- some test cases show how to use functions and variations

## Goal:
My personal utility belt dumping ground for scripts. 

I'll probably never build this out completely.

I build these as tasking calls for it in my role with Prisma Cloud.
