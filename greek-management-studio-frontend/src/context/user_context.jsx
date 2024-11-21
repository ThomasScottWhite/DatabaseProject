import React, { createContext, useContext, useState } from "react";

// Create the context
const UserContext = createContext(null);

// Create the provider
export const UserProvider = ({ children }) => {
  const [user, setUser] = useState({
    organization_id: null,
    auth_token: null,
    email: null,
    is_admin: true,
  });

  const login = (organization_id, auth_token, email, is_admin) => {
    setUser({ organization_id, auth_token, email, is_admin });
  };

  const get_auth_token = () => {
    if (user === null) {
      return null;
    } else {
      return user.authToken;
    }
  };
  const post_with_headers = async (route, payload) => {
    const response = await fetch(route, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: user.authToken,
        Email: user.email,
        "Organization-Id": user.organizationId,
      },
      body: JSON.stringify(payload),
    });

    return response;
  };
  const get_with_headers = async (route) => {
    response = await fetch(route, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: user.authToken,
        Email: user.email,
        "Organization-Id": user.organizationId,
      },
    });
    return response;
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <UserContext.Provider
      value={{ user, login, logout, post_with_headers, get_with_headers }}
    >
      {children}
    </UserContext.Provider>
  );
};

// Custom hook to use the UserContext
export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error("useUser must be used within a UserProvider");
  }
  return context;
};
