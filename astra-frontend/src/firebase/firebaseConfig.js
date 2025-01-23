// src/firebase/firebaseConfig.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getDatabase } from "firebase/database";
// import { getStorage } from "firebase/storage";

// PRODUCTION
const firebaseConfig = {
  apiKey: "AIzaSyADJ5vPmOfXKfaMQTqkwPBBoUrhbKuku6Q",
  authDomain: "auth-astra.firebaseapp.com",
  databaseURL:
    "https://auth-astra-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "auth-astra",
  storageBucket: "auth-astra.appspot.com",
  messagingSenderId: "310634675231",
  appId: "1:310634675231:web:f2a30378746a764986292a",
  measurementId: "G-V8Q3JMBPVR",
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
