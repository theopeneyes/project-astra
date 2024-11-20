import * as React from "react";
import * as ReactDOM from "react-dom";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import './index.css'
import App from './App.jsx'

const router = createBrowserRouter([
    {
        path: "/:emailId/:fileName",
        element: <App/>,
    },
]);

ReactDOM.createRoot(
    document.getElementById('root')
).render(
    <RouterProvider router={router} /> 
); 
