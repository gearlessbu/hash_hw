#include <chrono>
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

float mean_hash_time(const std::string& hash_type,
                     std::shared_ptr<std::vector<uint32_t>> structured_keys)
{
    size_t keys_num = structured_keys->size();
    std::vector<float> mean_probing_cnts;
    std::vector<float> mean_insert_nanosec;
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
    auto start = std::chrono::high_resolution_clock::now();
    for (size_t i = 0; i < keys_num; ++i)
    {
        auto index = hashfunc_ptr->hash(structured_keys->at(i));
    }
    auto end = std::chrono::high_resolution_clock::now();
    return std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() /
           float(keys_num);
}

void mean_probing_100(const std::string& hash_type,
                      std::shared_ptr<std::vector<uint32_t>> structured_keys,
                      std::string dataname = "")
{
    size_t keys_num = structured_keys->size();
    std::vector<float> mean_probing_cnts;
    std::vector<float> mean_insert_nanosec;
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
        auto start = std::chrono::high_resolution_clock::now();
        float hash_probing_cnt_mean = mean_probing_cnt(hash_table, structured_keys);
        auto end = std::chrono::high_resolution_clock::now();
        mean_insert_nanosec.push_back(
            std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() /
            float(keys_num));
        mean_probing_cnts.push_back(hash_probing_cnt_mean);
    }
    std::string mean_prob_file;
    std::string mean_insert_nanosec_file;
    if (dataname.size() == 0)
    {
        mean_insert_nanosec_file = "tmp/" + hash_type + "_mean_insert_nanosec.txt";
        mean_prob_file = "tmp/" + hash_type + "_mean_probing_cnts.txt";
    }
    else
    {
        mean_insert_nanosec_file =
            "tmp/" + dataname + "_" + hash_type + "__mean_insert_nanosec.txt";
        mean_prob_file = "tmp/" + dataname + "_" + hash_type + "_mean_probing_cnts.txt";
    }
    SaveVectortxt(mean_probing_cnts, mean_prob_file);
    SaveVectortxt(mean_insert_nanosec, mean_insert_nanosec_file);
}

int main()
{
    auto structured_keys = hypercube_data(20);

    std::vector<float> mean_hash_times;
    mean_hash_times.push_back(mean_hash_time("UnivMultShift", structured_keys));
    mean_hash_times.push_back(mean_hash_time("Indpd2MultShift", structured_keys));
    mean_hash_times.push_back(mean_hash_time("Indpd5MersennePrime", structured_keys));
    mean_hash_times.push_back(mean_hash_time("SimpleTabulation", structured_keys));
    mean_hash_times.push_back(mean_hash_time("Indpd5TZTable", structured_keys));
    SaveVectortxt(mean_hash_times, "tmp/mean_hash_time.txt");

    mean_probing_100("UnivMultShift", structured_keys);
    mean_probing_100("Indpd2MultShift", structured_keys);
    mean_probing_100("Indpd5MersennePrime", structured_keys);
    mean_probing_100("SimpleTabulation", structured_keys);
    mean_probing_100("Indpd5TZTable", structured_keys);
    return 0;
}