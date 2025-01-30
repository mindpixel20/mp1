import random as r

class mem_cell:
    def __init__(self, addr, data):
        self.addr = addr
        self.data = data

class ram:
    def __init__(self, ham_thres=0.9, celltype=1, rnd=False):
        self.memory_cells = []
        self.ham_thres = ham_thres
        self.celltype = celltype
        self.rnd = rnd
        
    def write(self, addr, data):
        index = self.ham_addr(addr)
        if index == -1:
            self.memory_cells.append(mem_cell(addr, data))
        else:
            self.memory_cells[index].data = data

    def read(self, addr):
        index = self.ham_addr(addr)
        if index == -1:
            if self.rnd == True:
                if self.celltype > 1:
                    tmp = []
                    for i in range(0, self.celltype):
                        tmp.append(r.randint(0, 1))
                    self.write(addr, tmp)
                    return tmp
                else:
                    val = r.randint(0, 1)
                    self.write(addr, val)
                    return val
            else:
                if self.celltype > 1:
                    tmp = []
                    for i in range(0, self.celltype):
                        tmp.append(0)
                    return tmp
                else:
                    return 0
        else:
            return self.memory_cells[index].data

    def ham_addr(self, addr):
        lowest_score = len(addr)+1
        winner = -1

        for mi in range(0, len(self.memory_cells)):
            m = self.memory_cells[mi]
            m_addr = m.addr
            diff = 0
            score = 1.0
            
            for i in range(0, len(m_addr)):
                if addr[i] != m_addr[i]:
                    diff += 1
            if diff == 0:
                lowest_score = 0.0
                winner = mi
            else:
                score = float(diff) / float(len(m_addr))
                score = 1.0 - score
                if score >= self.ham_thres:
                    if score <= lowest_score:
                        lowest_score = score
                        winner = mi 
        return winner

class layer:
    def __init__(self, fields, field_width):
        
        ham_thres = 0.9
        celltype = 1
        random_output = True

        self.last_input = []
        self.last_output = [] 
        
        self.total_input_length = fields*field_width 
        self.ram_count = fields
        self.rams = [] 
        conns = []
        for i in range(0, self.total_input_length):
            conns.append(i) 
        r.shuffle(conns)

        for i in range(0, fields):
            self.rams.append(ram(ham_thres, celltype, random_output))

        self.connections = self.chunk_list(conns, field_width)

    def chunk_list(self, lst, n):
        return [lst[i:i + n] for i in range(0, len(lst), n)]

    def transpose_address(self, addr): # should be a list of 1's and 0's
        transposed = [] 
        for field in self.connections:
            tmp = []
            for i in field:
                tmp.append(addr[i])
            transposed.append(tmp)
        return transposed # will be a chunked list

    def align_address(self, addr): # to keep things within boundaries
        if len(addr) < self.total_input_length:
            while len(addr) < self.total_input_length:
                addr.append(0)
            return addr
        
        elif len(addr) > self.total_input_length:
            return addr[0:self.total_input_length]

        else:
            return addr 
            

    def read(self, addr):
        addr = self.align_address(addr)
        self.last_input = addr
        trans_addr = self.transpose_address(addr)
        outputs = []
        for i in range(0, len(trans_addr)):
            bit = self.rams[i].read(trans_addr[i])
            outputs.append(bit)
        self.last_output = outputs
        return outputs

    def write(self, addr, data):
        addr = self.align_address(addr)
        trans_addr = self.transpose_address(addr)
        if isinstance(data, int):
            for i in range(0, len(trans_addr)):
                self.rams[i].write(trans_addr[i], data)
        else:
            for i in range(0, len(trans_addr)):
                self.rams[i].write(trans_addr[i], data[i])

    def write_last(self, data):
        self.write(self.last_input, data) 

class stack:
    def __init__(self, config):
        # config is a 2d array of [fields, field width] len number of layers
        self.layers = []
        for c in config:
            self.layers.append(layer(c[0],c[1]))

    def read(self, addr):
        last_input = addr
        last_output = []

        for i in range(0, len(self.layers)):
            last_output = self.layers[i].read(last_input)
            last_input = last_output
        return last_output

    def write(self, addr, data):
        self.read(addr)
        self.layers[len(self.layers)-1].write_last(data)

    def write_without_prior_read(self, addr, data):
        self.layers[len(self.layers)-1].write_last(data)
            
