import React from "react";
import { Link } from "react-router-dom";
const Footer = () => {
  const currentYear = new Date().getFullYear();
  return (
    <footer>
      <div className="row">
        <div className="col text-start">
          <div className="copyright-block"> © Copyright {currentYear} <Link to="/" target="_blank">ASTRA</Link> <span className="px-1">|</span> Powered by <Link to="https://www.theopeneyes.com/" target="_blank">OpenEyes Technologies Inc.</Link></div>
        </div>
        <div className="col text-end">
          <ul className="footer-links">
            <li><Link target="_blank" to="/">About us</Link></li>
            <li><Link target="_blank" to="/">Privacy Policy</Link></li>
            <li><Link target="_blank" to="/">Terms of use</Link></li>
          </ul>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
