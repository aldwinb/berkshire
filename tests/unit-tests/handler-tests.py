from berkshire import app

from mock import Mock
from nose_parameterized import parameterized
from tornado.testing import AsyncHTTPTestCase

import http
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
        assert response.code == http.HTTPStatus.OK
        assert 'application/json' in response.headers['Content-Type']
        assert response.body == json.dumps(self.__get_response).encode('utf-8')
        self.__db.get.assert_called_with(id='123')

    def test_should_not_get_activity(self):
        # given

        # when
        response = self.fetch('/activity')

        # then
        assert response.code == http.HTTPStatus.NOT_FOUND

    def test_should_put_activity(self):
        # given
        request_body_json = {'name': 'Yolo'}
        request_body = json.dumps(request_body_json).encode('utf-8')

        # when

        response = self.fetch('/activity/123', method='PUT', body=request_body)

        # then
        assert response.code == http.HTTPStatus.CREATED
        self.__db.upsert.assert_called_with(id='123', obj=request_body_json)

    def test_should_delete_activity(self):
        # given

        # when

        response = self.fetch('/activity/123', method='DELETE')

        # then
        print('Response body: {}'.format(response.body))
        assert response.code == http.HTTPStatus.NO_CONTENT
        assert len(response.body) == 0
        self.__db.delete.assert_called_with(id='123')

    @parameterized.expand([
        ('PUT'),
        ('POST'),
    ])
    def test_should_not_allow_method(self, method):
        # given
        request_body = json.dumps({'name': 'yar'}).encode('utf-8')

        # when
        response = self.fetch('/activity/', method=method,
                              body=request_body)

        # then
        print('Response code: {}'.format(response.code))
        assert response.code == http.HTTPStatus.METHOD_NOT_ALLOWED
