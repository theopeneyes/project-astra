import React, { createContext, useContext, useState } from "react";

const ComponentNameContext = createContext();

export const ComponentNameProvider = ({ children }) => {
  const [componentName, setComponentName] = useState("");

  return (
    <ComponentNameContext.Provider value={{ componentName, setComponentName }}>
      {children}
    </ComponentNameContext.Provider>
  );
};

export const useComponentName = () => useContext(ComponentNameContext);
