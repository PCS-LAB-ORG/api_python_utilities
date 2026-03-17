#!/python
import sys
import pprint
# sys.modules is a dictionary; keys are module names
current_imports = sorted(sys.modules.keys()) 
pprint.pprint(current_imports) # Uncomment to see the full list
import repositories
help(repositories)

from apu.repositories import get_repo

get_repo.get_vcs_repository_page()
