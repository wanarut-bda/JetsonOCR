from pywebio.input import *
from pywebio.output import *
from pywebio.session import *

web_html = open("web_html.html", "r").read()
img = open('cur_pic.png', 'rb').read()
put_image(img, width='1280px')
put_html(web_html)