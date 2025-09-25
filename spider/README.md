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

query = "richard alba"
result1 = search(query, Scholar)
result2 = seacrch(query, Scholar, choice=BrowserChoice.firefox)

for result in results:
    print(result1)

print(result2)

   </code>

  </pre>

</div>

<p>
Save your result in persistent storage like a JSON file, so you don't send too many queries to
the search engine. The view model provides functions for storing data <code>store_data(data, file_path)</code> and loading stored data
<code>load_data(file_path)</code>
</p>

<div>

  <pre>

   <code>

from base import BrowserChoice
from engine import Scholar
from util import search
from view import store_data
from pathlib import Path

query = "louis pentingi"
data = google_search(query)

filename = Path('../target/data.json')
# store data
store_data(result, filename)
# retrieve data
results = load_data(filename)

for result in results:
    print(result1)

print(result2)

   </code>

  </pre>

</div>

<p>You can also omit the file's path and name</p>

<div>

  <pre>

   <code>

from base import BrowserChoice
from engine import Scholar
from util import search
from view import store_data
from pathlib import Path

query = "louis pentingi"
data = google_search(query)

# default file path Path('../target/data.json')
# store data
store_data(result)
# retrieve data
results = load_data()

for result in results:
    print(result1)

print(result2)

   </code>

  </pre>

</div>
