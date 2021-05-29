#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Copyright (c) 2021 Lorenzo Carbonell <a.k.a. atareao>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import uvicorn
import toml
from keyval import KeyVal
from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.responses import PlainTextResponse, HTMLResponse


DATABASE = '/app/db/keyval.db'
CONFIG = '/app/config/keyval.toml'
HTML_403_PAGE = "<!doctype html><html><body><p>403 Forbidden</p></body></html>"
DATA  = toml.load(CONFIG)
ENDPOINTS = DATA['endpoint']
TOKENS = DATA['tokens']
SERVER = DATA['server']
PORT = DATA['port']


routes = [
        Route("/api/1.0/{endpoint}/{key}", KeyValAPI),
]


async def forbidden(request, exc):
    return HTMLResponse(content=HTML_403_PAGE, status_code=exc.status_code)


class KeyValAPI(HTTPEndpoint):

    async def get(self, request):
        endpoint = request.path_params['endpoint']
        key = request.path_params['key']
        token = request.headers['Token']
        if endpoint in ENDPOINTS and token in TOKENS:
            keyVal = KeyVal(DATABASE)
            result = keyVal.get(key)
            return PlainTextResponse(result)
        return HTMLResponse(content=HTML_403_PAGE, status_code=403)

    async def post(self, request):
        endpoint = request.path_params['endpoint']
        key = request.path_params['key']
        token = request.headers['Token']
        if endpoint in ENDPOINTS and token in TOKENS:
            keyVal = KeyVal(DATABASE)
            result = keyVal.get(key)
            return PlainTextResponse(result)
        return HTMLResponse(content=HTML_403_PAGE, status_code=403)


if __name__ == '__main__':
    keyVal = KeyVal(DATABASE)
    app = Starlette(routes=routes)
