#include <iostream>
#include <numeric>

#include "basic/include/log.hpp"
#include "dictionary/include/structured_data.hpp"
#include "dictionary/include/tabulation.hpp"

float mean_probing_cnt(HashTable& table, std::shared_ptr<std::vector<uint32_t>> structured_keys)
{
    size_t keys_num = structured_keys->size();
    float probing_numsum = 0.;
    for (size_t i = 0; i < keys_num; ++i)
    {
        // if (i % 10000 == 0) std::cout << i << std::endl;
        size_t probing_num = table.insert(structured_keys->at(i));
        // if (i % 10000 == 0) std::cout << probing_num << std::endl;
        probing_numsum += probing_num;
    }
    return probing_numsum / keys_num;
}

std::vector<size_t> probing_hist(HashTable& table,
                                 std::shared_ptr<std::vector<uint32_t>> structured_keys)
{
    size_t keys_num = structured_keys->size();
    std::vector<size_t> key_probing_nums;
    key_probing_nums.resize(3000, 0);
    for (size_t i = 0; i < keys_num; ++i)
    {
        size_t probing_num = table.insert(structured_keys->at(i));
        if (probing_num < 3000) key_probing_nums[probing_num] += 1;
    }
    return key_probing_nums;
}

// void test_probing(std::shared_ptr<std::vector<uint32_t>> structured_keys)
// {
//     std::shared_ptr<Hash> SimpleTabulation_ptr = std::make_shared<SimpleTabulation>();
//     HashTable SimpleTabulation_table(1 << 21, SimpleTabulation_ptr);
//     std::vector<size_t> SimpleTabulation_probing_cnt =
//         probing_cnt(SimpleTabulation_table, structured_keys);
//     SaveVectortxt(SimpleTabulation_probing_cnt, "tmp/SimpleTabulation_probing_cnt.txt");
//     // std::shared_ptr<Hash> UnivMultShift_ptr = std::make_shared<UnivMultShift>(32, 21);
//     // HashTable UnivMultShift_table(1 << 21, UnivMultShift_ptr);
//     // std::vector<size_t> UnivMultShift_probing_cnt =
//     //     probing_cnt(UnivMultShift_table, structured_keys);
//     // SaveVectortxt(UnivMultShift_probing_cnt, "tmp/UnivMultShift_probing_cnt.txt");
// }

void test_SimpleTabulation_probing_100(std::shared_ptr<std::vector<uint32_t>> structured_keys)
{
    size_t keys_num = structured_keys->size();
    std::vector<float> mean_probing_cnts;
    for (size_t i = 0; i < 100; ++i)
    {
        std::shared_ptr<Hash> SimpleTabulation_ptr = std::make_shared<SimpleTabulation>();
        HashTable SimpleTabulation_table(1 << 21, SimpleTabulation_ptr);
        float SimpleTabulation_probing_cnt_mean =
            mean_probing_cnt(SimpleTabulation_table, structured_keys);
        mean_probing_cnts.push_back(SimpleTabulation_probing_cnt_mean);
    }
    SaveVectortxt(mean_probing_cnts, "tmp/SimpleTabulation_mean_probing_cnts.txt");
}

void test_Indpd5TZTable_probing_100(std::shared_ptr<std::vector<uint32_t>> structured_keys)
{
    size_t keys_num = structured_keys->size();
    std::vector<float> mean_probing_cnts;
    for (size_t i = 0; i < 100; ++i)
    {
        std::shared_ptr<Hash> hashfunc_ptr = std::make_shared<Indpd5TZTable>();
        HashTable hash_table(1 << 21, hashfunc_ptr);
        float hash_probing_cnt_mean = mean_probing_cnt(hash_table, structured_keys);
        mean_probing_cnts.push_back(hash_probing_cnt_mean);
    }
    SaveVectortxt(mean_probing_cnts, "tmp/Indpd5TZTable_mean_probing_cnts.txt");
}

void test_UnivMultShift_probing_100(std::shared_ptr<std::vector<uint32_t>> structured_keys)
{
    size_t keys_num = structured_keys->size();
    std::vector<float> mean_probing_cnts;
    for (size_t i = 0; i < 100; ++i)
    {
        std::shared_ptr<Hash> UnivMultShift_ptr = std::make_shared<UnivMultShift>(32, 21);
        HashTable UnivMultShift_table(1 << 21, UnivMultShift_ptr);
        float UnivMultShift_probing_cnt_mean =
            mean_probing_cnt(UnivMultShift_table, structured_keys);
        // std::cout << "UnivMultShift_probing_cnt_mean=" << UnivMultShift_probing_cnt_mean
        //           << std::endl;
        mean_probing_cnts.push_back(UnivMultShift_probing_cnt_mean);
    }
    SaveVectortxt(mean_probing_cnts, "tmp/UnivMultShift_mean_probing_cnts.txt");
}

