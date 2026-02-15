/**
 * REST API Server
 * A minimal REST API with in-memory data store.
 * Author: Jay Singh (iamjaysingh)
 * Run: node index.js
 */

const http = require("http");

const PORT = 3000;
const store = new Map();
let nextId = 1;

// Seed some initial data
store.set(nextId++, { id: 1, name: "Learn JavaScript", done: false, createdAt: new Date().toISOString() });
store.set(nextId++, { id: 2, name: "Build REST API", done: true, createdAt: new Date().toISOString() });
store.set(nextId++, { id: 3, name: "Practice DSA", done: false, createdAt: new Date().toISOString() });

function parseBody(req) {
    return new Promise((resolve, reject) => {
        let body = "";
        req.on("data", (chunk) => (body += chunk));
        req.on("end", () => {
            try {
                resolve(body ? JSON.parse(body) : {});
            } catch (e) {
                reject(new Error("Invalid JSON"));
            }
        });
    });
}

function sendJSON(res, statusCode, data) {
    res.writeHead(statusCode, {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
    });
    res.end(JSON.stringify(data, null, 2));
}

async function handleRequest(req, res) {
    const url = new URL(req.url, `http://localhost:${PORT}`);
    const path = url.pathname;
    const method = req.method;

    console.log(`${method} ${path}`);

    // CORS preflight
    if (method === "OPTIONS") {
        res.writeHead(204, {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
            "Access-Control-Allow-Headers": "Content-Type",
        });
        return res.end();
    }

    // Routes
    if (path === "/api/tasks" && method === "GET") {
        // GET all tasks
        const tasks = Array.from(store.values());
        const filter = url.searchParams.get("done");
        const filtered = filter !== null
            ? tasks.filter((t) => t.done === (filter === "true"))
            : tasks;
        return sendJSON(res, 200, { count: filtered.length, tasks: filtered });
    }

    if (path.match(/^\/api\/tasks\/\d+$/) && method === "GET") {
        // GET single task
        const id = parseInt(path.split("/").pop());
        const task = store.get(id);
        if (!task) return sendJSON(res, 404, { error: "Task not found" });
        return sendJSON(res, 200, task);
    }

    if (path === "/api/tasks" && method === "POST") {
        // CREATE task
        const body = await parseBody(req);
        if (!body.name) return sendJSON(res, 400, { error: "Name is required" });
        const task = {
            id: nextId++,
            name: body.name,
            done: false,
            createdAt: new Date().toISOString(),
        };
        store.set(task.id, task);
        return sendJSON(res, 201, task);
    }

    if (path.match(/^\/api\/tasks\/\d+$/) && method === "PUT") {
        // UPDATE task
        const id = parseInt(path.split("/").pop());
        const task = store.get(id);
        if (!task) return sendJSON(res, 404, { error: "Task not found" });
        const body = await parseBody(req);
        if (body.name !== undefined) task.name = body.name;
        if (body.done !== undefined) task.done = body.done;
        task.updatedAt = new Date().toISOString();
        store.set(id, task);
        return sendJSON(res, 200, task);
    }

    if (path.match(/^\/api\/tasks\/\d+$/) && method === "DELETE") {
        // DELETE task
        const id = parseInt(path.split("/").pop());
        if (!store.has(id)) return sendJSON(res, 404, { error: "Task not found" });
        store.delete(id);
        return sendJSON(res, 200, { message: "Task deleted" });
    }

    if (path === "/api/stats" && method === "GET") {
        // Stats endpoint
        const tasks = Array.from(store.values());
        return sendJSON(res, 200, {
            total: tasks.length,
            completed: tasks.filter((t) => t.done).length,
            pending: tasks.filter((t) => !t.done).length,
        });
    }

    // 404
    return sendJSON(res, 404, {
        error: "Not found", availableRoutes: [
            "GET    /api/tasks",
            "GET    /api/tasks/:id",
            "POST   /api/tasks",
            "PUT    /api/tasks/:id",
            "DELETE /api/tasks/:id",
            "GET    /api/stats",
        ]
    });
}

const server = http.createServer(async (req, res) => {
    try {
        await handleRequest(req, res);
    } catch (err) {
        console.error("Error:", err.message);
        sendJSON(res, 500, { error: "Internal server error" });
    }
});

server.listen(PORT, () => {
    console.log("=".repeat(50));
    console.log(`  🚀 REST API Server running on port ${PORT}`);
    console.log("=".repeat(50));
    console.log(`  Endpoints:`);
    console.log(`    GET    http://localhost:${PORT}/api/tasks`);
    console.log(`    POST   http://localhost:${PORT}/api/tasks`);
    console.log(`    GET    http://localhost:${PORT}/api/stats`);
    console.log("=".repeat(50));
});
