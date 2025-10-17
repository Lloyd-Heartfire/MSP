// Cela va permettre de paramétrer le toggle light & dark et ce qui y est lié

import React, {createContext, useState, useEffect, useContext} from "react";

// Context creation
const ThemeContext = createContext();

// Provider
export const ThemeProvider = ({children}) => {
    // State
    const [theme, setTheme] = useState (() => {
        const savedTheme = localStorage.getItem("who-theme");
        return savedTheme || "light";
    });

    // Function for theme changing
    const toggleTheme = () => {
        setTheme((prevTheme) => (prevTheme === "light" ? "dark" : "light"));
    };

    // Function for define a specific theme
    const setThemeMode = (mode) => {
        if (mode === "light" || mode === "dark") {
            setTheme(mode);
        }
    };

    // Apply the theme
    useEffect(() => {
        document.body.setAttribute("data-theme", theme);
        localStorage.setItem("who-theme", theme);
    }, [theme]);

    // Available values for all the components
    const value = {
        theme,
        toggleTheme,
        setThemeMode,
        isDark: theme === "dark",
        isLight: theme === "light",
    };

    return (
        <ThemeContext.Provider value={value}>
            {children}
        </ThemeContext.Provider>
    );
};

// Custom hooks
export const useTheme = () => {
    const context = useContext(ThemeContext);

    if (!context) {
        throw new Error("useTheme doit être utilisé à l\'intérieur de ThemeProvider");
    }

    return context;
};

export default ThemeContext;