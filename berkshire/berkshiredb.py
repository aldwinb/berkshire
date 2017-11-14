import sys
import couchdb
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)


class DbContext(object):
    """The base class for all database contexts."""

    __context_types = {
        'couchdb': 'CouchDbContext',
    }

    def get(self, id):
        """Gets the database record associated with an identifier.

        This should be implemented by deriving classes.
        """
        raise NotImplementedError()

    def delete(self, id):
        """Deletes a database record associated with an identifier.

        This should be implemented by deriving classes.
        """
        raise NotImplementedError()

    def upsert(self, id, obj):
        """Creates or updates a database record.

        If the record doesn't exist, it gets created. Otherwise, it gets
        updated. This should be implemented by deriving classes.
        """
        raise NotImplementedError()

    @classmethod
    def create(cls, context_type, **kwargs):
        """Creates an instance of a DbContext class.

        This method follows a factory pattern in creating new DbContext
        instances.

        Args:
            context_type: A string indicating the type of DbContext class to
            instantiate.

        Returns:
            A new instance of a valid DbContext class.

        Raises:
            RuntimeError: An error occurred when the type of DbContext class
            being created is invalid.

        """
        this = sys.modules[__name__]
        try:
            context_class = cls.__context_types[context_type]
        except KeyError:
            raise RuntimeError('Invalid database context: {}'.format(
                context_type))

        return getattr(this, context_class)(**kwargs)


class CouchDbContext(DbContext):
    """A DbContext that wraps a CouchDb server."""

    DOCUMENT_RESERVED_KEYS = {'_id', '_rev'}

    def __init__(self, host, db_name):
        server = couchdb.Server(host)
        if db_name not in server:
            raise ValueError('Database \'{}\' doesn\'t exist'.format(db_name))

        self.__db = server[db_name]

    def get(self, id):
        """Gets the CouchDb document associated with the identifier.

        Args:
            id: A string that identifies the CouchDB document.

        Returns:
            If found, a dictionary without the special attributes that
            CouchDb adds (i.e. id and rev). If not, an empty dictionary.
        """
        doc = self.__db.get(id)
        if doc:
            for key in self.DOCUMENT_RESERVED_KEYS:
                doc.pop(key)

        return doc or {}

    def delete(self, id):
        """Deletes the CouchDB document associated with the identfier.

        The method will retrieve the document first, then attempt to delete.
        As long as it's getting a ResourceConflict error , it will
        repeat the retrieval-deletion process.

        Args:
            id: A string that identifies the CouchDB document.
        """

        # If document doesn't exist, just exit the loop and do nothing.
        conflict = True
        while conflict:
            doc = self.__db.get(id)
            if doc:
                try:
                    self.__db.delete(doc)
                    conflict = False
                except couchdb.ResourceConflict as e:
                    conflict = True
            else:
                conflict = False

    def upsert(self, id, obj):
        """Creates or updates a CouchDB document.

        Creates a new one if the document doesn't exist. Otherwise,
        it updates it.

        Args:
            id: A string that identifies the CouchDb document.
            obj: A dictionary representing the CouchDb document.

        Returns:
            An integer value indicating if the operation was an insert or
            update (0 = insert, 1 = update).
        """

        doc = self.__db.get(id)
        if doc:
            obj['_rev'] = doc.rev
            self.__db[id] = obj
        else:
            # Set the id of the document to the id that was passed as input
            obj['_id'] = id
            self.__db.save(obj)

        return 1 if doc else 0
