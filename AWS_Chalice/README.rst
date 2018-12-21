===============================
Creating Your Project
===============================

The next thing we’ll do is use the chalice command to create a new project:

.. code-block:: sh

   $ chalice new-project helloworld

This will create a helloworld directory. Cd into this directory. You’ll see several files have been created for you:

.. code-block:: sh

   $ cd helloworld
   $ ls -la
   drwxr-xr-x   .chalice
   -rw-r--r--   app.py
   -rw-r--r--   requirements.txt
You can ignore the .chalice directory for now, the two main files we’ll focus on is app.py and requirements.txt.

Let’s take a look at the app.py file:

.. code-block:: py

   from chalice import Chalice

   app = Chalice(app_name='helloworld')


   @app.route('/')
   def index():
       return {'hello': 'world'}
       
The new-project command created a sample app that defines a single view, /, that when called will return the JSON body
.. code-block:: json

   {"hello": "world"}.

===============================
Deploying
===============================
Let’s deploy this app. Make sure you’re in the helloworld directory and run chalice deploy:
.. code-block:: sh
   $ chalice deploy


Initiating first time deployment...
--------------------------------

https://abcdefg.execute-api.us-west-2.amazonaws.com/api/

You now have an API up and running using API Gateway and Lambda:
.. code-block:: sh

   $ curl https://abcdefg.execute-api.us-west-2.amazonaws.com/api/
   {"hello": "world"}
   
Try making a change to the returned dictionary from the index() function. You can then redeploy your changes by running chalice deploy.

using httpie instead of curl (https://github.com/jakubroztocil/httpie) to test our API. You can install httpie using pip install httpie, or if you’re on Mac, you can run brew install httpie. The Github link has more information on installation instructions. Here’s an example of using httpie to request the root resource of the API we just created. Note that the command name is http:
.. code-block:: json

   $ http https://abcdefg.execute-api.us-west-2.amazonaws.com/api/
   HTTP/1.1 200 OK
   Connection: keep-alive
   Content-Length: 18
   Content-Type: application/json
   Date: Mon, 30 May 2016 17:55:50 GMT
   X-Cache: Miss from cloudfront

   {
       "hello": "world"
   }
   
Additionally, the API Gateway endpoints will be shortened to https://endpoint/api/ for brevity. Be sure to substitute https://endpoint/api/ for the actual endpoint that the chalice CLI displays when you deploy your API (it will look something like https://abcdefg.execute-api.us-west-2.amazonaws.com/api/.
