import asmuthBloom as A
import random
import mathlib as M

maxNum = 0
kBytes = 0
hBytes = 0
numSecrets = 0
test = 0
mode = 0
op = 0

def runTests(n, t, s): 
    ab = A.AsmuthBloom(n, t, s, op) 
    #! generate secrets and encode their secret shares
    secrets = []
    secretTemp = int(input("enter value to secret or 0 for random the rest: "))
    for i in range(0, numSecrets):
        if(secretTemp == 0):
            secrets.append(random.randint(0,maxNum))
        else:
            secrets.append(secretTemp)
            secretTemp = int(input("enter value for secret or 0 for random the rest: "))
    # res array which contains the amount of secrets which were succe
    res = [0]*numSecrets

    for i in range(0, test):        
        shares = []
        for i in range(0, numSecrets):
            shares.append(ab.generate_shares(secrets[i], kBytes, hBytes))

        secret = secrets[0]
        secret_shares = shares[0]

        recovered = secret
        numOfOps = 0
        for i in range(1, numSecrets):
            if mode == 0:
                secret *= secrets[i]
                secret_shares = ab.multshares(secret_shares, shares[i])
            else:
                secret += secrets[i]
                secret_shares = ab.addshares(secret_shares, shares[i])

            # Mr = secret_shares[0:t + 1]
            recovered = ab.combine_shares(secret_shares)
            if ((recovered % ab._p) != (secret % ab._p)):
                break
            numOfOps += 1

        res[numOfOps] += 1

    #! print the results for the tests  
    print("\n\n| Results of ", test ," tests:           ")
    print("|----------------------------------------")
    print("| num of secrets: ", numSecrets ,"       ")
    print("| ratio of participants to s (maximum number for no information):", n//s)
    if (op == 0):
        print("| using random generated M for the secrets, the results are:")
    else:
        print("| using Optimal M(=pMs) for the secrets, the results are:")
    for i in range(0, numSecrets):
        print("| for " ,i+1, " secrets multiplied/added: ", res[i], "/", test ,"maximal successes to restore the secret")
    print("|-------------------------------------------")

            
def main():
    val = 0
    n = t = s = 0
    while 1:
        while val <= 0 or val >= 4:
            print("[1] enter values:")
            print("[2] run tests")
            print("[3] exit")
            val = int(input("pls enter a choice: "))
        
        if val == 1:
            global maxNum
            global kBytes
            global hBytes
            global test
            global numSecrets
            global mode
            global op

            print("\n[1] use values 1:")
            print("n = 10\nt = 6\ns = 2\nmaxNum = 10000\nkBytes = 20\nhBytes = 30\ntests = 1000\nnum of secrets = 6\nusing multiplication\noptimal M = yes\n")
            print("\n[2] use values 2:")
            print("n = 21\nt = 13\ns = 3\nmaxNum = 60\nkBytes = 7\nhBytes = 9\ntests = 1000\nnum of secrets = 5\nusing multiplication\noptimal M = no\n")
            print("\n[3] use values 3:")
            print("n = 12\nt = 6\ns = 2\nmaxNum = 1500\nkBytes = 20\nhBytes = 30\ntests = 1000\nnum of secrets = 400\nusing addition\noptimal M = yes\n")
            decision = int(input("[4] custom values\n\n enter choice: "))
            if(decision == 1):
                n = 10
                t = 6
                s = 2
                maxNum = 10000
                kBytes = 20
                hBytes = 30
                test = 100
                numSecrets = 8 
                mode = 0
                op = 1

            elif(decision == 2):
                n = 21
                t = 13
                s = 3
                maxNum = 12345
                kBytes = 20
                hBytes = 30
                test = 100
                numSecrets = 8
                mode = 0
                op = 0

            elif(decision == 3):
                n = 12
                t = 6
                s = 2
                maxNum = 1500
                kBytes = 20
                hBytes = 30
                test = 1000
                numSecrets = 50
                mode = 1
                op = 1

            else:
                n = int(input("enter number of participants(n): "))
                t = int(input("enter number of participants to discover the secret(t): "))
                s = int(input("enter number of participants who will gain no knowledge(s): "))

                maxNum = int(input("enter upper bound for secrets during the tests (for random purposes): "))

                print("enter number of bytes for prime p (needs to be more bytes than ", M.bit_len(maxNum) ," bytes): ")
                kBytes = int(input())

                print("enter number of bytes for primes m_i (needs to be more than ", kBytes ," bytes): ")
                hBytes = int(input())

                test = int(input("how many tests would you like to do: "))
                print("enter number of secrets to mul/add (n/s =", (n // s),"):")
                numSecrets = int(input())
                mode = int(input("choose operation: 0 - multiplication, 1 - addition: "))

                op = int(input("Random M - 0, Optimized M (M = pMs) - 1: "))

        if val == 2:
            if n == 0:
                print("you need to enter values first")
            else:
                runTests(n, t, s)

        if val == 3:
            exit(0)

        val = 0

if __name__ == "__main__":
    main()
#ab = A.AsmuthBloom(10,6,2,1)
#shares1 = ab.generate_shares(10, 5, 6)
#shares2 = ab.generate_shares(15, 5, 6)
#print(ab.combine_shares(shares1))
#print(ab.combine_shares(shares2))
#shares1 = ab.multshares(shares1,shares2)
#res = ab.combine_shares(shares1)
#print(res)