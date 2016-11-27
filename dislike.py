###############################################################################
# MIT License
#
# Copyright (c) 2016 omegafrost
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
###############################################################################

from urllib.request import build_opener, HTTPCookieProcessor
from urllib.parse import urlencode
from http.cookiejar import CookieJar
from getpass import getpass
import zlib, base64

###############################################################################
#
###############################################################################

cookies = CookieJar()
opener = build_opener(HTTPCookieProcessor(cookies))
opener.addheaders = [('User-Agent', 
"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"),
("Host", "forum.outerspace.com.br"), ("Referer", 
"http://forum.outerspace.com.br/index.php")]

###############################################################################
#
###############################################################################

_xfToken = ""

def update_token(content):
    global _xfToken

    s = '<input type="hidden" name="_xfToken" value="'
    i = content.find(s)
    if i >= 0:
        i = i + len(s)
        _xfToken = content[i:content.find('"', i)]

def get(url):
    
    response = opener.open(url)
    content = response.read().decode()
    update_token(content)

    return content

def post(url, data):

    data = dict(data)
    data.update((("_xfToken", _xfToken),))
    data = urlencode(data).encode()
    
    response = opener.open(url, data)
    content = response.read().decode()
    update_token(content)

    return content

###############################################################################
#
###############################################################################

def login():

    username = input('Username: ')
    password = getpass('Password: ')

    print('logging in... ', end='', flush=True)

    page = post('http://forum.outerspace.com.br/index.php?login/login', {
        "login"         : username, 
        "password"      : password, 
        "register"      : "0",
        "remember"      : "0",
        "cookie_check"  : "0",
        "redirect"      : "http://forum.outerspace.com.br/index.php",
    })

    if page.find('section visitorPanel') < 0:
        print('failed!')
        print(page)
        raise Exception("Login failed!")

    print('ok.')

###############################################################################
#
###############################################################################

def dislike_one(p):

    url = 'http://forum.outerspace.com.br/index.php?%s/like' % p
    page = get(url)

    if page.find('value="Curtir (remover) Post"') >= 0:

        post(url, {})
        return True

    elif page.find('value="Aprovar Post"'):

        return False

    else:

        raise Exception('Uh oh! (dislike_one)')

###############################################################################
#
###############################################################################

def dislike(posts):

    login()

    print('going through %d posts...' % len(posts))

    for p in posts:

        # Posts or Profile posts
        if p[0:2] == 'po' or p[0:2] == 'pr':

            pass

        # Threads
        elif p[0:2] == 'th':

            # Find the first post of the thread            
            url = 'http://forum.outerspace.com.br/index.php?%slike' % post
            page = get(url)
            s = '/like'
            i = page.find(s)

            if i < 0:
                raise Exception('Uh oh! (i)')

            j = page.rfind('posts', 0, i)

            if j < 0:
                raise Exception('Uh oh! (j)')

            # Set p as the post id
            p = page[i:j]

        else:
            raise Exception('Unknown option %s' % p)

        print('-' if dislike_one(p) else '.', end='', flush=True)

###############################################################################
# Post list compressed using zlib and encoded in base 64
###############################################################################

