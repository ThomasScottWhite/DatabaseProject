import React, { createContext, useContext, useState } from 'react';

// Create the context
const UserContext = createContext(null);

// Create the provider
export const UserProvider = ({ children }) => {
    const [user, setUser] = useState({"authToken": null, "email": null, "organizationId": null});

    const login = (email, organizationId, accountId, authToken) => {
        setUser({ email, organizationId, accountId, authToken });
    };


    const fetch_with_headers = async(route) => {await fetch(route, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': user.authToken,
            'Email' : user.email,
            'Organization-Id' : user.organizationId,
        },
        body: JSON.stringify(payload),
    })}

    const get_auth_token = () => {
        if (user === null) {
            return null;
        }
        else{
            return user.authToken; 
        }
        
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
