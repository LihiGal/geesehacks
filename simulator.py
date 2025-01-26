from family_profiles import MotherGoose, Geeseling
import csv
from datetime import date

def read_data() -> list[dict,dict,date]:
    #mapping from username to object (Geeseling or MotherGoose)
    geeselings = {}
    mothergeese = {}

    #read previous data
    with open('mothergeese.txt') as f:
        reader = csv.reader(f)

        for user in reader:
            line = line.split(":") #username shouldn't have ":"
            
            username = line[1]
            password = line[2]
            name = line[3]
            phone_num = line[4]
            balance = line[5]
            children = line[6].split(",")
            interest_rate = line[7]
            year = line[8]
            month = line[7]
            day = line[6]

            last_date = date(year,month,day)

            children_dict = {x for x in children}

            mothergeese[username] = MotherGoose(username=username, password=password, name=name, phone_num=phone_num, 
                                            balance=balance, interest_rate=interest_rate, children=children_dict)
            
    with open('geeselings.txt') as f:
        reader = csv.reader(f)

        for user in reader:
            line = line.split(":") #username shouldn't have ":"
            
            username = line[1]
            password = line[2]
            name = line[3]
            chequing_amount = line[4]
            savings_amount = line[5]
            mother = line[6]

            geeselings[username] = Geeseling(username=username, password=password, name=name, chequing_amount=chequing_amount,
                                        savings_amount=savings_amount, mother=mothergeese[mother])

    for mother in mothergeese.values():
        for geeseling in geeselings.values():
            if geeseling.mother is mother:
                mother.children[geeseling.name] = geeseling
    
    return [geeselings, mothergeese, last_date]

def geeseling_login(geeselings: dict) -> Geeseling:
    geeselings_passwords = {geeseling.username: geeseling.get_password for geeseling in geeselings}

    is_logged_in = None

    while is_logged_in is None:
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username in geeselings and password in geeselings_passwords:
            print("Logged in!")
            return geeselings[username]
        
        print("Username or password incorrect. Try again.")

def mothergoose_login(mothergeese: dict) -> MotherGoose:
    mothergeese_passwords = {{mothergeese.username: mothergeese.get_password for mothergeese in mothergeese}}

    is_logged_in = None

    while is_logged_in is None:
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username in geeselings and password in mothergeese_passwords:
            print("Logged in!")
            return mothergeese[username]
        
        print("Username or password incorrect. Try again.")

def run_geeseling(geeseling: Geeseling) -> None:
    MENU = "Menu:\n1: Withdraw from chequing\n2. Withdraw from savings\n3: Logout\nEnter action:"

    logout = False
    action = None

    while not logout:
        print("Chequing: " + str(geeseling.get_chequing()))
        print("Savings: " + str(geeseling.get_savings()))

        while action is not '1' and action is not '2' and action is not '3':
            action = input(MENU)

        if action == '1':
            amount = input("Withdraw amount: ")
            geeseling.withdraw_chequing(amount)
        elif action == '2':
            amount = input("Withdraw amount: ")
            geeseling.withdraw_savings(amount)
        else:
            logout = True

        print("Success")
 
def run_mothergoose(mother: MotherGoose) -> None:
    MENU = "Menu:\n1: Add child\n2. Set Interest\n3: Add to balance\n4: Logout\nEnter action:"

    logout = False
    action = None

    while not logout:
        for geeseling in mother.children_list.values():
            print(geeseling.name + "'s account:")
            print("Chequing: " + str(geeseling.get_chequing()))
            print("Savings: " + str(geeseling.get_savings()))

        while action is not '1' and action is not '2' and action is not '3' and action is not '4':
            action = input(MENU)

        if action == '1':
            username = input("New geesling username: ")
            password = input("New geeseling password: ")
            name = input("New geeseling name: ")
            
            new_geeseling = Geeseling(username=username, password=password, name=name, mother=mother)
            mother.add_child(new_geeseling)
        elif action == '2':
            amount = input("Set interest (%): ")
            frequency = input("Set compounding frequency (days): ")

            mother.set_interest_rate(amount=amount, frequency=frequency)
        elif action == '3':
            amount = input("Add amount: ")
            mother.add_to_balance(amount=amount)
        else:
            logout = True
        
        print("Success")

def save_data(geeselings: dict, mothergeese: dict, day: int, year: int, month: int) -> None:

    f_geeseling = open("geeselings.txt", "a")

    f_mothergeese = open("mothergeese.txt", "a")

    for geeseling in geeselings.values():
        line = geeseling.username + ":"
        + str(geeseling.get_password()) + ":"
        + geeseling.name + ":"
        + str(geeseling.chequing_amount) + ":"
        + str(geeseling.saving_amount) + ":"
        + str(geeseling.mother.username)

        f_geeseling.write(line)
    f_geeseling.close()

    for mother in mothergeese.values():
        children = str([mother.children_list[x].username + ":" for x in mother.children_list])

        line = mother.username + ":"
        + str(mother.get_password()) + ":"
        + mother.name + ":"
        + children
        + mother.balance + ":"
        + mother.interest_rate + ":"
        + mother.phone_num + ":"
        + year + ":"
        + month + ":"
        + day

        f_mothergeese.write(line)


    f_mothergeese.close()

if __name__ == "__main__":
    #read previous data
    data = read_data()
    
    geeselings = data[0]
    mothergeese = data[1]
    last_recorded_date = data[2]

    current_time = date.today()

    #log in
    login_as = None

    for mothergoose in mothergeese.values():
        interest = (current_time - last_recorded_date).days()//mothergoose.interest_rate[0]

        for geeseling in mothergoose.children_list.values():
            mothergoose.inc_geeseling_saving(geeseling)


    while login_as is not '1' and login_as is not '2':
        login_as = input("Enter '1' to log in as a Mothergoose, '2' to log in as a geeseling:")
    
    if login_as == '1':
        geeseling = geeseling_login(geeselings)
        run_geeseling(geeseling)
    else:
        mothergoose = mothergoose_login(mothergeese)
        run_mothergoose(mothergoose)

    #save data
    print("Logged out.")
    save_data(geeselings, mothergeese, current_time.day, current_time.year, current_time.month)

