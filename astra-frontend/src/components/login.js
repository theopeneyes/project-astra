import React, { useState, useEffect } from "react";
import { useAuth } from "../contexts/authContext";
import { useNavigate, useLocation } from "react-router-dom";
import { goTo } from "./common/goTo";
import Cookies from "js-cookie";
import axios from "axios";
// import { setAutoLogout, clearAutoLogout } from "../utils/authTimeout";
import { Input, Checkbox } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import logo from "../assets/images/logo.png";
import avimg from "../assets/images/ai-vector-img.png";

const Login = () => {
  const navigate = useNavigate();
  const currentLocation = useLocation(); // Get the current location dynamically
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [checkbox, setCheckbox] = useState(false);
  const [errors, setErrors] = useState({});
  // let logoutTimeout;

  useEffect(() => {
    const authData = Cookies.get("authData");  
    if (authData && currentLocation.pathname === "/") {
      goTo(navigate, "/dashboard");
    }
  }, [navigate]); 
  

  const validateForm = () => {
    const newErrors = {};
    if (!email.trim()) {
      newErrors.email = "Email is required.";
    } else {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        newErrors.email = "Please enter a valid email address.";
      }
    }

    if (!password.trim()) {
      newErrors.password = "Password is required.";
    }
    if (!checkbox) {
      newErrors.checkbox = "Required.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (validateForm()) {
      try {
        await login(email, password);
        // await axios.post("http://localhost:5000/create-user-folders", {
        //   email,
        // });
        // logoutTimeout = setAutoLogout(handleLogout, 5000);
        goTo(navigate, "/dashboard");
      } catch (err) {
        setErrors({ global: "Failed to log in. Please try again." });
      }
    } else {
      console.log("Form validation failed");
    }
  };

  // const handleLogout = () => {
  //   Cookies.remove("authData");
  //   clearAutoLogout(logoutTimeout);
  //   goTo(navigate, "/");
  // };

  // useEffect(() => {
  //   return () => {
  //     clearAutoLogout(logoutTimeout); // Clear timeout on unmount
  //   };
  // }, [logoutTimeout]);

  return (
    <div className="login-main align-items-center d-flex">
      <div className="cornerpattern cp-left"></div>
      <div className="cornerpattern cp-right"></div>
      <div className="container-fluid">
        <div className="login-inner d-flex justify-content-between align-items-center">
          <div className="project-info">
            <div className="login-logo">
              <img src={logo} alt="Logo" />
            </div>
            <h1 className="mt-0 mb-4">
              Generating Questions of Multiple Types
            </h1>
            <div className="smallheading">Welcome to ASTRA!</div>
            <p>
              Lorem Ipsum is simply dummy text of the printing and typesetting
              industry. Lorem Ipsum has been the industry's standard dummy text.
            </p>
            <div className="ai-vector">
              <img src={avimg} alt="" />
            </div>
          </div>
          <div className="login-box">
            <h2>Sign in</h2>
            {errors && <p style={{ color: "red" }}>{errors.global}</p>}
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>
                  <span>*</span>Email Address
                </label>
                <Input
                  type="text"
                  name="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter email address"
                />
                {errors.email && (
                  <div className="k-form-error k-text-start">
                    {errors.email}
                  </div>
                )}
              </div>
              <div className="form-group">
                <label>
                  <span>*</span>Password
                </label>
                <Input
                  type="password"
                  name="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter password"
                />
                {errors.password && (
                  <div className="k-form-error k-text-start">
                    {errors.password}
                  </div>
                )}
                <div className="forgottext">
                  <span
                    className="link-text"
                    onClick={() => goTo(navigate, "/forgot-password")}
                  >
                    Forgot password?
                  </span>
                </div>
              </div>
              <div className="form-group">
                <Checkbox
                  id="agree"
                  className="align-items-start"
                  type="checkbox"
                  name="checkbox"
                  checked={checkbox}
                  onChange={(e) => setCheckbox(e.target.value)}
                >
                  <label className="k-checkbox-label" htmlFor="agree">
                    By selecting continue, you agree to our 
                    <a href="#">Terms of Service</a> and acknowledge our{" "}
                    <a href="#">Privacy Policy</a>.
                  </label>
                </Checkbox>
                {errors.checkbox && (
                  <div className="k-form-error k-text-start">
                    {errors.checkbox}
                  </div>
                )}
              </div>
              <div className="form-group text-center">
                <Button className="btn-design btn-1 w-100" type="submit">
                  Submit
                </Button>
              </div>
              <div className="text-center fw-medium">
                New to ASTRA?{" "}
                <span
                  className="link-text"
                  onClick={() => goTo(navigate, "/signup")}
                >
                  Sign up
                </span>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
