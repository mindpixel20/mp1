import random as r 
import uuid 
import math

vecsize = 1024 
vectors = {} 

class vec:
    def __init__(self, id, data, comps, links):
        self.id = id
        self.data = data
        self.comps = comps
        self.links = links  

    def __str__(self):
        return f"ID: {self.id}\nCOMPONENTS: {self.comps}\nLINKS: {self.links}\nVECTOR DATA: {self.data}\n"

def genvec():
    bits = []
    for i in range(0, vecsize):
        bits.append(r.randint(0, 100)%2)
    return vec(str(uuid.uuid4()), bits, [], [])

def mulvec(vec1, vec2):
    vec1bits = vec1.data
    vec2bits = vec2.data
    vec3bits = []
    for i in range(0, vecsize):
        vec3bits.append(vec1bits[i] * vec2bits[i])
    return vec(str(uuid.uuid4()), vec3bits, [vec1.id, vec2.id], [])

def addvec(vec1, vec2):
    vec1bits = vec1.data
    vec2bits = vec2.data
    vec3bits = []
    for i in range(0, vecsize):
        vec3bits.append(vec1bits[i] + vec2bits[i])
    return vec(str(uuid.uuid4()), vec3bits, [vec1.id, vec2.id], [])

def permvec(vec, dir):
    vecbits = vec.data 
    newbits = vecbits[dir:]+vecbits[:dir]
    return vec(str(uuid.uuid4()), newbits, [vec.id], [])

def hamming(vec1, vec2):
    rawdist = 0.0
    total = 0.0 + vecsize 
    for i in range(0, vecsize):
        if vec1.data[i] != vec2.data[i]:
            rawdist = rawdist + 1.0
    ham = 1.0 
    if rawdist > 0.0:
        ham = 1 - (rawdist / total)
    return ham 

def dot_product(vec1, vec2):
    vec1bits = vec1.data
    vec2bits = vec2.data 
    sum = 0.0 
    for i in range(0, vecsize):
        sum = sum + (vec1bits[i] * vec2bits[i])
    return sum 

def magnitude(vec1):
    vec1bits = vec1.data 
    sum = 0.0 
    for i in range(0, vecsize):
        sum = sum + (vec1bits[i] * vec1bits[i])
    return math.sqrt(sum)  

def cos_sim(vec1, vec2):
    dot_a_b = dot_product(vec1, vec2) 
    
    if dot_a_b == 0.0:
        return 0.0 
        
    mag_a = magnitude(vec1)
    if mag_a == 0.0:
        return 0.0
        
    mag_b = magnitude(vec2) 
    if mag_b == 0.0:
        return 0.0
        
    return dot_a_b / (mag_a * mag_b)

def roll_add(vecs): # for some reason, sometimes it gets a zero-length list?
    # THIS IS DUCT TAPE CODE
    if len(vecs) == 0:
        acc = []
        for i in range(0, 1024):
            acc.append(0)
        return acc 
    # END DUCT TAPE CODE 
    acc = vectors[vecs[0]]
    for v in vecs:
        acc = addvec(acc, vectors[v])
    return acc

def roll_mul(vecs):
    acc = vecs[0]
    for v in vecs:
        acc = mulvec(acc, vectors[v])
    return acc
    
 
char2vec = {} 
vec2char = {} # searched via similarity 

def char_to_vector(char):
    if char not in char2vec: 
        v = genvec() 
        vectors[v.id] = v
        char2vec[char] = v.id 
        vec2char[v.id] = char
        return v.id
    else:
        return char2vec[char]

def vector_to_char(vec_id):
    if vec_id in vec2char: 
        return vec2char[vec_id]
        
    max_sim = 0.0 
    winner = None 
    vec = vectors[vec_id]
    vec_data = vec.data 
    for v_id in list(vec2char.keys()):
        vec_b = vectors[v_id]
        vec_b_data = vec_b.data
        vec_sim = hamming(vec, vec_b)
        if vec_sim >= max_sim:
            max_sim = vec_sim 
            winner = v_id 
    if winner is not None:
        return vec2char[v_id]

def word_to_vector(word): # will need cleanups and comparisons just like the others
    vecs = []
    for char in word:
        vecs.append(char_to_vector(char))
    rolled = roll_add(vecs)
    if rolled.id not in vectors:
        vectors[rolled.id] = rolled
    return rolled.id

def message_to_vector(message):
    words = message.split(" ")
    word_vector_ids = []
    for w in words:
        word_vector_ids.append(word_to_vector(w))
    rolled = roll_add(word_vector_ids)
    if rolled.id not in vectors:
        vectors[rolled.id] = rolled
    return rolled.id

def convert_to_bin_threshold(vec_id):
    vec_data = vectors[vec_id].data
    max_elem = -1
    for d in vec_data:
        if d > max_elem:
            max_elem = d
    bits = []
    threshold = int(max_elem/2)
    for d in vec_data:
        if d >= threshold:
            bits.append(1)
        else:
            bits.append(0)
    return bits 

def encode(message):
    base_vec = message_to_vector(message)
    encoded_vec = convert_to_bin_threshold(base_vec)
    return encoded_vec
