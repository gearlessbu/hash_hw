#ifndef HASH_DICTIONARY_STRUCTURED_DATA
#define HASH_DICTIONARY_STRUCTURED_DATA

#include <memory>
#include <vector>

std::shared_ptr<std::vector<uint32_t>> hypercube_data(size_t bit_num)
{
    auto seq = std::make_shared<std::vector<uint32_t>>();
    for (int i = 0; i < 1 << bit_num; ++i)
    {
        seq->push_back(i);
    }
    return seq;
}

#endif