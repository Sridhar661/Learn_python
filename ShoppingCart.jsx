import React, { useMemo, useState } from "react";

const products = [
  { id: 1, name: "Rice 5kg", price: 420, barcode: "8901001000011" },
  { id: 2, name: "Cooking Oil 1L", price: 145, barcode: "8901001000012" },
  { id: 3, name: "Bath Soap", price: 38, barcode: "8901001000013" },
  { id: 4, name: "Notebook", price: 55, barcode: "8901001000014" },
  { id: 5, name: "Tea 250g", price: 110, barcode: "8901001000015" },
];

const formatINR = (value) =>
  new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR" }).format(value);

export default function ShoppingCart() {
  const [cart, setCart] = useState([]);
  const [barcode, setBarcode] = useState("");
  const [discount, setDiscount] = useState(0);
  const [taxRate, setTaxRate] = useState(5);
  const [message, setMessage] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("Cash");
  const [lastReceipt, setLastReceipt] = useState(null);

  const subtotal = useMemo(
    () => cart.reduce((sum, line) => sum + line.price * line.quantity, 0),
    [cart]
  );
  const discountAmount = Math.min(subtotal, Math.max(0, Number(discount) || 0));
  const taxableAmount = Math.max(0, subtotal - discountAmount);
  const taxAmount = taxableAmount * (Number(taxRate) / 100);
  const total = taxableAmount + taxAmount;
  const itemCount = cart.reduce((sum, line) => sum + line.quantity, 0);

  function addProduct(product) {
    setCart((current) => {
      const found = current.find((line) => line.id === product.id);
      if (found) {
        return current.map((line) =>
          line.id === product.id ? { ...line, quantity: line.quantity + 1 } : line
        );
      }
      return [...current, { ...product, quantity: 1 }];
    });
    setMessage(`${product.name} added to cart.`);
  }

  function scanBarcode(event) {
    event.preventDefault();
    const found = products.find((item) => item.barcode === barcode.trim());
    if (!found) {
      setMessage("No product found for this barcode.");
      return;
    }
    addProduct(found);
    setBarcode("");
  }

  function changeQuantity(id, amount) {
    setCart((current) =>
      current
        .map((line) => line.id === id
          ? { ...line, quantity: Math.max(0, line.quantity + amount) }
          : line)
        .filter((line) => line.quantity > 0)
    );
  }

  function removeLine(id) {
    setCart((current) => current.filter((line) => line.id !== id));
  }

  function clearCart() {
    setCart([]);
    setDiscount(0);
    setMessage("Cart cleared.");
  }

  function completeSale() {
    if (cart.length === 0) {
      setMessage("Add at least one product before checkout.");
      return;
    }
    const receipt = {
      number: `SALE-${Date.now()}`,
      date: new Date().toLocaleString("en-IN"),
      lines: cart,
      subtotal,
      discount: discountAmount,
      tax: taxAmount,
      total,
      paymentMethod,
    };
    setLastReceipt(receipt);
    setCart([]);
    setDiscount(0);
    setMessage("Sale completed successfully.");
  }

  return (
    <main style={styles.page}>
      <header style={styles.header}>
        <div>
          <h1 style={styles.title}>POS Checkout</h1>
          <p style={styles.muted}>Scan products, adjust quantities, and complete a sale.</p>
        </div>
        <span style={styles.counter}>{itemCount} items</span>
      </header>

      {message && <p role="status" style={styles.message}>{message}</p>}

      <form onSubmit={scanBarcode} style={styles.scanForm}>
        <input
          autoFocus
          value={barcode}
          onChange={(event) => setBarcode(event.target.value)}
          placeholder="Enter or scan barcode..."
          style={styles.input}
        />
        <button style={styles.primary}>Add barcode</button>
      </form>

      <section style={styles.layout}>
        <div style={styles.panel}>
          <h2 style={styles.sectionTitle}>Available products</h2>
          <div style={styles.productGrid}>
            {products.map((product) => (
              <button key={product.id} style={styles.product}
                onClick={() => addProduct(product)}>
                <strong>{product.name}</strong>
                <span>{formatINR(product.price)}</span>
                <small>{product.barcode}</small>
              </button>
            ))}
          </div>
        </div>

        <div style={styles.panel}>
          <h2 style={styles.sectionTitle}>Current cart</h2>
          {cart.length === 0 ? (
            <p style={styles.muted}>Your cart is empty. Select a product to begin.</p>
          ) : (
            <div style={styles.lines}>
              {cart.map((line) => (
                <div key={line.id} style={styles.line}>
                  <div style={styles.lineInfo}>
                    <strong>{line.name}</strong>
                    <small>{formatINR(line.price)} each</small>
                  </div>
                  <div style={styles.quantity}>
                    <button onClick={() => changeQuantity(line.id, -1)} aria-label={`Decrease ${line.name}`}>−</button>
                    <span>{line.quantity}</span>
                    <button onClick={() => changeQuantity(line.id, 1)} aria-label={`Increase ${line.name}`}>+</button>
                  </div>
                  <strong>{formatINR(line.price * line.quantity)}</strong>
                  <button style={styles.remove} onClick={() => removeLine(line.id)}>×</button>
                </div>
              ))}
            </div>
          )}

          <div style={styles.controls}>
            <label>
              Discount (₹)
              <input type="number" min="0" value={discount}
                onChange={(event) => setDiscount(event.target.value)} style={styles.input} />
            </label>
            <label>
              Tax rate (%)
              <select value={taxRate} onChange={(event) => setTaxRate(event.target.value)} style={styles.input}>
                <option value="0">0%</option>
                <option value="5">5%</option>
                <option value="12">12%</option>
                <option value="18">18%</option>
                <option value="28">28%</option>
              </select>
            </label>
            <label>
              Payment
              <select value={paymentMethod} onChange={(event) => setPaymentMethod(event.target.value)} style={styles.input}>
                <option>Cash</option><option>UPI</option><option>Card</option>
              </select>
            </label>
          </div>

          <div style={styles.totals}>
            <p><span>Subtotal</span><strong>{formatINR(subtotal)}</strong></p>
            <p><span>Discount</span><strong>− {formatINR(discountAmount)}</strong></p>
            <p><span>Tax ({taxRate}%)</span><strong>{formatINR(taxAmount)}</strong></p>
            <p style={styles.grandTotal}><span>Total</span><strong>{formatINR(total)}</strong></p>
          </div>
          <div style={styles.buttons}>
            <button onClick={clearCart} style={styles.secondary}>Clear cart</button>
            <button onClick={completeSale} style={styles.primary}>Complete sale</button>
          </div>
        </div>
      </section>

      {lastReceipt && (
        <section style={styles.receipt}>
          <h2>Last sale receipt</h2>
          <p>{lastReceipt.number} · {lastReceipt.date}</p>
