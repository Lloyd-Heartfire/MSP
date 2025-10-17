// Ce fichier sert à gérer le login et le logout de l'utilisateur

import React, {createContext, useState, useEffect, useContext } from 'react';

// Context creation
const AuthContext = createContext();

// Provider
export const AuthProvider = ({children}) => {
    // State
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [token, setToken] = useState(null);

    // Auth verification in loading
    useEffect(() => {
        checkAuth();
    }, []);

    // Verification if the user is already login
    const checkAuth = () => {
        try {
            const savedToken = localStorage.getItem("who-token");
            const savedUser = localStorage.getItem("who-user");

            if (savedToken && savedUser) {
                setToken(savedToken);
                setUser(JSON.parse(savedUser));
            }
        } catch (error) {
            console.error("Erreur lors de la vérification de l\'authentification:", error);
        } finally {
            setLoading(false);
        }
    };

    // Connexion
    const login = async (username, password) => {
        try {
            const response = await fetch('http://localhost:8000/api/auth/login/', {
                method: 'POST',
                headers: {
                    "Content-Type": 'application/json',
                },
                body: JSON.stringify({username, password}),
            });
        
            if (!response.ok) {
                throw new Error("Identifiants incorrects");
            }
        
            const data = await response.json();
            
            console.log("=== LOGIN SUCCESS ===");
            console.log("Response data:", data);
        
            // Token storage - VÉRIFIE que data.access existe
            const accessToken = data.access;
            console.log("Access token:", accessToken);
            
            setToken(accessToken);
            setUser(data.user);
            localStorage.setItem("who-token", accessToken);
            localStorage.setItem("who-user", JSON.stringify(data.user));
            
            console.log("Token stocké:", localStorage.getItem("who-token"));
        
            return {success: true};
        } catch (error) {
            console.error("Erreur de connexion:", error);
            return {success: false, error: error.message};
        }
    };

    // Deconnexion
    const logout = () => {
        setUser(null);
        setToken(null);
        localStorage.removeItem("who-token");
        localStorage.removeItem("who-user");
    };

    // Permission verification
    const hasPermission = (permission) => {
        if (!user) return false;

        // Admin has all permissions
        if (user.role === "admin") return true;

        // Verification of specific permission
        return user.permissions?.includes(permission) || false;
    };

    // Role verification
    const hasRole = (role) => {
        return user?.role === role;
    };

    // Available value
    const value = {
        user,
        token,
        loading,
        isAuthenticated: !!user,
        login,
        logout,
        hasPermission,
        hasRole,
        isAdmin: user?.role === "admin",
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

// Custom hooks
export const useAuth = () => {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error("useAuth doit être utilisé à l\'intérieur de AuthProvider");
    }

    return context;
};

export default AuthContext;