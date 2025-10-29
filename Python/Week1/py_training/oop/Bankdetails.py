class Bankdetails:
    def __init__(self, custid, cname,bal):
        self.custid = custid
        self.cname = cname
        self.bal = bal

    def mssg(self):
        print("Welcome to BOI PEOPL'S BANK FOR PEOPLE")

    def display(self):
        print(f'{self.custid}')