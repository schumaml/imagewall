import logging
import webapp2
#from google.appengine.api import images
import Image, ImageDraw
from google.appengine.ext import blobstore
import StringIO

class MainPage(webapp2.RequestHandler):
    def get(self):
		logging.info('MainPage')
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('Hello, webapp2 World!')
		return

class TileGenerator(webapp2.RequestHandler):
	def get(self, zs, xs, ys):
		logging.info('TileGenerator')
		# TODO check if title exists, retrieve
		z, x, y = tuple(map(lambda x: int(x), [zs, xs, ys]))
		
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
	webapp2.Route(r'/foo', handler=MainPage),
	webapp2.Route(r'/tile/<zs:\d+>/<xs:\d+>/<ys:\d+>.png', handler=TileGenerator),
], debug=True)

