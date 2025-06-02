import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchCanFrames } from '../services/apiService';
import MainPage from './MainPage';

export default function HomePage() {
    const [data, setData] = useState([]);
    const [filters, setFilters] = useState([]);
    const [searchField, setSearchField] = useState("id");
    const [searchValue, setSearchValue] = useState("");
    const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'dark');
    const navigate = useNavigate();

    useEffect(() => {
        // Appliquer le thème sur la racine HTML
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    }, [theme]);

    useEffect(() => {
        const filterObj = filters.reduce((acc, { field, value }) => {
            acc[field] = value;
            return acc;
        }, {});
        fetchCanFrames(filterObj)
            .then(setData)
            .catch(() => setData([]));
    }, [filters]);

    const addFilter = () => {
        if (!searchValue.trim()) return;
        if (filters.some(f => f.field === searchField)) {
            alert("Filter for this field already added");
            return;
        }
        setFilters([...filters, { field: searchField, value: searchValue.trim() }]);
        setSearchValue("");
    };

    const removeFilter = (field) => {
        setFilters(filters.filter(f => f.field !== field));
    };

    const handleLogout = () => {
        navigate('/');
    };

    const toggleTheme = () => {
        setTheme(theme === 'dark' ? 'light' : 'dark');
    };

    return (
        <MainPage
            data={data}
            filters={filters}
            removeFilter={removeFilter}
            searchField={searchField}
            setSearchField={setSearchField}
            searchValue={searchValue}
            setSearchValue={setSearchValue}
            addFilter={addFilter}
            onLogout={handleLogout}
            theme={theme}
            toggleTheme={toggleTheme}
            exportData={data}
        />
        
    );
}
