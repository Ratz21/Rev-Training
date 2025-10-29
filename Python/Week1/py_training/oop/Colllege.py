class College:
    def __init__(self, ccode, cname):
        self._ccode = ccode
        self._cname = cname

    def set_ccode(self, ccode):
        self._ccode = ccode

    def get_ccode(self):
        return self._ccode

    def set_name(self, cname):
        self._cname = cname

    def get_name(self):
        return self._cname

    def __str__(self):
        return f"College Code: {self._ccode}, College Name: {self._cname}"

    def display(self):
        print(f"College Code: {self._ccode}, College Name: {self._cname}")