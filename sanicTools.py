from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from sanic.response import html

''' A Sanic tool pack. Provided Flask-style render_template function. ''' 


env = Environment(loader = FileSystemLoader('templates'), autoescape = select_autoescape(['html', 'xml'])) 

def _render(template, context):
    html_template = env.get_template(str(template))
    html_content = html_template.render(context)
    return html_content

def render_template(template, **context):
    content = _render(template, context)
    return html(content)

if __name__ == '__main__':
    from sanic import Sanic
    app = Sanic()

    @app.route('/')
    async def index(request):
        return render_template('home.html')
    
    app.run(host = 'localhost', port = 4040, debug = True)