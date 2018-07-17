# -*- coding:utf-8 -*-
import os
from kiwi.app import KiwiLoader

app = KiwiLoader.bootstrap('kiwi_config.example.yml', 'logging_config.example.ini')

if __name__ == "__main__":
    app.start()