// Indpd2MultShift

void test_Indpd2MultShift_probing_100(std::shared_ptr<std::vector<uint32_t>> structured_keys)
{
    size_t keys_num = structured_keys->size();
    std::vector<float> mean_probing_cnts;
    for (size_t i = 0; i < 100; ++i)
    {
        std::shared_ptr<Hash> hashfunc_ptr = std::make_shared<Indpd2MultShift>(32, 21);
        HashTable hash_table(1 << 21, hashfunc_ptr);
        float hash_probing_cnt_mean = mean_probing_cnt(hash_table, structured_keys);
        mean_probing_cnts.push_back(hash_probing_cnt_mean);
    }
    SaveVectortxt(mean_probing_cnts, "tmp/Indpd2MultShift_mean_probing_cnts.txt");
}

void test_Indpd5MersennePrime_probing_100(std::shared_ptr<std::vector<uint32_t>> structured_keys)
{
    size_t keys_num = structured_keys->size();
    std::vector<float> mean_probing_cnts;
    for (size_t i = 0; i < 100; ++i)
    {
        std::shared_ptr<Hash> Indpd5MersennePrime_ptr =
            std::make_shared<PolynomialMersenneHash>(5, 61, 32);
        HashTable Indpd5MersennePrime_table(1 << 21, Indpd5MersennePrime_ptr);
        float Indpd5MersennePrime_probing_cnt_mean =
            mean_probing_cnt(Indpd5MersennePrime_table, structured_keys);
        // std::cout << "Indpd5MersennePrime_probing_cnt_mean=" <<
        // Indpd5MersennePrime_probing_cnt_mean
        //           << std::endl;
        mean_probing_cnts.push_back(Indpd5MersennePrime_probing_cnt_mean);
    }
    SaveVectortxt(mean_probing_cnts, "tmp/Indpd5MersennePrime_mean_probing_cnts.txt");
}

void mean_probing_100(const std::string& hash_type,
                      std::shared_ptr<std::vector<uint32_t>> structured_keys,
                      std::string dataname = "")
{
    size_t keys_num = structured_keys->size();
    std::vector<float> mean_probing_cnts;
    for (size_t i = 0; i < 100; ++i)
    {
        std::shared_ptr<Hash> hashfunc_ptr;
        if (hash_type == "UnivMultShift")
        {
            hashfunc_ptr = std::make_shared<UnivMultShift>(32, 21);
        }
        else if (hash_type == "Indpd2MultShift")
        {
            hashfunc_ptr = std::make_shared<Indpd2MultShift>(32, 21);
        }
        else if (hash_type == "SimpleTabulation")
        {
            hashfunc_ptr = std::make_shared<SimpleTabulation>();
        }
        else if (hash_type == "Indpd5TZTable")
        {
            hashfunc_ptr = std::make_shared<Indpd5TZTable>();
        }
        else if (hash_type == "Indpd5MersennePrime")
        {
            hashfunc_ptr = std::make_shared<PolynomialMersenneHash>(5, 61, 32);
        }
        else
        {
            std::cerr << "Unknown hash type.\n";
        }
        HashTable hash_table(1 << 21, hashfunc_ptr);
        float hash_probing_cnt_mean = mean_probing_cnt(hash_table, structured_keys);
        mean_probing_cnts.push_back(hash_probing_cnt_mean);
    }
    std::string mean_prob_file;
    if (dataname.size() == 0)
        mean_prob_file = "tmp/" + hash_type + "_mean_probing_cnts.txt";
    else
        mean_prob_file = "tmp/" + dataname + "_" + hash_type + "_mean_probing_cnts.txt";
    SaveVectortxt(mean_probing_cnts, mean_prob_file);
}

int main()
{
    auto structured_keys = hypercube_data(20);
    // test_SimpleTabulation_probing_100(structured_keys);
    // test_UnivMultShift_probing_100(structured_keys);
    // test_Indpd5MersennePrime_probing_100(structured_keys);
    // test_Indpd2MultShift_probing_100(structured_keys);
    // test_Indpd5TZTable_probing_100(structured_keys);
    mean_probing_100("UnivMultShift", structured_keys);
    mean_probing_100("Indpd2MultShift", structured_keys);
    mean_probing_100("Indpd5MersennePrime", structured_keys);
    mean_probing_100("SimpleTabulation", structured_keys);
    mean_probing_100("Indpd5TZTable", structured_keys);
    return 0;
}