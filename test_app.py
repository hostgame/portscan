import unittest
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web
from app import create_app

class PortScanTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = create_app()
        return app

    @unittest_run_loop
    async def test_valid_target(self):
        resp = await self.client.request('GET', '/127.0.0.1/8080/8081')
        assert resp.status == 200

    @unittest_run_loop
    async def test_invalid_ip(self):
        resp = await self.client.request('GET', '/345.0.0.1/8080/8081')
        assert resp.status == 400
        text = await resp.text()
        assert '{"error": "Invalid IP"}' == text

    @unittest_run_loop
    async def test_invalid_end_port(self):
        resp = await self.client.request('GET', '/127.0.0.1/8080/98081')
        assert resp.status == 400
        text = await resp.text()
        assert '{"error": "Invalid end port"}' == text

    @unittest_run_loop
    async def test_invalid_port(self):
        resp = await self.client.request('GET', '/127.0.0.1/98080/8081')
        assert resp.status == 400
        text = await resp.text()
        assert '{"error": "Invalid begin port"}' == text

    @unittest_run_loop
    async def test_open_port(self):
        # 45.33.32.156 is scanme.nmap.org
        resp = await self.client.request('GET', '/45.33.32.156/443/443')
        assert resp.status == 200
        text = await resp.text()
        print(text)
        assert '[{"port": 443, "state": "close"}]' == text

    @unittest_run_loop
    async def test_open_port(self):
        # 45.33.32.156 is scanme.nmap.org
        resp = await self.client.request('GET', '/45.33.32.156/80/80')
        assert resp.status == 200
        text = await resp.text()
        assert '[{"port": 80, "state": "open"}]' == text

if __name__ == '__main__':
    unittest.main()
