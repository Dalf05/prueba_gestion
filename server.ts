import express from "express";
import { createServer as createViteServer } from "vite";
import Database from "better-sqlite3";
import path from "path";

const db = new Database("incidencias.db");

// Inicializar base de datos (Espejo de la lógica de Django)
db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    role TEXT CHECK(role IN ('student', 'staff', 'admin'))
  );

  CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    category TEXT,
    priority TEXT CHECK(priority IN ('low', 'medium', 'high', 'urgent')),
    status TEXT DEFAULT 'open' CHECK(status IN ('open', 'in_progress', 'resolved', 'closed')),
    location TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
  );

  CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id INTEGER,
    user_id INTEGER,
    text TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(incident_id) REFERENCES incidents(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
  );
`);

// Datos iniciales
const rowCount = db.prepare("SELECT count(*) as count FROM users").get() as { count: number };
if (rowCount.count === 0) {
  db.prepare("INSERT INTO users (name, email, role) VALUES (?, ?, ?)").run("Admin UniFix", "admin@universidad.edu", "admin");
  db.prepare("INSERT INTO incidents (title, description, category, priority, location, user_id) VALUES (?, ?, ?, ?, ?, ?)")
    .run("Falla de red en Biblioteca", "La conexión Wi-Fi se cae constantemente en la sala de lectura.", "TI", "high", "Edificio Central - Piso 1", 1);
}

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // API Routes (Mismo comportamiento que Django Rest Framework)
  app.get("/api/incidents", (req, res) => {
    const incidents = db.prepare("SELECT * FROM incidents ORDER BY created_at DESC").all();
    res.json(incidents);
  });

  app.get("/api/incidents/:id", (req, res) => {
    const incident = db.prepare("SELECT * FROM incidents WHERE id = ?").get(req.params.id);
    const comments = db.prepare(`
      SELECT c.*, u.name as user_name 
      FROM comments c 
      JOIN users u ON c.user_id = u.id 
      WHERE c.incident_id = ? 
      ORDER BY c.created_at ASC
    `).all(req.params.id);
    res.json({ ...incident, comments });
  });

  app.post("/api/incidents", (req, res) => {
    const { title, description, category, priority, location } = req.body;
    const result = db.prepare(
      "INSERT INTO incidents (title, description, category, priority, location, user_id) VALUES (?, ?, ?, ?, ?, ?)"
    ).run(title, description, category, priority, location, 1);
    res.json({ id: result.lastInsertRowid });
  });

  app.post("/api/incidents/:id/comments", (req, res) => {
    const { text } = req.body;
    db.prepare("INSERT INTO comments (incident_id, user_id, text) VALUES (?, ?, ?)").run(req.params.id, 1, text);
    res.json({ success: true });
  });

  app.patch("/api/incidents/:id", (req, res) => {
    const { status } = req.body;
    db.prepare("UPDATE incidents SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?").run(status, req.params.id);
    res.json({ success: true });
  });

  app.get("/api/stats", (req, res) => {
    const stats = {
      total: db.prepare("SELECT count(*) as count FROM incidents").get(),
      open: db.prepare("SELECT count(*) as count FROM incidents WHERE status = 'open'").get(),
      resolved: db.prepare("SELECT count(*) as count FROM incidents WHERE status = 'resolved'").get(),
      byCategory: db.prepare("SELECT category, count(*) as count FROM incidents GROUP BY category").all()
    };
    res.json(stats);
  });

  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    app.use(express.static(path.join(process.cwd(), "dist")));
    app.get("*", (req, res) => {
      res.sendFile(path.join(process.cwd(), "dist/index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Preview server running on http://localhost:${PORT}`);
  });
}

startServer();
