// src/firebase/firebaseConfig.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getDatabase } from "firebase/database";
// import { getStorage } from "firebase/storage";

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  databaseURL: process.env.REACT_APP_FIREBASE_DATABASE_URL,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID,
  measurementId: process.env.REACT_APP_FIREBASE_MEASUREMENT_ID,
};

// ANSHUMAN LOCAL
//  const firebaseConfig = {
//    apiKey: "AIzaSyAoyeW7myV56P4BjtQjoxSR3vfpPpoQPZQ",
//    authDomain: "neww-53636.firebaseapp.com",
//    projectId: "neww-53636",
//    storageBucket: "neww-53636.firebasestorage.app",
//    messagingSenderId: "35158755879",
//    appId: "1:35158755879:web:54a0e90860a433a2a7dc02",
//    measurementId: "G-C83FKK4P2P"
//  };

// Initialize Firebase
// const firebaseApp = initializeApp(firebaseConfig);

// Initialize Firebase Authentication
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const database = getDatabase(app);
// const storage = getStorage(firebaseApp);

export { auth, database };
