import React, { useState, useEffect } from "react";
import { useData } from "../../context/DataContext";
import "./FilterPanel.css";

const FilterPanel = () => {
    const {
        filters,
        updateFilters,
        availableOptions,
        loadingOptions,
        fetchRegions,
    } = useData();

    // Local state for open dropdown
    const [openDropdown, setOpenDropdown] = useState(null);

    // Load the regions
    useEffect(() => {
        if (availableOptions.who_regions.length === 0) {
            fetchRegions();
        }
    }, []);

    // Open/Close dropdown
    const handleDropdownClick = (dropdownName) => {
        setOpenDropdown(openDropdown === dropdownName ? null : dropdownName);
    };

    // Select a who-region
    const handleRegionSelect = (region) => {
        updateFilters({ who_region: region.id });
        setOpenDropdown(null);
    };

    // Select a country
    const handleCountrySelect = (country) => {
        updateFilters({ country: country.id });
        setOpenDropdown(null);
    };

    // Select a province/state
    const handleStateSelect = (state) => {
        updateFilters({ state: state.id });
        setOpenDropdown(null);
    };

    // Select a city
    const handleCitySelect = (city) => {
        updateFilters({ city: city.id });
        setOpenDropdown(null);
    };

    // Get the label for each filter
    const getSelectedLabel = (filterKey, options) => {
        const selected = options.find(opt => opt.id === filters[filterKey]);
        return selected?.name || `Select ${filterKey}`;
    };

    // Vérifier si States est vide après chargement
    const hasStates = availableOptions.states.length > 0;
    const hasCities = availableOptions.city.length > 0;

    return (
        <div className="filter-panel">
            {/* Who-Region */}
            <Dropdown
                label={filters.who_region ? getSelectedLabel("who_region", availableOptions.who_regions) : "Select a region"}
                isOpen={openDropdown === "who_region"}
                onClick={() => handleDropdownClick("who_region")}
                loading={loadingOptions.who_regions}
                disabled={false}
            >
                {availableOptions.who_regions.map((region) => (
                    <DropdownItem
                        key={region.id}
                        onClick={() => handleRegionSelect(region)}
                        selected={filters.who_region === region.id}
                    >
                        {region.name}
                    </DropdownItem>
                ))}
            </Dropdown>

            {/* Country */}
            <Dropdown
                label={filters.country ? getSelectedLabel("country", availableOptions.countries) : "Select a country"}
                isOpen={openDropdown === "country"}
                onClick={() => handleDropdownClick("country")}
                loading={loadingOptions.countries}
                disabled={!filters.who_region}
            >
                {availableOptions.countries.map((country) => (
                    <DropdownItem
                        key={country.id}
                        onClick={() => handleCountrySelect(country)}
                        selected={filters.country === country.id}
                    >
                        {country.name}
                    </DropdownItem>
                ))}
            </Dropdown>

            {/* Province/State - DÉSACTIVÉ si pas de country OU pas de states disponibles */}
            <Dropdown
                label={
                    !filters.country 
                        ? "Select a country first"
                        : !hasStates && !loadingOptions.states
                        ? "No states available"
                        : filters.state 
                        ? getSelectedLabel("state", availableOptions.states) 
                        : "Select a state"
                }
                isOpen={openDropdown === "state"}
                onClick={() => handleDropdownClick("state")}
                loading={loadingOptions.states}
                disabled={!filters.country || (!hasStates && !loadingOptions.states)}
            >
                {availableOptions.states.map((state) => (
                    <DropdownItem
                        key={state.id}
                        onClick={() => handleStateSelect(state)}
                        selected={filters.state === state.id}
                    >
                        {state.name}
                    </DropdownItem>
                ))}
            </Dropdown>

            {/* City - DÉSACTIVÉ si pas de state OU pas de cities disponibles */}
            <Dropdown
                label={
                    !filters.state 
                        ? "Select a state first"
                        : !hasCities && !loadingOptions.city
                        ? "No cities available"
                        : filters.city 
                        ? getSelectedLabel("city", availableOptions.city) 
                        : "Select a city"
                }
                isOpen={openDropdown === "city"}
                onClick={() => handleDropdownClick("city")}
                loading={loadingOptions.city}
                disabled={!filters.state || (!hasCities && !loadingOptions.city)}
            >
                {availableOptions.city.map((city) => (
                    <DropdownItem
                        key={city.id}
                        onClick={() => handleCitySelect(city)}
                        selected={filters.city === city.id}
                    >
                        {city.name}
                    </DropdownItem>
                ))}
            </Dropdown>
        </div>
    );
};

// Reusable Dropdown Component
const Dropdown = ({ label, isOpen, onClick, children, loading, disabled }) => {
    return (
        <div className={`dropdown ${disabled ? "dropdown-disabled" : ""}`}>
            <button
                className={`dropdown-button ${isOpen ? "dropdown-open" : ""}`}
                onClick={onClick}
                disabled={disabled}
            >
                <span className="dropdown-label">{label}</span>
                <svg
                    viewBox="0 0 24 24"
                    width="20"
                    height="20"
                    className={`dropdown-arrow ${isOpen ? "arrow-up" : ""}`}
                >
                    <path d="M6 9l6 6 6-6" stroke="currentColor" strokeWidth="2" fill="none" />
                </svg>
            </button>

            {isOpen && !disabled && (
                <div className="dropdown-menu">
                    {loading ? (
                        <div className="dropdown-loading">
                            <div className="spinner"></div>
                            <span>Loading...</span>
                        </div>
                    ) : (
                        <div className="dropdown-items">
                            {children}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

// Dropdown item
const DropdownItem = ({ children, onClick, selected }) => {
    return (
        <button
            className={`dropdown-item ${selected ? "item-selected" : ""}`}
            onClick={onClick}
        >
            {children}
            {selected && (
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                    <path d="M20 6L9 17l-5-5" stroke="currentColor" strokeWidth="2" fill="none" />
                </svg>
            )}
        </button>
    );
};

export default FilterPanel;