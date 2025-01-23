import React, { useState } from "react";
import { useAuth } from "../contexts/authContext";
import { useNavigate } from "react-router-dom";
import { goTo } from "./common/goTo";
import { Input } from "@progress/kendo-react-inputs";
import { Button } from "@progress/kendo-react-buttons";
import logo from "../assets/images/logo.png";
import avimg from "../assets/images/ai-vector-img.png";
import eyeoff from "../assets/images/eye-off.svg";
import eyeon from "../assets/images/eye.svg";

const Register = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [showPassword2, setShowPassword2] = useState(false);

  const validate = () => {
    const newErrors = {};
    if (!formData.firstName.trim())
      newErrors.firstName = "First name is required.";
    if (!formData.lastName.trim())
      newErrors.lastName = "Last name is required.";
    if (!formData.email.trim()) newErrors.email = "Email address is required.";
    else if (!/\S+@\S+\.\S+/.test(formData.email))
      newErrors.email = "Invalid email address.";
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
      await register(
        formData.email,
        formData.password,
        formData.firstName,
        formData.lastName
      );
      goTo(navigate, "/dashboard"); 
    } catch (err) {
      if (err.message === "Firebase: Error (auth/email-already-in-use).") {
        var emailErrorMessage = "Email address is already in use.";
        setErrors({ email: emailErrorMessage });
      } else {
        var errorMessage = "Failed to register. Please try again later.";
        setErrors({ form: errorMessage });
      }
    }
  };

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
              industry.
            </p>
            <div className="ai-vector">
              <img src={avimg} alt="" />
            </div>
          </div>
          <div className="login-box">
            <h2>Sign up</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>
                  <span>*</span>First Name
                </label>
                <Input
                  type="text"
                  name="firstName"
                  placeholder="Enter first name"
                  value={formData.firstName}
                  onChange={handleChange}
                />
                {errors.firstName && (
                  <div className="k-form-error k-text-start">
                    {errors.firstName}
                  </div>
                )}
              </div>
              <div className="form-group">
                <label>
                  <span>*</span>Last Name
                </label>
                <Input
                  type="text"
                  name="lastName"
                  placeholder="Enter last name"
                  value={formData.lastName}
                  onChange={handleChange}
                />
                {errors.lastName && (
                  <div className="k-form-error k-text-start">
                    {errors.lastName}
                  </div>
                )}
              </div>
              <div className="form-group">
                <label>
                  <span>*</span>Email Address
                </label>
                <Input
                  type="text"
                  name="email"
                  placeholder="Enter email address"
                  value={formData.email}
                  onChange={handleChange}
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
                  type={showPassword ? "text" : "password"}
                  name="password"
                  placeholder="Enter password"
                  value={formData.password}
                  onChange={handleChange}
                />
                <div
                  className="password-icon"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  <img
                    src={showPassword ? eyeoff : eyeon}
                    alt={showPassword ? "Hide" : "Show"}
                  />
                </div>
                {errors.password && (
                  <div className="k-form-error k-text-start">
                    {errors.password}
                  </div>
                )}
              </div>
              <div className="form-group">
                <label>
                  <span>*</span>Confirm Password
                </label>
                <Input
                  type={showPassword2 ? "text" : "password"}
                  name="confirmPassword"
                  placeholder="Enter confirm password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                />
                <div
                  className="password-icon"
                  onClick={() => setShowPassword2(!showPassword2)}
                >
                  <img
                    src={showPassword2 ? eyeoff : eyeon}
                    alt={showPassword2 ? "Hide" : "Show"}
                  />
                </div>
                {errors.confirmPassword && (
                  <div className="k-form-error k-text-start">
                    {errors.confirmPassword}
                  </div>
                )}
              </div>
              {errors.form && (
                <div className="k-form-error k-text-start text-center">
                  {errors.form}
                </div>
              )}
              <div className="form-group text-center">
                <Button className="btn-design btn-1 w-100">Submit</Button>
              </div>
              <div className="text-center fw-medium">
                Already have an account?{" "}
                <span className="link-text" onClick={() => goTo(navigate, "/")}>
                  Sign in
                </span>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
