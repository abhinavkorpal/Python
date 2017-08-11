#!/bin/py

import weakref, gc

class A:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)
