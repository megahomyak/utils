"""
How much does it cost to store some data in Ethereum?
"""
gas_per_256_bits = 20000  # Defined in the Ethereum yellow paper
gas_per_byte = gas_per_256_bits / 32
eth_per_gwei = 0.000000001
eth_per_gas = float(input("How much does one gas cost now, in gwei?: ")) * eth_per_gwei
eth_per_byte = gas_per_byte * eth_per_gas
currency_per_eth = float(input("How much does one ETH cost now, in your currency?: "))
amount_of_bytes_to_store = float(input("How many bytes (blocks of 8 bits) of information do you wish to store?: "))
total_cost = amount_of_bytes_to_store * eth_per_byte * currency_per_eth
print(f"Storing {amount_of_bytes_to_store} bytes of information on the Ethereum blockchain will cost you {total_cost} of your currency.")
