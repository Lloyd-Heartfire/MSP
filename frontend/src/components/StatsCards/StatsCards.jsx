import React from "react";
import {useData} from "../../context/DataContext"
import "./StatsCards.css"

const StatsCards = () => {
    const {data, isValidated} = useData();

    // Do not display anything if the data has not been validated
    if (!isValidated) {
        return null;
    }

    // Number formatting (with thousands separators)
    const formatNumber = (num) => {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(2) + " M";
        } else if (num >= 1000) {
            return (num / 1000).toFixed(2) + " K";
        }
        return num.toLocaleString();
    };

    return (
        <div className="stats-cards-container">
            {/* New Cases */}
            <StatsCard
                title={('dashboard.newCases') || "New Cases"}
                value={formatNumber(data.stats.newCases)}
                colorClass="stat-new-cases"
            />

            {/* Total Cases */}
            <StatsCard
                title={('dashboard.totalCases') || "Total Cases"}
                value={formatNumber(data.stats.totalCases)}
                colorClass="stat-total-cases"
            />

            {/* New Deaths */}
            <StatsCard
                title={('dashboard.newDeaths') || "New Deaths"}
                value={formatNumber(data.stats.newDeaths)}
                colorClass="stat-new-deaths"
            />

            {/* Total Deaths */}
            <StatsCard
                title={('dashboard.totalDeaths') || "Total Deaths"}
                value={formatNumber(data.stats.totalDeaths)}
                colorClass="stat-total-deaths"
            />

            {/* Active Cases */}
            <StatsCard
                title={('dashboard.activeCases') || "Active Cases"}
                value={formatNumber(data.stats.activeCases)}
                colorClass="stat-active-cases"
            />

            {/* Total Recovered */}
            <StatsCard
                title={('dashboard.totalRecovered') || "Total Recovered"}
                value={formatNumber(data.stats.totalRecovered)}
                colorClass="stat-total-recovered"
            />
        </div>
    );
};

// Individual component in card
const StatsCard = ({title, value, colorClass}) => {
    return (
        <div className={`stats-card ${colorClass}`}>
            <h4 className="stats-card-title">{title}</h4>
            <p className="stats-card-value">{value}</p>
        </div>
    );
};

export default StatsCards;