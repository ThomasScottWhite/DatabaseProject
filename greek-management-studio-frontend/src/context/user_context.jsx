import React, { createContext, useContext, useState, useEffect } from "react";

const UserContext = createContext(null);

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState({
    chapter_id: null,
    auth_token: null,
    email: null,
    is_admin: true,
  });

  const login = (chapter_id, auth_token, email, is_admin, callback) => {
    setUser({ chapter_id, auth_token, email, is_admin });
    if (callback) {
      callback();
    }
  };
  const get_auth_token = () => {
    if (!user || !user.auth_token) {
      return null;
    }
    return user.auth_token;
  };

  const post_with_headers = async (route, payload) => {
    const response = await fetch(route, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: user.auth_token,
      },
      body: JSON.stringify(payload),
    });

    return response;
  };
  const patch_with_headers = async (route, payload) => {
    const response = await fetch(route, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: user.auth_token,
      },
      body: JSON.stringify(payload),
    });

    return response;
  };


  const get_with_headers = async (route) => {
    const response = await fetch(route, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: user.auth_token,
      },
    });
    return response;
  };

  const logout = () => {
    setUser({
      chapter_id: null,
      auth_token: null,
      email: null,
      is_admin: true,
    });
  };

  return (
    <UserContext.Provider
      value={{ user, login, logout, post_with_headers, get_with_headers, patch_with_headers }}
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
