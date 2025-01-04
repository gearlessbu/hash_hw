#include "dictionary/include/tabulation.hpp"

#include <iostream>
#include <random>

#include "basic/include/log.hpp"

uint32_t generateRandom(uint64_t range_size)
{
    std::mt19937 generator(std::random_device{}());

    std::uniform_int_distribution<uint32_t> distribution(0, range_size - 1);

    return distribution(generator);
}

UnivMultShift::UnivMultShift(size_t l, size_t l_out) : m_l(l), m_l_out(l_out)
{
    m_a = generateRandom(4294967296) | 1;
}
uint32_t UnivMultShift::hash(uint32_t x)
{
    // return (m_a * x) & 0xFFFFFFFF;
    // return (m_a * x) & m_mask;
    return (m_a * x) >> (m_l - m_l_out);
}

PolynomialMersenneHash::PolynomialMersenneHash(size_t k, uint32_t b, size_t l_out)
    : m_k(k), m_b(b), m_l_out(l_out), m_p((1ULL << b) - 1ULL)
{
    m_a = new uint32_t[k];
    for (size_t i = 0; i < k; ++i)
    {
        m_a[i] = generateRandom(UINT32_MAX);
    }
}

uint32_t PolynomialMersenneHash::hash(uint32_t x)
{
    // https://thomasahle.com/papers/mersenne.pdf Alg 1.
    __uint128_t y = m_a[m_k - 1];
    for (int i = m_k - 2; i >= 0; --i)
    {
        y = y * x + m_a[i];
        y = (y & m_p) + (y >> m_b);
    }
    y = (y & m_p) + (y >> m_b);
    return y & ((1ULL << m_l_out) - 1);
}

PolynomialMersenneHash::~PolynomialMersenneHash() { delete[] m_a; }

SimpleTabulation::SimpleTabulation(size_t num_tables, size_t domain_size, uint64_t range_size)
    : m_num_tables(num_tables), m_domain_size(domain_size), m_range_size(range_size)
{
    m_hash_tables = new uint32_t *[num_tables];

    // std::mt19937_64 rng(time(0));
    // std::uniform_int_distribution<uint32_t> dist(0, UINT32_MAX - 1);
    for (size_t i = 0; i < num_tables; ++i)
    {
        m_hash_tables[i] = new uint32_t[domain_size];
        for (size_t j = 0; j < domain_size; ++j)
        {
            m_hash_tables[i][j] = generateRandom(range_size);
            // m_hash_tables[i][j] = dist(rng);
            // std::cout << m_hash_tables[i][j] << "    ";
        }
        // std::cout << std::endl;
    }
}

uint32_t SimpleTabulation::hash(uint32_t x)
{
    uint32_t h = 0;
    uint8_t c;
    for (size_t i = 0; i < m_num_tables; ++i)
    {
        c = x;
        h ^= m_hash_tables[i][c];
        x = x >> 8;
    }
    return h;
}

SimpleTabulation::~SimpleTabulation()
{
    for (size_t i = 0; i < m_num_tables; ++i)
    {
        delete[] m_hash_tables[i];
    }
    delete[] m_hash_tables;
}

HashTable::HashTable(size_t capacity, std::shared_ptr<Hash> hash_func)
    : m_capacity(capacity), m_size(0), m_hash_func(hash_func)
{
    m_table.resize(capacity, std::nullopt);
}

size_t HashTable::insert(uint32_t key)
{
    if (m_size == m_capacity)
    {
        std::cerr << "Hash table is full!\n";
        return false;
    }

    size_t index = m_hash_func->hash(key) % m_capacity;
    // printf("{%d}dd\n", index);

    size_t probing_time = 1;
    // Linear probing
    while (m_table[index].has_value())
    {
        if (m_table[index].value() == key)
        {
            // Key already exists
            return 0;
        }
        index = (index + 1) % m_capacity;  // Move to the next slot
        probing_time += 1;
    }

    m_table[index] = key;  // Insert the key
    ++m_size;
    return probing_time;
}