import React, { useMemo, useState } from "react";

const initialProducts = [
  { id: 1, name: "Rice 5kg", sku: "GRO-001", category: "Groceries", price: 420, stock: 18 },
  { id: 2, name: "Cooking Oil 1L", sku: "GRO-002", category: "Groceries", price: 145, stock: 7 },
  { id: 3, name: "Bath Soap", sku: "PER-001", category: "Personal Care", price: 38, stock: 32 },
  { id: 4, name: "Notebook", sku: "STA-001", category: "Stationery", price: 55, stock: 0 },
];

const money = (amount) =>
  new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR" }).format(amount);

export default function ProductCatalog() {
  const [products, setProducts] = useState(initialProducts);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All");
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [notice, setNotice] = useState("");
  const emptyForm = { name: "", sku: "", category: "Groceries", price: "", stock: "" };
  const [form, setForm] = useState(emptyForm);

  const categories = useMemo(
    () => ["All", ...new Set(products.map((item) => item.category))],
    [products]
  );

  const visibleProducts = useMemo(() => {
    const term = search.trim().toLowerCase();
    return products.filter((item) => {
      const matchesText =
        item.name.toLowerCase().includes(term) ||
        item.sku.toLowerCase().includes(term);
      const matchesCategory = category === "All" || item.category === category;
      return matchesText && matchesCategory;
    });
  }, [products, search, category]);

  function updateField(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  function startAdd() {
    setEditingId(null);
    setForm(emptyForm);
    setShowForm(true);
  }

  function startEdit(product) {
    setEditingId(product.id);
    setForm({
      name: product.name,
      sku: product.sku,
      category: product.category,
      price: String(product.price),
      stock: String(product.stock),
    });
    setShowForm(true);
  }

  function saveProduct(event) {
    event.preventDefault();
    const price = Number(form.price);
    const stock = Number(form.stock);
    if (!form.name.trim() || !form.sku.trim() || price < 0 || stock < 0) {
      setNotice("Enter a name, SKU, and valid non-negative values.");
      return;
    }

    const duplicate = products.some(
      (item) => item.sku.toLowerCase() === form.sku.trim().toLowerCase()
        && item.id !== editingId
    );
    if (duplicate) {
      setNotice("That SKU is already in use.");
      return;
    }

    const productData = {
      id: editingId ?? Date.now(),
      name: form.name.trim(),
      sku: form.sku.trim(),
      category: form.category,
      price,
      stock,
    };

    setProducts((current) =>
      editingId
        ? current.map((item) => item.id === editingId ? productData : item)
        : [productData, ...current]
    );
    setShowForm(false);
    setNotice(editingId ? "Product updated." : "Product added.");
  }

  function deleteProduct(id) {
    const confirmed = window.confirm("Delete this product?");
    if (!confirmed) return;
    setProducts((current) => current.filter((item) => item.id !== id));
    setNotice("Product deleted.");
  }

  function closeForm() {
    setShowForm(false);
    setNotice("");
  }

  return (
    <main style={styles.page}>
      <header style={styles.header}>
        <div>
          <h1 style={styles.heading}>Product Catalog</h1>
          <p style={styles.subheading}>Manage products and inventory for your POS.</p>
        </div>
        <button style={styles.primaryButton} onClick={startAdd}>Add product</button>
      </header>

      {notice && <p role="status" style={styles.notice}>{notice}</p>}

      <section style={styles.toolbar}>
        <input
          aria-label="Search products"
          placeholder="Search by product or SKU..."
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          style={styles.input}
        />
        <select
          aria-label="Filter category"
          value={category}
          onChange={(event) => setCategory(event.target.value)}
          style={styles.input}
        >
          {categories.map((item) => <option key={item}>{item}</option>)}
        </select>
      </section>

      {showForm && (
        <form onSubmit={saveProduct} style={styles.form}>
          <h2 style={styles.formTitle}>{editingId ? "Edit product" : "New product"}</h2>
          <label style={styles.field}>
            Product name
            <input name="name" value={form.name} onChange={updateField} style={styles.input} required />
          </label>
          <label style={styles.field}>
            SKU / barcode
            <input name="sku" value={form.sku} onChange={updateField} style={styles.input} required />
          </label>
          <label style={styles.field}>
            Category
            <select name="category" value={form.category} onChange={updateField} style={styles.input}>
              <option>Groceries</option>
              <option>Personal Care</option>
              <option>Stationery</option>
              <option>Electronics</option>
            </select>
          </label>
          <label style={styles.field}>
            Price (₹)
            <input name="price" type="number" min="0" step="0.01" value={form.price} onChange={updateField} style={styles.input} required />
          </label>
          <label style={styles.field}>
            Stock quantity
            <input name="stock" type="number" min="0" value={form.stock} onChange={updateField} style={styles.input} required />
          </label>
          <div style={styles.actions}>
            <button type="submit" style={styles.primaryButton}>Save product</button>
            <button type="button" onClick={closeForm} style={styles.secondaryButton}>Cancel</button>
          </div>
        </form>
      )}

      <section style={styles.summary}>
        <span>{visibleProducts.length} products shown</span>
        <span>{products.filter((item) => item.stock <= 5).length} products with low stock</span>
      </section>

      <div style={styles.tableWrap}>
        <table style={styles.table}>
          <thead>
            <tr>
              <th>Product</th><th>SKU</th><th>Category</th>
              <th>Price</th><th>Stock</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {visibleProducts.map((item) => (
              <tr key={item.id}>
                <td>{item.name}</td>
                <td>{item.sku}</td>
                <td>{item.category}</td>
                <td>{money(item.price)}</td>
                <td>
                  <span style={item.stock <= 5 ? styles.lowStock : styles.stock}>
                    {item.stock}
                  </span>
                </td>
                <td>