posts = ''.join("""
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
+0bK7B4y7pfWdj1Yj36ZZX6wnmJlp7+u5+vLyZrMxQrguHc7dabr6fXw9FWJzf3O719+en6w7nw+fPv
2x/lsdWl1YjRb1uwRX+zZh9OPw/XpYtLm2crh8XpGQRjsD89uZW34n6/nt4/a3xd9+3qw+jo9375ZDc
KyaUX8/fysirLWd1XH+/6k8itz0vWrUHvrs6cp3N4/WakdD1e7zxrUt9Oft+9+k32iVxXM+fF8kzV6x
1yCeHvHW2VYPq3Ajvff1d+sQ+pjD3vn0Pftz32Wt1nOu8i0B073r/fH5yng7LquHV/sr/l4XB9/6+bK
5IOaipXG+ftx6YD2pYfv9oUmSvfss3hnl72eH57uT3vX1Tuta/w8vhf2/hartmd1nv0lU1TM5MLnTe3
4dHxUKg83KSSBpqJ9UkYt+5JwM3HrD7sk72q6ZZ4W+5aejRx31+O/D/cX9VVroJYJG8e+WnPbS9cSOB
7sh9+tXT/b47sp5F1E3n9/Pd0amEmHL2o4t97/oCZgY4+l89vl7rw/6r7kZR+OnvTFd5ZLG4u+Px+/m
Xj9cnk8vxzV5d4HIAnv4/PL+f7HbE+vuP9W/TZcu/qzj7DLD8f3In+S6HJlfn603rEXy9tbvjwf9MD7
W+02pTvt/GtzPP3x9f71/NYgreQPJihPTxpqXq0mrW+qu6R5lMHbsw9fHu5V9bvYfTi+nNRzno9fZgk
8zAH4+3EKmNT92HH87dVuON6/anyco8/xOu+ay3Fvd81c3Jq11fksJrvCb7z6lvvTtAjJlVdJFBuhvx
0frL5mwn4g/KmfJbDt7fvY8Gppq26t0r+rub2V85P1fbUJS+/ycv55uQ1BX46P5yl/63629PuYuOdqN
lFTPX5qdLh+ub9YUia5rcatFViOrcddrZc+P86R+Od8aJti7u75/FO5+aKk53LjW9L/ujzf30nl4DAy
X2KJSHIe9oRM1P18vZ/iRFL7rXvpzutUXKRkzLxPy/TbC34cX66vj2rnv0u+XH47fX1RUsfDH3uWb8n
ilUqleOn28HB5fvqu0e163nUc+/zLnQ3jlvSLWrsNjyYJDl9fn62iTrNDWo/7djT6clJbqbut9i3Fve
6fLr+fHi6PNh5ZCZp0tWFH5aW2867+vPw4P9/p+eifN1VP+pWpNKc7GxdnCWgAeFTbOn/9/aDzc6Y0v
smUww/79sPp7vxibdvasmmvtU0DxFuSGo+ep+Zjj1nWvv5+enk5nJ7alOSn+yn6ZioSs/aWx/mLWsXz
wcmJ67vq2H79w4rv/v54d/yLW/6uSKhet/qfMlZ/ydjFJOS9ZeHxr7LwuzVza6mP/yEL0yz/n7JQPsn
C6Q8rnmfrSRKyX6xyLn9dJD+O0tVezn+dn1D9PMV0xdfHm8Y2e/je+acEetbk5evF+vyrZNVUC77t1T
M13rpHzntL6vv5i3WPi3SZp/vrx4B7a/Pfjj8vz1N9nmLD+rxSmL63/6lw8ieFY5OEq/rwk37+efm55
+uviufl8jwnPdcY/kMJzQ18f52pXaZLuL9OjXsOnufHV4nM88P7mPJ3rQalAvX+mw220gqtuA833FN7
10PPf+7jzIPE4oNGPpuVqNDuLP+SGko2x/8PJZc+KbkHVcJflMDzxcSsvf3PN3lp2fzj8NvzXxZa2V0
YMPS9TGFt2TlZTZ3uL3sGrhd9wz4kSn8xSfdiiuesGumHD2rwL6/SrXT0rxNVz5fXx7uDyuf7j5db+7
IxTxLwdJsaTKl3//pyfGtuR9/cypihjz+maD9Pz88fg5vmdbOJ2N8md78c73/MX+3v5TeJKo1318OX8
5+mCNg0126citlR95mgvup1MxLuomKaZmgNcZZt0lxo0S5t4J8Doc3gTlbw92crPSU1D6X9T9UdP5Gw
3y7fpqbxF9X3MJ/6vzbDeD79dS3vsWvfa/k0BYU0QhuqdvVRCsth11zmh9nQs8+gbaiXZmza3unrXjr
Vd7N9mjMnFXruqylXs0v/4/r19V5CQ4+/DeE2CJm6edHIZx9qEut519el3h7fNMDfVIj2Hq1K+InrXl
i/23Rynw9+eT7LInB38XNC++F51s2nevX7lPu7WsbrfEkYq7L7j8fTvXqPTRieZMlQId8Eh82vLpfv9
zY3fjCZ/TDnFMebynXnmoNSnsdlr9m3lvrdBPfRZdmmgk+Xu7c3vJXUszWSvUG5NNsM+bikabOWo02x
bXZguvz1TYE8fj19uWigVe72b23dWwJ+O9/faxS8+9f5648PqW+5sRZsmszp5/n+U+Fvc5NcPp3q2ND
/Yk3mQdYca1c/THe7WSdeny6PUxO8Wh86nXdLxbR6PZyev2rSf/iYQJqc+brPIV/30niYJfNeZw02JN
X4RRqXdPqbWmvt9fn0Xdaguw9Tjwblo32UbDhKJVXXjL/ZzOgoyT1zc9OV3jqHiT2JQxOwr1YUb8akX
bwc7t8m7LcDot77+vn6ePq3DBznr9Jsny9/nh4Ps1beJy6mjNmIokdjX6Xwg2kp1npNf52d5fTHkyk2
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
DypR1HF/AdgG38c=""".split()).encode()

###############################################################################
# Main
###############################################################################

if __name__ == "__main__":
    posts = zlib.decompress(base64.b64decode(posts))
    dislike(posts.decode().split())