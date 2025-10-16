// Centralize data retrieved from the back-end (avoids calling the API in every component)

import React, {createContext, useState, useContext} from "react";

// Context creation
const DataContext = createContext();

// To Do : Replace with API when we have it
const API_BASE_URL = "http://localhost:8000/";

// Provider
export const DataProvider = ({children}) => {
    // State of filters selectable
    const [filters, setFilters] = useState({
        // pandemic: null,
        who_region: null,
        country: null,
        state: null,
        city: null,
        startDate: "2020-03-01",
        endDate: "2022-03-01",
        change_metric: false,    // 1 per 100 000
    });

    // State for availbale option for the dropdown
    const [availableOptions, setAvailableOptions] = useState({
        // pandemics: [],
        who_regions: [],
        countries: [],
        states: [],
        city: [],
    });

    // State for visualized data
    const [data, setData] = useState({
        stats: {
            newCases: 0,
            totalCases: 0,
            newDeaths: 0,
            totalDeaths: 0,
            activeCases: 0,
            totalRecovered: 0,
        },
        charts: {
            horizontalBar: [],
            lineChart: [],
            groupedBar: [],
        },
    });

    // Loading state
    const [loading, setLoading] = useState(false);
    const [loadingOptions, setLoadingOptions] = useState({
        // pandemics: false,
        who_regions: false,
        countries: false,
        states: false,
        city: false,
    });
    const [error, setError] = useState(null);
    const [isValidated, setIsValidated] = useState(false);

    // Récupère le token depuis localStorage
    const getAuthHeaders = () => {
        const token = localStorage.getItem("who-token");
        return token ? {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        } : {
            'Content-Type': 'application/json'
        };
    };

    // FUNCTION FOR DROPDOWN OPTIONS

    // Load the list of pandemics
    // const fetchPandemics = async () => {
    //     setLoadingOptions((prev) => ({ ...prev, pandemics: true}));
    //     try {
    //         const response = await fetch(`${API_BASE_URL}api/pandemics/`);

    //         if (!response.ok) throw new Error('Erreur de chargement des pandémies');

    //         const data = await response.json();
    //         setAvailableOptions((prev) => ({ ...prev, pandemics: data}));

    //         return {success: true, data};
    //     } catch (error) {
    //         console.error("Erreur fetchPandemics:", error);
    //         return { success: false, error: error.message};
    //     } finally {
    //         setLoadingOptions((prev) => ({ ...prev, pandemics: false}));
    //     }
    // };

    // Load the list of the OMS regions
    const fetchRegions = async () => {
        setLoadingOptions((prev) => ({ ...prev, who_regions: true}));
        try {
            const response = await fetch(`${API_BASE_URL}api/continents/`, {
                headers: getAuthHeaders()
            });

            if (!response.ok) throw new Error('Erreur de chargement des régions');

            const data = await response.json();
            setAvailableOptions((prev) => ({ ...prev, who_regions: data}));

            return {success: true, data};
        } catch (error) {
            console.error("Erreur fetchRegions:", error);
            return { success: false, error: error.message};
        } finally {
            setLoadingOptions((prev) => ({ ...prev, who_regions: false}));
        }
    };

    // Load the countries
    const fetchCountries = async (who_region) => {
        if (!who_region) {
            setAvailableOptions((prev) => ({ ...prev, countries: [] }));
            return;
        }

        setLoadingOptions((prev) => ({ ...prev, countries: true }));
        try {
            const response = await fetch(`${API_BASE_URL}api/countries/?continents=${who_region}`, {
                headers: getAuthHeaders()
            });

            if (!response.ok) throw new Error('Erreur de chargement des pays');

            const data = await response.json();
            setAvailableOptions((prev) => ({ ...prev, countries: data}));

            return {success: true, data};
        } catch (error) {
            console.error("Erreur fetchCountries:", error);
            return { success: false, error: error.message};
        } finally {
            setLoadingOptions((prev) => ({ ...prev, countries: false}));
        }
    };

    // Load the provinces / states
    const fetchStates = async (country) => {
        if (!country) {
            setAvailableOptions((prev) => ({ ...prev, states: [] }));
            return;
        }

        setLoadingOptions((prev) => ({ ...prev, states: true }));
        try {
            const response = await fetch(`${API_BASE_URL}api/states/?countries=${country}`, {
                headers: getAuthHeaders()
            });

            if (!response.ok) throw new Error('Erreur de chargement des provinces');

            const data = await response.json();
            setAvailableOptions((prev) => ({ ...prev, states: data}));

            return {success: true, data};
        } catch (error) {
            console.error("Erreur fetchStates:", error);
            return { success: false, error: error.message};
        } finally {
            setLoadingOptions((prev) => ({ ...prev, states: false}));
        }
    };

    // Load the cities
    const fetchCity = async (state) => {
        if (!state) {
            setAvailableOptions((prev) => ({ ...prev, city: [] }));
            return;
        }

        setLoadingOptions((prev) => ({ ...prev, city: true }));
        try {
            const response = await fetch(`${API_BASE_URL}api/admin2/?states=${state}`, {
                headers: getAuthHeaders()
            });

            if (!response.ok) throw new Error('Erreur de chargement des city');

            const data = await response.json();
            setAvailableOptions((prev) => ({ ...prev, city: data}));

            return {success: true, data};
        } catch (error) {
            console.error("Erreur fetchCity:", error);
            return { success: false, error: error.message};
        } finally {
            setLoadingOptions((prev) => ({ ...prev, city: false}));
        }
    };

    // FILTER GESTION

    // Updating filters with cascading reset
    const updateFilters = (newFilters) => {
        setFilters((prev) => {
            const updated = { ...prev, ...newFilters};

            // Cascading reset if region change
            if (newFilters.who_region !== undefined && newFilters.who_region !== prev.who_region) {
                updated.country = null;
                updated.state = null;
                updated.city = null;
                // Load the countries of a new region
                if (newFilters.who_region) {
                    fetchCountries(newFilters.who_region);
                }
            }

            // Cascading reset if country change
            if (newFilters.country !== undefined && newFilters.country !== prev.country) {
                updated.state = null;
                updated.city = null;
                // Load the states of a new country
                if (newFilters.country) {
                    fetchStates(newFilters.country);
                }
            }

            // Cascading reset if province change
            if (newFilters.state !== undefined && newFilters.state !== prev.state) {
                updated.city = null;
                // Load the city of a new province
                if (newFilters.state) {
                    fetchCity(newFilters.state);
                }
            }

            return updated;
        });

        // Regenerate the validation
        setIsValidated(false);
    };

    // Complete regeneration of the filters
    const resetFilters = () => {
        setFilters({
            // pandemic: null,
            who_region: null,
            country: null,
            state: null,
            city: null,
            startDate: "2020-03-01",
            endDate: "2022-03-01",
            change_metric: false,
        });
        setAvailableOptions((prev) => ({
            ...prev,
            countries: [],
            states: [],
            city: [],
        }));
        setIsValidated(false);
    };

    // HELPER FUNCTIONS FOR DATA TRANSFORMATION

    // Calculate stats from Django response
    const calculateStats = (dataArray) => {
        if (!dataArray || dataArray.length === 0) {
            return {
                newCases: 0,
                totalCases: 0,
                newDeaths: 0,
                totalDeaths: 0,
                activeCases: 0,
                totalRecovered: 0
            };
        }

        let totalCases = 0;
        let totalDeaths = 0;
        let totalRecovered = 0;
        let newCases = 0;
        let newDeaths = 0;

        dataArray.forEach(location => {
            if (location.values && location.values.length > 0) {
                const lastPeriod = location.values[location.values.length - 1];
                totalCases += lastPeriod.cases || 0;
                totalDeaths += lastPeriod.deaths || 0;
                totalRecovered += lastPeriod.recovered || 0;
                newCases += lastPeriod.new_cases || 0;
                newDeaths += lastPeriod.new_deaths || 0;
            }
        });

        return {
            newCases,
            totalCases,
            newDeaths,
            totalDeaths,
            activeCases: totalCases - totalDeaths - totalRecovered,
            totalRecovered
        };
    };

    // Build horizontal bar chart data
    const buildHorizontalBarData = (dataArray) => {
    if (!dataArray || dataArray.length === 0) return [];

    return dataArray.map(location => {
        const lastPeriod = location.values[location.values.length - 1];
            return {
                label: location.country || location.province_state || location.continent,
                totalCases: lastPeriod?.cases || 0,
                totalDeaths: lastPeriod?.deaths || 0
            };
        }).slice(0, 15);
    };

    // Build line chart data
    const buildLineChartData = (abscisse, ordonne) => {
        if (!abscisse || !ordonne || ordonne.length === 0) return { periods: [], newCases: [], newDeaths: [] };

        const newCasesDataset = ordonne.find(ds => 
            ds.label && (ds.label.toLowerCase().includes('nouveaux cas') || ds.label.toLowerCase().includes('new_cases'))
        );

        const newDeathsDataset = ordonne.find(ds => 
            ds.label && (ds.label.toLowerCase().includes('nouveaux décès') || ds.label.toLowerCase().includes('new_deaths'))
        );

        return {
            periods: abscisse,
            newCases: newCasesDataset?.data || [],
            newDeaths: newDeathsDataset?.data || []
        };
    };

    // Build grouped bar chart data
    const buildGroupedBarData = (dataArray) => {
        if (!dataArray || dataArray.length === 0) return [];

        return dataArray.map(location => {
            const lastPeriod = location.values[location.values.length - 1];
            const activeCases = (lastPeriod?.cases || 0) - (lastPeriod?.deaths || 0) - (lastPeriod?.recovered || 0);

            return {
                category: location.country || location.province_state || location.continent,
                activeCases: activeCases > 0 ? activeCases : 0,
                totalRecovered: lastPeriod?.recovered || 0
            };
        }).slice(0, 10);
    };

    // DATA RECUPERATION

    // Recovery of the data within Django API
    const fetchData = async () => {
        setLoading(true);
        setError(null);

        try {
            // Transform filters to Django expected format
            const payload = {
                pandemie: "Covid-19",
                startDate: filters.startDate,
                endDate: filters.endDate,
                granularity: "monthly",
                continents: filters.who_region ? [filters.who_region] : [],
                countries: filters.country ? [filters.country] : [],
                states: filters.state ? [filters.state] : [],
                cities: filters.city ? [filters.city] : [],
                metrics: ["cases", "deaths", "recovered", "new_cases", "new_deaths"]
            };

            const response = await fetch(`${API_BASE_URL}api/data/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Erreur ${response.status}: ${errorText}`);
            }

            const result = await response.json();

            // Transform Django response to frontend format
            const adaptedData = {
                stats: calculateStats(result.data),
                charts: {
                    horizontalBar: buildHorizontalBarData(result.data),
                    lineChart: buildLineChartData(result.abscisse, result.ordonne),
                    groupedBar: buildGroupedBarData(result.data)
                }
            };

            setData(adaptedData);
            setIsValidated(true);
            return { success: true };
        } catch (error) {
            setError(error.message);
            console.error("Erreur de récupération des données:", error);
            return { success: false, error: error.message };
        } finally {
            setLoading(false);
        }
    };

    // EXPORT

    // Data export
    const exportData = async (format="csv") => {
        try {
            // Transform filters to Django expected format
            const payload = {
                pandemie: "Covid-19",
                startDate: filters.startDate,
                endDate: filters.endDate,
                granularity: "monthly",
                continents: filters.who_region ? [filters.who_region] : [],
                countries: filters.country ? [filters.country] : [],
                states: filters.state ? [filters.state] : [],
                cities: filters.city ? [filters.city] : [],
                metrics: ["cases", "deaths", "recovered", "new_cases", "new_deaths"]
            };

            const response = await fetch(`${API_BASE_URL}api/data/download/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                throw new Error("Erreur lors de l'export");
            }

            // Download files
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            link.download = `who-data-${Date.now()}.${format}`;
            document.body.appendChild(link);
            link.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(link);

            return {success: true};
        } catch (error) {
            console.error("Erreur d'export:", error);
            return {success: false, error: error.message};
        }
    };

    // Export values
    const value = {
        // Filters
        filters,
        updateFilters,
        resetFilters,

        // Dropdown options
        availableOptions,
        loadingOptions,

        // Function for options loading
        // fetchPandemics,
        fetchRegions,
        fetchCountries,
        fetchStates,
        fetchCity,

        // Datavisualisation
        data: data,
        loading,
        error,
        isValidated,

        // Fetching and actions
        fetchData,
        exportData,
    };

    return (
        <DataContext.Provider value={value}>
            {children}
        </DataContext.Provider>
    );
};

// Custom hook
export const useData = () => {
  const context = useContext(DataContext);
  
  if (!context) {
    throw new Error('useData doit être utilisé à l\'intérieur de DataProvider');
  }
  
  return context;
};

export default DataContext;