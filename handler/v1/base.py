import json
import re
from typing import Optional, Awaitable

from tornado import web

from db.base import session


class BaseHandler(web.RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def send_json(self, data=None, errcode=200, errmsg='', status_code=200):
        if data is None:
            data = {}
        res = {
            'errcode': errcode,
            'errmsg': errmsg if errmsg else '请求成功'
        }
        res.update(data)

        json_str = json.dumps(res)

        json_p = self.get_argument('jsonp', '')
        if json_p:
            json_p = re.sub(r'[^\w.]', '', json_p)
            self.set_header('Content-Type', 'text/javascript; charet=UTF-8')
            json_str = '%s(%s)' % (json_p, json_str)
        else:
            self.set_header('Content-Type', 'application/json')

        origin = self.request.headers.get("Origin")
        origin = '*' if not origin else origin

        self.set_header("Access-Control-Allow-Origin", origin)
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        self.set_header('Access-Control-Allow-Methods', 'OPTIONS, GET, POST, PUT, DELETE')

        self.set_status(status_code)
        self.write(json_str)
        self.finish()

    def on_finish(self):
        session.close()


# noinspection PyBroadException,PyPep8Naming,PyPep8Naming
class APIHandler(BaseHandler):
    """
    确保只有三种返回结果
    1. dict(errcode=404, errmsg='Not Found', data=[])
    2. dict(errcode=500, errmsg='报错信息', data=[])
    3. dict(errcode=200, errmsg='服务正常', data=data)

    实现类只使用，self.send_json(xxx)返回结果，不要指定errcode和errmsg,有需要统一添加

    返回data定义:
        若没有数据，返回空列表

    自定义异常：
        使用 assert False, msg 其中[msg]作为返回给客户端的信息
    """
    NOT_FOUND = dict(status_code=404, errcode=404, errmsg='Not Found')

    async def common_get(self):
        return self.send_json(**self.NOT_FOUND)

    async def _common_post(self):
        return self.send_json(**self.NOT_FOUND)

    def data_received(self, chunk):
        pass

    async def get(self):
        try:
            return await getattr(self, '_get')()
        except AssertionError as e:
            if e.args:
                return self.send_json(errcode=500, errmsg=e.args[0])
            else:
                import traceback
                return self.send_json(errcode=500, errmsg=traceback.format_exc())
        except Exception:
            import traceback
            traceback.print_exc()
            return self.send_json(errcode=500, errmsg=traceback.format_exc())

    async def post(self):
        try:
            return await getattr(self, "_post")()
        except AssertionError as e:
            if e.args:
                return self.send_json(errcode=500, errmsg=e.args[0])
            else:
                import traceback
                return self.send_json(errcode=500, errmsg=traceback.format_exc())
        except Exception:
            import traceback
            traceback.print_exc()
            return self.send_json(errcode=500, errmsg=traceback.format_exc())

    async def put(self):
        try:
            return await getattr(self, "_put")()
        except AssertionError as e:
            if e.args:
                return self.send_json(errcode=500, errmsg=e.args[0])
            else:
                import traceback
                traceback.print_exc()
                return self.send_json(errcode=500, errmsg=traceback.format_exc())
        except Exception:
            import traceback
            return self.send_json(errcode=500, errmsg=traceback.format_exc())

    async def delete(self):
        try:
            return await getattr(self, "_delete")()
        except AssertionError as e:
            if e.args:
                return self.send_json(errcode=500, errmsg=e.args[0])
            else:
                import traceback
                traceback.print_exc()
                return self.send_json(errcode=500, errmsg=traceback.format_exc())
        except Exception:
            import traceback
            return self.send_json(errcode=500, errmsg=traceback.format_exc())

    def send_json(self, data=None, errcode=200, errmsg='', status_code=200):
        if not data:
            result = {'data': []}
        else:
            result = {'data': data}
        super().send_json(result, errcode, errmsg, status_code)


# noinspection PyBroadException,PyPep8Naming,PyPep8Naming
class MobileHandler(BaseHandler):
    NOT_FOUND = dict(status_code=404, errcode=404, errmsg='Not Found')

    async def common_get(self):
        return self.send_json(**self.NOT_FOUND)

    async def _common_post(self):
        return self.send_json(**self.NOT_FOUND)

    def data_received(self, chunk):
        pass

    async def get(self, method):
        try:
            if not method:
                return await getattr(self, 'common_get')()
            if not hasattr(self, method):
                return self.send_json(**self.NOT_FOUND)
            await getattr(self, method)()
        except AssertionError as e:
            if e.args:
                return self.send_json(errcode=500, errmsg=e.args[0])
            else:
                import traceback
                return self.send_json(errcode=500, errmsg=traceback.format_exc())
        except Exception:
            import traceback
            return self.send_json(errcode=500, errmsg=traceback.format_exc())

    async def post(self, method):
        try:
            if not method:
                return await getattr(self, '_%s' % 'common_post')()
            if not hasattr(self, '_%s' % method):
                return self.send_json(**self.NOT_FOUND)
            await getattr(self, '_%s' % method)()
        except AssertionError as e:
            if e.args:
                return self.send_json(errcode=500, errmsg=e.args[0])
            else:
                import traceback
                return self.send_json(errcode=500, errmsg=traceback.format_exc())
        except Exception:
            import traceback
            return self.send_json(errcode=500, errmsg=traceback.format_exc())

    def send_json(self, data=None, errcode=200, errmsg='', status_code=200):
        if not data:
            result = {'data': []}
        else:
            result = {'data': data}
        super().send_json(result, errcode, errmsg, status_code)
