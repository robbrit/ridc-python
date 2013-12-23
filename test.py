'''
The MIT License (MIT)

Copyright (c) 2013 Rob Britton (rob@robbritton.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from twisted.internet import reactor, defer
from ridc.twisted_connector import RidcTwisted


@defer.inlineCallbacks
def do_all_the_things3():
    db = RidcTwisted("localhost", 3001)

    yield db.create_index("hello")
    yield db.create_index("sweet")

    res = yield db.indexes()

    print res

    reactor.stop()


@defer.inlineCallbacks
def do_all_the_things():
    # connect first
    db = RidcTwisted("localhost", 3001)

    last = None
    times = 10000

    # first stick 100 elements in
    for i in range(times):
        data = {"hello": "blah", "field": str(i)}
        res = yield db.create(data)
        #print res

    # now create some indexes
    yield db.create_index("hello")

    # now add 100 more
    for i in range(times):
        data = {"hello": "blah", "field": str(i)}
        last = yield db.create(data)

    # create another index
    yield db.create_index("field")

    # show all our indexes
    res = yield db.indexes()
    print res

    # fetch something
    res = yield db.find_by_id(last["id"])
    print res

    print "Getting by index:"
    res = yield db.find("field", "8")

    if len(res) != 2:
        print "somesing is wrong"

    print res

    res = yield db.find("field", "3")
    print res

    # now delete some stuff
    res = yield db.delete_all("field", "3")
    print res
    res = yield db.delete(last["id"])
    print res

    # now try to fetch that stuff, shouldn't get it
    res = yield db.find_by_id(last["id"])
    print res

    res = yield db.find("field", "3")
    print res

    reactor.stop()

do_all_the_things()
reactor.run()
