import math
import random

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y

def mod_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("Pas d'inverse")
    return x % m

def pollard_rho(n):
    if n % 2 == 0:
        return 2

    x = random.randint(2, n-1)
    y = x
    c = random.randint(1, n-1)
    d = 1

    while d == 1:
        x = (pow(x, 2, n) + c) % n
        y = (pow(y, 2, n) + c) % n
        y = (pow(y, 2, n) + c) % n
        d = math.gcd(abs(x - y), n)

    return d if d != n else None


def is_prime(n, k=8):
    if n < 2:
        return False

    small = [2,3,5,7,11,13,17,19,23]
    for p in small:
        if n == p:
            return True
        if n % p == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    def check(a):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return True
        return False

    for _ in range(k):
        a = random.randint(2, n - 2)
        if not check(a):
            return False

    return True

def pollard_pminus1(n, B=100000):
    a = 2
    for j in range(2, B):
        a = pow(a, j, n)
        d = gcd(a - 1, n)
        if 1 < d < n:
            return d
    return None

def factorize(n, factors=None):
    if factors is None:
        factors = []

    if n == 1:
        return factors

    if is_prime(n):
        factors.append(n)
        return factors

    for _ in range(5):  # limite essais
        facteur = pollard_rho(n)
        if facteur and facteur != n:
            break
    else:
        return factors

    if n % facteur != 0:
        return factorize(n, factors)

    factorize(facteur, factors)
    factorize(n // facteur, factors)

    return factors





def rsa_decrypt(c, d, n):
    return pow(c, d, n)

def int_to_bytes_variants(x, length):
    min_len = max(1, (x.bit_length() + 7) // 8)
    return [
        x.to_bytes(min_len, "big"),
        x.to_bytes(min_len, "little"),
        x.to_bytes(length, "big"),
        x.to_bytes(length, "little"),
    ]

def xor(data, key_bytes):
    return bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data))

def score_text(data):
    if not data:
        return 0
    return sum(32 <= b < 127 for b in data) / len(data)

def header(title):
    print("\n" + "=" * 70)
    print(f"{title:^70}")
    print("=" * 70 + "\n")



n = 71632723108922042565754944705405938190163585182073827738737257362015607916694427702407539315166426071602596601779609881448209515844638662529498857637473895727439924386515509746946997356908229763669590304560652312325131017845440601438692992657035378159812499525148161871071841049058092385268270673367938496513

e = 1009

q_chiffre = 70785482415899901219256855373079758876285923471951840038722877622097582944768442919300478197733262514534911901131859013939654902078384994979880540719293485131574905521151256806126737353610928922434810670654618891838295876181905553857594653764136067479449117470741836721372149447795646290103141292761424726007

p_chiffre = 55044587110698448189468021909149190373421069219506981148292634221985403129928367209713497911359302701069378532959510957622709061077384648566361893749771744973388835727259855002207844685526295296408852878202498675158924213264474587673461598376054133832370354928763624202425050121409987087150490459351809040858

g_chiffre = 43089172300844684958445369204000423742543038862350925279569289644298734265625491619486408239703259462606739540181409010715678916496299388069246398890469779970287613357772582024703107603034996120914490203805569384580718393586094166173301167583379300330660182750028000520221960355249560831414918130647224546308

header("FACTORIZATION RSA")

facteur = pollard_pminus1(n)
if facteur is None:
    print("p-1 method failed → switching to Pollard Rho")
    facteur = pollard_rho(n)

p = facteur
q = n // p

print(f"p = {p}")
print(f"q = {q}")

phi = (p - 1) * (q - 1)
d = mod_inverse(e, phi)

print(f"\nphi(n) = {phi}")
print(f"d      = {d}")

header("DECRYPTION DIFFER HELLMAN PARAMETERS")

qdh = rsa_decrypt(q_chiffre, d, n)
pdh = rsa_decrypt(p_chiffre, d, n)
gdh = rsa_decrypt(g_chiffre, d, n)

print(f"q = {qdh}")
print(f"p = {pdh}")
print(f"g = {gdh}")

header("XOR DECRYPTION SALAIRES")

with open("salaires.mm", "rb") as f:
    ciphertext = f.read()



keys_int = [1, pdh - 1]
key_length = (pdh.bit_length() + 7) // 8

results = []

for k in keys_int:
    for vid, key_bytes in enumerate(int_to_bytes_variants(k, key_length)):
        plaintext = xor(ciphertext, key_bytes)
        score = score_text(plaintext)
        results.append((score, k, vid, plaintext[:800]))

results.sort(reverse=True, key=lambda x: x[0])

for i, (score, k, vid, preview) in enumerate(results[:5], 1):
    print(f"\n--- test #{i} ---")
    print(f"Score     : {score:.4f}")
    print(f"Key       : {k}")
    print(f"Variant   : {vid}")
    print("-" * 50)
    print(preview.decode("utf-8", errors="replace"))


#Trouver
mdp_encrypte =[81530476374664351124876242644701327168836407987,
               83740877821201430552252653974153238737996745098,
               51373667846507963545859239582447701017826406175,
               61167846837720209456441528754183777549647735855,
               42340513171888188994504759277496496710896088718,
               65069303637151076134861115122997306654987857614,
               32785990179062766920584737848735367794508677603]


header("DECRYPTION SALAIRES")

n_salaire=86062381025757488680496918738059554508315544797
e_2=13

facteurs = factorize(n_salaire)

print("\nFacteurs trouvés :")

for f in facteurs:
    print(f)




phi_2 = 1


for p in facteurs:

    phi_2 *= (p-1)




d_2 = mod_inverse(e_2, phi_2)

mdp_decrypte = []



print("\nsalaire decrypte :")
for chiffre in mdp_encrypte:


    clair = rsa_decrypt(
        chiffre,
        d_2,
        n_salaire
    )


    mdp_decrypte.append(clair)


    print(f"Salaire{len(mdp_decrypte)-1} = {clair}")



