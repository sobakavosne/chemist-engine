module Utils

export check_for_errors

function check_for_errors(sol)
  if any(isnan, sol.u) || any(isinf, sol.u)
    return "Solution contains NaN or Inf values. Check equations and parameters."
  end
  return nothing
end

end
