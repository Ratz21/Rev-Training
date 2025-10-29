from oop.Bankdetails import Bankdetails


class CreditsCards(Bankdetails):
    def __init__(self, custid, cname , bal , creditscore, status):
        super().__init__(custid,cname,bal)

        self.creditscore = creditscore
        self.status = status

    def mssg(self):
        print(f'Welcome to BOI PEOPLS BANK FOR PEOPLE, {self.cname}')

    def display_cc_details(self):
        print(f'{self.creditscore} - {self.status}')
