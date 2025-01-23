import React, { useState, useEffect } from "react";
import { Input } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import logo from "../assets/images/logo.png";
import forgotpassword from "../assets/images/forgotpassword.png";
import { useNavigate } from "react-router-dom";
import { goTo } from "./common/goTo";
import { useAuth } from "../contexts/authContext";

const ForgotPassword = () => {
  const navigate = useNavigate();
  const { resetPassword } = useAuth();
  const [email, setEmail] = useState("");
  const [errors, setErrors] = useState({});

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
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (validateForm()) {
      try {
        await resetPassword(email);
        goTo(navigate, "/dashboard");
      } 
      catch (err) {
        setErrors({ global: "Failed to send email. Please try again." });
      }
    }
  };
  return (
    <>
      <div className="login-main align-items-center d-flex">
        <div className="cornerpattern cp-left"></div>
        <div className="cornerpattern cp-right"></div>
        <div className="container-fluid">
          <div className="login-inner d-flex justify-content-between align-items-center">
            <div className="project-info">
              <div className="login-logo">
                <img src={logo} alt="Logo" />
              </div>
              <div className="smallheading">Welcome to ASTRA!</div>
              <p>
                Don't worry, it happens to all of us. Please enter your email
                address in the field on the right side to recover your password.
              </p>
              <div className="ai-vector forgotpassword-img">
                <img src={forgotpassword} alt="" />
              </div>
            </div>
            <div className="login-box">
              <h2>Forgot Password?</h2>
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
                <div className="form-group text-center">
                  <Button className="btn-design btn-1 w-100" type="submit">
                    Submit
                  </Button>
                </div>
                <div className="text-center fw-medium">
                  Remember your password? Back to{" "}
                  <span
                    className="link-text"
                    onClick={() => goTo(navigate, "/")}
                  >
                    Sign in
                  </span>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ForgotPassword;
