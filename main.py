from os import system
import asmuthBloom as A
import random

def runTests(n, t, s):
    
    modeSecret = int(input("enter mode for secret input:\n[0] random\n[1] custom\nenter choice: "))
    if modeSecret == 0:
        maxNum = int(input("enter upper bound for secret: "))
    
    kBytes = int(input("enter number of bytes for prime p (needs to be more bytes than the secret bytes): "))
    hBytes = int(input("enter number of bytes for primes m_i (needs to be more bytes than p bytes): "))

    test = int(input("how many tests would you like to do: "))
    #mul = int(input("how many multiplication would you like to do: (n/s = %d)", (n/s)))
    #add = int(input("how many addition would you like to do: (n/s = %d)", (n/s)))
    secret1 = 0
    secret2 = 0
    
    for i in range(0, test):
        if modeSecret == 0:
            secret1 = int(random.random()*maxNum)
            secret2 = int(random.random()*maxNum)
        else:
            secret1 = input(int("enter secret1 for next test: "))
            secret2 = input(int("enter secret2 for next test: "))
        print("")
        print("test number: ", i)
        ab1 = A.AsmuthBloom(n, t, s)
        ab2 = A.AsmuthBloom(n, t, s)
        shares1 = ab1.generate_shares(secret1, kBytes, hBytes)
        shares2 = ab2.generate_shares(secret2, kBytes, hBytes) # for testing purposes using 

        recovered = secret1
        numOfOps = 0
        while (recovered == secret1):
            secret1 *= secret2
            ab1.multshares(shares2)

            #    secret1 += secret2
            #    ab1.addshares(shares2)

            recovered = ab1.combine_self_shares()
            numOfOps += 1

            print("secret in iteration ",numOfOps,":", secret1)
            print("recovered in iteration ",numOfOps,":", recovered)
        
        if numOfOps < (int)(n/s):
            print("failed after %d operations expected %d", numOfOps, (int)(n/s))
        else:
            print("succesfuly performed")     
            
def main1():
    val = 0
    n = t = s = 0
    while 1:
        while val <= 0 or val >= 4:
            print("[1] enter values:")
            print("[2] run tests")
            print("[3] exit")
            val = int(input("pls enter a choice: "))
        
        if val == 1:
            n = float(input("enter number of participants(n): "))
            t = float(input("enter number of participants to discover the secret(t): "))
            s = float(input("enter number of participants who will gain no knowledge(s): "))

        if val == 2:
            if n == 0:
                print("you need to enter values first")
            else:
                runTests(n, t, s)

        if val == 3:
            exit(0)

        val = 0

def main():
    success1 = 0
    success2 = 0
    success3 = 0
    
    ab1 = A.AsmuthBloom(21, 9, 5)
    secret = 1234646556124891264991237098040000000000000000000000000000000000000
    tests = 30000
    for i in range (0, tests):
        shares = ab1.generate_shares(secret, 1000000, 200000000)
        restore1 = ab1.combine_shares([shares[9]])
        restore2 = ab1.combine_shares([shares[2],shares[3],shares[9]])
        restore3 = ab1.combine_shares([shares[10], shares[15], shares[12],shares[3],shares[9]])
        if(restore1 == secret):
            success1 += 1
        if(restore2 == secret):
            success2 += 1
        if(restore3 == secret):
            success3 += 1
    print("num of tests: ", tests)
    print(success1," ",success2," ",success3)

if __name__ == "__main__":
    main()