import logging
import webapp2
#from google.appengine.api import images
import Image, ImageDraw
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import StringIO

# datastore entities
class Being(db.Model):
	designation = db.StringProperty();
	federation	= db.StringProperty();

class Tile(db.Model):
	x 		= db.IntegerProperty;
	y 		= db.IntegerProperty;
	z		= db.IntegerProperty;
	contentkey	= blobstore.BlobReferenceProperty();

class MainPage(webapp2.RequestHandler):
    def get(self):
		logging.info('MainPage')
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Hello, webapp2 World!')
		return

class OpenIDHandler(webapp2.RequestHandler):
	def get(self):
		pass
		

class TileUploader(blobstore_handlers.BlobstoreUploadHandler):
	def get(self):
		logging.info('TileUploader GET')
		# the upload url
		upload_url = blobstore.create_upload_url('/upload/')
	
		# and a short form
		self.response.out.write('<html><body>')
		self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
		self.response.out.write("""Coordinates: Zoom: <input name="z"> x: <input name="x"> y: <input name="y"><br /> 
								Upload File: <input type="file" name="file"><br> 
								<input type="submit"
								name="submit" value="Submit"> </form></body></html>""")
		return

	def post(self):
		logging.info('TileUploader POST')
		# the uploaded tile is already in the blobstore
		upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
		
		# and this is the corresponding blobinfo entity in the datastore
		blob_info = upload_files[0]
		self.redirect('/serve/%s' % blob_info.key())
		
		# we need some additional data, the coordinates (x, y, z)
		x = self.request.get('x')
		y = self.request.get('y')
		z = self.request.get('z')
		
		# todo: assign this as a created tile to the current user
		# createdTile = new Tile
		# createdTile.x = x
		# createdTile.y = y
		# createdTile.z = z
		# createdTile.contentKey = blob_info.key()
		
		return

class TileLoader(webapp2.RequestHandler):
	def get(self, zs, xs, ys):
		logging.info('TileLoader')
		return
		
		
class TileGenerator(webapp2.RequestHandler):
	def get(self, zs, xs, ys):
		logging.info('TileGenerator')
		# TODO check if title exists, retrieve
		z, x, y = tuple(map(lambda x: int(x), [zs, xs, ys]))
		
        # TODO check if a stored tile matches the requested one exactly 
		if True :
			# PIL setup
			size = 256, 256
			tile = Image.new("RGB", size, (255, 255, 255))
			draw = ImageDraw.Draw(tile)
			
			# draw boundary
			draw.rectangle([(0,0), tile.size], fill=(255, 255, 255), outline=(0,0,0))
			
			# draw label
			label = ' x: %d y: %d zoom: %d' % (x, y, z)
			labelwidth, labelheight = draw.textsize(label)
			tilewidth, tileheight   = tile.size
			labelposition 			= tuple([(tilewidth-labelwidth)/2, (tileheight-labelheight)/2])
			draw.text(labelposition, label, fill=(0,0,0))
			del draw

			output = StringIO.StringIO()
			tile.save(output, format="png")
			output_data = output.getvalue()
			output.close()
			
			self.response.headers['Content-Type'] = 'image/png'
			self.response.out.write(output_data)
		# TODO store to blobstore
			
		else :
			# TODO serve from blobstore
			pass
		return

application = webapp2.WSGIApplication([
	webapp2.Route(r'/foo/', handler=MainPage),
	webapp2.Route(r'/upload/', handler=TileUploader),
	webapp2.Route(r'/_ah/login_required', handler=OpenIDHandler),
	webapp2.Route(r'/tile/<zs:\d+>/<xs:\d+>/<ys:\d+>.png', handler=TileGenerator),
], debug=True)
