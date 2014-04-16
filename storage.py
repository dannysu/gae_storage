import webapp2
import json
from google.appengine.ext import db

class Data(db.Model):
    identifier = db.StringProperty(required=True)
    version = db.IntegerProperty(required=True)
    content = db.BlobProperty(required=True)

class MainPage(webapp2.RequestHandler):
    def latest(self, identifier):
        q = Data.gql("WHERE identifier = :1 ORDER BY version DESC LIMIT 1", identifier)
        latest = q.get()
        return latest

    def get(self, identifier):

        self.response.headers["Access-Control-Allow-Origin"] = "*"
        self.response.headers["Content-Type"] = "application/json"

        data = None

        version = self.request.get('v')
        if version != '':
            try:
                q = Data.gql("WHERE identifier = :1 AND version = :2", identifier, int(version))
                data = q.get()
            except ValueError:
                pass
        else:
            data = self.latest(identifier)

        if data != None:
            self.response.out.write(json.dumps({'success': True, 'data': data.content, 'version': data.version, 'identifier': data.identifier}))
        else:
            self.response.set_status(404);

    def post(self, identifier):

        self.response.headers["Access-Control-Allow-Origin"] = "*"
        self.response.headers["Content-Type"] = "application/json"

        latest = self.latest(identifier)
        version = 1
        if latest != None:
            version = latest.version
            # Only increment the version if content is different
            if latest.content != self.request.body:
                version += 1

        data = Data(key_name=identifier+':'+str(version),
                    identifier=identifier,
                    version=version,
                    content=self.request.body)
        try:
            data.put()
            self.response.out.write(json.dumps({'success': True, 'version': version, 'identifier': identifier}))
        except db.TransactionFailedError:
            self.response.out.write(json.dumps({'success': False, 'version': version, 'identifier': identifier}))

app = webapp2.WSGIApplication([
        ('/([0-9a-zA-Z\-_]*)', MainPage)
    ],
    debug=False)
