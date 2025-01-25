from dataclasses import dataclass
from __future__ import annotations
from typing import Dict, Optional

"""a document organizing the following dataclasses:
Geeseling,
ChildAccount,
MotherGoose,
ParentAccount
"""

@dataclass
class Geeseling:
    username: str
    _password: any
    name: str
    mother: MotherGoose

    def __init__(self, chequing_amount: float = 0.0, savings_amount: float = 0.0):
        self.chequing_amount = chequing_amount
        self.savings_amount = savings_amount
        
    def login(self, username: str, password: any) -> bool:
        """function to create the login of the geeseling"""
        return self.username == username and self._password == password
    

    def withdraw_chequing(self, amount: float) -> bool:
        """withdraw from chequing account if sufficient balance"""
        if amount > self.chequing_amount:
            print("insufficient funds in chequing")
            return False
        self.chequing_amount -= amount
        print(f"Withdrawn ${amount:.2f} from chequing. Remaining: ${self.chequing_amount:.2f}")
        return True

    def withdraw_savings(self, amount: float) -> bool:
        """Withdraw from savings account if sufficient balance."""
        if amount > self.savings_amount:
            print("Insufficient funds in savings.")
            return False
        self.savings_amount -= amount
        print(f"Withdrawn ${amount:.2f} from savings. Remaining: ${self.savings_amount:.2f}")
        return True
    
@dataclass
class MotherGoose:

    username: str
    _password: any
    name: str
    children_list: Dict[str, Geeseling]
    balance: float
    interest_rate: Optional[list[int,int]] = None # [interest rate as percent, frequency of compouding] for the geeslings' savings
    phone_num: int

    def __init__(self, username: str, password: str, name: str, balance: float, phone_num: int) -> None:
        self.username = username
        self._password = password
        self.name = name
        self.children_list = []
        self.balance = 0
        self.interest_rate = []
        self._phone_num = phone_num

    def add_child(self, child: Geeseling):
        """add a child to the children list"""
        if child.username in self.children_list:
            print("child with username {child.username} already exists")
        else:
            self.children_list[child.username] = child
            print("added child: {child.name} (username: {child.username})")

    def remove_child(self, username: str):
        """remove a child from the children list"""
        if username in self.children_list:
            removed_child = self.children_list.pop(username)
            print("removed child: {removed_child.name} (username: {username})")
        else:
            print("no child with username {username} found.") 

    def set_interest_rate(self, rate: int, frequency: int)  -> None:
        self.interest_rate[0] = rate
        self.interest_rate[1] = frequency
        print("Successfully changed interest rate to " + rate + "%!")

    def add_to_balance(self, amount: float) -> None:
        self.balance = round(self.balance + amount, 2)
        print("Successfully added $" + amount + " to balance!")
    
    def inc_geeseling_balance(self, child_user: str) -> None:
        self.children_list[child_user].savings = round((1 + self.interest_rate/100) * self.children_list[child_user].savingse, 2)

    def change_password(self, phone_num: int, new_pass: str) -> bool:
        
        if phone_num == self._phone_num:
            self._password = new_pass
            print("Successfully changed password.")
            return True
        else:
            print("Phone number does not match.")
            return False
        
    def change_geeseling_password(self, phone_num: int, geeseling_username: str, new_pass: str) -> bool:
        
        if phone_num == self._phone_num:
            self.children_list[geeseling_username] = new_pass
            print("Successfully changed password.")
            return True
        else:
            print("Phone number does not match.")
            return False

#TEST SUITE
def test_add_amount() -> None:
    mother = MotherGoose(username="mother123", _password="password", name="Mother Goose Jane", phone_num=123)
    assert mother.add_to_balance(mother, 4.5) == 4.5

# Test profile to see if this works
if __name__ == "__main__":
    # Create Mother Goose
    mother = MotherGoose(username="mother123", _password="password", name="Mother Goose Jane")

    # Create Geeseling and Child Accounts
    child1 = Geeseling(username="child1", _password="password1", name="First Geeseling Tom")

    child2 = Geeseling(username="child2", _password="password2", name="Second Geeseling Sam")

    # Add children to Mother Goose
    mother.add_child(child1)
    mother.add_child(child2)

    # login child 1
    if child1.login(username="child1", password="password1"):
        print("Child 1 logged in successfully!")
    else:
        print("log in failed for Child 1.")

    # login child 2
    if child2.login(username="child2", password="password2"):
        print("child 2 logged in successfully!")
    else:
        print("log in failed for Child 2.")
    
    # Child Account Transactions
    child1_account = Geeseling(chequing_amount=50.0, savings_amount=100.0)
    child1_account.withdraw_chequing(20.0)
    child1_account.withdraw_savings(50.0)
