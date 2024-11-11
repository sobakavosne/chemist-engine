#include <crow.h>
#include "reactions/ReactionsApi.hpp"
#include "thermodynamics/ThermodynamicsApi.hpp"

void RunServer()
{
  crow::SimpleApp app;

  ReactionsApi reactions_service;
  ThermodynamicsApi thermodynamics_service;

  // Define a route for reactions
  CROW_ROUTE(app, "/api/reactions")
  ([&reactions_service](const crow::request &req)
   {
        // Assuming processRequest is defined in ReactionsApi to handle requests
        return crow::response(reactions_service.processRequest(req)); });

  // Define a route for thermodynamics
  CROW_ROUTE(app, "/api/thermodynamics")
  ([&thermodynamics_service](const crow::request &req)
   {
        // Assuming processRequest is defined in ThermodynamicsApi to handle requests
        return crow::response(thermodynamics_service.processRequest(req)); });

  // Start the server on port 50051
  std::cout << "Server listening on http://0.0.0.0:50051" << std::endl;
  app.port(50051).multithreaded().run();
}
