# coding: utf-8

from huhuran.config import SERVER_PORT, DEBUG
from huhuran.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run('0.0.0.0', SERVER_PORT, debug=DEBUG)
