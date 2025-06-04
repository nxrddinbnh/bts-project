import React from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import DataTable from '../components/DataTable';

export default function MainPage({
  data,
  filters,
  removeFilter,
  searchField,
  setSearchField,
  searchValue,
  setSearchValue,
  addFilter,
  onLogout,
  theme,       // reçu depuis App
  toggleTheme, // reçu depuis App
}) {
  return (
    <div className="dashboard">
      <Sidebar theme={theme} toggleTheme={toggleTheme} />

      <div className="main">
        <Header onLogout={onLogout} />
        <DataTable
          data={data}
          filters={filters}
          removeFilter={removeFilter}
          searchField={searchField}
          setSearchField={setSearchField}
          searchValue={searchValue}
          setSearchValue={setSearchValue}
          addFilter={addFilter}
        />
      </div>
    </div>
  );
}
