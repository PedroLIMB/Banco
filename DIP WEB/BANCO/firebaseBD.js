// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getFirestore } from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyANYkT7ZSHghAaTX8HibAl6D4nDrKVTI9c",
  authDomain: "bancodip-7873e.firebaseapp.com",
  projectId: "bancodip-7873e",
  storageBucket: "bancodip-7873e.appspot.com",
  messagingSenderId: "125038942319",
  appId: "1:125038942319:web:c9023e47db87841790959a",
  measurementId: "G-QFTVGH2C2M"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const db = getFirestore(app);

