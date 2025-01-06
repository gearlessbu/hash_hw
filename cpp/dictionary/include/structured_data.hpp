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

std::shared_ptr<std::vector<uint32_t>> dense_interval(size_t bit_num = 20, uint64_t size = 1000000)
{
    auto seq = std::make_shared<std::vector<uint32_t>>();
    std::vector<uint32_t> origin_seq;
    for (int i = 0; i < 1 << bit_num; ++i)
    {
        origin_seq.push_back(i);
    }
    std::random_device rd;
    std::mt19937 gen(rd());
    std::shuffle(origin_seq.begin(), origin_seq.end(), gen);
    for (uint64_t i = 0; i < size; ++i)
    {
        seq->push_back(origin_seq[i]);
    }
    return seq;
}

#endif