from api.app import app
import os

port = int(os.environ.get('PORT', 5000))
debug = os.environ.get('DEBUG', True)
app.run(host='0.0.0.0', debug = debug, port=port)
