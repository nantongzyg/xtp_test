#!/home/vagrant/anaconda2/bin/python
# -*- encoding: utf-8 -*-


class Attribute:

    # --------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        if len(args) >= 1 and type(args[0]) is dict:
            self.attributes = args[0]
        else:
            self.attributes = {}

    # --------------------------------------------------
    def __str__(self):
        return self.attributes.__str__()

    # --------------------------------------------------
    def __len__(self):
        return len(self.attributes)

    # --------------------------------------------------
    def __getattr__(self, key):
        """属性提取"""
        if key in self.attributes:
            return self.attributes[key]
        else:
            raise AttributeError(key)

    # --------------------------------------------------
    def __getitem__(self, key):
        """属性提取"""
        if key in self.attributes:
            return self.attributes[key]
        else:
            raise AttributeError(key)

    # --------------------------------------------------
    def __setitem__(self, key, value):
        """属性重赋值"""
        self.attributes[key] = value

    # --------------------------------------------------
    def __delitem__(self, key):
        if key in self.attributes:
            del self.attributes[key]
        else:
            raise AttributeError(key)

    # --------------------------------------------------
    def __iter__(self):
        return iter(self.attributes)

    # --------------------------------------------------
    def __reversed__(self):
        return reversed(self.attributes)

    # --------------------------------------------------
    def all(self):
        """属性集"""
        return self.attributes
