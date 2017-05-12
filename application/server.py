# -*- coding: utf-8 -*-

from backend import app

def main():
    import os
    debug = os.environ["DEBUG"] == "True"
    app.run(debug=debug, host="0.0.0.0")


if __name__ == "__main__":
    main()
