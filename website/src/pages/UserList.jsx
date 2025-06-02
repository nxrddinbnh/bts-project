import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import { ChevronsLeft, ChevronsRight } from "lucide-react";

const UserList = ({ theme, toggleTheme }) => {
  const [data, setData] = useState([]);
  const [searchEmail, setSearchEmail] = useState("");
  const [searchId, setSearchId] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const usersPerPage = 10;

  useEffect(() => {
    fetch("http://172.18.199.9/solarpanel/api/index.php?path=login")
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) =>
        console.error("Erreur lors du chargement des utilisateurs :", error)
      );
  }, []);

  const filteredUsers = data.filter((user) => {
    const matchEmail = user.email
      .toLowerCase()
      .includes(searchEmail.toLowerCase());
    const matchId = searchId === "" || String(user.id).includes(searchId);
    return matchEmail && matchId;
  });

  const indexOfLastUser = currentPage * usersPerPage;
  const indexOfFirstUser = indexOfLastUser - usersPerPage;
  const currentUsers = filteredUsers.slice(indexOfFirstUser, indexOfLastUser);
  const totalPages = Math.ceil(filteredUsers.length / usersPerPage);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  return (
    <div className="dashboard">
      <Sidebar theme={theme} toggleTheme={toggleTheme} />
      <main className="main">
        <Header title="Liste des utilisateurs" />
        <div className="content-box">
          {/* Filtres */}
          <div className="filters" style={{ display: "flex", gap: "1rem" }}>
            <input
              type="text"
              placeholder="Rechercher par email"
              value={searchEmail}
              onChange={(e) => {
                setSearchEmail(e.target.value);
                setCurrentPage(1);
              }}
              className="search-input"
              style={{ flex: 0.4, minWidth: "100px" }}
            />
            <input
              type="text"
              placeholder="Rechercher par ID"
              value={searchId}
              onChange={(e) => {
                setSearchId(e.target.value);
                setCurrentPage(1);
              }}
              className="search-input"
              style={{ minWidth: "220px", flexShrink: 0 }}
            />
          </div>

          {/* Tableau */}
          <table className="data-table" style={{ width: "100%", marginTop: "1rem" }}>
            <thead>
              <tr>
                <th style={{ width: "20%" }}>ID</th>
                <th style={{ width: "80%" }}>Email</th>
              </tr>
            </thead>
            <tbody>
              {currentUsers.length > 0 ? (
                currentUsers.map((user) => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td>{user.email}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="2" style={{ textAlign: "center", padding: "1rem" }}>
                    Aucun utilisateur trouvé.
                  </td>
                </tr>
              )}
            </tbody>
          </table>

          {/* Pagination */}
          <div className="filters" style={{ justifyContent: "flex-end", marginTop: "1rem" }}>
            <button
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              disabled={currentPage === 1}
              aria-label="Page précédente"
            >
              <ChevronsLeft size={20} />
            </button>
            <span style={{ color: "var(--text-100)", margin: "0 0.5rem" }}>
              Page {currentPage} sur {totalPages || 1}
            </span>
            <button
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages || totalPages === 0}
              aria-label="Page suivante"
            >
              <ChevronsRight size={20} />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default UserList;
