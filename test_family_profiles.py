from family_profiles import MotherGoose, Geeseling

def test_add_amount() -> None:
    amount = 4.5
    mother = MotherGoose(username="mother123", password="password", name="Mother Goose Jane", phone_num=123)
    old_balance = mother.balance

    mother.add_to_balance(amount=amount)
    mother.add_to_balance(amount=amount)

    assert mother.balance == amount*4

if __name__ == "__main__":
    test_add_amount()