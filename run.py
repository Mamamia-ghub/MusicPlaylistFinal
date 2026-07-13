import os
import sys
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

dotenv_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path)

print(f"[DEBUG ENGINE] Verifying Last.fm API Key: {os.getenv('LASTFM_API_KEY')}")

from __init__ import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)








