import mimetypes
mimetypes.init()
mimetypes.add_type('application/wasm', '.wasm', strict=True)

print(mimetypes.guess_type('foo.wasm'))
assert mimetypes.guess_type('foo.wasm')[0] == 'application/wasm'

from http.server import test, SimpleHTTPRequestHandler
test(SimpleHTTPRequestHandler, port=3000)