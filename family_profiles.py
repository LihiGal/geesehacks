from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

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
    chequing_amount: Optional[float]
    savings_amount: Optional[float]
    mother: MotherGoose

    def __init__(self, username: str, password: any, name: str, chequing: Optional[float], savings: Optional[float], mother: MotherGoose):
        self.chequing_amount = chequing
        self.savings_amount = savings
        self.username = username
        self.set_password(password)
        self.name = name
        self.mother = mother


    def get_chequing(self) -> float:
        return self.chequing_amount
    
    def get_savings(self) -> float:
        return self.savings_amount
    
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
    
    def set_password(self, password: str) -> None:
        self._password = password

    def get_password(self) -> str:
        return self._password
    
@dataclass
class MotherGoose:

    username: str
    _password: any
    name: str
    children_dict: dict[str, Geeseling]
    balance: float
    interest_rate: Optional[list[int,int]] # [interest rate as percent, frequency of compouding] for the geeslings' savings
    phone_num: int

    def __init__(self, username: str, password: str, name: str, phone_num: int, balance: Optional[float], interest: Optional[list[int,int]], children_dict: Optional[dict[str, Geeseling]]) -> None:
        """
        Preconditions:
        - ":" not in username & "," not in username
        """
        self.username = username
        self.name = name
        self.children_dict = []
        self.interest_rate = interest
        self.children_dict = children_dict

        if balance is None:
            self.balance = 0
        else:
            self.balance = balance
        
        self.phone_num = phone_num

    def get_password(self) -> str:
        return self._password
    
    def add_child(self, child: Geeseling):
        """add a child to the children list"""
        if child.username in self.children_dict:
            print("child with username {child.username} already exists")
        else:
            self.children_dict[child.username] = child
            print("added child: {child.name} (username: {child.username})")

    def remove_child(self, username: str):
        """remove a child from the children list"""
        if username in self.children_dict:
            removed_child = self.children_dict.pop(username)
            print("removed child: {removed_child.name} (username: {username})")
        else:
            print("no child with username {username} found.") 

    def set_interest_rate(self, rate: int, frequency: int)  -> None:
        self.interest_rate[0] = rate
        self.interest_rate[1] = frequency
        print("Successfully changed interest rate to " + rate + "%!")

    def add_to_balance(self, amount: float) -> None:
        self.balance = round(self.balance + amount, 2)
        print("Successfully added $" + str(amount) + " to balance!")
    
    def add_to_chequing(self, geeseling: str, amount: float) -> None:
        self.children_dict[geeseling].chequing_amount += amount
        self.balance -= amount

    def inc_geeseling_savings(self, child_user: str) -> None:
        amount1 = self.interest_rate[0]/100 * self.children_dict[child_user].savings_amount
        amount = round((1 + self.interest_rate[0]/100) * self.children_dict[child_user].savings_amount, 2)
        self.balance -= amount1
        self.children_dict[child_user].savings = amount

      