import React, { useState, useEffect } from 'react';
import { X, Plus, ChevronsLeft, ChevronsRight } from "lucide-react";
import { fetchCanFrames } from '../services/apiService';

export default function DataTable({ onExportDataChange }) {
    const [data, setData] = useState([]);
    const [filters, setFilters] = useState([]);
    const [searchField, setSearchField] = useState('');
    const [searchValue, setSearchValue] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const pageSize = 5;

    useEffect(() => {
        fetchCanFrames()
            .then(rawData => {
                let filteredData = rawData;

                if (startDate && endDate) {
                    const start = new Date(startDate);
                    const end = new Date(endDate);
                    end.setHours(23, 59, 59, 999);

                    filteredData = filteredData.filter(item => {
                        if (!item.date) return false;
                        const itemDate = new Date(item.date);
                        return itemDate >= start && itemDate <= end;
                    });
                }

                if (filters.length > 0) {
                    filteredData = filteredData.filter(item =>
                        filters.every(({ field, value }) => {
                            if (!item[field]) return false;
                            return String(item[field]).toLowerCase().includes(value.toLowerCase());
                        })
                    );
                }

                setData(filteredData);
                setCurrentPage(1);

                if (typeof onExportDataChange === 'function') {
                    onExportDataChange(filteredData);
                }
            })
            .catch(() => {
                setData([]);
                if (typeof onExportDataChange === 'function') {
                    onExportDataChange([]);
                }
            });
    }, [filters, startDate, endDate, onExportDataChange]);

    return (
        <div className="content-box">
            {/* Filtres de date */}
            <div className="filters" style={{ marginBottom: '1rem' }}>
                <input
                    type="date"
                    value={startDate}
                    onChange={e => setStartDate(e.target.value)}
                />
                <input
                    type="date"
                    value={endDate}
                    onChange={e => setEndDate(e.target.value)}
                />
            </div>

            {/* Filtres de champ/valeur */}
            <div className="filters">
                <input
                    type="text"
                    placeholder="Search..."
                    value={searchValue}
                    onChange={e => setSearchValue(e.target.value)}
                />
                <select value={searchField} onChange={e => setSearchField(e.target.value)}>
                    <option value="">Select field</option>
                    {data.length > 0 && Object.keys(data[0]).map(field => (
                        <option key={field} value={field}>{field}</option>
                    ))}
                </select>
                <button
                    onClick={() => {
                        if (searchField && searchValue) {
                            if (!filters.some(f => f.field === searchField && f.value === searchValue)) {
                                setFilters([...filters, { field: searchField, value: searchValue }]);
                            }
                            setSearchValue('');
                        }
                    }}
                    aria-label="Add filter"
                >
                    <Plus size={16} /> Add
                </button>
            </div>

            {/* Liste des filtres */}
            <div className="filter-list">
                {filters.map(({ field, value }) => (
                    <div key={field + value} className="filter-pill">
                        {field}: {value}
                        <button
                            onClick={() => setFilters(filters.filter(f => !(f.field === field && f.value === value)))}
                            aria-label={`Remove filter ${field}`}
                        >
                            <X size={12} />
                        </button>
                    </div>
                ))}
            </div>

            {/* Tableau */}
            <div style={{ overflowX: "auto" }}>
                <table className="data-table">
                    <thead>
                        <tr>
                            <th>Field</th>
                            {data.slice((currentPage - 1) * pageSize, currentPage * pageSize).map((item, i) => (
                                <th key={i}>
                                    {item.date
                                        ? new Date(item.date).toLocaleDateString('fr-FR') + " " + item.date.substring(11)
                                        : `Élément ${i + 1}`}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {data.length > 0 && Object.keys(data[0]).map(field => (
                            <tr key={field}>
                                <td>{field}</td>
                                {data.slice((currentPage - 1) * pageSize, currentPage * pageSize).map((item, i) => (
                                    <td key={i}>
                                        {String(item[field]).match(/^\d{4}-\d{2}-\d{2}/)
                                            ? new Date(item[field]).toLocaleDateString('fr-FR') + " " + item[field].substring(11)
                                            : item[field]}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Pagination */}
            <div className="filters" style={{ justifyContent: 'flex-end', marginTop: '1rem' }}>
                <button onClick={() => setCurrentPage(p => Math.max(1, p - 1))} disabled={currentPage === 1} aria-label="Previous page">
                    <ChevronsLeft size={20} />
                </button>
                <span style={{ color: 'var(--text-100)' }}>
                    Page {currentPage} of {Math.ceil(data.length / pageSize) || 1}
                </span>
                <button
                    onClick={() => setCurrentPage(p => Math.min(Math.ceil(data.length / pageSize), p + 1))}
                    disabled={currentPage === Math.ceil(data.length / pageSize) || data.length === 0}
                    aria-label="Next page"
                >
                    <ChevronsRight size={20} />
                </button>
            </div>
        </div>
    );
}
