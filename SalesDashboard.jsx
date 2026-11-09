import React, { useMemo, useState } from "react";

const sampleSales = [
  { id: "S-1001", date: "2026-11-01", customer: "Walk-in", method: "UPI", amount: 2450 },
  { id: "S-1002", date: "2026-11-01", customer: "Arun", method: "Cash", amount: 860 },
  { id: "S-1003", date: "2026-11-02", customer: "Meena", method: "Card", amount: 1720 },
  { id: "S-1004", date: "2026-11-03", customer: "Walk-in", method: "UPI", amount: 3200 },
  { id: "S-1005", date: "2026-11-04", customer: "Kumar", method: "Cash", amount: 540 },
  { id: "S-1006", date: "2026-11-05", customer: "Walk-in", method: "Card", amount: 1980 },
];

const inr = (amount) =>
  new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(amount);

export default function SalesDashboard() {
  const [sales, setSales] = useState(sampleSales);
  const [fromDate, setFromDate] = useState("2026-11-01");
  const [toDate, setToDate] = useState("2026-11-30");
  const [methodFilter, setMethodFilter] = useState("All");
  const [query, setQuery] = useState("");
  const [selectedSale, setSelectedSale] = useState(null);

  const filteredSales = useMemo(() => {
    const term = query.trim().toLowerCase();
    return sales.filter((sale) => {
      const dateMatch = sale.date >= fromDate && sale.date <= toDate;
      const methodMatch = methodFilter === "All" || sale.method === methodFilter;
      const textMatch = sale.id.toLowerCase().includes(term)
        || sale.customer.toLowerCase().includes(term);
      return dateMatch && methodMatch && textMatch;
    });
  }, [sales, fromDate, toDate, methodFilter, query]);

  const totalRevenue = filteredSales.reduce((sum, sale) => sum + sale.amount, 0);
  const averageSale = filteredSales.length ? totalRevenue / filteredSales.length : 0;
  const paymentTotals = useMemo(() => {
    return filteredSales.reduce((result, sale) => {
      result[sale.method] = (result[sale.method] || 0) + sale.amount;
      return result;
    }, {});
  }, [filteredSales]);

  const highestSale = filteredSales.reduce(
    (best, sale) => !best || sale.amount > best.amount ? sale : best,
    null
  );

  function exportCSV() {
    const header = ["Sale ID", "Date", "Customer", "Payment", "Amount"];
    const rows = filteredSales.map((sale) =>
      [sale.id, sale.date, sale.customer, sale.method, sale.amount]
    );
    const csv = [header, ...rows].map((row) =>
      row.map((value) => `"${String(value).replaceAll('"', '""')}"`).join(",")
    ).join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "sales-report.csv";
    link.click();
    URL.revokeObjectURL(url);
  }

  function addDemoSale() {
    const nextNumber = 1001 + sales.length;
    const today = new Date().toISOString().slice(0, 10);
    const newSale = {
      id: `S-${nextNumber}`,
      date: today,
      customer: "Demo customer",
      method: "UPI",
      amount: 999,
    };
    setSales((current) => [newSale, ...current]);
  }

  function clearFilters() {
    setFromDate("2026-11-01");
    setToDate("2026-11-30");
    setMethodFilter("All");
    setQuery("");
  }

  return (
    <main style={styles.page}>
      <header style={styles.header}>
        <div>
          <h1 style={styles.title}>Sales Dashboard</h1>
          <p style={styles.muted}>Review revenue, payment methods, and transactions.</p>
        </div>
        <div style={styles.headerActions}>
          <button style={styles.secondary} onClick={addDemoSale}>Add demo sale</button>
          <button style={styles.primary} onClick={exportCSV}>Export CSV</button>
        </div>
      </header>

      <section style={styles.filters}>
        <label>
          From
          <input type="date" value={fromDate} onChange={(event) => setFromDate(event.target.value)} style={styles.input} />
        </label>
        <label>
          To
          <input type="date" value={toDate} onChange={(event) => setToDate(event.target.value)} style={styles.input} />
        </label>
        <label>
          Payment method
          <select value={methodFilter} onChange={(event) => setMethodFilter(event.target.value)} style={styles.input}>
            <option>All</option><option>Cash</option><option>UPI</option><option>Card</option>
          </select>
        </label>
        <label>
          Search
          <input value={query} onChange={(event) => setQuery(event.target.value)}
            placeholder="Sale ID or customer" style={styles.input} />
        </label>
        <button style={styles.clear} onClick={clearFilters}>Reset</button>
      </section>

      <section style={styles.cards}>
        <article style={styles.card}>
          <span style={styles.cardLabel}>Total revenue</span>
          <strong style={styles.metric}>{inr(totalRevenue)}</strong>
          <small>{filteredSales.length} transactions</small>
        </article>
        <article style={styles.card}>
          <span style={styles.cardLabel}>Average sale value</span>
          <strong style={styles.metric}>{inr(averageSale)}</strong>
          <small>Revenue divided by transaction count</small>
        </article>
        <article style={styles.card}>
          <span style={styles.cardLabel}>Highest sale</span>
          <strong style={styles.metric}>{inr(highestSale?.amount || 0)}</strong>
          <small>{highestSale?.id || "No transaction"}</small>
        </article>
      </section>

      <section style={styles.panel}>
        <h2 style={styles.heading}>Payment summary</h2>
        <div style={styles.paymentGrid}>
          {["Cash", "UPI", "Card"].map((method) => {
            const amount = paymentTotals[method] || 0;
            const percent = totalRevenue ? (amount / totalRevenue) * 100 : 0;
            return (
              <div key={method} style={styles.paymentItem}>
                <div style={styles.paymentHeading}>
                  <strong>{method}</strong><span>{inr(amount)}</span>
                </div>
                <div style={styles.track}>
                  <div style={{ ...styles.fill, width: `${percent}%` }} />
                </div>
                <small>{percent.toFixed(1)}% of revenue</small>
              </div>
            );
          })}
        </div>
      </section>

      <section style={styles.panel}>
        <div style={styles.tableHeading}>
          <h2 style={styles.heading}>Transactions</h2>
          <span style={styles.muted}>{filteredSales.length} records</span>
        </div>
        <div style={styles.tableWrap}>
          <table style={styles.table}>
            <thead>
              <tr><th>Sale ID</th><th>Date</th><th>Customer</th><th>Payment</th><th>Amount</th><th>Details</th></tr>
            </thead>
            <tbody>
              {filteredSales.map((sale) => (
                <tr key={sale.id}>
                  <td>{sale.id}</td><td>{sale.date}</td><td>{sale.customer}</td>
                  <td><span style={styles.pill}>{sale.method}</span></td>
                  <td>{inr(sale.amount)}</td>
                  <td><button style={styles.linkButton} onClick={() => setSelectedSale(sale)}>View</button></td>
                </tr>
              ))}
              {filteredSales.length === 0 && (
                <tr><td colSpan="6" style={styles.empty}>No sales match these filters.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </section>

      {selectedSale && (
        <div style={styles.overlay} role="presentation" onClick={() => setSelectedSale(null)}>
          <section role="dialog" aria-modal="true" aria-labelledby="sale-dialog-title"
            style={styles.dialog} onClick={(event) => event.stopPropagation()}>
            <h2 id="sale-dialog-title">Sale details</h2>
            <p><strong>Sale ID:</strong> {selectedSale.id}</p>
            <p><strong>Date:</strong> {selectedSale.date}</p>
            <p><strong>Customer:</strong> {selectedSale.customer}</p>
            <p><strong>Payment:</strong> {selectedSale.method}</p>
            <p><strong>Amount:</strong> {inr(selectedSale.amount)}</p>
            <button style={styles.primary} onClick={() => setSelectedSale(null)}>Close</button>
          </section>
        </div>
      )}
