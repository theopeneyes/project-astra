import React, { createContext, useContext, useState, useEffect } from "react";
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  sendPasswordResetEmail,
  confirmPasswordReset,
  updateEmail,
  EmailAuthProvider,
  reauthenticateWithCredential,
  deleteUser,
} from "firebase/auth";
import { auth, database } from "../firebase/firebaseConfig";
import Cookies from "js-cookie";
import { ref, set, get, update, remove } from "firebase/database";

const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(null);

  // Helper to handle cookie expiration
  const COOKIE_EXPIRATION_MINUTES = 5;

  const setAuthCookie = (authData) => {
    Cookies.set("authData", JSON.stringify(authData), {
      expires: COOKIE_EXPIRATION_MINUTES / 1440,
    });
  };

  const clearAuthCookie = () => {
    Cookies.remove("authData");
  };

  const register = async (email, password, firstName, lastName) => {
    debugger;
    try {
      const userCredential = await createUserWithEmailAndPassword(
        auth,
        email,
        password
      );
      const authData = {
        uid: userCredential.user.uid,
        email: userCredential.user.email,
      };

      setIsAuthenticated(authData);
      setAuthCookie(authData);

      // Reference to the user's data by their UID
      const userRef = ref(database, `register/users/${authData.uid}`);
      await set(userRef, {
        firstName,
        lastName,
        email,
        password,
        createdAt: new Date().toISOString(),
      });
    } catch (error) {
      console.error("Error during registration:", error);
      throw error;
    }
  };

  const updateUserData = async (uid, updatedData) => {
    try {
      const user = auth.currentUser;
      const userRef = ref(database, `register/users/${uid}`);
      const userSnapshot = await get(userRef);

      // Update data in Realtime Database
      if (userSnapshot.exists()) {
        await update(userRef, updatedData);
        console.log("User data updated in Realtime Database:", uid);
      } else {
        await set(userRef, {
          ...updatedData,
          createdAt: new Date().toISOString(),
        });
        console.log("New user created in Realtime Database:", uid);
      }

      // Update email in Firebase Authentication
      if (updatedData.email && user) {
        // Reauthenticate the user
        const credential = EmailAuthProvider.credential(
          user.email,
          updatedData.password
        );
        await reauthenticateWithCredential(user, credential);
        console.log("User reauthenticated");

        // Update the email in Firebase Authentication
        await updateEmail(user, updatedData.email);
        console.log("Email updated in Firebase Authentication");
      }
    } catch (error) {
      console.error("Error updating user data:", error);
      throw error;
    }
  };

  // const updateEmailAndReauthenticate = async (email, password, updatedData) => {
  //   try {
  //     const user = auth.currentUser;
  //     if (!user) throw new Error("User is not authenticated");

  //     // Re-authenticate the user before updating the email
  //     const credential = EmailAuthProvider.credential(user.email, password);
  //     await reauthenticateWithCredential(user, credential);

  //     // Update the email in Firebase Authentication
  //     await updateEmail(user, email);
  //     console.log("Email updated in Firebase Authentication");

  //     // Update the user data in the database as well
  //     await updateUserData(user.uid, updatedData);

  //     // Log out the user to force re-login with the new email
  //     await signOut(auth);
  //     console.log("User logged out after email update");

  //     return "Email updated successfully, please log in again.";
  //   } catch (error) {
  //     console.error("Error updating email:", error);
  //     throw new Error("Failed to update email, please try again.");
  //   }
  // };

  const login = async (email, password) => {
    try {
      const userCredential = await signInWithEmailAndPassword(
        auth,
        email,
        password
      );
      const authData = {
        uid: userCredential.user.uid,
        email: userCredential.user.email,
      };
      setIsAuthenticated(authData);
      setAuthCookie(authData);
    } catch (error) {
      console.error("Error during login:", error);
      throw error;
    }
  };

  const resetPassword = async (email) => {
    const actionCodeSettings = {
      url: "http://localhost:3000/reset-password",
      handleCodeInApp: true,
    };
    try {
      await sendPasswordResetEmail(auth, email, actionCodeSettings);
    } catch (error) {
      console.error("Error during reset password:", error);
      throw error;
    }
  };

  const newResetPassword = async (oobCode, password) => {
    debugger;
    try {
      await confirmPasswordReset(auth, oobCode, password);
      console.log("Password reset successful!");
    } catch (error) {
      console.error("Error during reset password:", error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await signOut(auth);
      setIsAuthenticated(null);
      clearAuthCookie();
    } catch (error) {
      console.error("Error during logout:", error);
    }
  };

  const deleteAuthUser = async () => {
    debugger;
    const user = auth.currentUser;
    if (!user) {
      console.error("No user is currently signed in.");
      return;
    }
    try {
      const userRef = ref(database, `register/users/${user.uid}`);
      const userSnapshot = await get(userRef);
      if (userSnapshot.exists()) {
        await remove(userRef);
        await deleteUser(user);
      }
      console.log("User account deleted successfully.");
    } catch (error) {
      throw error;
    }
  };

  useEffect(() => {
    // Restore user from cookies on app load
    const storedAuthData = Cookies.get("authData");

    if (storedAuthData) {
      try {
        const parsedAuthData = JSON.parse(storedAuthData);
        setIsAuthenticated(parsedAuthData);
      } catch (error) {
        console.error("Failed to parse auth data from cookie", error);
        clearAuthCookie(); // Clear cookie in case of parse error
        setIsAuthenticated(null);
      }
    } else {
      setIsAuthenticated(null); // No auth data found, user is not authenticated
    }
  }, []);

  const value = {
    isAuthenticated,
    register,
    login,
    resetPassword,
    newResetPassword,
    updateUserData,
    logout,
    deleteAuthUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
