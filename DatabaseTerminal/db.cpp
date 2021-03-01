#include <iostream>
#include <mariadb/mysql.h>
#include <fstream>
#include <vector>
#include <time.h>

std::string HOST = "localhost";
std::string USER = "deltaX72";
std::string PASSWORD = "mypassword";
std::string NAME = "co2_concentration";
const char* TABLE = "info";
const int PORT = 0;

void exitWithError(MYSQL* connect);
int loadDataFromFile(std::string filename, std::string version, MYSQL* connect);
std::vector<std::string> split(std::string& str, std::string delimiter);

int main(int argc, char* argv[]) {
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
    
    size_t yearFrom = atoi(argv[1]);
    size_t monthFrom = atoi(argv[2]);
    size_t yearTo = atoi(argv[3]);
    size_t monthTo = atoi(argv[4]);
    std::string version = argv[5];

    size_t year = yearFrom;
    size_t month = monthFrom;

    time_t totalTime = 0;
    time_t localTime = 0;
    char buffer[80];

    while (true) {
        if (month > 12) {
            year++;
            month = 1;
        }
        std::string monthMask = (month > 0 && month < 10) ? "0" + std::to_string(month) : std::to_string(month);
        char fmt_mask[] = "./file_buffer/%s%s_%s.txt";
        snprintf(buffer, sizeof(buffer), fmt_mask, std::to_string(year).c_str(), monthMask.c_str(), version.c_str());
        
        time_t startTime;
        time(&startTime);
        auto out = loadDataFromFile(buffer, version, connect);
        if (out == 0) {
            time_t finishTime;
            time(&finishTime);
            localTime = finishTime - startTime;
            totalTime += localTime;
            std::cout << "[" << year << "-" << monthMask << "] local time = " << localTime << ", total time = " << totalTime << std::endl;
        } else if (out == 1) {
            std::cerr << "[" << year << "-" << monthMask << "] File not found!" << std::endl;
        }
        std::cout << "[" << year << "-" << monthMask << "]" << std::endl;

        if (year == yearTo && month == monthTo) 
            break;
        month++;
    }

    mysql_close(connect);
    return 0;
}

void exitWithError(MYSQL* connect) {
    std::cerr << mysql_error(connect) << std::endl;
    mysql_close(connect);
    exit(1);
}

int loadDataFromFile(std::string filename, std::string version, MYSQL* connect) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        return 1;
    }

    std::string line;
    char buffer[512];
    MYSQL_RES* result;

    std::string queryLine = "INSERT INTO `info` (`date`, `time`, `latitude`, `longitude`, `concentration`, `version`) VALUES ";
    bool isError = false;

    while (!file.eof()) {
        getline(file, line);
        auto array = split(line, " ");
        if (array.size() != 5) {
            isError = true;
            break;
        }
        
        char fmt_ex[] = "SELECT * FROM `info` WHERE (`date`=\"%s\" AND `time`=\"%s\" AND `latitude`=%f AND `longitude`=%f AND `concentration`=%f AND `version`=\"%s\")";
        snprintf(buffer, sizeof(buffer), fmt_ex, array[0].c_str(), array[1].c_str(), atof(array[2].c_str()), atof(array[3].c_str()), atof(array[4].c_str()), version.c_str());
        if (mysql_query(connect, buffer)) exitWithError(connect);
        result = mysql_store_result(connect);
        
        int rows = mysql_num_rows(result);
        if (rows == 1) continue;

        char fmt[] = "('%s', '%s', %f, %f, %f, '%s'),";
        snprintf(buffer, sizeof(buffer), fmt, array[0].c_str(), array[1].c_str(), atof(array[2].c_str()), atof(array[3].c_str()), atof(array[4].c_str()), version.c_str());
        // std::cout << buffer << std::endl;
        queryLine += buffer;
    }
    queryLine.erase(queryLine.size() - 1);
    mysql_query(connect, queryLine.c_str());
    // std::cout << queryLine << std::endl;
    // if (mysql_query(connect, queryLine.c_str())) {
    //     exitWithError(connect);
    // }

    // =================== запрос по одному ===========================
    // while (!file.eof()) {
    //     getline(file, line);
    //     auto array = split(line, " ");
    //     if (array.size() != 5) break;
        
    //     char fmt_ex[] = "SELECT * FROM `%s` WHERE (`date`=\"%s\" AND `time`=\"%s\" AND `latitude`=%f AND `longitude`=%f AND `concentration`=%f AND `version`=\"%s\")";
    //     // // SELECT EXISTS (SELECT * FROM `info` WHERE (`date`='2009-04-27' AND `time`='01:11:24.301' AND `latitude`=21.145601 AND `longitude`=177.22966 AND `concentration`=387.71246 AND `version`='V02.75') LIMIT 1)
    //     snprintf(buffer, sizeof(buffer), fmt_ex, TABLE, array[0].c_str(), array[1].c_str(), atof(array[2].c_str()), atof(array[3].c_str()), atof(array[4].c_str()), version.c_str());

    //     if (mysql_query(connect, buffer)) exitWithError(connect);
    //     result = mysql_store_result(connect);
        
    //     int rows = mysql_num_rows(result);
    //     // std::cout << rows << std::endl;
    //     // break;
    //     if (rows == 1) continue;
        
    //     char fmt[] = "INSERT INTO `%s` (`date`, `time`, `latitude`, `longitude`, `concentration`, `version`) VALUES ('%s', '%s', %f, %f, %f, '%s')";
    //     // INSERT INTO `info`(`date`, `time`, `latitude`, `longitude`, `concentration`, `version`) VALUES ('2009-04-27','01:11:24.301',21.145601,177.22966,387.71246,'V02.75')
    //     snprintf(buffer, sizeof(buffer), fmt, TABLE, array[0].c_str(), array[1].c_str(), atof(array[2].c_str()), atof(array[3].c_str()), atof(array[4].c_str()), version.c_str());
    //     // std::cout << buffer << std::endl;
    //     if (mysql_query(connect, buffer)) {
    //         exitWithError(connect);
    //     }

    //     // SELECT EXISTS (SELECT * FROM info WHERE date="2009-04-27" AND time="00:00:01.123" AND latitude=100.0 AND longitude=200.0 AND concentration=400.0 AND version="V02.75") LIMIT 1;

    // }
    
    file.close();
    return 0;
}

// std::vector<char*> split(std::string str, std::string delimiter) {
//     size_t pos = 0;
//     std::vector<char*> array;
//     str += delimiter;
//     while ((pos = str.find(delimiter)) != std::string::npos) {
//         char *tmp = (char*)str.substr(0, pos).c_str();

//         array.push_back(tmp);
//         str.erase(0, pos + delimiter.length());
//         std::cout << tmp << std::endl;
//     }
//     return array;
// }

std::vector<std::string> split(std::string& str, std::string delimiter) {
    size_t pos = 0;
    std::vector<std::string> array;
    str += delimiter;
    while ((pos = str.find(delimiter)) != std::string::npos) {
        array.push_back(str.substr(0, pos));
        str.erase(0, pos + delimiter.length());
    }
    return array;
}