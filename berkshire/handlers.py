import http
import simplejson as json

from datetime import datetime
from tornado.web import RequestHandler

try:
    from .validators import is_payload_valid
except ImportError:
    from validators import is_payload_valid


DATETIME_FORMAT = '%Y-%m-%dT%X'


class BaseRequestHandler(RequestHandler):
    """Serves as the base class of all the request handlers used in this
    application.

    It contains the common methods that are shared by the
    deriving request handler classes.
    """
    def __get_error_response(self, message):
        """Returns the payload of an unsuccessful response.

        Args:
            message: The error message.

        Returns:
            A dictionary representing the payload of the response.
        """
        return {
            'err': message,
            'datetime': datetime.now().strftime(DATETIME_FORMAT)
        }

    def options(self, o):
        """Handles the OPTIONS method."""
        self.set_status(http.HTTPStatus.NO_CONTENT)
        self.finish()

    def get_cors_kwargs(self):
        """Creates a CORS configuration dictionary.

        Used by the `set_default_headers` method to set CORS-related headers.

        Returns:
            A dictionary containing CORS configuration.
        """
        allowed_headers = 'Origin, X-Requested-With, User-Agent, ' \
                          'Content-Type, Accept'
        allowed_methods = 'GET, HEAD, POST, PUT, DELETE, OPTIONS'
        return {
            'origin': '*',
            'headers': allowed_headers,
            'methods': allowed_methods
        }

    def set_default_headers(self):
        """Sets the default headers of the response."""
        cors = self.get_cors_kwargs()
        self.set_header("Access-Control-Allow-Origin", cors['origin'])
        self.set_header("Access-Control-Allow-Headers", cors['headers'])
        self.set_header('Access-Control-Allow-Methods', cors['methods'])


class ActivitiesHandler(BaseRequestHandler):
    """Serves as the request handler for /activities endpoint."""
    def initialize(self, db):
        self.__db = db

    def get_cors_kwargs(self):
        cors = super(ActivitiesHandler, self).get_cors_kwargs()
        cors['methods'] = 'GET, POST, OPTIONS'
        return cors

    def get(self, group_id):
        """Gets the list """
        self.set_status(http.HTTPStatus.OK)
        self.finish()

    def post(self, group_id):
        """Handles the POST method of the /activities endpoint.

        Creates a new activity object."""
        # payload = json.loads(self.request.body.decode('utf-8'))
        # activity_id = payload.get('activity_id')
        # if not activity_id:
        #     self.set_status(http.HTTPStatus.INTERNAL_SERVER_ERROR)
        #     self.write({'error': 'Missing activity ID'})
        #
        # self.__db.upsert(id=payload['activity_id'], obj=payload)
        self.set_status(http.HTTPStatus.CREATED)
        # self.write({'message': 'Success'})
        self.finish()

class ActivityHandler(BaseRequestHandler):
    """Serves as the request handler for /activity endpoint."""
    def initialize(self, db):
        self.__db = db

    def get_cors_kwargs(self):
        cors = super(ActivityHandler, self).get_cors_kwargs()
        cors['methods'] = 'GET, PUT, DELETE, OPTIONS'
        return cors

    def put(self, group_id, activity_id):
        """Handles the PUT method of the /activity endpoint.

        Creates or updates an activity object.

        Args:
            activity_id: The unique identifier of the activity.
        """
        # payload = json.loads(self.request.body.decode('utf-8'))
        # self.__db.upsert(id=activity_id, obj=payload)
        self.set_status(http.HTTPStatus.CREATED)
        self.finish()

    def get(self, group_id, activity_id):
        """Handles the GET method of the /activity endpoint.

        Gets an activity object.

        Args:
            activity_id: The unique identifier of the activity.
        """
        # activity = self.__db.get(id=activity_id)
        # if not activity:
        #     self.set_status(http.HTTPStatus.NOT_FOUND)
        #     self.finish()
        # else:
        self.set_status(http.HTTPStatus.OK)
        self.finish()

    def delete(self, group_id, activity_id):
        """Handles the DELETE method of the /activity endpoint.

        Deletes an activity object.

        Args:
            activity_id: The unique identifier of the activity.
        """
        # self.__db.delete(id=activity_id)
        self.set_status(http.HTTPStatus.NO_CONTENT)
        self.finish()


class GroupHandler(BaseRequestHandler):
    """Serves as the request handler for /group endpoint."""
    def initialize(self, db):
        self.__db = db

    def get_cors_kwargs(self):
        cors = super(GroupHandler, self).get_cors_kwargs()
        cors['methods'] = 'GET, PUT, DELETE, OPTIONS'
        return cors

    def put(self, group_id):
        """Handles the PUT method of the /group endpoint.

        Creates or updates a group object.

        Args:
            group_id: The unique identifier of the group.
        """
        payload = json.loads(self.request.body.decode('utf-8'))

        is_valid = is_payload_valid(payload)

        if not is_valid:
            self.set_status(http.HTTPStatus.BAD_REQUEST)
            self.finish()

        self.__db.upsert(id=group_id, obj=payload)
        self.set_status(http.HTTPStatus.CREATED)
        self.finish()

    def get(self, group_id):
        """Handles the GET method of the /group endpoint.

        Gets an group object.

        Args:
            group_id: The unique identifier of the group.
        """
        group = self.__db.get(id=group_id)
        if group:
            self.set_status(http.HTTPStatus.OK)
            self.write(group)
        else:
            self.set_status(http.HTTPStatus.NOT_FOUND)
            self.finish()

    def delete(self, group_id):
        """Handles the DELETE method of the /group endpoint.

        Deletes an group object.

        Args:
            group_id: The unique identifier of the group.
        """
        self.__db.delete(id=group_id)
        self.set_status(http.HTTPStatus.NO_CONTENT)
        self.finish()


class PingHandler(BaseRequestHandler):
    """Serves as the request handler for /ping endpoint."""
    def get_cors_kwargs(self):
        cors = super(PingHandler, self).get_cors_kwargs()
        cors['methods'] = 'GET, OPTIONS'
        return cors

    def get(self):
        """Handles the GET method of the /activity endpoint.

        Gets the date and time when the request is made. This is usually used
        for checking if the application is online.
        """
        self.set_status(http.HTTPStatus.OK)
        self.write({'datetime': datetime.now().strftime(DATETIME_FORMAT)})
