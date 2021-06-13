from connect import *

c = connect()
c.conn()


def trade(take_trade, Money):
    ACTIVES = pair
    print(ACTIVES)
    expirations_mode = 1
    if take_trade == "buy":
        check, id = Iq.buy(Money, ACTIVES, "call", expirations_mode)
        print("start check win please wait")
        while True:
            trade = Iq.check_win_v3(id)
            if trade > 0:
                print("you won")
            elif trade == 0:
                print("you got nothing")
                print("take the trade sell for martaingle")

            else:
                print("you loss")
                print("take the trade sell for martaingle")

            break
            time.sleep(1)

    elif take_trade == "sell":
        check, id = Iq.buy(Money, ACTIVES, "put", expirations_mode)
        print("start check win please wait")
        while True:
            # print(Iq.check_win_v3(id))
            trade = Iq.check_win_v3(id)
            if trade > 0:
                print("you won")
            elif trade == 0:
                print("you got nothing")
                print("take the trade sell for martaingle")
            else:
                print("you loss")
                print("take the trade sell for martaingle")
            break
            time.sleep(1)
    else:
        print("somthing went wrong")
