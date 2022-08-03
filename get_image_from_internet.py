

def enable_esp32():
    from network_esp32 import wifi

    if wifi.isconnected() == False:
        for i in range(5):
            try:
                wifi.reset(is_hard=True)
                print('try AT connect wifi...')
                wifi.connect(SSID, PASW)
                if wifi.isconnected():
                    break
            except Exception as e:
                print(e)
    print('network state:', wifi.isconnected(), wifi.ifconfig())


enable_esp32()

try:
    import usocket as socket
except:
    import socket

class Response:

    def __init__(self, f):
        self.raw = f
        self.encoding = "utf-8"
        self._cached = None

    def close(self):
        if self.raw:
            self.raw.close()
            self.raw = None
        self._cached = None

    @property
    def content(self):
        if self._cached is None:
            try:
                self._cached = self.raw.read()
            finally:
                self.raw.close()
                self.raw = None
        return self._cached

    @property
    def text(self):
        return str(self.content, self.encoding)

    def json(self):
        import ujson
        return ujson.loads(self.content)

def request(method,url,data=None,json=None,headers={},stream=None,parse_headers=True):
    redir_cnt = 1
    if json is not None:
        assert data is None
        import ujson
        data = ujson.dumps(json)

    while True:
        try:
            proto, dummy, host, path = url.split("/", 3)
        except ValueError:
            proto, dummy, host = url.split("/", 2)
            path = ""
        if proto == "http:":
            port = 80
        elif proto == "https:":
            port = 443
        else:
            raise ValueError("Unsupported protocol: " + proto)

        if ":" in host:
            host, port = host.split(":", 1)
            port = int(port)

        ai = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)
        ai = ai[0]

        resp_d = None
        if parse_headers is not False:
            resp_d = {}

        s = socket.socket(ai[0], ai[1], ai[2])
        try:
            s.connect(ai[-1])
            if proto == "https:":
                s = ssl.wrap_socket(s, server_hostname=host)
            s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
            if not "Host" in headers:
                s.write(b"Host: %s\r\n" % host)
            # Iterate over keys to avoid tuple alloc
            for k in headers:
                s.write(k)
                s.write(b": ")
                s.write(headers[k])
                s.write(b"\r\n")
            if json is not None:
                s.write(b"Content-Type: application/json\r\n")
            if data:
                s.write(b"Content-Length: %d\r\n" % len(data))
            s.write(b"Connection: close\r\n\r\n")
            if data:
                s.write(data)

            l = s.readline()
            #print(l)
            l = l.split(None, 2)
            status = int(l[1])
            reason = ""
            if len(l) > 2:
                reason = l[2].rstrip()

            while True:
                    l = s.readline()
                    if not l or l == b"\r\n":
                        break
                    #print(l)

                    if l.startswith(b"Transfer-Encoding:"):
                        if b"chunked" in l:
                            raise ValueError("Unsupported " + l)
                    elif l.startswith(b"Location:") and 300 <= status <= 399:
                        if not redir_cnt:
                            raise ValueError("Too many redirects")
                        redir_cnt -= 1
                        url = l[9:].decode().strip()
                        #print("redir to:", url)
                        status = 300
                        break

                    if parse_headers is False:
                        pass
                    elif parse_headers is True:
                        l = l.decode()
                        k, v = l.split(":", 1)
                        resp_d[k] = v.strip()
                    else:
                        parse_headers(l, resp_d)

        except OSError:
            s.close()
            raise

        if status != 300:
            break

    resp = Response(s)
    resp.status_code = status
    resp.reason = reason
    if resp_d is not None:
         resp.headers = resp_d
    return resp

def head(url, **kw):
    return request("HEAD", url, **kw)

def get(url, **kw):
    return request("GET", url, **kw)

def post(url, **kw):
    return request("POST", url, **kw)

def put(url, **kw):
    return request("PUT", url, **kw)

def patch(url, **kw):
    return request("PATCH", url, **kw)

def delete(url, **kw):
    return request("DELETE", url, **kw)

headers = {
    "User-Agent": "MaixPy"
}

res = get("http://static.sipeed.com/example/MaixPy.jpg", headers=headers)

print("response:", res.status_code)

content = res.content

print("get img, length:{}, should be:{}".format(
    len(content), int(res.headers['Content-Length'])))

if len(content) != int(res.headers['Content-Length']):
    print("download image failed, not complete, try again")
else:
    print("save to /flash/MaixPy.jpg")
    f = open("/flash/MaixPy.jpg", "wb")
    f.write(content)
    f.close()
    del content
    print("save ok")
    print("display")
    import lcd
    import image
    img = image.Image("/flash/MaixPy.jpg")
    lcd.init()
    lcd.display(img)

