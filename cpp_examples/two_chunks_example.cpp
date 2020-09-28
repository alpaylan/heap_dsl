#include"z3++.h"
#include<bits/stdc++.h>

z3::context c;


#define sym_malloc(solver, chunk, size)  solver.add(chunk->size == c.bv_val(size, 32));                                          

struct symbolic_chunk {
    int id;
    z3::expr pos;
    z3::expr size;
};


using sym_chunk_ptr =  struct symbolic_chunk*;

void init_sym_chunk(sym_chunk_ptr s, int id) {
    std::cout << "Initalizing Sym Chunk with id = " << id << std::endl;

    s->id = id;
    s->pos = c.bv_const((std::string("p_") + std::to_string(s->id)).c_str(), 32);
    s->size = c.bv_const((std::string("s_") + std::to_string(s->id)).c_str(), 32);
}



void print_sym_chunk(sym_chunk_ptr s) {
    std::cout << "\nPrinting Symbolic Chunk\n";
    std::cout << "Id: " << s->id << std::endl;
    std::cout << "Position: " << s->pos << std::endl;
    std::cout << "Size: " << s->size << std::endl;
}

void print_modeled_chunk(sym_chunk_ptr s, z3::model m) {
    std::cout << "\nPrinting Symbolic Chunk Model\n";
    std::cout << "Id: " << m[s->id] << std::endl;
    std::cout << "Position: " << m[s->pos] << std::endl;
    std::cout << "Size: " << m[s->size] << std::endl;
}

int main() {
    sym_chunk_ptr s1 = (sym_chunk_ptr)malloc(sizeof(struct symbolic_chunk));
    sym_chunk_ptr s2 = (sym_chunk_ptr)malloc(sizeof(struct symbolic_chunk));
    
    init_sym_chunk(s1, 0);
    init_sym_chunk(s2, 1);

    int heap_size = 0x400;

    z3::solver s(c);

    // s.add((s1->pos > s2->pos && s1->pos < s2->pos + s2->size) || (s2->pos > s1->pos && s2->pos < s1->pos + s1->size));
    
    print_sym_chunk(s1);
    print_sym_chunk(s2);

    std::vector<int> chunk_positions = {0x000, 0x100, 0x200, 0x300}; 
    z3::expr_vector temp1(c);
    z3::expr_vector temp2(c);
    for(auto i : chunk_positions) {
        temp1.push_back(s1->pos == i);
        temp2.push_back(s2->pos == i);
    }
    s.add(z3::mk_or(temp1));
    s.add(z3::mk_or(temp2));

    s.add(s1->pos != s2->pos);

    s.add(s1->pos + s1->size < heap_size && s1->pos + s1->size > 0 );
    s.add(s2->pos + s2->size < heap_size && s2->pos + s2->size > 0 );

    s.add(s1->size == 0x100);
    s.add(s2->size == 0x100);


    std::cout << s.check() << std::endl;

    z3::model m = s.get_model();


    std::cout << std::endl << m << std::endl; 
    return 0;
}