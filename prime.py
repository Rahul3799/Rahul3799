value = int(input("Enter any number:"))

# Handling values less than 2
if value < 2:
    print("Please enter a valid value. The number should be 2 or greater.")
elif value == 2 or value == 3:
    print("Value is a prime number.")
else:
    # Loop to check divisibility from 2 to sqrt(value)
    for i in range(2, int(value ** 0.5) + 1):  # Ensure the range end is an integer
        if value % i == 0:
            print("The value is a composite number.")
            print("The value is divisible by", i)
            break  # Exit the loop as soon as we find a divisor
    else:
        # If no divisors are found, it's a prime number
        print("Value is a prime number.")

print("The operation is complete.")


