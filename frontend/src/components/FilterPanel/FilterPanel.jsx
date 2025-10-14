import React, {useState, useEffect} from "react";
import {useData} from "../../context/DataContext";
import "./FilterPanel.css";

const FilterPanel = () => {
    const {
        filters,
        updateFilters,
        availableOptions,
        loadingOptions,
        fetchPandemics,
        fetchRegions,
    } = useData();

    // Local state for open dropdown
    const {openDropdown, setOpenDropdown} = useState(null);

    // Load the pandemics
    useEffect(() => {
        if (availableOptions.pandemics.length === 0) {
            fetchPandemics();
        }
    }, []);

    // Load the regions
    useEffect(() => {
        if (availableOptions.regions.length === 0) {
            fetchRegions();
        }
    }, []);

    // Open/Close dropdown
    const handleDropdownClick = (dropdownName) => {
        setOpenDropdown(openDropdown === dropdownName ? null : dropdownName);
    };

    // Select a who-region
    const handleRegionSelect = (region) => {
        updateFilters({region: region.id});
        setOpenDropdown(null);
    };

    // Select a country
    const handleCountrySelect = (country) => {
        updateFilters({country: country.id});
        setOpenDropdown(null);
    };

    // Select a province
    const handleProvinceSelect = (province) => {
        updateFilters({province: province.id});
        setOpenDropdown(null);
    };

    // Select a admin2
    const handleAdmin2Select = (admin2) => {
        updateFilters({admin2: admin2.id});
        setOpenDropdown(null);
    };

    // Get the label for each filter
    const getSelectedLabel = (filterKey, options) => {
        const selected = options.find(opt => opt.id === filters[filterKey]);
        return selected?.name || `Select ${filterKey}`;
    };

    return (
        <div className="filter-panel">
            {/* Who-Region */}
            <Dropdown
                label={filters.region ? getSelectedLabel("region", availableOptions.regions) : "Eastern Mediterranean Region"}
                isOpen={openDropdown === "region"}
                onClick={() => handleDropdownClick("region")}
                loading={loadingOptions.regions}
            >
                {availableOptions.regions.map((region) => (
                    <DropdownItem
                        key={region.id}
                        onClick={() => handleRegionSelect(region)}
                        selected={filters.region === region.id}
                    >
                        {region.name}
                    </DropdownItem>
                ))}
            </Dropdown>

            {/* Country */}
            <Dropdown
                label={filters.country ? getSelectedLabel("country", availableOptions.countries) : "Saint Vincent and the Grenadines"}
                isOpen={openDropdown === "country"}
                onClick={() => handleDropdownClick("country")}
                loading={loadingOptions.countries}
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

            {/* Province/State */}
            <Dropdown
                label={filters.province ? getSelectedLabel("province", availableOptions.provinces) : "Saint Helena, Ascension and Tristan da Cunha"}
                isOpen={openDropdown === "province"}
                onClick={() => handleDropdownClick("province")}
                loading={loadingOptions.provinces}
            >
                {availableOptions.provinces.map((province) => (
                    <DropdownItem
                        key={province.id}
                        onClick={() => handleProvinceSelect(province)}
                        selected={filters.province === province.id}
                    >
                        {province.name}
                    </DropdownItem>
                ))}
            </Dropdown>

            {/* Admin2 */}
            <Dropdown
                label={filters.admin2 ? getSelectedLabel("admin2", availableOptions.countries) : "Bristol Bay plus Lake and Peninsula"}
                isOpen={openDropdown === "admin2"}
                onClick={() => handleDropdownClick("admin2")}
                loading={loadingOptions.countries}
            >
                {availableOptions.countries.map((admin2) => (
                    <DropdownItem
                        key={admin2.id}
                        onClick={() => handleAdmin2Select(admin2)}
                        selected={filters.admin2 === admin2.id}
                    >
                        {admin2.name}
                    </DropdownItem>
                ))}
            </Dropdown>
        </div>
    );
};

// Reusable Dropdown Component
const Dropdown = ({label, isOpen, onClick, children, loading, disabled}) => {
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

            {isOpen && (
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
const DropdownItem = ({children, onClick, selected}) => {
    return (
        <button
            className={`dropdown-item ${selected ? "item-selected" : ""}`}
            onClick={onClick}
        >
            {children}
            {selected && (
                <svg viewBow="0 0 24 24" width="16" height="16" fill="currentColor">
                    <path d="M20 6L9 17l-5-5" stroke="currentColor" strokeWidth="2" fill="none" />
                </svg>
            )}
        </button>
    );
};

export default FilterPanel;