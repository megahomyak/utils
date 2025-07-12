free_daily_buzz = 25
reaction_daily_buzz = 100
buzz_per_usd = 1000
usd_paid = 5
accts_cnt = 4
paid_buzz = usd_paid * buzz_per_usd
one_day_buzz_from_all_accts = (free_daily_buzz + reaction_daily_buzz) * accts_cnt
recoup_days = paid_buzz / one_day_buzz_from_all_accts
print(f"{usd_paid} dollars can be recouped with {accts_cnt} accounts in {recoup_days} days")
