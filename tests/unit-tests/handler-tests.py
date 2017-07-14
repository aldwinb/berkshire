from berkshire import app
from mock import Mock
from nose_parameterized import parameterized
from tornado.testing import AsyncHTTPTestCase

import simplejson as json


class TestActivityEndpoint(AsyncHTTPTestCase):

    def setUp(self):

        self.__get_response = {'activityId': '123'}
        self.__put_response = {'message': 'Success'}
        db = Mock()
        db.get = Mock(return_value=self.__get_response)
        self.__db = db

        super(TestActivityEndpoint, self).setUp()

    def get_app(self):
        return app.make_app(db=self.__db)

    def test_should_get_activity(self):
        # given

        # when
        response = self.fetch('/activity/123')

        # then
        assert response.code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert response.body == json.dumps(self.__get_response).encode('utf-8')

    def test_should_not_get_activity(self):
        # given

        # when
        response = self.fetch('/activity')

        # then
        assert response.code == 404

    def test_should_put_activity(self):
        # given
        request_body = json.dumps({'name': 'Yolo'}).encode('utf-8')

        # when

        response = self.fetch('/activity/123', method='PUT', body=request_body)

        # then
        assert response.code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert response.body == json.dumps(self.__put_response).encode('utf-8')

    @parameterized.expand([
        ('PUT'),
        ('POST')
    ])
    def test_should_not_allow_method(self, method):
        # given
        request_body = json.dumps({'name': 'yar'}).encode('utf-8')

        # when
        response = self.fetch('/activity/', method=method,
                              body=request_body)

        # then
        print('Response code: {}'.format(response.code))
        assert response.code == 405
