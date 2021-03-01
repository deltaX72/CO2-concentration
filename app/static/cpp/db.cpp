#include <iostream>
#include <mariadb/mysql.h>
#include <fstream>
#include <vector>

std::string HOST = "localhost";
std::string USER = "deltaX72";
std::string PASSWORD = "mypassword";
std::string NAME = "co2_concentration";
std::string TABLE = "info";
const int PORT = 0;

void exitWithError(MYSQL* connect);
void loadDataFromFile(std::string filename, MYSQL* connect);
std::vector<std::string> split(std::string& str, std::string delimiter);

int main() {
    MYSQL* connect = mysql_init(nullptr);
    if (!connect) exitWithError(connect);
    if (!mysql_real_connect(
        connect, 
        HOST.c_str(), 
        USER.c_str(), 
        PASSWORD.c_str(), 
        NAME.c_str(), 
        PORT, 
        nullptr, 
        0)
    ) exitWithError(connect);

    

    // std::string query = "SELECT * FROM " + TABLE;
    // if (!mysql_query(connect, query.c_str())) exitWithError(connect);

    // MYSQL_RES* result = mysql_store_result(connect);
    // if (!result) exitWithError(connect);

    // int num_fields = mysql_num_fields(result);
    // MYSQL_ROW row;

    // while (row = mysql_fetch_row(result)) {
    //     for (int i = 0; i < num_fields; i++) {
    //         std::cout << row[i] ? row[i] : NULL;
    //     }
    //     std::cout << std::endl;
    // }

    mysql_free_result(result);
    mysql_close(connect);
    return 0;
}

void exitWithError(MYSQL* connect) {
    std::cerr << mysql_error(connect) << std::endl;
    mysql_close(connect);
    exit(1);
}

void loadDataFromFile(std::string filename, MYSQL* connect) {
    std::ifstream file(filename);
    std::string line;
    while (!file.eof()) {
        getline(file, line);
        auto array = split(line, " ");
        std::string query = "INSERT INTO `" + 
        TABLE + 
        "`(`date`, `time`, `latitude`, `longitude`, `concentration`) VALUES (" +
        array[0] + ", " + 
        array[1] + ", " + 
        array[2] + ", " + 
        array[3] + ", " + 
        array[4] + ")"
        ;
        if(!mysql_query(connect, query.c_str())) exitWithError(connect);
        std::cout << query << std::endl;
    }

    file.close();
}

std::vector<std::string> split(std::string& str, std::string delimiter) {
    size_t pos = 0;
    std::vector<std::string> array;
    while ((pos = str.find(delimiter)) != std::string::npos) {
        array.push_back(str.substr(0, pos));
        str.erase(0, pos + delimiter.length());
    }
    return array;
}