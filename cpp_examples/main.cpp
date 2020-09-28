#include"z3++.h"

#include<bits/stdc++.h>


std::vector<const char*> c_pos_str;
std::vector<const char*> c_size_str;


struct symbolic_chunk {
    int id;
    z3::expr pos;
    z3::expr size;
};


using sym_chunk_ptr =  struct symbolic_chunk*;

void init_sym_chunk(z3::context& c, sym_chunk_ptr s, int id) {
    std::cout << "Initalizing Sym Chunk with id = " << id << std::endl;


    s->id = id;
    std::cout << "Chkpt1" << std::endl;
    s->pos = c.bv_const(c_pos_str[id], 32);
    std::cout << "Chkpt2" << std::endl;
    s->size = c.bv_const(c_size_str[id], 32);

    std::cout << "Initalized Sym Chunk with id = " << id << std::endl;
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
    z3::context c;
    std::vector<sym_chunk_ptr> chunks;
    for(int i = 0 ; i < 5 ; i++) {
        char p_[] = "p_";

        char s_[] = "s_";
        
        const char* p = strcat(p_, std::to_string(i).c_str());
        const char* s = strcat(s_, std::to_string(i).c_str());
        c_pos_str.push_back(p);
        c_size_str.push_back(s);
    }
    for(int i = 0; i < 5 ; i++) {
        std::cout << sizeof(struct symbolic_chunk) << std::endl;
        
        sym_chunk_ptr s = (sym_chunk_ptr)malloc(sizeof(struct symbolic_chunk));

        init_sym_chunk(c, s, i);

        chunks.push_back(s);
        
        
    }
    return 0;

    int heap_size = 0x400;

    z3::solver s(c);

    // s.add((s1->pos > s2->pos && s1->pos < s2->pos + s2->size) || (s2->pos > s1->pos && s2->pos < s1->pos + s1->size));
    
    std::vector<int> chunk_positions = {0x000, 0x100, 0x200, 0x300}; 
    std::vector<z3::expr_vector> or_vecs;
    
    for(int i = 0 ; i < 5 ; i++) {
        or_vecs.push_back(z3::expr_vector(c));
    }

    for(auto i : chunk_positions) {
        for(int j = 0 ; j < 5 ; j++) {
            or_vecs[j].push_back(chunks[j]->pos == i);
        }
    }
    for (int i = 0 ; i < 5 ; i++) {
        s.add(z3::mk_or(or_vecs[i]));
    }
    
    for (int i = 0 ; i < 5 ; i++) {
        for (int j = 0 ; j < 5 ; j++) {
            if(i == j)
                continue;
            s.add(chunks[i]->pos != chunks[j]->pos);
        }
    }

    for (int i = 0 ; i < 5 ; i++) {
        s.add(chunks[i]->pos + chunks[i]->size < heap_size && chunks[i]->pos + chunks[i]->size > 0 );
    }
    
    for (int i = 0 ; i < 5 ; i++) {
        s.add(chunks[i]->size == 0x100);
    }
    


    std::cout << s.check() << std::endl;

    // z3::model m = s.get_model();


    // std::cout << std::endl << m << std::endl; 
    return 0;
}