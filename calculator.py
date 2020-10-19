import traceback

"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

def home():
    page = """
    <h1>Welcome to the WSGI Calculator</h1>
    <h3>Here are the operations you can do:</h3>
    <table>
        <tr><th>Add</th><td>/add/{num1}/{num2}</td></tr>
        <tr><th>Subtract</th><td>/subtract/{num1}/{num2}</td></tr>
        <tr><th>Multiply</th><td>/multiply/{num1}/{num2}</td></tr>
        <tr><th>Divide</th><td>/divide/{num1}/{num2}</td></tr>
    </table>
    """
    return page


def add(num1, num2):
    """ Returns a STRING with the sum of the arguments """
    adding = int(num1) + int(num2)
    page = f"""
            <h1> You have added {num1} and {num2} which equals {adding}</h1>
            """
    return page


def subtract(num1, num2):
    """ Returns a STRING with the difference of the arguments """
    difference = int(num1) - int(num2)
    page = f"""
            <h1> You have subtracted {num1} and {num2} which equals {difference}</h1>
            """
    return page


def multiply(num1, num2):
    """ Returns a STRING of the two numbers multiplied"""
    times = int(num1) * int(num2)
    page = f"""
            <h1> You have multiplied {num1} and {num2} which equals
            {times}</h1>
            """
    return page


def divide(num1, num2):
    """ Returns a STRING of the two numbers divided"""
    divided = int(num1) / int(num2)
    page = f"""
            <h1> You have divided {num1} and {num2} which equals
            {divided}</h1>
            """
    return page


def resolve_path(path):

    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {
        '': home,
        'add': add,
        'multiply': multiply,
        'divide': divide,
        'subtract': subtract,
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)

        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

