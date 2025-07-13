import math
INCLUDE_UNSTABLE = True
free_daily_buzz = 25 # Just click a button in the generator
daily_post_buzz = 25 # Post+delete
generator_feedback_buzz = 20 # Halved because I don't want to give fake feedback, might fuck up the stats for the models
following_buzz = 30 if INCLUDE_UNSTABLE else 0 # Follow+unfollow
reaction_daily_buzz = 100 # React to newest, there are enough to not even do fake reactions
buzz_per_usd = 1000
usd_paid = 5
accts_cnt = 4
paid_buzz = usd_paid * buzz_per_usd
one_day_buzz_from_all_accts = (following_buzz + daily_post_buzz + free_daily_buzz + generator_feedback_buzz + reaction_daily_buzz) * accts_cnt
recoup_days = paid_buzz / one_day_buzz_from_all_accts
print(f"{usd_paid} dollars can be recouped with {accts_cnt} accounts in {math.ceil(recoup_days)} days")
