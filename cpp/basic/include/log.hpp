#ifndef HASH_BASIC_LOG
#define HASH_BASIC_LOG

#include <fstream>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

template <typename T>
void SaveVectortxt(const std::vector<T>& vector_src, const std::string& dst_path)
{
    std::ofstream ofs(dst_path);
    if (!ofs)
    {
        std::cerr << "Failed to open file for writing\n";
        return;
    }

    for (const auto& val : vector_src)
    {
        ofs << val << " ";
    }

    ofs.close();
}

#endif