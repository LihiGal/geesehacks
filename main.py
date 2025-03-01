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
            line = str(user)[2:-2]
            line = line.split(":") #username shouldn't have ":"
            
            username = line[0]
            password = line[1]
            name = line[2]
            phone_num = line[3]
            balance = line[4]
            children = line[5].split("=")
            interest_rate = line[6]
            frequency = line[7]
            year = int(line[8])
            month = int(line[9])
            day = int(line[10])
            last_date = date(year,month,day)

            children = {x: None for x in children}

            mother_obj =  MotherGoose(username=username, password=password, name=name, phone_num=int(phone_num), balance=float(balance), interest=[int(interest_rate),int(frequency)], children_dict=children)
            
            mothergeese[username] = mother_obj

    with open('geeselings.txt') as f:
        reader = csv.reader(f)

        for user in reader:
            line = str(user)[2:-2]
            line = line.split(":") #username shouldn't have ":"
            
            username = line[0]
            password = line[1]
            name = line[2]
            chequing_amount = line[3]
            savings_amount = line[4]
            mother = line[5]

            geeselings[username] = Geeseling(username=username, password=password, name=name, chequing=float(chequing_amount),
                                        savings=float(savings_amount), mother=mothergeese[mother])

    for mother in mothergeese.values():
        for geeseling in geeselings.values():
            if geeseling.mother is mother:
                mother.children_dict[geeseling.username] = geeselings[geeseling.username]

    return [geeselings, mothergeese, last_date]

def geeseling_login(geeselings: dict) -> Geeseling:
    is_logged_in = None

    while is_logged_in is None:
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username in geeselings and password == geeselings[username].get_password():
            print("Logged in!")
            return geeselings[username]
        
        print("Username or password incorrect. Try again.")

def mothergoose_login(mothergeese: dict) -> MotherGoose:
    is_logged_in = None

    while is_logged_in is None:
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username in mothergeese and password == mothergeese[username].get_password():
            print("Logged in!")
            return mothergeese[username]
        
        print("Username or password incorrect. Try again.")

def run_geeseling(geeseling: Geeseling) -> None:
    MENU = "Menu:\n1: Withdraw from chequing\n2. Withdraw from savings\n3: Logout\nEnter action:"

    logout = False
    action = None

    while not logout:
        print("\n-------------------------------------------")
        print(geeseling.name + "'s account:")
        print("Chequing: " + str(geeseling.get_chequing()))
        print("Savings: " + str(geeseling.get_savings()))
        print("-------------------------------------------")

        while action is not '1' and action is not '2' and action is not '3':
            action = input(MENU)

        if action == '1':
            amount = input("Withdraw amount: ")
            geeseling.withdraw_chequing(float(amount))
        elif action == '2':
            amount = input("Withdraw amount: ")
            geeseling.withdraw_savings(float(amount))
        else:
            logout = True
            return

        print("Success")
        action = 0
 
def run_mothergoose(mother: MotherGoose, geeselings: dict[Geeseling]) -> None:
    MENU = "Menu:\n1: Add child\n2. Set Interest\n3: Add to balance\n4: Logout\nEnter action:"

    logout = False
    action = None

    while not logout:
        for geeseling in mother.children_dict.values():
            print("\n-------------------------------------------")
            print(geeseling.name + "'s account:")
            print("Chequing: " + str(geeseling.get_chequing()))
            print("Savings: " + str(geeseling.get_savings()))
            print("-------------------------------------------")

        while action is not '1' and action is not '2' and action is not '3' and action is not '4':
            action = input(MENU)

        if action == '1':
            username = input("New geesling username: ")
            password = input("New geeseling password: ")
            name = input("New geeseling name: ")
            
            new_geeseling = Geeseling(username=username, password=password, name=name, mother=mother, chequing=0, savings=0)
            mother.add_child(new_geeseling)
            mother.children_dict[new_geeseling.username] = new_geeseling
            geeselings[new_geeseling.username] = new_geeseling
        elif action == '2':
            amount = input("Set interest (%): ")
            frequency = input("Set compounding frequency (days): ")

            mother.set_interest_rate(rate=amount, frequency=frequency)
        elif action == '3':
            amount = input("Add amount: ")
            mother.add_to_balance(amount=amount)
        else:
            logout = True
        
        print("Success")
        action=0

def save_data(geeselings: dict, mothergeese: dict, day: int, year: int, month: int) -> None:

    with open("geeselings.txt", "w") as f_geeseling:
        for geeseling in geeselings.values():
            line = geeseling.username + ":" + str(geeseling.get_password()) + ":" + geeseling.name + ":"+ str(geeseling.chequing_amount) + ":"+ str(geeseling.savings_amount) + ":"+ str(geeseling.mother.username)

            f_geeseling.write(line+"\n")
    
    f_geeseling.close()

    with open("mothergeese.txt", "w") as f_mothergeese:
        for mother in mothergeese.values():
            line = mother.username + ":"+ str(mother.get_password()) + ":"+ mother.name + ":" + str(mother.phone_num) + ":" + str(mother.balance) + ":"
            
            for child_user in mother.children_dict:
                line += child_user + "="
            
            line = line[0:-1] + ":"

            line += str(mother.interest_rate[0]) + ":" + str(mother.interest_rate[1]) + ":"+ str(year) + ":"+ str(month) + ":"+ str(day)

            f_mothergeese.write(line+"\n")
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
        interest = (current_time - last_recorded_date).days//mothergoose.interest_rate[0]

        for geeseling in mothergoose.children_dict.values():
            mothergoose.inc_geeseling_savings(geeseling.username)


    while login_as is not '1' and login_as is not '2':
        login_as = input("Enter '1' to log in as a geeseling, '2' to log in as mother goose:")
    
    if login_as == '1':
        geeseling = geeseling_login(geeselings)
        run_geeseling(geeseling)
    else:
        mothergoose = mothergoose_login(mothergeese)
        run_mothergoose(mothergoose, geeselings)

    #save data

    print("Logged out.")
    save_data(geeselings, mothergeese, current_time.day, current_time.year, current_time.month)

