import cgi

import sqlite3

conn= sqlite3.connect('user.db')

form = '''
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <!-- Bootstrap CSS -->
    <!-- https://cdnjs.com/libraries/twitter-bootstrap/5.0.0-beta1 -->
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.0.0-beta1/css/bootstrap.min.css"
    />
    <!-- Icons: https://getbootstrap.com/docs/5.0/extend/icons/ -->
    <!-- https://cdnjs.com/libraries/font-awesome -->
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.2/css/all.min.css"
    />
    <title>Hello, world!</title>
  </head>
  <body>
    <div class="container-fluid p-0">
        <div class="row">
            <div class="col">
                <form action="/contact" method='POST'>
                    <div class="m-3 d-flex justify-content-center align-items-center flex-column">
                        <input type="text" class="form-control" placeholder="Username" name='name'>
                        <input type="password" class="form-control mt-3" placeholder="password" name='password'>
                        <input type="submit" class="btn btn-primary mt-4" value='Register'>
                    </div>
                </form>
            </div>
        </div>
    </div>
    <!-- Optional JavaScript; choose one of the two! -->
    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.0.0-beta1/js/bootstrap.bundle.min.js"></script>
    <!-- Option 2: Separate Popper and Bootstrap JS -->
    <!-- https://cdnjs.com/libraries/popper.js/2.5.4 -->
    <!-- <script
      src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.5.4/umd/popper.min.js"
    ></script>
    <script
      src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.0.0-beta1/js/bootstrap.min.js"
    ></script> -->
    <!-- More: https://getbootstrap.com/docs/5.0/getting-started/introduction/ -->
</body>
</html>
'''
c= conn.cursor()

# c.execute(""" CREATE TABLE users (
#     id integer,
#     username text,
#     passw text
# )""")

# c.execute("INSERT INTO users VALUES ('1', 'ayten', 'ayten1234')")

print(c.execute("SELECT * FROM users"))
result = c.fetchall()

username = result[0][1]
p = result[0][2]
print(p,username)

print(result)

conn.commit()

conn.close()


def render_template(template_name='contact.html', context={}):
    # html_str = ""
    with open(template_name, 'r') as f:
        html_str = f.read()
        html_str = html_str.format(**context)
    return html_str

def app(environ, start_response):
    html = form

    if environ['REQUEST_METHOD'] == 'POST':
        print('qwqww')
        post_env = environ.copy()
        post_env['QUERY_STRING'] = ''
        post = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=post_env,
            # keep_blank_values=True
        )
        html = post['name'].value
        password = post['password'].value
        print(html,password)
        if html==username and password==p:
            start_response('200 OK', [('Content-Type', 'text/html')])
            # return [html]
            data =  render_template(template_name="contact.html",context={"path": html})
            data = data.encode()
            return [data]
        else:
            print("sehvsenn")






if __name__ == '__main__':
    try:
        from wsgiref.simple_server import make_server
        httpd = make_server('', 8080, app)
        print('Serving on port 8080...')
        print("http://localhost:8080")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Goodbye.')