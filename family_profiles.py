from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Geeseling:
    username: str
    _password: any
    name: str

    def login(self, username: str, password: any) -> bool:
        """function to create the login of the geeseling"""
        return self.username == username and self._password == password
    
@dataclass
class MotherGoose:
    username: str
    _password: any
    name: str
    children_list: Dict[str, Geeseling]

    def __init__(self, username: str, _password: any, name: str, children_list: Dict[str, Geeseling] = None):
        self.username = username
        self._password = _password
        self.name = name
        self.children_list = children_list or {}

    def add_child(self, child: Geeseling):
        """add a child to the children list"""
        if child.username in self.children_list:
            print("child with username {chiled.username} already exists")
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