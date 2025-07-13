import math
INCLUDE_UNSTABLE = False
free_daily_buzz = 25 # Just click a button in the generator
daily_post_buzz = 25 # Post+delete
generator_feedback_buzz = 20 # Click on thumbs up for good generations; halved to maintain realism
following_buzz = 30 if INCLUDE_UNSTABLE else 0 # Follow+unfollow
reaction_daily_buzz = 100 # React to newest, there are enough to not even do fake reactions
buzz_per_usd = 1000
usd_paid = 5
accts_cnt = 4
paid_buzz = usd_paid * buzz_per_usd
one_day_buzz_from_all_accts = (following_buzz + daily_post_buzz + free_daily_buzz + generator_feedback_buzz + reaction_daily_buzz) * accts_cnt
recoup_days = paid_buzz / one_day_buzz_from_all_accts
print(f"{usd_paid} dollars can be recouped with {accts_cnt} accounts in {math.ceil(recoup_days)} days")
print(f"In one day, from all {accts_cnt} accounts you can earn {one_day_buzz_from_all_accts} buzz")
print(f"If you only need 7 buzz for a draft and 15 for hi-res, and it takes 2 high-reses and 5 drafts for one final image, you'll be able to produce {math.floor(one_day_buzz_from_all_accts / (7*5 + 15*2))} final images in a day")
