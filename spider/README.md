## Code Examples

<div>
<p>Samples:</p>

<pre>
 <code>
from util import google_search, search

query = "alexander tsanov"
results = google_search(query)

for result in results:
    print(result)

 </code>
</pre>
</div>



<div>

  <pre>

   <code>

from base import BrowserChoice
from engine import Scholar
from util import search

query = "alexander tsanov"
result1 = search(query, Scholar)
result2 = seacrch(query, Scholar, choice=BrowserChoice.firefox)

for result in results:
    print(result1)

print(result2)

   </code>

  </pre>

</div>
