The MonkeyPatchWarning or RuntimeWarning when using grequests occurs because grequests automatically performs gevent monkey-patching upon import. If other modules that use ssl or socket are imported before grequests, gevent cannot patch them correctly, leading to potential recursion errors or incorrect behavior. 
GitHub
GitHub
 +3
How to Fix the Warning
To resolve this, you must ensure that grequests is the very first import in your script, or manually trigger the monkey-patch before any other libraries are loaded. 
Move the grequests import to the top:
Ensure import grequests appears before import requests or any other library that might use network sockets.
python
import grequests  # Must be first
import requests
Manual Monkey-Patching (Recommended):
For the most reliable behavior, manually call patch_all() at the absolute beginning of your entry point script.
python
from gevent import monkey
monkey.patch_all()

import grequests
Suppressing the Warning:
If you have confirmed that the order of imports is correct but still see the warning (common in environments like Jupyter Notebooks), you can suppress it using the standard warnings module:
python
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='gevent')
 
GitHub
GitHub
 +4
Common Causes
Late Monkey-Patching: Importing a library like requests or ssl before grequests causes the original synchronous versions of those modules to be loaded into memory, which gevent cannot safely replace afterward.
Double Patching: If your application already calls monkey.patch_all(), and then you import grequests, you may see a warning that patching is occurring more than once.
Environment Conflicts: Libraries that use their own event loops or internal threading (like some database drivers or async frameworks) can conflict with gevent's global patching. 
GitHub
GitHub
 +4