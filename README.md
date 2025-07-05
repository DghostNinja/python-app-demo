# python-app-demo 

---
### Build (Recommended)

```bash
git clone https://github.com/DghostNinja/python-app-demo.git
cd python-app-demo
python3 app.py
```

OR

### ✅ 1. **Build the Docker Image Locally**

From your project root (where the `Dockerfile` is located):

```bash
docker build -t fauxmart:local .
```

This creates a local image named `fauxmart` with the `local` tag.

---

### ✅ 2. **Run the Container**

```bash
docker run -p 5000:5000 fauxmart:local
```

This command:

* Maps your **local port 5000** to the container’s **internal port 5000**
* Starts the app
* Makes it accessible at: [http://localhost:5000](http://localhost:5000)

---

### ✅ 3. **Test Your App**

Open your browser and go to:

```
http://localhost:5000
```

You should see the FauxMart homepage (make sure `app.py` is using `host='0.0.0.0'`):

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

---

###  4. **Stop the Container**

Press `Ctrl + C` in the terminal, or find the container ID:

```bash
docker ps
```

Then stop it:

```bash
docker stop <container-id>
```

---

###  Optional: Make Live Code Changes (Dev Mode)

If you want Flask hot-reload without rebuilding every time:

```bash
docker run -p 5000:5000 -v $PWD:/app fauxmart:local
```

That mounts your code into the container — changes reflect live (assuming Flask dev mode is enabled).

---

### 🛠 Local Test Cheat Sheet

```bash
docker build -t fauxmart:local .
docker run -p 5000:5000 fauxmart:local
```

✅ Done. Your app is now running locally in Docker.
