import React, { createContext, useState, useContext } from 'react';

const UserContext = createContext();

export const useUser = () => {
    return useContext(UserContext);
};

export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null); // User details
    const [organizationId, setOrganizationId] = useState(null); // Organization ID
    const [accountId, setAccountId] = useState(null); // Account ID

    const login = (userData, orgId, accId) => {
        setUser(userData); // Set the logged-in user
        setOrganizationId(orgId); // Set the organization ID
        setAccountId(accId); // Set the account ID
    };

    const logout = () => {
        setUser(null);
        setOrganizationId(null);
        setAccountId(null);
    };

    return (
        <UserContext.Provider value={{ user, organizationId, accountId, login, logout }}>
            {children}
        </UserContext.Provider>
    );
};
