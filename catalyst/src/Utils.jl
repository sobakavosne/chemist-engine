module Utils

export check_for_errors

# Utility function to check for errors in the solution
function check_for_errors(sol)
  # Check if the solution contains invalid values (NaN or Inf)
  if any(isnan, sol.u) || any(isinf, sol.u)
    return "Solution contains NaN or Inf values. Check equations and parameters."
  end
  return nothing  # No errors found
end

end
