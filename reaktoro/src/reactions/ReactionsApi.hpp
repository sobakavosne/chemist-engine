#pragma once

#include <crow.h>
#include <string>

class ReactionsApi {
public:
    std::string processRequest(const crow::request& req);  // New function for handling Crow requests
};
