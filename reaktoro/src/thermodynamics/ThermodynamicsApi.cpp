#include "ThermodynamicsApi.hpp"
#include "ThermodynamicsCore.hpp"

std::string ThermodynamicsApi::processRequest(const crow::request& req) {
    // Parse query parameters, e.g., substance
    std::string substance = req.url_params.get("substance") ? req.url_params.get("substance") : "";

    ThermodynamicsCore core;
    return core.calculateProperties(substance);
}
