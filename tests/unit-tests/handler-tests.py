from berkshire import app

from mock import Mock
from nose_parameterized import parameterized
from tornado.testing import AsyncHTTPTestCase

import http
import simplejson as json


class TestGenericResourceEndpoint(AsyncHTTPTestCase):
    """Tests the shared functionality that all the request
    handlers have.

    The tests that are run are:
        - assertion of status codes
        - assertion of the database abstraction being called

    Instead of using separate test classes for each handler that test the
    same functionality, it's more efficient to parameterize the routes that
    we are testing.
    """
    def get_app(self):
        self.__dbs = self.__get_dbs()

        return app.make_app(activity_db=self.__dbs['activity']['db'],
                            group_db=self.__dbs['group']['db'])

    @parameterized.expand([
        ('/activity/123', 'activity', '123'),
        ('/group/456', 'group', '456'),
    ])
    def test_should_get_resource(self, route, db_id, resource_id):
        # given

        # when
        response = self.fetch(route)
        db = self.__dbs[db_id]['db']
        expected_body = self.__dbs[db_id]['response']

        # then
        assert response.code == http.HTTPStatus.OK
        assert 'application/json' in response.headers['Content-Type']
        assert response.body == json.dumps(expected_body).encode('utf-8')
        db.get.assert_called_with(id=resource_id)

    @parameterized.expand([
        ('/activity/', 'activity'),
        ('/activity/456', 'activity'),
        ('/group/', 'group'),
        ('/group/780131', 'group'),
    ])
    def test_should_not_get_activity(self, route, db_id):
        # given
        db = self.__dbs[db_id]['db']
        db.get = Mock(return_value=None)

        # when
        response = self.fetch(route)

        # then
        assert response.code == http.HTTPStatus.NOT_FOUND

    @parameterized.expand([
        ('/activity/123', {'name': 'Yolo'}, 'activity', '123'),
        ('/group/456', {'name': 'my-grouper'}, 'group', '456'),
    ])
    def test_should_put_resource(self, route, request_body_json,
                                 db_id, resource_id):
        # given
        request_body = json.dumps(request_body_json).encode('utf-8')

        # when

        response = self.fetch(route, method='PUT', body=request_body)
        db = self.__dbs[db_id]['db']

        # then
        assert response.code == http.HTTPStatus.CREATED
        db.upsert.assert_called_with(id=resource_id, obj=request_body_json)

    @parameterized.expand([
        ('/activity/123', 'activity', '123'),
        ('/group/456', 'group', '456'),
    ])
    def test_should_delete_resource(self, route, db_id, resource_id):
        # given

        # when

        response = self.fetch(route, method='DELETE')
        db = self.__dbs[db_id]['db']

        # then
        assert response.code == http.HTTPStatus.NO_CONTENT
        assert len(response.body) == 0
        db.delete.assert_called_with(id=resource_id)

    @parameterized.expand([
        ('/activity/', 'PUT'),
        ('/activity/', 'POST'),
        ('/group/', 'PUT'),
        ('/group/', 'POST'),
    ])
    def test_should_not_allow_method(self, route, method):
        # given
        request_body = json.dumps({'name': 'yar'}).encode('utf-8')

        # when
        response = self.fetch(route, method=method,
                              body=request_body)

        # then
        assert response.code == http.HTTPStatus.METHOD_NOT_ALLOWED

    def __get_dbs(self):
        """Mocks the databases that are used by the request handlers."""
        get_responses = {
            'activity': {'activityId': '123'},
            'group': {'name': 'my-grouper'}
        }
        dbs = {}
        for k, v in get_responses.items():
            db = Mock()
            db.get = Mock(return_value=v)
            dbs[k] = {'db': db, 'response': v}
        return dbs
