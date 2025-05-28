import React, { useState, useEffect } from 'react';
import { X, Plus, ChevronsLeft, ChevronsRight } from "lucide-react";
import { fetchCanFrames } from '../services/apiService';

export default function DataTable() {
    const [data, setData] = useState([]);
    const [filters, setFilters] = useState([]);
    const [searchField, setSearchField] = useState('');
    const [searchValue, setSearchValue] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const pageSize = 5;

    // Convierte filtros a objeto para consulta API
    const filtersObj = filters.reduce((acc, cur) => {
        acc[cur.field] = cur.value;
        return acc;
    }, {});

    // Carga datos al cambiar filtros
    useEffect(() => {
        fetchCanFrames(filtersObj)
            .then(d => {
                setData(Array.isArray(d) ? d : []);
                setCurrentPage(1);
            })
            .catch(() => setData([]));
    }, [filtersObj]);

    const fields = data.length > 0 ? Object.keys(data[0]) : [];

    const totalPages = Math.ceil(data.length / pageSize);
    const paginatedData = data.slice((currentPage - 1) * pageSize, currentPage * pageSize);

    function addFilter() {
        if (searchField && searchValue) {
            if (!filters.some(f => f.field === searchField && f.value === searchValue)) {
                setFilters([...filters, { field: searchField, value: searchValue }]);
            }
            setSearchValue('');
        }
    }

    function removeFilter(field) {
        setFilters(filters.filter(f => f.field !== field));
    }

    return (
        <div className="content-box">
            <div className="filters">
                <input
                    type="text"
                    placeholder="Search..."
                    value={searchValue}
                    onChange={e => setSearchValue(e.target.value)}
                />
                <select value={searchField} onChange={e => setSearchField(e.target.value)}>
                    <option value="">Select field</option>
                    {fields.map(field => (
                        <option key={field} value={field}>{field}</option>
                    ))}
                </select>
                <button onClick={addFilter} aria-label="Add filter">
                    <Plus size={16} /> Add
                </button>
            </div>

            <div className="filter-list">
                {filters.map(({ field, value }) => (
                    <div key={field} className="filter-pill">
                        {field}: {value}
                        <button onClick={() => removeFilter(field)} aria-label={`Remove filter ${field}`}>
                            <X size={12} />
                        </button>
                    </div>
                ))}
            </div>

            <div style={{ overflowX: "auto" }}>
                <table className="data-table">
                    <thead>
                        <tr>
                            <th>Field</th>
                            {paginatedData.map((_, i) => (
                                <th key={i}>Item {i + 1}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {fields.map(field => (
                            <tr key={field}>
                                <td>{field}</td>
                                {paginatedData.map((item, i) => (
                                    <td key={i}>{item[field]}</td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div style={{ display: "flex", justifyContent: "flex-end", alignItems: "center", gap: "1rem", marginTop: "1rem" }}>
                <button onClick={() => setCurrentPage(p => Math.max(1, p - 1))} disabled={currentPage === 1} aria-label="Previous page">
                    <ChevronsLeft size={20} />
                </button>
                <span>
                    Page {currentPage} of {totalPages || 1}
                </span>
                <button onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))} disabled={currentPage === totalPages || totalPages === 0} aria-label="Next page">
                    <ChevronsRight size={20} />
                </button>
            </div>
        </div>
    );
}
