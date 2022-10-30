import math
import argparse

parser = argparse.ArgumentParser(description="This program calculates loans \
depends of their type.")

parser.add_argument("--type", choices=["diff", "annuity"], help="You need to choose the type of loan")
parser.add_argument("--principal", type=int)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float)
parser.add_argument("--payment", type=int)
args = parser.parse_args()
arguments = [args.principal, args.periods, args.interest, args.principal]
warning = "Incorrect parameters"
if args.type == "diff":
    if args.principal and args.periods and args.interest:
        interest = (args.interest / 100) / 12
        payments = []
        for x in range(args.periods):
            fraction = (args.principal * x) / args.periods
            dm = (args.principal / args.periods) + interest * (args.principal - fraction)
            payments.append(int(math.ceil(dm)))
            print(f"Month {x + 1}: payment is {int(math.ceil(dm))}")
        print(f"Overpayment = {sum(payments) - args.principal}")
    else:
        print(warning)
elif args.type == "annuity":
    if args.payment and args.periods and args.interest:
        interest = (args.interest / 100) / 12
        x = (interest * (1 + interest) ** args.periods) / ((1 + interest) ** args.periods - 1)
        principal = args.payment / x
        overpayment = args.payment * args.periods - principal
        print(f"Your loan principal = {principal}!\nOverpayment = {overpayment}")
    elif args.principal and args.payment and args.interest:
        interest = (args.interest / 100) / 12
        value = (args.payment / (args.payment - interest * args.principal))
        months = math.log(value, (1 + interest))
        overpayment = args.payment * round(months) - args.principal
        if round(months) % 12 == 0:
            print(f"It will take {int(round(months) / 12)} years to repay this loan!")
        else:
            print(f"It will take {math.floor(months / 12)} years and {math.ceil(months % 12)} months to repay this loan!")
        print(f"Overpayment = {overpayment}")
    elif args.principal and args.periods and args.interest:
        interest = (args.interest / 100) / 12
        fraction = (interest * (1 + interest) ** args.periods) / ((1 + interest) ** args.periods - 1)
        annuity = math.ceil(args.principal * fraction)
        overpayment = math.ceil(annuity * args.periods - args.principal)
        print(f"Your annuity payment = {annuity}!\nOverpayment = {overpayment}")
    else:
        print(warning)
else:
    print(warning)
