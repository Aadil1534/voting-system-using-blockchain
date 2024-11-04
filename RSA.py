import  random

def totient(number):
    if (prime(number)):
        return number-1
    else:
        return False
    
def prime(n):
    if(n<=1):
        return False
    if(n<=3):
        return True
    if (n%2==0 or n%3==0):
        return False
    
    i=5
    while(i*i<=n):
        if(n%i==0 or n%(i+2)==0):
            return False
        i+=6
    return True



def generate_E(num):
    def mdc(n1,n2):
        rest=1
        while(n2!=0):
            rest=n1%n2
            n1=n2
            n2=rest
        return n1
    while True:
        e=random.randrange(2,num)
        if (mdc(num,e)==1):
            return e



def  generate_prime (): # generate the prime number - small
    while  True : # 2 ** 2048 is the RSA standart keys
        x = random . randrange ( 1 , 100 ) # define the range of the primes
        if ( prime ( x ) == True ):
            return  x

def  mod ( a , b ): # mod function
    if ( a < b ):
        return  a
    else :
        c = a % b
        return  c

def  cipher ( words , e , n ): # get the words and compute the cipher
    tam  =  len ( words )
    i  =  0
    list  = []
    while ( i  <  tam ):
        letter  =  words [ i ]
        k  =  ord ( letter )
        k  =  k ** e
        d  =  mod ( k , n )
        list . append ( d )
        i+=1
    return  list

def  decrypts ( cipher , n , d ):
    list  = []
    i  =  0
    size  =  len ( cipher )
    # text = cipher ^ d mod n
    while  i  <  size :
        result  =  cipher [ i ] ** d
        text  =  mod ( result , n )
        letter  =  chr ( text )
        list . append ( letter )
        i+=1
    return  list




def  calculate_private_key ( toti , e ):
    d  =  0
    while ( mod ( d * e , toti )!=1 ):
        d+=1
    return  d


