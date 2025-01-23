import Cookies from "js-cookie";
import { Base64 } from "js-base64";

export const checkAuthAndNavigate = (navigate, redirectPath = "/dashboard") => {
  debugger
  const encodedAuthData = Cookies.get("authData");
  if (encodedAuthData) {
    try {
      const authData = JSON.parse(Base64.decode(encodedAuthData));
      console.log("Decoded Auth Data:", authData); // Optional: For debugging
      // navigate(redirectPath);
    } catch (error) {
      console.error("Error decoding auth data:", error);
    }
  }
};
