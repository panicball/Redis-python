import redis

redis_host = "localhost"
redis_port = 6379
redis_password = ""

r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

bank_account = 123
_id = 0
id_ = 0

def menu():
    print (" ")
    print ("  Transaction Options Are:  ")
    print ("-----------------------------")
    print ("1. New client registration ")
    print ("2. New account opening ")
    print ("3. Money transfer operation from one account to another ")
    print ("4. Depositing or withdrawing money from an account ")
    print ("5. Exit ")
    print (" ")
    return int(input ("Choose your option: "))


def registration():
    print ("New client registration ")
    name = input("Enter your name: ")
    surname = input("Enter your surname: ")
    r.hset(str(_id), 'name', name)
    r.hset(str(_id), 'surname', surname)
    print (" ")
    print ("Bank registrated new user: ")  
    print (r.hget(str(_id), 'name') + ' ' + r.hget(str(_id), 'surname'))


def new_account_opening():
    print ("New account opening ")
    how_much = input("Enter how much money will be transferred to the account: ")
    r.hset('LT' + str(bank_account), 'balance', how_much)
    r.hset('LT' + str(bank_account), 'ID', str(id_))
    print ("New account with its balance: ")  
    print ("LT" + str(bank_account) + ' ' + r.hget('LT' + str(bank_account), 'balance') + ' ')


def money_transfer():
    how_much_to_transfer = input("Enter how much money will be transferred from one account to another: ")
    how_much_to_transfer = int(how_much_to_transfer)
    from_where = input("Enter account number from which to transfer money: ")
    to_where = input("Enter account number to which to transfer money: ")
    p = r.pipeline()
    #TODO first if 
    p.watch(from_where)
    p.multi()
    if int(r.hget(from_where, 'balance'))  >= how_much_to_transfer: 
        if p.exists(from_where) and p.exists(to_where):
            p.hincrby(from_where, 'balance', -how_much_to_transfer)
            p.hincrby(to_where, 'balance', how_much_to_transfer)
            p.execute()
            r.sadd('T', 'money transfered from '+ from_where + ' to ' + to_where +' sum transfered '+ str (how_much_to_transfer))
            print ("Balances: ")
            print (from_where + ' ' + r.hget(from_where, 'balance'))
            print (to_where + ' ' + r.hget(to_where, 'balance'))
        else:
            print ("The account does not exist")
    else:
        print ("Account balance not big enough")


def transfer_withdraw_money():
    account = input("Enter account number: ")
    how_much = r.hget(account, 'balance')
    how_much_int = int(how_much)
    what_to_do = input("Transfer money to the account (t) or withdrow money from it (w): ")
    p = r.pipeline()
    p.watch(how_much_int)
    p.multi()
    if p.exists(account):
        if what_to_do == 't':
            how_much_to_transfer = input("Enter how much money will be transferred into the account: ")
            how_much_to_transfer = int(how_much_to_transfer)
            p.hincrby(account, 'balance', how_much_to_transfer)
            r.sadd('T/W', str (how_much_to_transfer) + ' transfered to ' + account)
        elif what_to_do == 'w':
            how_much_to_withdrow = input("Enter how much money will be withdrowed from the account: ")
            how_much_to_withdrow = int(how_much_to_withdrow)
            if how_much_int >= int(how_much_to_withdrow):
                p.hincrby(account, 'balance', -how_much_to_withdrow)
                r.sadd('T/W', str (how_much_to_withdrow) + ' withdrowed from ' + account)
            else:
                print ("Account balances is not big enough ")
                print ("Current account balance : ")
        p.execute()
        print (account + ' ' + r.hget(account, 'balance'))
    else:
        print ("The account does not exist")


print (" ")
print ("Simple banking system using redis")
loop = 1
choice = 0
while loop == 1:
    choice = menu()
    print (" ")
    if choice == 1:
        registration()
        _id += 1
        print (" ")
        print ("Open a new account for the registered user? y/n")
        answer = input("Enter your choice: ")
        if answer == 'y':
            print (" ")
            new_account_opening()
            bank_account += 1
            id_ += 1
    elif choice == 2:
        new_account_opening()
        bank_account += 1
        id_ += 1
    elif choice == 3:
        money_transfer()
    elif choice == 4:
        transfer_withdraw_money()
    elif choice == 5:
        loop = 0


