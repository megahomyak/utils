maze = list("""
  #############################
  #       # #     #       #   #
# # ##### # ### ### ######### #
#     # #     #         #   # #
# # ### ### # ##### ### ### # #
# #   #   # # #   #   #   #   #
##### # ### # ### ####### # # #
#     #     # # # #     #   # #
######### # # # # ### ### #####
# #     # # # #     #         #
# # ### ### ####### ######### #
#   #       #     #     #     #
### ##### # ##### ##### # ### #
# #   #   #   #     #     # # #
# # ### ##### # ##### # # # # #
# # #   #   #   # # # # #   # #
# ### # # ##### # # # ##### ###
#     # #   # # # # #   # # # #
# ##### ### # # # # # # # ### #
#     # # # #   #     #   # # #
### # ### # ####### # # ### # #
#   # #           # # #     # #
##### # ####### # # # ##### # #
# #   #     #   #   # #   #   #
# # ### ### # ##### ##### # # #
#   #     # # # # # #       # #
### ### ####### # # ### # # ###
# # # # #       #   # # # #   #
# # # # # ####### ### # ##### #
#               # #     #      
#############################  
""".strip("\n"))
maze[0] = ":loafStare:"
maze[-1] = ":kcpCake:"
output = "".join(maze).replace("#", ":white_large_square:").replace(" ", ":black_large_square:")

DISCORD_CHARACTER_LIMIT = 2000

buckets = []
bucket = []
for line in output.splitlines():
    if len("".join(bucket)) + len(line) > DISCORD_CHARACTER_LIMIT:
        buckets.append(bucket)
        bucket = [line]
    else:
        bucket.append(line)
buckets.append(bucket)

for bucket in buckets:
    print("\n".join(bucket))
    print("\n\n")
