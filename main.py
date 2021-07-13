import asmuthBloom as A

def runTests(n, t, s):
    secret = int(input("enter secret to run tests on or -1 for random: "))
    if secret == -1:
        print("make random secret here")
    
    test = int(input("how many tests would you like to do: "))
    mul = int(input("how many multiplication would you like to do: (n/s = %d)", (n/s)))
    add = int(input("how many addition would you like to do: (n/s = %d)", (n/s)))
    for i in range(0, test):
        exit(0)


def main():
    val = 0
    n, t, s = 0
    while 1:
        while val <= 0 | val >= 5:
            print("[1] enter values:")
            print("[2] run tests one secret")
            print("[3] run tests multiple secret")
            print("[4] exit")
            val = input("pls enter a choice:")
        
        if val == 1:
            exit(0)

        if val == 2:
            runTests(n, t, s)

        if val == 3:
            random = random.SystemRandom()
            secret = random.getrandbits(int(sys.argv.pop(2))) 

        if val == 4:
            exit(0)

 
def getData():
    n = int(input("enter number of participants(n): "))
    t = int(input("enter number of participants to discover the secret(t): "))
    s = int(input("enter number of participants who will gain no knowledge(s): "))

if __name__ == "__main__":
    main()