# tillit_task

Implementation of web crawler with gevent.

### How to run the code?

In the command line run the following:

`$python3 main.py --url url --num num`

[--url] - url to process
[--num] - optional, number of workers used by gevent, default is set to 10.

### How to run the test? 

In the command line run the following:

`$python3 -m unittest test.test`

### Implementation 

The crawler is implemented as a class with the following attributes:

self.url            => root url passed as input parameter for processing.<br />
self.workers        => number of workers used by gevent, default set to 10.<br />
self.output_list    => list of all the source urls and their respective destinations. Each entry of the list is a tuple (src, destination).<br />
self.q              => queue that stores all urls that need to be processed.<br />
self.visited        => list of urls already visited.<br />

And functions:

get_res(url)                      => returns response from the url passed as argument.<br />
get_urls(url)                     => returns the list of urls that url passed as argument points to.<br />
check_visited(url)                => returns boolean value, True if the url has been visited, or False if it was not.<br />
check_if_valid_url(url)           => returns boolean value, True if url is valid, False if not.<br />
is_internal_url(child_url)        => returns boolean value, True if the url is interanl link, False if not.<br />
iterate_nodes(pid)                => itterates all the nodes in the queue.<br />
iterate_urls(urls_list, node)     => itterates over all the urls that given node points to, porcesses it and add to the the output.<br />
print_output()                    => prints the output list to the std.<br />
process()                         => calls the functions to perform processing of the url.<br />

File requiremnts.txt contains versions of python libraries used in implementation. 
