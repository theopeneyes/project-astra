import React, { useState } from "react";
import { Input } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import logo from "../assets/images/logo.png";
import forgotpassword from "../assets/images/forgotpassword.png";
import eyeoff from "../assets/images/eye-off.svg";
import eyeon from "../assets/images/eye.svg";
import { useNavigate, useLocation } from "react-router-dom";
import { goTo } from "./common/goTo";
import { useAuth } from "../contexts/authContext";
const ResetPassword = () => {
  const navigate = useNavigate();
  const { newResetPassword } = useAuth();
  const location = useLocation();
  const [formData, setFormData] = useState({
    password: "",
    confirmPassword: "",
  });
  const [errors, setErrors] = useState({});

  const [showPassword, setShowPassword] = useState(false);
  const [showPassword2, setShowPassword2] = useState(false);

  const validate = () => {
    const newErrors = {};
    if (!formData.password) newErrors.password = "Password is required.";
    else if (formData.password.length < 6)
      newErrors.password = "Password must be at least 6 characters.";
    if (formData.confirmPassword !== formData.password)
      newErrors.confirmPassword = "Passwords do not match.";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });

    // Clear the error for the specific field as the user types
    setErrors((prevErrors) => {
      const { [name]: _, ...rest } = prevErrors;
      return rest;
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    try {
      const urlParams = new URLSearchParams(location.search);
      const oobCode = urlParams.get("oobCode");
      if (!oobCode) {
        setErrors("Invalid password reset link.");
        return;
      }
      await newResetPassword(oobCode, formData.password);
      goTo(navigate, "/");
    } catch (err) {
      setErrors({ global: "Failed to send email. Please try again." });
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
                Your new password must be different from your previous password.
              </p>
              <div className="ai-vector forgotpassword-img">
                <img src={forgotpassword} alt="" />
              </div>
            </div>
            <div className="login-box">
              <h2>Reset Password</h2>
              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label>
                    <span>*</span>New Password
                  </label>
                  <Input
                    type={showPassword ? "text" : "password"}
                    name="password"
                    placeholder="Enter new password"
                    value={formData.password}
                    onChange={handleChange}
                  />
                  <div
                    className="password-icon"
                    onClick={() => setShowPassword((prev) => !prev)}
                  >
                    {showPassword ? (
                      <img src={eyeoff} alt="Hide" />
                    ) : (
                      <img src={eyeon} alt="Show" />
                    )}
                  </div>
                  {errors.password && (
                    <div className="k-form-error k-text-start">
                      {errors.password}
                    </div>
                  )}
                </div>
                <div className="form-group">
                  <label>
                    <span>*</span>Confirm New Password
                  </label>
                  <Input
                    type={showPassword2 ? "text" : "password"}
                    name="confirmPassword"
                    placeholder="Enter confirm new password"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                  />
                  <div
                    className="password-icon"
                    onClick={() => setShowPassword2((prev) => !prev)}
                  >
                    {showPassword2 ? (
                      <img src={eyeoff} alt="Hide" />
                    ) : (
                      <img src={eyeon} alt="Show" />
                    )}
                  </div>
                  {errors.confirmPassword && (
                    <div className="k-form-error k-text-start">
                      {errors.confirmPassword}
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
                  <span className="link-text">Sign in</span>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ResetPassword;
