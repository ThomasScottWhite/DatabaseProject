import React, { createContext, useContext, useState } from 'react';

// Create the context
const UserContext = createContext(null);

// Create the provider
export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    const login = (email, organizationId, accountId) => {
        setUser({ email, organizationId, accountId });
    };

    const logout = () => {
        setUser(null);
    };

    return (
        <UserContext.Provider value={{ user, login, logout }}>
            {children}
        </UserContext.Provider>
    );
};

// Custom hook to use the UserContext
export const useUser = () => {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error('useUser must be used within a UserProvider');
    }
    return context;
};
