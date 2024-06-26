import math

def double_point(p1, a, p):
    if p1 == (0, 0):  
        return (0,0)
    x_p1, y_p1 = p1
    slope = (3*pow(p1[0],2) + a) * pow((2 * p1[1]), -1, p)
    #solve for x
    x = (pow(slope,2) - x_p1 - x_p1) % p

    #solve for y
    y = (slope * (x_p1 - x) - y_p1) % p

    return (x,y)

def add_point(p1,p2,a,p):

    if p1 == (0, 0):  
        return p2
    elif p2 == (0, 0): 
        return p1
    elif p1[0] == p2[0] and (p1[1] + p2[1]) % p == 0:  
        return (0, 0)

    x_p1, y_p1 = p1
    x_p2, y_p2 = p2

    #solve slope
    if p1 == p2:
        ans = double_point(p1,a,p)
    else:
        slope = (y_p1 - y_p2) * pow((x_p1 - x_p2), -1, p)
        x = (pow(slope,2) - x_p1 - x_p2) % p
        y = (slope * (x_p1 - x) - y_p1) % p
        ans = (x,y)

    return ans

def scalar_mult(p1, n,a,p):
    count = 0
    prev_count = 0
    ans = (0,0)

    while (n > 0):
        if n & 1 == 1:
            for i in range(count - prev_count):
                p1 = double_point(p1, a, p)
            prev_count = count
            ans = add_point(ans, p1, a, p)

        count += 1
        n >>= 1
    
    return ans 

if __name__ == "__main__":
    print("Enter the values of a, b, and p: ")
    a = int(input())
    b = int(input())
    p = int(input())
    print("Enter the generator point coordinates x, and y:")
    x = int(input())
    y = int(input())

    G = (x,y)
    alice_pr = int(input('Enter Alice’s private key:'))
    bob_pr = int(input('Enter Bob’s private key:'))


    alice_pub = scalar_mult(G, alice_pr , a, p)
    bob_pub = scalar_mult(G, bob_pr , a, p)

    print('Public Keys:')
    print('Alice: ', alice_pub)
    print('Bob: ', bob_pub)

    print('Agreed Upon Keys: ')
    k_1 = scalar_mult(alice_pub, bob_pr, a, p)
    k_2 = scalar_mult(bob_pub, alice_pr, a, p) 
    print(k_1[0])
    print(k_2[0])