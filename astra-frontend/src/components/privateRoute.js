import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../contexts/authContext";

const PrivateRoute = ({ element, ...rest }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? element : <Navigate to="/" />;
};

export default PrivateRoute;
