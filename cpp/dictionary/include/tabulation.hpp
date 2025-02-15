#ifndef HASH_DICTIONARY_TABULATION
#define HASH_DICTIONARY_TABULATION

#include <memory>
#include <optional>
#include <vector>

struct Hash
{
    virtual uint32_t hash(uint32_t x) = 0;
};

struct UnivMultShift : public Hash
{
    UnivMultShift(size_t l, size_t l_out);
    uint32_t hash(uint32_t x);

    const size_t m_l, m_l_out;
    uint32_t m_a;
    uint32_t m_mask;
};

struct Indpd2MultShift : public Hash
{
    Indpd2MultShift(size_t l, size_t l_out);
    uint32_t hash(uint32_t x);

    const size_t m_l, m_l_out;
    uint64_t m_a;
    uint64_t m_b;
};

struct PolynomialMersenneHash : public Hash
{
    PolynomialMersenneHash(size_t k, uint32_t b, size_t l_out);
    ~PolynomialMersenneHash();

    uint32_t hash(uint32_t x);

    const size_t m_k;
    // Mersenne prime p = 2^b - 1
    const uint32_t m_b;
    const uint64_t m_p;
    const size_t m_l_out;
    uint32_t *m_a;
};

struct SimpleTabulation : public Hash
{
    SimpleTabulation(size_t num_tables = 4, size_t domain_size = 256,
                     uint64_t range_size = 4294967296);
    ~SimpleTabulation();

    uint32_t hash(uint32_t x);

    const size_t m_num_tables;
    const size_t m_domain_size;
    const uint64_t m_range_size;
    uint32_t **m_hash_tables;
};

struct Indpd5TZTable : public Hash
{
    Indpd5TZTable();

    uint32_t hash(uint32_t x);

    uint32_t T0[256][2];
    uint32_t T1[256][2];
    uint32_t T2[256][2];
    uint32_t T3[256][2];
    uint32_t T4[1024];
    uint32_t T5[1024];
    uint32_t T6[4096];
};

struct HashTable
{
    HashTable(size_t capacity, std::shared_ptr<Hash> hash_func);
    // return the time of probing in the insert process
    size_t insert(uint32_t key);

    size_t m_size;
    size_t m_capacity;
    std::shared_ptr<Hash> m_hash_func;
    std::vector<std::optional<uint32_t>> m_table;
};

#endif
