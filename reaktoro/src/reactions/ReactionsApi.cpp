#include "ReactionsApi.hpp"
#include "ReactionsCore.hpp"

std::string ReactionsApi::processRequest(const crow::request& req) {
    // Example processing logic based on request
    // Parse query parameters, e.g., species1 and species2
    std::string species1 = req.url_params.get("species1") ? req.url_params.get("species1") : "";
    std::string species2 = req.url_params.get("species2") ? req.url_params.get("species2") : "";

    ReactionsCore core;
    return core.computeReaction(species1, species2);
}
