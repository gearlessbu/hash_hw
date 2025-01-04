#include "dictionary/include/tabulation.hpp"

#include <iostream>
#include <random>

#include "basic/include/log.hpp"

uint64_t generateRandom(uint64_t range_size)
{
    std::mt19937 generator(std::random_device{}());

    std::uniform_int_distribution<uint64_t> distribution(0, range_size - 1);

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

Indpd2MultShift::Indpd2MultShift(size_t l, size_t l_out) : m_l(l), m_l_out(l_out)
{
    m_a = generateRandom(UINT64_MAX);
    m_b = generateRandom(UINT64_MAX);
}

uint32_t Indpd2MultShift::hash(uint32_t x)
{
    // return (m_a * x) & 0xFFFFFFFF;
    // return (m_a * x) & m_mask;
    return (m_a * x + m_b) >> (2 * m_l - m_l_out);
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
    m_hash_tables = new uint32_t*[num_tables];

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

Indpd5TZTable::Indpd5TZTable()
{
    for (size_t i = 0; i < 256; ++i)
    {
        for (size_t j = 0; j < 2; ++j)
        {
            T0[i][j] = generateRandom(UINT32_MAX);
            T1[i][j] = generateRandom(UINT32_MAX);
            T2[i][j] = generateRandom(UINT32_MAX);
            T3[i][j] = generateRandom(UINT32_MAX);
        }
    }
    for (size_t i = 0; i < 1024; ++i)
    {
        T4[i] = generateRandom(UINT32_MAX);
        T5[i] = generateRandom(UINT32_MAX);
    }
    for (size_t i = 0; i < 4096; ++i)
    {
        T6[i] = generateRandom(UINT32_MAX);
    }
}

inline uint32_t compressChar32(uint32_t i)
{
    const uint32_t Mask1 = (((uint32_t)3) << 20) + (((uint32_t)3) << 10) + 3;
    const uint32_t Mask2 = (((uint32_t)255) << 20) + (((uint32_t)255) << 10) + 255;
    const uint32_t Mask3 = (((uint32_t)3) << 20) + (((uint32_t)3) << 10) + 3;
    return Mask1 + (i & Mask2) - ((i >> 8) & Mask3);
}

uint32_t Indpd5TZTable::hash(uint32_t x)
{
    uint32_t h = 0;
    uint8_t x0, x1, x2, x3;
    x0 = x;
    x = x >> 8;
    x1 = x;
    x = x >> 8;
    x2 = x;
    x = x >> 8;
    x3 = x;
    uint32_t* a0 = T0[x0];
    uint32_t* a1 = T1[x1];
    uint32_t* a2 = T2[x2];
    uint32_t* a3 = T3[x3];
    uint32_t c = a0[1] + a1[1] + a2[1] + a3[1];
    c = compressChar32(c);
    return a0[0] ^ a1[0] ^ a2[0] ^ a3[0] ^ T4[c & 1023] ^ T5[(c >> 10) & 1023] ^ T6[c >> 20];
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